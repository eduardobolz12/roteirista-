"""Extração de capítulos, notas e bibliografia de PDFs com marcadores."""

from collections import Counter
from dataclasses import dataclass, replace
from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader
from pypdf._page import PageObject


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
    tamanho: float
    ordem: int


@dataclass(frozen=True)
class Linha:
    texto: str
    x: float
    y: float
    tamanho: float
    pagina: int
    fragmentos: tuple[Fragmento, ...]


_PALAVRA = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*")
_FIM_DE_LINHA_HIFENIZADA = re.compile(r"([^\W\d_]+)-$")
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

    def visitar(texto: str, cm: list[float], tm: list[float], _fonte, tamanho: float) -> None:
        partes = texto.splitlines()
        if not partes and texto and not texto.isspace():
            partes = [texto]
        for parte in partes:
            fragmentos.append(
                Fragmento(
                    texto=parte,
                    x=tm[4] * cm[0] + tm[5] * cm[2] + cm[4],
                    y=tm[4] * cm[1] + tm[5] * cm[3] + cm[5],
                    tamanho=tamanho,
                    ordem=len(fragmentos),
                )
            )

    pagina.extract_text(visitor_text=visitar)
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


def _juntar_linhas(linhas: list[str], vocabulario: set[str]) -> str:
    resultado = linhas[0]
    for linha in linhas[1:]:
        anterior = _FIM_DE_LINHA_HIFENIZADA.search(resultado)
        seguinte = _INICIO_DE_PALAVRA.match(linha)
        if anterior and seguinte and seguinte.group(1)[0].islower():
            com_hifen = f"{anterior.group(1)}-{seguinte.group(1)}"
            sem_hifen = f"{anterior.group(1)}{seguinte.group(1)}"
            if com_hifen not in vocabulario or sem_hifen in vocabulario:
                resultado = resultado[:-1]
            resultado += linha
        else:
            resultado += f" {linha}"
    return _texto(resultado)


def _separar_notas(
    paginas: list[list[Linha]], corpo: float, vocabulario: set[str]
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


def _linhas_capitulo(
    paginas: list[list[Linha]], marcadores: list[tuple[str, int]], indice: int
) -> list[Linha]:
    titulo, inicio = marcadores[indice]
    if indice + 1 == len(marcadores):
        selecao = [list(linhas) for linhas in paginas[inicio:]]
        selecao[0] = _depois_do_titulo(selecao[0], titulo)
        return [linha for linhas in selecao for linha in linhas]

    proximo_titulo, fim = marcadores[indice + 1]
    selecao = [list(linhas) for linhas in paginas[inicio:fim + 1]]
    selecao[0] = _depois_do_titulo(selecao[0], titulo)
    selecao[-1] = _antes_do_titulo(selecao[-1], proximo_titulo)
    return [linha for linhas in selecao for linha in linhas]


def _paragrafos(linhas: list[Linha], vocabulario: set[str]) -> list[str]:
    paragrafos: list[str] = []
    atual: list[Linha] = []

    for linha in linhas:
        if atual:
            anterior = atual[-1]
            if anterior.pagina != linha.pagina:
                quebra = _FIM_DE_PARAGRAFO.search(anterior.texto) is not None
            else:
                recuo = anterior.y - linha.y
                tamanho = max(anterior.tamanho, linha.tamanho, 1)
                quebra = recuo > tamanho * 1.8
            if quebra:
                paragrafos.append(_juntar_linhas([item.texto for item in atual], vocabulario))
                atual = []
        atual.append(linha)

    if atual:
        paragrafos.append(_juntar_linhas([item.texto for item in atual], vocabulario))
    return paragrafos


def _e_bibliografia(titulo: str) -> bool:
    return _texto(titulo).casefold() in _BIBLIOGRAFIAS


def _capitulos_por_pagina(
    marcadores: list[tuple[str, int]], numeros: list[int | None], total: int
) -> dict[int, int | None]:
    resultado = {}
    for indice, (_, inicio) in enumerate(marcadores):
        fim = marcadores[indice + 1][1] - 1 if indice + 1 < len(marcadores) else total - 1
        for pagina in range(inicio, fim + 1):
            resultado[pagina] = numeros[indice]
    return resultado


def extrair(caminho: Path) -> Livro:
    leitor = PdfReader(caminho)
    marcadores = [
        (item.title, leitor.get_destination_page_number(item))
        for item in leitor.outline
        if not isinstance(item, list)
    ]
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
    vocabulario = {
        palavra
        for linhas in paginas
        for linha in linhas
        for palavra in _PALAVRA.findall(linha.texto)
    }
    paginas, notas_por_pagina = _separar_notas(paginas, corpo, vocabulario)

    numeros: list[int | None] = []
    numero = 0
    for titulo, _ in marcadores:
        if _e_bibliografia(titulo):
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
    for indice, (titulo, _) in enumerate(marcadores):
        paragrafos = _paragrafos(
            _linhas_capitulo(paginas, marcadores, indice), vocabulario
        )
        numero_capitulo = numeros[indice]
        if numero_capitulo is None:
            bibliografia.extend(paragrafos)
        else:
            capitulos.append(
                Capitulo(
                    titulo=titulo,
                    paragrafos=paragrafos,
                    notas=notas_por_capitulo.get(numero_capitulo, []),
                )
            )
    return Livro(capitulos, bibliografia)
