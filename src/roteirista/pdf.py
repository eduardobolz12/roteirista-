"""Extração de capítulos e parágrafos de PDFs com marcadores."""

from dataclasses import dataclass
from pathlib import Path
import re
import unicodedata

from pypdf import PdfReader


@dataclass(frozen=True)
class Capitulo:
    titulo: str
    paragrafos: list[str]


def _normalizar(texto: str) -> str:
    texto = " ".join(linha.strip() for linha in texto.splitlines())
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", texto).strip())


def _paragrafos(texto: str) -> list[str]:
    blocos = re.split(r"\n[\t ]*\n+", texto)
    return [_normalizar(bloco) for bloco in blocos if _normalizar(bloco)]


def _apos_titulo(texto: str, titulo: str) -> str:
    posicao = texto.find(titulo)
    return texto[posicao + len(titulo):] if posicao >= 0 else texto


def _antes_titulo(texto: str, titulo: str) -> str:
    posicao = texto.find(titulo)
    return texto[:posicao] if posicao >= 0 else texto


def _texto_capitulo(
    paginas: list[str], marcadores: list[tuple[str, int]], indice: int
) -> str:
    titulo, inicio = marcadores[indice]
    if indice + 1 == len(marcadores):
        partes = paginas[inicio:]
        partes[0] = _apos_titulo(partes[0], titulo)
        return "\n".join(partes)

    proximo_titulo, fim = marcadores[indice + 1]
    if inicio == fim:
        texto = _apos_titulo(paginas[inicio], titulo)
        return _antes_titulo(texto, proximo_titulo)

    partes = paginas[inicio:fim + 1]
    partes[0] = _apos_titulo(partes[0], titulo)
    partes[-1] = _antes_titulo(partes[-1], proximo_titulo)
    return "\n".join(partes)


def extrair(caminho: Path) -> list[Capitulo]:
    leitor = PdfReader(caminho)
    marcadores = [
        (item.title, leitor.get_destination_page_number(item))
        for item in leitor.outline
        if not isinstance(item, list)
    ]
    paginas = [pagina.extract_text(extraction_mode="layout") for pagina in leitor.pages]
    return [
        Capitulo(titulo, _paragrafos(_texto_capitulo(paginas, marcadores, indice)))
        for indice, (titulo, _) in enumerate(marcadores)
    ]
