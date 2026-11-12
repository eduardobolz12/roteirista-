"""Conferências determinísticas entre as versões de um roteiro."""

from dataclasses import dataclass
import os
from pathlib import Path
import re
import unicodedata

from roteirista import banco


_ID_SIMPLES = r"(?:\d{2}\.(?:\d{3}|n\d{2})|W\d{2}\.\d{3})"
_REFERENCIA = rf"{_ID_SIMPLES}(?:[-–]{_ID_SIMPLES})?"
_CITACAO = re.compile(
    rf'(?:"([^"\n]*)"|“([^”\n]*)”|«([^»\n]*)»)'
    rf"\s*\[\s*({_REFERENCIA})\s*\]"
)
_MARCA_ID = re.compile(rf"\[\s*{_REFERENCIA}\s*\]")


@dataclass
class Resultado:
    saida: str
    codigo: int


def citacoes(texto: str) -> list[tuple[str, str]]:
    """Devolve texto e id das citações, na ordem em que aparecem."""
    return [
        (
            unicodedata.normalize(
                "NFC",
                next(grupo for grupo in achado.groups()[:3] if grupo is not None),
            ),
            achado.group(4),
        )
        for achado in _CITACAO.finditer(texto)
    ]


def sem_citacoes(texto: str) -> str:
    """Remove citações e marcas de id, preservando o texto narrado."""
    return _MARCA_ID.sub(" ", _CITACAO.sub(" ", texto))


def ler_roteiro(arquivo: Path) -> list[tuple[int, list[str]]]:
    """Lê capítulos numerados e parágrafos separados por linha em branco."""
    capitulos: list[tuple[int, list[str]]] = []
    numero = None
    paragrafos: list[str] = []
    partes: list[str] = []

    def fechar_paragrafo() -> None:
        nonlocal partes
        if partes:
            paragrafos.append(" ".join(partes))
            partes = []

    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        achado = re.fullmatch(r"##\s+(\d+)\s*", linha)
        if achado:
            fechar_paragrafo()
            if numero is not None:
                capitulos.append((numero, paragrafos))
            numero = int(achado.group(1))
            paragrafos = []
        elif numero is not None and not linha.startswith("#"):
            if linha.strip():
                partes.append(linha.strip())
            else:
                fechar_paragrafo()
    fechar_paragrafo()
    if numero is not None:
        capitulos.append((numero, paragrafos))
    return capitulos


def _contem_forma(texto: str, formas: str) -> bool:
    texto = unicodedata.normalize("NFC", texto)
    for forma in formas.split("|"):
        expressao = re.escape(unicodedata.normalize("NFC", forma)).replace(
            r"\ ", r"\s+"
        )
        if re.search(rf"(?<!\w){expressao}(?!\w)", texto, re.IGNORECASE):
            return True
    return False


def conferir_glossario(
    slug: str, lingua: str, portugues: Path, traduzido: Path
) -> Resultado:
    termos = banco.glossario(slug, lingua)
    antes = ler_roteiro(portugues)
    depois = dict(ler_roteiro(traduzido))
    alertas = []
    for numero, paragrafos in antes:
        traduzidos = depois.get(numero, [])
        if len(paragrafos) != len(traduzidos):
            alertas.append(
                f"cap. {numero}: {len(paragrafos)} parágrafos no português, "
                f"{len(traduzidos)} na tradução"
            )
            continue
        for indice, (original, traducao) in enumerate(
            zip(paragrafos, traduzidos), start=1
        ):
            original = sem_citacoes(original)
            traducao = sem_citacoes(traducao)
            for termo, esperado in termos:
                if _contem_forma(original, termo) and not _contem_forma(
                    traducao, esperado
                ):
                    alertas.append(f"{numero}.{indice}: {termo} sem {esperado}")
    alertas.append(f"{len(termos)} termos, {len(alertas)} alertas")
    return Resultado("\n".join(alertas) + "\n", 1 if len(alertas) > 1 else 0)


_PALAVRA = re.compile(r"[^\W\d_]+(?:[-’'][^\W\d_]+)*", re.UNICODE)


def lingua_arquivo(arquivo: Path) -> str | None:
    nome = arquivo.name[:-3] if arquivo.name.endswith(".md") else arquivo.name
    return next((parte for parte in nome.split("-") if parte in {"pt", "en", "fr"}), None)


def _mapa_numeros(itens) -> dict[str, int]:
    return {
        palavra: valor
        for valor, palavras in itens
        for palavra in palavras.split()
    }


_NUMEROS = {
    "pt": _mapa_numeros(
        [
            (1, "um uma"), (2, "dois duas ambos ambas"), (3, "três"),
            (4, "quatro"), (5, "cinco"), (6, "seis"), (7, "sete"),
            (8, "oito"), (9, "nove"), (10, "dez"), (11, "onze"),
            (12, "doze dúzia dúzias"), (13, "treze"),
            (14, "catorze quatorze"), (15, "quinze"), (16, "dezesseis"),
            (17, "dezessete"), (18, "dezoito"), (19, "dezenove"),
            (20, "vinte"), (30, "trinta"), (40, "quarenta"),
            (50, "cinquenta"), (60, "sessenta"), (70, "setenta"),
            (80, "oitenta"), (90, "noventa"), (100, "cem cento"),
            (200, "duzentos duzentas"), (300, "trezentos trezentas"),
            (400, "quatrocentos quatrocentas"), (500, "quinhentos quinhentas"),
            (600, "seiscentos seiscentas"), (700, "setecentos setecentas"),
            (800, "oitocentos oitocentas"), (900, "novecentos novecentas"),
            (1000, "mil"), (1000000, "milhão milhões"),
        ]
    ),
    "en": _mapa_numeros(
        [
            (1, "one"), (2, "two both"), (3, "three"), (4, "four"),
            (5, "five"), (6, "six"), (7, "seven"), (8, "eight"),
            (9, "nine"), (10, "ten"), (11, "eleven"),
            (12, "twelve dozen dozens"), (13, "thirteen"), (14, "fourteen"),
            (15, "fifteen"), (16, "sixteen"), (17, "seventeen"),
            (18, "eighteen"), (19, "nineteen"), (20, "twenty"),
            (30, "thirty"), (40, "forty"), (50, "fifty"), (60, "sixty"),
            (70, "seventy"), (80, "eighty"), (90, "ninety"),
            (100, "hundred hundreds"), (1000, "thousand thousands"),
            (1000000, "million millions"),
        ]
    ),
    "fr": _mapa_numeros(
        [
            (1, "un une"), (2, "deux"), (3, "trois"), (4, "quatre"),
            (5, "cinq"), (6, "six"), (7, "sept"), (8, "huit"),
            (9, "neuf"), (10, "dix"), (11, "onze"),
            (12, "douze douzaine douzaines"), (13, "treize"),
            (14, "quatorze"), (15, "quinze"), (16, "seize"),
            (20, "vingt vingts"), (30, "trente"), (40, "quarante"),
            (50, "cinquante"), (60, "soixante"), (100, "cent cents"),
            (1000, "mille"), (1000000, "million millions"),
        ]
    ),
}

_MULTIPLICADORAS = {
    "pt": _mapa_numeros([(12, "dúzia dúzias"), (1000, "mil"), (1000000, "milhão milhões")]),
    "en": _mapa_numeros(
        [(12, "dozen dozens"), (100, "hundred hundreds"),
         (1000, "thousand thousands"), (1000000, "million millions")]
    ),
    "fr": _mapa_numeros(
        [(12, "douzaine douzaines"), (100, "cent cents"),
         (1000, "mille"), (1000000, "million millions")]
    ),
}
_MULTIPLICADORAS_PLURAIS = {
    "pt": {"dúzias", "milhões"},
    "en": {"dozens", "hundreds", "thousands", "millions"},
    "fr": {"douzaines", "cents", "millions"},
}
_UNIDADES_ARTIGO = {"pt": {"um", "uma"}, "en": {"one"}, "fr": {"un", "une"}}
_CONECTORES = {"pt": "e", "en": "and", "fr": "et"}
_TOKEN_NUMERO = re.compile(r"(?<!\w)\d+(?:[.,]\d+)*(?!\w)|[^\W\d_]+", re.UNICODE)


def _casa_livre(valor: int, lingua: str) -> int:
    if lingua == "fr" and valor in {60, 80}:
        return 19
    if 100 <= valor <= 900 and valor % 100 == 0:
        return 99
    if 10 <= valor <= 90 and valor % 10 == 0:
        return 9
    return 0


def _proximo_token_numero(
    texto: str, tokens: list[tuple[str, int, int]], indice: int, fim: int, lingua: str
) -> int | None:
    separador = r"(?:\s|-)+"
    if indice >= len(tokens) or not re.fullmatch(
        separador, texto[fim : tokens[indice][1]]
    ):
        return None
    if tokens[indice][0] == _CONECTORES[lingua]:
        indice += 1
        if indice >= len(tokens) or not re.fullmatch(
            separador, texto[tokens[indice - 1][2] : tokens[indice][1]]
        ):
            return None
    return indice


def _ler_numero(
    texto: str, tokens: list[tuple[str, int, int]], inicio: int, lingua: str
) -> tuple[int, int] | None:
    palavra = tokens[inicio][0]
    multiplicadoras = _MULTIPLICADORAS[lingua]
    artigo_a = lingua == "en" and palavra == "a"
    contextual = artigo_a or palavra in _UNIDADES_ARTIGO[lingua]
    if palavra[0].isdigit():
        total = int(re.sub(r"[.,]", "", palavra))
        livre = 0
    elif palavra in multiplicadoras:
        if palavra in _MULTIPLICADORAS_PLURAIS[lingua]:
            return None
        total = multiplicadoras[palavra]
        livre = total - 1
    elif artigo_a:
        total = 1
        livre = 0
    elif palavra in _NUMEROS[lingua]:
        total = _NUMEROS[lingua][palavra]
        livre = _casa_livre(total, lingua)
    else:
        return None

    parcela = total
    maior_multiplicadora = total if palavra in multiplicadoras else 0
    fim = inicio + 1
    continuou = False
    while True:
        proximo = _proximo_token_numero(texto, tokens, fim, tokens[fim - 1][2], lingua)
        if proximo is None:
            break
        seguinte = tokens[proximo][0]
        if seguinte[0].isdigit():
            break
        if seguinte in multiplicadoras:
            if artigo_a and not continuou and seguinte in _MULTIPLICADORAS_PLURAIS[lingua]:
                break
            valor = multiplicadoras[seguinte]
            if maior_multiplicadora and valor <= maior_multiplicadora:
                total -= parcela
                parcela *= valor
                total += parcela
            else:
                total *= valor
                parcela = total
                maior_multiplicadora = valor
            livre = valor - 1
        else:
            if seguinte not in _NUMEROS[lingua] or seguinte == "a":
                break
            valor = _NUMEROS[lingua][seguinte]
            if lingua == "fr" and parcela == 4 and valor == 20:
                total += 80 - parcela
                parcela = 80
                livre = 19
            else:
                if valor > livre:
                    break
                total += valor
                parcela = valor
                livre = _casa_livre(valor, lingua)
        fim = proximo + 1
        continuou = True
    if contextual and not continuou:
        return None
    return total, fim


def _numeros(texto: str, lingua: str) -> list[int]:
    narrado = sem_citacoes(texto).casefold()
    tokens = [(a.group(), a.start(), a.end()) for a in _TOKEN_NUMERO.finditer(narrado)]
    encontrados = []
    indice = 0
    while indice < len(tokens):
        numero = _ler_numero(narrado, tokens, indice, lingua)
        if numero is None:
            indice += 1
        else:
            valor, indice = numero
            encontrados.append(valor)
    return encontrados


def _texto_para_nomes(texto: str) -> str:
    def substituir(achado) -> str:
        citacao = next(grupo for grupo in achado.groups()[:3] if grupo is not None)
        return citacao.rstrip()[-1] if citacao.rstrip().endswith((".", "!", "?")) else " "

    return _MARCA_ID.sub(" ", _CITACAO.sub(substituir, texto))


_TITULOS = ("Dr", "Dra", "Sr", "Sra", "Mr", "Mrs", "Ms", "Prof", "St")


def _primeira_da_frase(texto: str, inicio: int) -> bool:
    prefixo = texto[:inicio]
    if not prefixo.strip():
        return True
    achado = re.search(r"([.!?])\s+$", prefixo)
    if achado is None:
        return False
    if achado.group(1) == ".":
        anterior = prefixo[: achado.start()]
        inicial = re.search(r"(?<!\w)([^\W\d_])$", anterior)
        if inicial and inicial.group(1).isupper():
            return False
        if re.search(rf"(?<!\w)(?:{'|'.join(_TITULOS)})$", anterior):
            return False
    return True


def _sem_possessivo(palavra: str) -> str:
    return re.sub(r"(?:['’]s)$", "", palavra)


def _ignorar_nome(palavra: str) -> bool:
    chave = palavra.casefold()
    return (
        chave in {titulo.casefold() for titulo in _TITULOS}
        or chave == "i"
        or re.fullmatch(r"i['’][^\W\d_]+", chave) is not None
    )


def _nomes_normais(texto: str) -> list[str]:
    nomes = []
    for achado in _PALAVRA.finditer(texto):
        palavra = _sem_possessivo(achado.group())
        if (
            palavra[0].isupper()
            and not _primeira_da_frase(texto, achado.start())
            and not _ignorar_nome(palavra)
        ):
            nomes.append(palavra)
    return nomes


def nomes_roteiro(capitulos: list[tuple[int, list[str]]]) -> dict[tuple[int, int], list[str]]:
    """Reconhece nomes com o contexto de maiúsculas do arquivo inteiro."""
    narrados = {
        (numero, indice): _texto_para_nomes(texto)
        for numero, paragrafos in capitulos
        for indice, texto in enumerate(paragrafos, start=1)
    }
    normais = {
        nome.casefold()
        for texto in narrados.values()
        for nome in _nomes_normais(texto)
    }
    minusculas = {
        _sem_possessivo(achado.group()).casefold()
        for texto in narrados.values()
        for achado in _PALAVRA.finditer(texto)
        if achado.group()[0].islower()
    }
    resultado = {}
    for posicao, texto in narrados.items():
        nomes = []
        vistos = set()
        for achado in _PALAVRA.finditer(texto):
            palavra = _sem_possessivo(achado.group())
            chave = palavra.casefold()
            if not palavra[0].isupper() or _ignorar_nome(palavra):
                continue
            if (
                _primeira_da_frase(texto, achado.start())
                and (chave not in normais or chave in minusculas)
            ):
                continue
            if chave not in vistos:
                nomes.append(palavra)
                vistos.add(chave)
        resultado[posicao] = nomes
    return resultado


def _palavras_nome(formas: str) -> set[str]:
    return {
        _sem_possessivo(achado.group()).casefold()
        for achado in _PALAVRA.finditer(formas.replace("|", " "))
    }


def _nomes_traduzidos(
    nome: str, termos: list[tuple[str, str]], invertido: bool
) -> set[str]:
    traduzidos = set()
    for termo, traducao in termos:
        origem, destino = (traducao, termo) if invertido else (termo, traducao)
        if _contem_forma(origem, nome):
            traduzidos.update(_palavras_nome(destino))
    return traduzidos


def _formatar_citacoes(valores: list[tuple[str, str]]) -> str:
    return " · ".join(f'"{texto}" [{id}]' for texto, id in valores) or "nenhuma"


def _formatar_numeros(valores: list[int]) -> str:
    return ", ".join(str(valor) for valor in sorted(valores)) or "nenhum"


def conferir_invariantes(
    slug: str, antes: Path, depois: Path, lingua_antes: str, lingua_depois: str
) -> Resultado:
    capitulos_antes = ler_roteiro(antes)
    capitulos_depois = ler_roteiro(depois)
    depois_por_numero = dict(capitulos_depois)
    nomes_antes = nomes_roteiro(capitulos_antes)
    nomes_depois = nomes_roteiro(capitulos_depois)
    lingua_glossario = None
    if lingua_antes != lingua_depois:
        if lingua_antes == "pt":
            lingua_glossario = lingua_depois
        elif lingua_depois == "pt":
            lingua_glossario = lingua_antes
    termos = banco.glossario(slug, lingua_glossario) if lingua_glossario else []
    invertido = lingua_depois == "pt"
    alertas = []
    conferidos = 0
    for numero, paragrafos in capitulos_antes:
        posteriores = depois_por_numero.get(numero, [])
        if len(paragrafos) != len(posteriores):
            alertas.append(
                f"cap. {numero}: {len(paragrafos)} parágrafos antes, "
                f"{len(posteriores)} depois"
            )
            continue
        for indice, (anterior, posterior) in enumerate(
            zip(paragrafos, posteriores), start=1
        ):
            conferidos += 1
            posicao = f"{numero}.{indice}"
            citacoes_antes = citacoes(anterior)
            citacoes_depois = citacoes(posterior)
            if citacoes_antes != citacoes_depois:
                alertas.append(
                    f"{posicao}: citações: {_formatar_citacoes(citacoes_antes)} → "
                    f"{_formatar_citacoes(citacoes_depois)}"
                )
            numeros_antes = _numeros(anterior, lingua_antes)
            numeros_depois = _numeros(posterior, lingua_depois)
            if sorted(numeros_antes) != sorted(numeros_depois):
                alertas.append(
                    f"{posicao}: números: {_formatar_numeros(numeros_antes)} → "
                    f"{_formatar_numeros(numeros_depois)}"
                )
            antes_nomes = nomes_antes[(numero, indice)]
            depois_nomes = nomes_depois[(numero, indice)]
            texto_antes = _texto_para_nomes(anterior)
            texto_depois = _texto_para_nomes(posterior)
            for nome in antes_nomes:
                traduzidos = _nomes_traduzidos(nome, termos, invertido)
                if not _contem_forma(texto_depois, nome) and not any(
                    _contem_forma(texto_depois, traduzido) for traduzido in traduzidos
                ):
                    alertas.append(f"{posicao}: nome sumiu: {nome}")
            for nome in depois_nomes:
                traduzidos = _nomes_traduzidos(nome, termos, not invertido)
                if not _contem_forma(texto_antes, nome) and not any(
                    _contem_forma(texto_antes, traduzido) for traduzido in traduzidos
                ):
                    alertas.append(f"{posicao}: nome novo: {nome}")
    alertas.append(f"{conferidos} parágrafos, {len(alertas)} alertas")
    return Resultado("\n".join(alertas) + "\n", 1 if len(alertas) > 1 else 0)


_PALAVRA_CONTAGEM = re.compile(r"[^\W_]+(?:[-’'][^\W_]+)*", re.UNICODE)


def _comprimento_frases(texto: str) -> list[int]:
    narrado = _texto_para_nomes(texto)
    comprimentos = []
    atual = 0
    for achado in _PALAVRA_CONTAGEM.finditer(narrado):
        if atual and _primeira_da_frase(narrado, achado.start()):
            comprimentos.append(atual)
            atual = 0
        atual += 1
    if atual:
        comprimentos.append(atual)
    return comprimentos


def _expressoes(lingua: str) -> list[str]:
    raiz = Path(
        os.environ.get(
            "ROTEIRISTA_EXPRESSOES",
            Path(__file__).resolve().parents[2] / "docs" / "expressoes",
        )
    )
    try:
        linhas = (raiz / f"{lingua}.txt").read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return []
    return [linha.strip() for linha in linhas if linha.strip() and not linha.startswith("#")]


def medir_legibilidade(
    slug: str, arquivo: Path, lingua: str, limiar: float = 3.0
) -> Resultado:
    from wordfreq import zipf_frequency

    capitulos = ler_roteiro(arquivo)
    nomes = nomes_roteiro(capitulos)
    termos_glossario = {
        palavra.casefold()
        for _, traducao in banco.glossario(slug, lingua)
        for palavra in _palavras_nome(traducao)
    }
    expressoes = _expressoes(lingua)
    saida = []
    paragrafos = 0
    total_longas = 0
    total_raras = 0
    total_expressoes = 0
    for numero, textos in capitulos:
        for indice, texto in enumerate(textos, start=1):
            paragrafos += 1
            posicao = f"{numero}.{indice}"
            longas = [total for total in _comprimento_frases(texto) if total > 25]
            for total in longas:
                saida.append(f"{posicao}: frase de {total} palavras")
            total_longas += len(longas)

            narrado = _texto_para_nomes(texto)
            nomes_paragrafo = {nome.casefold() for nome in nomes[(numero, indice)]}
            raras = set()
            for achado in _PALAVRA.finditer(narrado):
                palavra = _sem_possessivo(achado.group()).casefold()
                if palavra in nomes_paragrafo or palavra in termos_glossario:
                    continue
                if zipf_frequency(palavra, lingua) < limiar:
                    raras.add(palavra)
            if raras:
                saida.append(f"{posicao}: raras: {', '.join(sorted(raras))}")
            total_raras += len(raras)

            narrado = sem_citacoes(texto)
            for expressao in expressoes:
                if _contem_forma(narrado, expressao):
                    saida.append(f"{posicao}: expressão: {expressao}")
                    total_expressoes += 1
    saida.append(
        f"{paragrafos} parágrafos, {total_longas} frases longas, "
        f"{total_raras} palavras raras, {total_expressoes} expressões"
    )
    return Resultado("\n".join(saida) + "\n", 0)
