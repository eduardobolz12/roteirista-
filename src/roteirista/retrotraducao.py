"""Retrotradução local de roteiros, parágrafo por parágrafo."""

from dataclasses import dataclass
from pathlib import Path
import re

from roteirista import banco, modelo, traducao


@dataclass(frozen=True)
class Resultado:
    conteudo: str
    avisos: list[str]
    paragrafos: int


def _marcar_citacoes(texto: str, numeradas: bool) -> tuple[str, list[str]]:
    originais: list[str] = []

    def marcar(achado: re.Match) -> str:
        originais.append(achado.group(0))
        marca = len(originais) if numeradas else "c"
        return f"⟦{marca}⟧"

    return traducao._CITACAO.sub(marcar, texto), originais


def _glossario(termos: list[tuple[str, str]], paragrafo: str) -> str:
    narrado = traducao.sem_citacoes(paragrafo)
    presentes = [
        (traduzido, termo)
        for termo, traduzido in termos
        if traducao._contem_forma(narrado, traduzido)
    ]
    if not presentes:
        return ""
    presentes.sort(key=lambda item: item[0].casefold())
    linhas = ["- Use estas traduções:\n"]
    for traduzido, termo in presentes:
        formas_traduzidas = ", ".join(traduzido.split("|"))
        formas_termo = ", ".join(termo.split("|"))
        linhas.append(f"  {formas_traduzidas} → {formas_termo}\n")
    return "".join(linhas)


def _limpar_resposta(resposta: str, citacoes: list[str]) -> tuple[str, bool]:
    resposta = re.sub(r"<think>.*?</think>", "", resposta, flags=re.DOTALL)
    resposta = re.sub(r"\s+", " ", resposta).strip()
    marcas = re.findall(r"⟦([^⟧]*)⟧", resposta)
    esperadas = [str(indice) for indice in range(1, len(citacoes) + 1)]
    validas = marcas == esperadas
    for indice, citacao in enumerate(citacoes, start=1):
        resposta = resposta.replace(f"⟦{indice}⟧", citacao)
    return resposta, validas


def retraduzir(slug: str, arquivo: Path, lingua: str) -> Resultado:
    capitulos = traducao.ler_roteiro(arquivo)
    termos = banco.glossario(slug, lingua)
    modelo_prompt = modelo._prompt("retraduzir.txt")
    lingua_extensa = {"en": "inglês", "fr": "francês"}[lingua]
    avisos = []
    total = 0
    linhas = [f"# Retrotradução de {arquivo.name} (qwen3:14b)", ""]

    for numero, paragrafos in capitulos:
        contexto = "\n\n".join(
            _marcar_citacoes(paragrafo, numeradas=False)[0]
            for paragrafo in paragrafos
        )
        linhas.extend((f"## {numero}", ""))
        for indice, paragrafo in enumerate(paragrafos, start=1):
            texto, citacoes = _marcar_citacoes(paragrafo, numeradas=True)
            prompt = (
                modelo_prompt.replace("{lingua}", lingua_extensa)
                .replace("{capitulo}", contexto)
                .replace("{texto}", texto)
                .replace("{glossario}", _glossario(termos, paragrafo))
            )
            resposta = modelo._pedir(prompt)
            retraduzido, citacoes_validas = _limpar_resposta(resposta, citacoes)
            if not citacoes_validas:
                avisos.append(f"{numero}.{indice}: citação perdida na retrotradução")
            linhas.extend((retraduzido, ""))
            total += 1

    return Resultado("\n".join(linhas) + "\n", avisos, total)
