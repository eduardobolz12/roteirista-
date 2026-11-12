"""Conferência das citações devolvidas por uma pesquisa na nuvem."""

import re
import unicodedata


_ID = re.compile(r"(?:\d{2}|W\d{2})\.\d{3}")
_CARACTERES = str.maketrans(
    {"“": '"', "”": '"', "‘": "'", "’": "'", "–": "-", "—": "-"}
)


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto).translate(_CARACTERES).casefold()
    return re.sub(r"\s+", " ", texto).strip()


def conferir(resposta: str, paragrafos: dict[str, str]) -> tuple[list[str], int, int]:
    """Aceita somente fatos cuja citação consta no parágrafo indicado."""
    linhas = []
    achados = 0
    recusados = 0
    for original in resposta.splitlines():
        if not original.strip() or original.strip().casefold() == "sem resposta":
            continue
        campos = [campo.strip() for campo in original.split("|")]
        if len(campos) != 3:
            continue
        fato, citacao, id = campos
        if not fato or len(citacao) < 2 or not citacao.startswith('"') or not citacao.endswith('"'):
            continue
        if not _ID.fullmatch(id):
            continue
        if id not in paragrafos:
            linhas.append(f"recusado (id fora das fontes): {original}")
            recusados += 1
            continue
        literal = citacao[1:-1]
        if _normalizar(literal) not in _normalizar(paragrafos[id]):
            linhas.append(f"recusado (citação não confere): {original}")
            recusados += 1
            continue
        linhas.append(f"{id} | {fato} | {citacao}")
        achados += 1
    return linhas, achados, recusados
