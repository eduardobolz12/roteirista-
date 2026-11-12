"""Conferências determinísticas entre as versões de um roteiro."""

from dataclasses import dataclass
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
