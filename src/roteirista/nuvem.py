"""Cliente da nuvem gratuito, com modelos tentados em ordem."""

import json
import os
import sys
from urllib import request


_MODELOS_PADRAO = (
    "openrouter/baidu/ernie-5.5-flash-preview:free,"
    "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"
)


class ChaveNaoInformada(Exception):
    """A variável ROTEIRISTA_NUVEM_CHAVE não foi definida."""


class NenhumModeloRespondeu(Exception):
    """Nenhum dos modelos configurados devolveu conteúdo."""


def _conteudo_json(dados: dict) -> str:
    escolhas = dados.get("choices")
    if not isinstance(escolhas, list) or not escolhas:
        raise ValueError("resposta sem choices")
    mensagem = escolhas[0].get("message", {})
    conteudo = mensagem.get("content")
    if not isinstance(conteudo, str):
        raise ValueError("resposta sem conteúdo")
    return conteudo


def _conteudo_eventos(bruto: str) -> str:
    partes = []
    for linha in bruto.splitlines():
        linha = linha.strip()
        if not linha.startswith("data:"):
            continue
        evento = linha[5:].strip()
        if evento == "[DONE]":
            continue
        try:
            dados = json.loads(evento)
        except ValueError:
            continue
        for escolha in dados.get("choices", []):
            delta = escolha.get("delta", {})
            conteudo = delta.get("content")
            if isinstance(conteudo, str):
                partes.append(conteudo)
    return "".join(partes)


def _extrair_conteudo(bruto: str) -> str:
    try:
        conteudo = _conteudo_json(json.loads(bruto))
    except (ValueError, AttributeError, TypeError):
        conteudo = _conteudo_eventos(bruto)
    if not conteudo.strip():
        raise ValueError("conteúdo vazio")
    return conteudo


def _pedir(modelo: str, prompt: str, chave: str) -> str:
    base = os.environ.get("ROTEIRISTA_NUVEM", "http://127.0.0.1:20128").rstrip("/")
    corpo = json.dumps(
        {
            "model": modelo,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
            "max_tokens": 20000,
            "stream": False,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    pedido = request.Request(
        f"{base}/v1/chat/completions",
        data=corpo,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {chave}",
        },
        method="POST",
    )
    with request.urlopen(pedido, timeout=600) as resposta:
        if resposta.status != 200:
            raise OSError(f"HTTP {resposta.status}")
        bruto = resposta.read().decode("utf-8")
    return _extrair_conteudo(bruto)


def responder(prompt: str) -> tuple[str, str]:
    """Devolve o nome do modelo e sua primeira resposta utilizável."""
    chave = os.environ.get("ROTEIRISTA_NUVEM_CHAVE", "").strip()
    if not chave:
        raise ChaveNaoInformada
    modelos = [
        modelo.strip()
        for modelo in os.environ.get("ROTEIRISTA_MODELOS", _MODELOS_PADRAO).split(",")
        if modelo.strip()
    ]
    for modelo in modelos:
        try:
            return modelo, _pedir(modelo, prompt, chave)
        except (OSError, UnicodeError, ValueError, AttributeError, TypeError) as erro:
            sys.stderr.write(f"modelo falhou, próximo: {modelo} ({erro})\n")
    raise NenhumModeloRespondeu
