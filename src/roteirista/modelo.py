"""Indexação de capítulos por meio da API do Ollama."""

from dataclasses import dataclass
from importlib import resources
import json
import os
import unicodedata
from urllib import request

from roteirista import banco


_TIPOS = {
    "doutrina",
    "cena",
    "caso",
    "numero",
    "contradicao",
    "termo",
    "informante",
    "marginal",
}


class CapituloInexistente(Exception):
    """O capítulo pedido não existe no livro."""


class ModeloInacessivel(Exception):
    """O Ollama não devolveu uma resposta utilizável."""

    def __init__(self, url: str):
        self.url = url
        super().__init__(url)


@dataclass(frozen=True)
class Item:
    id: str
    tipo: str
    ancora: str
    afirmacao: str


@dataclass
class Resultado:
    itens: list[Item]
    avisos: list[str]
    rejeitados: int


def _url() -> str:
    return os.environ.get("ROTEIRISTA_OLLAMA", "http://localhost:11434").rstrip("/")


def _prompt(nome: str) -> str:
    return (
        resources.files("roteirista")
        .joinpath("prompts", nome)
        .read_bytes()
        .decode("utf-8")
    )


def _pedir(prompt: str) -> str:
    url = _url()
    corpo = json.dumps(
        {
            "model": "qwen3:14b",
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0,
                "num_ctx": 16384,
                "num_predict": 3000,
                "repeat_penalty": 1.1,
            },
            "prompt": prompt,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    pedido = request.Request(
        f"{url}/api/generate",
        data=corpo,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(pedido, timeout=600) as resposta:
            dados = json.loads(resposta.read().decode("utf-8"))
    except (OSError, UnicodeError, ValueError) as erro:
        raise ModeloInacessivel(url) from erro
    if not isinstance(dados, dict) or not isinstance(dados.get("response"), str):
        raise ModeloInacessivel(url)
    return dados["response"]


def _trecho(paragrafos: list[tuple[str, str]]) -> str:
    return "\n\n".join(f"[{id}] {texto}" for id, texto in paragrafos)


def _ler_itens(
    slug: str,
    capitulo: str,
    paragrafos: list[tuple[str, str]],
    resposta: str,
) -> Resultado:
    ids = {id for id, _ in paragrafos}
    resultado = Resultado(itens=[], avisos=[], rejeitados=0)
    for linha in resposta.splitlines():
        if not linha.strip():
            continue
        campos = [campo.strip() for campo in linha.split("|")]
        if len(campos) != 4:
            motivo = "formato"
        else:
            id, tipo, ancora, afirmacao = campos
            if id.startswith("[") and id.endswith("]"):
                id = id[1:-1].strip()
            if not banco.existe_paragrafo(slug, id):
                motivo = "id inexistente"
            elif id not in ids:
                motivo = "id fora do capítulo"
            elif tipo not in _TIPOS:
                motivo = "tipo inválido"
            else:
                motivo = None
                resultado.itens.append(Item(id, tipo, ancora, afirmacao))
        if motivo is not None:
            resultado.avisos.append(f"rejeitado ({motivo}): {linha}")
            resultado.rejeitados += 1
    return resultado


def _tokens(texto: str) -> int:
    caracteres = len(unicodedata.normalize("NFC", texto))
    return -(-caracteres // 4)


def _janelas(
    paragrafos: list[tuple[str, str]], limite: int
) -> list[list[tuple[str, str]]]:
    janelas = []
    atual: list[tuple[str, str]] = []
    total = 0
    for paragrafo in paragrafos:
        tokens = _tokens(paragrafo[1])
        if atual and total + tokens > limite:
            janelas.append(atual)
            ultimo = atual[-1]
            if _tokens(ultimo[1]) + tokens <= limite:
                atual = [ultimo]
                total = _tokens(ultimo[1])
            else:
                atual = []
                total = 0
        atual.append(paragrafo)
        total += tokens
    if atual:
        janelas.append(atual)
    return janelas


def indexar(slug: str, capitulo: str, janela: int = 2000) -> Resultado:
    paragrafos = banco.paragrafos_capitulo(slug, capitulo)
    if paragrafos is None:
        raise CapituloInexistente(capitulo)
    resultado = Resultado(itens=[], avisos=[], rejeitados=0)
    vistos = set()
    for janela_atual in _janelas(paragrafos, janela):
        resposta = _pedir(_prompt("indexar.txt") + _trecho(janela_atual))
        parcial = _ler_itens(slug, capitulo, paragrafos, resposta)
        resultado.avisos.extend(parcial.avisos)
        resultado.rejeitados += parcial.rejeitados
        for item in parcial.itens:
            chave = (item.id, item.tipo, item.ancora.casefold())
            if chave not in vistos:
                vistos.add(chave)
                resultado.itens.append(item)
    banco.substituir_itens(
        slug,
        capitulo,
        [(item.id, item.tipo, item.ancora, item.afirmacao) for item in resultado.itens],
    )
    return resultado
