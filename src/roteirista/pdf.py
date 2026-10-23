"""Extração de capítulos e parágrafos de PDFs com marcadores."""

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader
from pypdf._page import PageObject


@dataclass(frozen=True)
class Capitulo:
    titulo: str
    paragrafos: list[str]


@dataclass(frozen=True)
class Linha:
    texto: str
    x: float
    y: float
    tamanho: float
    pagina: int
    ordem: int = 0


_PALAVRA = re.compile(r"[^\W\d_]+(?:-[^\W\d_]+)*")
_FIM_DE_LINHA_HIFENIZADA = re.compile(r"([^\W\d_]+)-$")
_INICIO_DE_PALAVRA = re.compile(r"^([^\W\d_]+)(.*)$", re.DOTALL)
_FIM_DE_PARAGRAFO = re.compile(r"[.!?…][\"'”’»]*$")


def _texto(texto: str) -> str:
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", texto).strip())


def _linhas_da_pagina(pagina: PageObject, numero: int) -> list[Linha]:
    fragmentos: list[Linha] = []

    def visitar(texto: str, cm: list[float], tm: list[float], _fonte, tamanho: float) -> None:
        partes = texto.splitlines()
        if not partes and texto and not texto.isspace():
            partes = [texto]
        for parte in partes:
            fragmentos.append(
                Linha(
                    texto=parte,
                    x=tm[4] * cm[0] + tm[5] * cm[2] + cm[4],
                    y=tm[4] * cm[1] + tm[5] * cm[3] + cm[5],
                    tamanho=tamanho,
                    pagina=numero,
                    ordem=len(fragmentos),
                )
            )

    pagina.extract_text(visitor_text=visitar)
    grupos: list[list[Linha]] = []
    for fragmento in sorted(fragmentos, key=lambda linha: -linha.y):
        if grupos and abs(grupos[-1][0].y - fragmento.y) <= 1:
            grupos[-1].append(fragmento)
        else:
            grupos.append([fragmento])

    return [
        Linha(
            texto=_texto("".join(
                fragmento.texto
                for fragmento in sorted(grupo, key=lambda linha: (linha.x, linha.ordem))
            )),
            x=min(fragmento.x for fragmento in grupo),
            y=max(fragmento.y for fragmento in grupo),
            tamanho=max(fragmento.tamanho for fragmento in grupo),
            pagina=numero,
        )
        for grupo in grupos
        if _texto("".join(fragmento.texto for fragmento in grupo))
    ]


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
                corpo = max(anterior.tamanho, linha.tamanho, 1)
                quebra = recuo > corpo * 1.8
            if quebra:
                paragrafos.append(_juntar_linhas([item.texto for item in atual], vocabulario))
                atual = []
        atual.append(linha)

    if atual:
        paragrafos.append(_juntar_linhas([item.texto for item in atual], vocabulario))
    return paragrafos


def extrair(caminho: Path) -> list[Capitulo]:
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
    paginas = _sem_cabecalhos_e_rodapes(
        paginas, [float(pagina.mediabox.height) for pagina in leitor.pages]
    )
    vocabulario = {
        palavra
        for linhas in paginas
        for linha in linhas
        for palavra in _PALAVRA.findall(linha.texto)
    }
    return [
        Capitulo(
            titulo,
            _paragrafos(_linhas_capitulo(paginas, marcadores, indice), vocabulario),
        )
        for indice, (titulo, _) in enumerate(marcadores)
    ]
