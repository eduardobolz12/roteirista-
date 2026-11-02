"""Extração de capítulos e parágrafos de livros em EPUB."""

from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata

from ebooklib import epub

from roteirista.pdf import Capitulo, Livro


def _texto(texto: str) -> str:
    return unicodedata.normalize("NFC", re.sub(r"\s+", " ", texto).strip())


class _Documento(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.titulo: str | None = None
        self.paragrafos: list[str] = []
        self._no_titulo = False
        self._no_paragrafo = False
        self._partes: list[str] = []

    def handle_starttag(self, tag: str, _attrs) -> None:
        tag = tag.casefold()
        if tag in {"h1", "h2"} and self.titulo is None and not self._no_titulo:
            self._no_titulo = True
            self._partes = []
        elif tag == "p" and not self._no_paragrafo:
            self._no_paragrafo = True
            self._partes = []
        elif tag == "br" and (self._no_titulo or self._no_paragrafo):
            self._partes.append(" ")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        if tag in {"h1", "h2"} and self._no_titulo:
            self.titulo = _texto("".join(self._partes))
            self._no_titulo = False
            self._partes = []
        elif tag == "p" and self._no_paragrafo:
            paragrafo = _texto("".join(self._partes))
            if paragrafo:
                self.paragrafos.append(paragrafo)
            self._no_paragrafo = False
            self._partes = []

    def handle_data(self, data: str) -> None:
        if self._no_titulo or self._no_paragrafo:
            self._partes.append(data)


def extrair(caminho: Path) -> Livro:
    livro = epub.read_epub(caminho)
    capitulos = []
    for idref, *_ in livro.spine:
        item = livro.get_item_with_id(idref)
        if item is None:
            continue
        documento = _Documento()
        documento.feed(item.get_content().decode("utf-8"))
        documento.close()
        if documento.titulo:
            capitulos.append(
                Capitulo(
                    titulo=documento.titulo,
                    paragrafos=documento.paragrafos,
                    notas=[],
                )
            )
    return Livro(capitulos=capitulos, bibliografia=[])
