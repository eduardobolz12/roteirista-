"""Indexação de capítulos por meio da API do Ollama."""

from dataclasses import dataclass
from importlib import resources
import json
import os
import re
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


@dataclass
class ResultadoRepescagem:
    itens: list[Item]
    sem_conteudo: list[str]
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


def _normalizar(texto: str) -> str:
    texto = re.sub(r"\[n\d{2}\]", "", texto)
    texto = texto.translate(str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"}))
    texto = unicodedata.normalize("NFC", texto).casefold()
    return re.sub(r"\s+", " ", texto).strip()


def _localizar_ancora(
    ancora: str, id: str, paragrafos: list[tuple[str, str]]
) -> str | None:
    procurada = _normalizar(ancora)
    if not procurada:
        return None
    posicao = next(pos for pos, (id_paragrafo, _) in enumerate(paragrafos) if id_paragrafo == id)
    if procurada in _normalizar(paragrafos[posicao][1]):
        return id
    for distancia in (1, 2, 3):
        for vizinho in (posicao - distancia, posicao + distancia):
            if 0 <= vizinho < len(paragrafos):
                if procurada in _normalizar(paragrafos[vizinho][1]):
                    return paragrafos[vizinho][0]
    return None


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
                id_localizado = _localizar_ancora(ancora, id, paragrafos)
                if id_localizado is None:
                    motivo = "âncora não encontrada"
                else:
                    motivo = None
                    if id_localizado != id:
                        resultado.avisos.append(
                            f"corrigido: {id} -> {id_localizado}: {ancora}"
                        )
                    resultado.itens.append(
                        Item(id_localizado, tipo, ancora, afirmacao)
                    )
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


def _ler_repescagem(
    slug: str,
    paragrafos: list[tuple[str, str]],
    lacunas: list[str],
    resposta: str,
) -> ResultadoRepescagem:
    ids = {id for id, _ in paragrafos}
    textos = dict(paragrafos)
    lista = set(lacunas)
    resultado = ResultadoRepescagem(
        itens=[], sem_conteudo=[], avisos=[], rejeitados=0
    )
    for linha in resposta.splitlines():
        if not linha.strip():
            continue
        campos = [campo.strip() for campo in linha.split("|")]
        marca = len(campos) == 2 and campos[1] == "sem-conteudo"
        if not marca and len(campos) != 4:
            motivo = "formato"
        else:
            id = campos[0]
            if id.startswith("[") and id.endswith("]"):
                id = id[1:-1].strip()
            if not banco.existe_paragrafo(slug, id):
                motivo = "id inexistente"
            elif id not in ids:
                motivo = "id fora do capítulo"
            elif id not in lista:
                motivo = "id fora da lista"
            elif marca:
                motivo = None
                resultado.sem_conteudo.append(id)
            else:
                _, tipo, ancora, afirmacao = campos
                if tipo not in _TIPOS:
                    motivo = "tipo inválido"
                elif not _normalizar(ancora) or _normalizar(ancora) not in _normalizar(textos[id]):
                    motivo = "âncora não encontrada"
                else:
                    motivo = None
                    resultado.itens.append(Item(id, tipo, ancora, afirmacao))
        if motivo is not None:
            resultado.avisos.append(f"rejeitado ({motivo}): {linha}")
            resultado.rejeitados += 1
    return resultado


def repescar(slug: str, capitulo: str, janela: int = 2000) -> ResultadoRepescagem:
    paragrafos = banco.paragrafos_capitulo(slug, capitulo)
    if paragrafos is None:
        raise CapituloInexistente(capitulo)
    lacunas = banco.lacunas(slug, capitulo)
    lista = set(lacunas)
    selecionados = [paragrafo for paragrafo in paragrafos if paragrafo[0] in lista]
    resultado = ResultadoRepescagem(
        itens=[], sem_conteudo=[], avisos=[], rejeitados=0
    )
    vistos = set()
    marcas = set()
    for janela_atual in _janelas(selecionados, janela):
        resposta = _pedir(_prompt("repescar.txt") + _trecho(janela_atual))
        parcial = _ler_repescagem(slug, paragrafos, lacunas, resposta)
        resultado.avisos.extend(parcial.avisos)
        resultado.rejeitados += parcial.rejeitados
        for item in parcial.itens:
            chave = (item.id, item.tipo, item.ancora.casefold())
            if chave not in vistos:
                vistos.add(chave)
                resultado.itens.append(item)
        for id in parcial.sem_conteudo:
            if id not in marcas:
                marcas.add(id)
                resultado.sem_conteudo.append(id)
    banco.gravar_repescagem(
        slug,
        [(item.id, item.tipo, item.ancora, item.afirmacao) for item in resultado.itens],
        resultado.sem_conteudo,
    )
    return resultado
