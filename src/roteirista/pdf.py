"""Extração de capítulos, notas e bibliografia de PDFs com marcadores."""

from collections import Counter
from dataclasses import dataclass, replace
from math import hypot
from pathlib import Path
import re
from statistics import median
import unicodedata

from pypdf import PdfReader
from pypdf._page import PageObject
from pypdf._text_extraction import Font, get_text_operands


@dataclass(frozen=True)
class Nota:
    numero: int
    texto: str


@dataclass(frozen=True)
class Capitulo:
    titulo: str
    paragrafos: list[str]
    notas: list[Nota]


@dataclass(frozen=True)
class Livro:
    capitulos: list[Capitulo]
    bibliografia: list[str]


@dataclass(frozen=True)
class Fragmento:
    texto: str
    x: float
    y: float
    fim: float
    tamanho: float
    ordem: int


@dataclass(frozen=True)
class Linha:
    texto: str
    x: float
    y: float
    fim: float
    tamanho: float
    pagina: int
    fragmentos: tuple[Fragmento, ...]


@dataclass(frozen=True)
class Marcador:
    titulo: str
    pagina: int
    folha: bool


_SERVICO = {
    "copyright",
    "copyright page",
    "direitos autorais",
    "contents",
    "table of contents",
    "sumário",
    "sommaire",
    "table des matières",
    "index",
    "índice",
    "índice remissivo",
}
_PALAVRA = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*")
_FIM_DE_LINHA_HIFENIZADA = re.compile(r"([^\W\d_]+(?:-[^\W\d_]+)*)-$")
_INICIO_DE_PALAVRA = re.compile(r"^([^\W\d_]+)(.*)$", re.DOTALL)
_FIM_DE_PARAGRAFO = re.compile(r"[.!?…][\"'”’»]*$")
_INICIO_DE_NOTA = re.compile(r"^(\d+)\s+(.+)$")
_BIBLIOGRAFIAS = {
    "bibliography",
    "annotated bibliography",
    "references",
    "works cited",
    "bibliografia",
    "referências",
    "bibliographie",
}


def _texto(texto: str) -> str:
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", texto).strip())


def _linhas_da_pagina(pagina: PageObject, numero: int) -> list[Linha]:
    fragmentos: list[Fragmento] = []
    medidas: list[Fragmento] = []
    recursos = pagina["/Resources"].get("/Font", {})
    fontes = {
        nome: Font.from_font_resource(referencia.get_object())
        for nome, referencia in recursos.items()
    }
    fonte_atual: Font | None = None
    tamanho_atual = 12.0
    espacamento = 0.0
    espacamento_de_palavra = 0.0
    escala_horizontal = 1.0
    avanco = 0.0
    estados = []

    def bases(cm: list[float], tm: list[float]) -> tuple[tuple[float, float], ...]:
        origem = (
            tm[4] * cm[0] + tm[5] * cm[2] + cm[4],
            tm[4] * cm[1] + tm[5] * cm[3] + cm[5],
        )
        horizontal = (
            tm[0] * cm[0] + tm[1] * cm[2],
            tm[0] * cm[1] + tm[1] * cm[3],
        )
        vertical = (
            tm[2] * cm[0] + tm[3] * cm[2],
            tm[2] * cm[1] + tm[3] * cm[3],
        )
        return origem, horizontal, vertical

    def registrar(operando, cm: list[float], tm: list[float]) -> None:
        nonlocal avanco
        if fonte_atual is None:
            return
        decodificado, _, largura_dos_glifos = get_text_operands(
            [operando], cm, tm, fonte_atual, (0, 90, 180, 270)
        )
        espacos = (
            decodificado.count(fonte_atual.space_char) if fonte_atual.space_char else 0
        )
        largura = (
            largura_dos_glifos * tamanho_atual / 1000
            + len(decodificado) * espacamento
            + espacos * espacamento_de_palavra
        ) * escala_horizontal
        origem, horizontal, vertical = bases(cm, tm)
        x = origem[0] + avanco * horizontal[0]
        y = origem[1] + avanco * horizontal[1]
        medidas.append(
            Fragmento(
                texto="",
                x=x,
                y=y,
                fim=x + largura * horizontal[0],
                tamanho=abs(tamanho_atual) * hypot(*vertical),
                ordem=len(medidas),
            )
        )
        avanco += largura

    def visitar_operador(operador: bytes, operandos: list, cm, tm) -> None:
        nonlocal fonte_atual, tamanho_atual, espacamento, espacamento_de_palavra
        nonlocal escala_horizontal, avanco
        if operador == b"q":
            estados.append(
                (
                    fonte_atual,
                    tamanho_atual,
                    espacamento,
                    espacamento_de_palavra,
                    escala_horizontal,
                )
            )
        elif operador == b"Q" and estados:
            (
                fonte_atual,
                tamanho_atual,
                espacamento,
                espacamento_de_palavra,
                escala_horizontal,
            ) = estados.pop()
        elif operador == b"Tf":
            fonte_atual = fontes.get(operandos[0])
            tamanho_atual = float(operandos[1])
        elif operador == b"Tc":
            espacamento = float(operandos[0])
        elif operador == b"Tw":
            espacamento_de_palavra = float(operandos[0])
        elif operador == b"Tz":
            escala_horizontal = float(operandos[0]) / 100
        elif operador in {b"BT", b"ET", b"Td", b"TD", b"Tm", b"T*"}:
            avanco = 0.0
        elif operador in {b"Tj", b"'", b'"'}:
            if operador != b"Tj":
                avanco = 0.0
            registrar(operandos[-1], cm, tm)
        elif operador == b"TJ" and operandos:
            for operando in operandos[0]:
                if isinstance(operando, (str, bytes)):
                    registrar(operando, cm, tm)
                else:
                    avanco -= (
                        float(operando)
                        * tamanho_atual
                        / 1000
                        * escala_horizontal
                    )

    def visitar(texto: str, cm: list[float], tm: list[float], fonte, tamanho: float) -> None:
        partes = texto.splitlines()
        if not partes and texto and not texto.isspace():
            partes = [texto]
        if not partes:
            return
        medidas_do_texto = medidas[:]
        medidas.clear()
        if texto.isspace() and not medidas_do_texto:
            return

        faixas: list[list[Fragmento]] = []
        for medida in sorted(medidas_do_texto, key=lambda item: -item.y):
            tolerancia = max(1, medida.tamanho * 0.5)
            if faixas and abs(faixas[-1][0].y - medida.y) <= tolerancia:
                faixas[-1].append(medida)
            else:
                faixas.append([medida])
        if len(partes) == 1 and medidas_do_texto:
            faixas = [medidas_do_texto]

        origem, horizontal, vertical = bases(cm, tm)
        for indice, parte in enumerate(partes):
            if faixas:
                faixa = faixas[min(indice, len(faixas) - 1)]
                x = min(medida.x for medida in faixa)
                y = max(medida.y for medida in faixa)
                fim = max(medida.fim for medida in faixa)
                tamanho_impresso = max(medida.tamanho for medida in faixa)
            else:
                largura = (
                    Font.from_font_resource(fonte).get_text_width(parte) * tamanho / 1000
                    if fonte is not None
                    else 0.0
                )
                x, y = origem
                fim = x + (
                    largura + max(len(parte) - 1, 0) * espacamento
                ) * escala_horizontal * horizontal[0]
                tamanho_impresso = abs(tamanho) * hypot(*vertical)
            fragmentos.append(
                Fragmento(
                    texto=parte,
                    x=x,
                    y=y,
                    fim=fim,
                    tamanho=tamanho_impresso,
                    ordem=len(fragmentos),
                )
            )

    pagina.extract_text(
        visitor_operand_after=visitar_operador,
        visitor_text=visitar,
    )
    grupos: list[list[Fragmento]] = []
    for fragmento in sorted(fragmentos, key=lambda item: -item.y):
        tolerancia = max(1, fragmento.tamanho * 0.5)
        if grupos and abs(grupos[-1][0].y - fragmento.y) <= tolerancia:
            grupos[-1].append(fragmento)
        else:
            grupos.append([fragmento])

    linhas = []
    for grupo in grupos:
        ordenados = tuple(sorted(grupo, key=lambda item: (item.x, item.ordem)))
        texto = _texto("".join(fragmento.texto for fragmento in ordenados))
        if texto:
            linhas.append(
                Linha(
                    texto=texto,
                    x=min(fragmento.x for fragmento in grupo),
                    y=max(fragmento.y for fragmento in grupo),
                    fim=max(fragmento.fim for fragmento in grupo),
                    tamanho=max(fragmento.tamanho for fragmento in grupo),
                    pagina=numero,
                    fragmentos=ordenados,
                )
            )
    return linhas


def _marcar_chamadas(paginas: list[list[Linha]], corpo: float) -> list[list[Linha]]:
    resultado = []
    for linhas in paginas:
        linhas_marcadas = []
        for linha in linhas:
            tem_corpo = any(fragmento.tamanho >= corpo for fragmento in linha.fragmentos)
            texto = ""
            for fragmento in linha.fragmentos:
                numero = fragmento.texto.strip()
                if tem_corpo and numero.isdigit() and fragmento.tamanho < corpo:
                    texto = texto.rstrip() + f"[n{int(numero):02d}]"
                else:
                    texto += fragmento.texto
            linhas_marcadas.append(replace(linha, texto=_texto(texto)))
        resultado.append(linhas_marcadas)
    return resultado


def _sem_cabecalhos_e_rodapes(
    paginas: list[list[Linha]], alturas: list[float]
) -> list[list[Linha]]:
    ocorrencias: Counter[str] = Counter()
    for linhas in paginas:
        ocorrencias.update({linha.texto for linha in linhas})

    paginas_limpas = []
    for linhas, altura in zip(paginas, alturas, strict=True):
        limpas = []
        for linha in linhas:
            faixa = linha.y >= altura * 0.86 or linha.y <= altura * 0.14
            repetida = ocorrencias[linha.texto] >= 3
            numero = re.fullmatch(r"\d+", linha.texto) is not None
            if not (faixa and (repetida or numero)):
                limpas.append(linha)
        paginas_limpas.append(limpas)
    return paginas_limpas


def _juntar_linhas(linhas: list[str], vocabulario: Counter[str]) -> str:
    resultado = linhas[0]
    for linha in linhas[1:]:
        if resultado.endswith(("—", "–")) or linha.startswith(("—", "–")):
            resultado += linha
            continue

        anterior = _FIM_DE_LINHA_HIFENIZADA.search(resultado)
        seguinte = _INICIO_DE_PALAVRA.match(linha)
        if anterior and seguinte:
            primeira = anterior.group(1)
            segunda = seguinte.group(1)
            if segunda[0].isupper():
                resultado += linha
                continue
            if segunda[0].islower():
                com_hifen = f"{primeira}-{segunda}"
                sem_hifen = f"{primeira}{segunda}"
                manter = sem_hifen not in vocabulario and (
                    com_hifen in vocabulario
                    or "-" in primeira
                    or (vocabulario[primeira] > 1 and vocabulario[segunda] > 1)
                )
                if not manter:
                    resultado = resultado[:-1]
                resultado += linha
                continue
        resultado += f" {linha}"
    return _texto(resultado)


def _separar_notas(
    paginas: list[list[Linha]], corpo: float, vocabulario: Counter[str]
) -> tuple[list[list[Linha]], dict[int, list[Nota]]]:
    paginas_sem_notas = []
    notas_por_pagina: dict[int, list[Nota]] = {}

    for numero_pagina, linhas in enumerate(paginas):
        linhas_de_corpo = [linha for linha in linhas if linha.tamanho >= corpo]
        ultima_de_corpo = min((linha.y for linha in linhas_de_corpo), default=None)
        corpo_da_pagina = []
        notas: list[Nota] = []
        linhas_da_nota: list[str] | None = None
        numero_da_nota = 0

        def terminar_nota() -> None:
            nonlocal linhas_da_nota
            if linhas_da_nota:
                notas.append(Nota(numero_da_nota, _juntar_linhas(linhas_da_nota, vocabulario)))
            linhas_da_nota = None

        for linha in linhas:
            no_pe = (
                ultima_de_corpo is not None
                and linha.y < ultima_de_corpo
                and linha.tamanho < corpo
            )
            inicio = _INICIO_DE_NOTA.match(linha.texto) if no_pe else None
            if inicio:
                terminar_nota()
                numero_da_nota = int(inicio.group(1))
                linhas_da_nota = [inicio.group(2)]
            elif no_pe and linhas_da_nota is not None:
                linhas_da_nota.append(linha.texto)
            else:
                corpo_da_pagina.append(linha)
        terminar_nota()
        paginas_sem_notas.append(corpo_da_pagina)
        if notas:
            notas_por_pagina[numero_pagina] = notas

    return paginas_sem_notas, notas_por_pagina


def _depois_do_titulo(linhas: list[Linha], titulo: str) -> list[Linha]:
    titulo = _texto(titulo)
    for indice, linha in enumerate(linhas):
        if linha.texto == titulo:
            return linhas[indice + 1:]
    return linhas


def _antes_do_titulo(linhas: list[Linha], titulo: str) -> list[Linha]:
    titulo = _texto(titulo)
    for indice, linha in enumerate(linhas):
        if linha.texto == titulo:
            return linhas[:indice]
    return linhas


def _sem_abertura(linhas: list[Linha], corpo: float) -> list[Linha]:
    resultado = []
    antes_do_corpo = True
    for linha in linhas:
        if antes_do_corpo and linha.tamanho > corpo:
            continue
        if linha.tamanho >= corpo:
            antes_do_corpo = False
        resultado.append(linha)
    return resultado


def _linhas_capitulo(
    paginas: list[list[Linha]], marcadores: list[Marcador], indice: int, corpo: float
) -> list[Linha]:
    atual = marcadores[indice]
    fim = len(paginas)
    proximo_impresso = False
    if indice + 1 < len(marcadores):
        proximo = marcadores[indice + 1]
        proximo_impresso = any(
            linha.texto == _texto(proximo.titulo) for linha in paginas[proximo.pagina]
        )
        fim = proximo.pagina + 1 if proximo_impresso else proximo.pagina
    if fim <= atual.pagina:
        return []

    selecao = [list(linhas) for linhas in paginas[atual.pagina:fim]]
    selecao[0] = _depois_do_titulo(selecao[0], atual.titulo)
    if proximo_impresso:
        selecao[-1] = _antes_do_titulo(selecao[-1], marcadores[indice + 1].titulo)
    return _sem_abertura(
        [linha for linhas in selecao for linha in linhas], corpo
    )


def _compor_paragrafos(
    linhas: list[Linha], vocabulario: Counter[str], quebras: list[bool]
) -> list[str]:
    paragrafos: list[str] = []
    atual: list[Linha] = []
    for linha, quebra in zip(linhas, quebras, strict=True):
        if atual and quebra:
            paragrafos.append(_juntar_linhas([item.texto for item in atual], vocabulario))
            atual = []
        atual.append(linha)
    if atual:
        paragrafos.append(_juntar_linhas([item.texto for item in atual], vocabulario))
    return paragrafos


def _margem_direita(linhas: list[Linha], corpo: float) -> float:
    grupos: list[list[float]] = []
    for fim in sorted(linha.fim for linha in linhas):
        if grupos and fim - grupos[-1][-1] <= 0.6 * corpo:
            grupos[-1].append(fim)
        else:
            grupos.append([fim])
    margem = max(grupos, key=lambda grupo: (len(grupo), sum(grupo) / len(grupo)))
    return sum(margem) / len(margem)


def _paragrafos(linhas: list[Linha], vocabulario: Counter[str], corpo: float) -> list[str]:
    if not linhas:
        return []
    de_corpo = [linha for linha in linhas if linha.tamanho == corpo]
    esquerda = min((linha.x for linha in de_corpo), default=0)
    recuadas = [linha.x - esquerda > 0.6 * corpo for linha in de_corpo]
    if sum(recuadas) < 3:
        quebras = [False]
        for anterior, linha in zip(linhas, linhas[1:]):
            if anterior.pagina != linha.pagina:
                quebra = _FIM_DE_PARAGRAFO.search(anterior.texto) is not None
            else:
                recuo = anterior.y - linha.y
                tamanho = max(anterior.tamanho, linha.tamanho, 1)
                quebra = recuo > tamanho * 1.8
            quebras.append(quebra)
        return _compor_paragrafos(linhas, vocabulario, quebras)

    direita = _margem_direita(de_corpo, corpo)
    cheias = [direita - linha.fim <= 0.6 * corpo for linha in de_corpo]
    curtas = [direita - linha.fim > 2.5 * corpo for linha in de_corpo]
    depois_da_margem = [
        indice
        for indice in range(1, len(de_corpo))
        if recuadas[indice] and not recuadas[indice - 1]
    ]
    glossario = len(depois_da_margem) >= 5 and (
        sum(cheias[indice - 1] for indice in depois_da_margem) / len(depois_da_margem) > 0.8
    )
    if glossario:
        return _compor_paragrafos(
            de_corpo, vocabulario, [False, *[not recuada for recuada in recuadas[1:]]]
        )

    distancias = [
        anterior.y - linha.y
        for anterior, linha in zip(de_corpo, de_corpo[1:])
        if anterior.pagina == linha.pagina and anterior.y > linha.y
    ]
    entrelinha = median(distancias) if distancias else corpo
    quebras = [False]
    for indice, (anterior, linha) in enumerate(zip(de_corpo, de_corpo[1:]), start=1):
        salto_vertical = (
            anterior.pagina == linha.pagina and anterior.y - linha.y > 1.6 * entrelinha
        )
        if recuadas[indice]:
            citacao = (
                recuadas[indice - 1]
                and not cheias[indice - 1]
                and not curtas[indice - 1]
                and not cheias[indice]
            )
            quebra = not citacao
        else:
            fim_de_recuo = recuadas[indice - 1] and not cheias[indice - 1]
            fim_curto = curtas[indice - 1] and re.search(
                r"[.!?…:][\"'”’»]*$", anterior.texto
            ) is not None
            quebra = fim_de_recuo or fim_curto
        quebras.append(salto_vertical or quebra)
    return _compor_paragrafos(de_corpo, vocabulario, quebras)


def _e_bibliografia(titulo: str) -> bool:
    return _texto(titulo).casefold() in _BIBLIOGRAFIAS


def _e_servico(titulo: str) -> bool:
    return _texto(titulo).casefold() in _SERVICO


def _ler_marcadores(itens: list, leitor: PdfReader) -> list[Marcador]:
    marcadores = []
    indice = 0
    while indice < len(itens):
        item = itens[indice]
        if isinstance(item, list):
            indice += 1
            continue
        tem_filhos = indice + 1 < len(itens) and isinstance(itens[indice + 1], list)
        marcadores.append(
            Marcador(
                titulo=item.title,
                pagina=leitor.get_destination_page_number(item),
                folha=not tem_filhos,
            )
        )
        if tem_filhos:
            marcadores.extend(_ler_marcadores(itens[indice + 1], leitor))
            indice += 2
        else:
            indice += 1
    return marcadores


def _capitulos_por_pagina(
    marcadores: list[Marcador], numeros: list[int | None], total: int
) -> dict[int, int | None]:
    resultado = {}
    for indice, marcador in enumerate(marcadores):
        fim = marcadores[indice + 1].pagina - 1 if indice + 1 < len(marcadores) else total - 1
        for pagina in range(marcador.pagina, fim + 1):
            resultado[pagina] = numeros[indice]
    return resultado


def extrair(caminho: Path) -> Livro:
    leitor = PdfReader(caminho)
    marcadores = _ler_marcadores(leitor.outline, leitor)
    paginas = [
        _linhas_da_pagina(pagina, numero)
        for numero, pagina in enumerate(leitor.pages)
    ]
    corpo = Counter(
        linha.tamanho for linhas in paginas for linha in linhas
    ).most_common(1)[0][0]
    paginas = _marcar_chamadas(paginas, corpo)
    paginas = _sem_cabecalhos_e_rodapes(
        paginas, [float(pagina.mediabox.height) for pagina in leitor.pages]
    )
    vocabulario = Counter(
        palavra
        for linhas in paginas
        for linha in linhas
        for palavra in _PALAVRA.findall(linha.texto)
    )
    paginas, notas_por_pagina = _separar_notas(paginas, corpo, vocabulario)

    numeros: list[int | None] = []
    numero = 0
    for marcador in marcadores:
        if not marcador.folha or _e_servico(marcador.titulo) or _e_bibliografia(marcador.titulo):
            numeros.append(None)
        else:
            numero += 1
            numeros.append(numero)
    capitulo_da_pagina = _capitulos_por_pagina(marcadores, numeros, len(paginas))
    notas_por_capitulo: dict[int, list[Nota]] = {}
    for pagina, notas in notas_por_pagina.items():
        numero_capitulo = capitulo_da_pagina.get(pagina)
        if numero_capitulo is not None:
            notas_por_capitulo.setdefault(numero_capitulo, []).extend(notas)

    capitulos = []
    bibliografia = []
    for indice, marcador in enumerate(marcadores):
        if not marcador.folha or _e_servico(marcador.titulo):
            continue
        paragrafos = _paragrafos(
            _linhas_capitulo(paginas, marcadores, indice, corpo), vocabulario, corpo
        )
        numero_capitulo = numeros[indice]
        if numero_capitulo is None:
            bibliografia.extend(paragrafos)
        else:
            capitulos.append(
                Capitulo(
                    titulo=marcador.titulo,
                    paragrafos=paragrafos,
                    notas=notas_por_capitulo.get(numero_capitulo, []),
                )
            )
    return Livro(capitulos, bibliografia)
