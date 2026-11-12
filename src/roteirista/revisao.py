"""Conferência dos apontamentos de fidelidade devolvidos pela nuvem."""

import re
import unicodedata


_ID = re.compile(r"(?<![\w.])(?:\d{2}|W\d{2})\.\d{3}(?![\w.])")
_ASPAS = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto).translate(_ASPAS).casefold()
    return re.sub(r"\s+", " ", texto).strip()


def conferir(texto: str, resposta: str, ids_material: set[str]) -> tuple[list[str], int, int]:
    """Separa apontamentos sustentados dos descartes, na ordem da resposta."""
    texto_normalizado = _normalizar(texto)
    linhas = []
    apontamentos = 0
    descartados = 0
    for original in resposta.splitlines():
        if not original.strip() or original.strip().casefold() == "nada":
            continue
        campos = [campo.strip() for campo in original.split("|")]
        if len(campos) != 3:
            continue
        frase, motivo, campo_ids = campos
        frase_sem_aspas = frase.strip().strip("\"'“”‘’")
        if not frase_sem_aspas or _normalizar(frase_sem_aspas) not in texto_normalizado:
            linhas.append(f"descartado (frase fora do texto): {original}")
            descartados += 1
            continue
        if campo_ids.casefold().startswith("sem apoio"):
            ids = "sem apoio"
        else:
            encontrados = _ID.findall(campo_ids)
            if not encontrados or any(id not in ids_material for id in encontrados):
                linhas.append(f"descartado (id fora do material): {original}")
                descartados += 1
                continue
            ids = ", ".join(encontrados)
        linhas.append(f"{ids} | {frase} | {motivo}")
        apontamentos += 1
    return linhas, apontamentos, descartados
