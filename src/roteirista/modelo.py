"""Indexação de capítulos por meio da API do Ollama."""

from dataclasses import dataclass
from importlib import resources
import json
import os
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


def indexar(slug: str, capitulo: str) -> Resultado:
    paragrafos = banco.paragrafos_capitulo(slug, capitulo)
    if paragrafos is None:
        raise CapituloInexistente(capitulo)
    resposta = _pedir(_prompt("indexar.txt") + _trecho(paragrafos))
    resultado = _ler_itens(slug, capitulo, paragrafos, resposta)
    banco.substituir_itens(
        slug,
        capitulo,
        [(item.id, item.tipo, item.ancora, item.afirmacao) for item in resultado.itens],
    )
    return resultado
