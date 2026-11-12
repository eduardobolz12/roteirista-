"""Leitura de artigos do Europe PMC e páginas da Wikipédia."""

from dataclasses import dataclass
import html
import json
import os
import re
import unicodedata
from urllib import error, parse, request


class FonteNaoSuportada(Exception):
    """A URL não pertence a uma das fontes aceitas."""


class FonteNaoEncontrada(Exception):
    """A API não encontrou o artigo ou a página pedida."""


class FonteSemTexto(Exception):
    """O artigo encontrado não tem resumo."""


class FonteInacessivel(Exception):
    """A API não devolveu uma resposta utilizável."""


@dataclass(frozen=True)
class Fonte:
    url: str
    autor: str
    ano: str
    titulo: str
    paragrafos: list[str]


def chave_url(url: str) -> str:
    """Compara URLs sem fragmento e sem percent-encoding."""
    partes = parse.urlsplit(url)
    return parse.urlunsplit(
        (partes.scheme, partes.netloc, parse.unquote(partes.path), partes.query, "")
    )


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFC", html.unescape(texto))
    return re.sub(r"\s+", " ", texto).strip()


def _pedir_json(url: str, parametros: dict[str, str | int]) -> dict:
    destino = f"{url}?{parse.urlencode(parametros)}"
    pedido = request.Request(destino, headers={"User-Agent": "roteirista/0.1"})
    try:
        with request.urlopen(pedido, timeout=60) as resposta:
            if resposta.status != 200:
                raise FonteInacessivel(destino)
            dados = json.loads(resposta.read().decode("utf-8"))
    except FonteInacessivel:
        raise
    except (OSError, UnicodeError, ValueError) as erro:
        raise FonteInacessivel(destino) from erro
    if not isinstance(dados, dict):
        raise FonteInacessivel(destino)
    return dados


def _autor_artigo(autores: str) -> str:
    primeiro, separador, _ = autores.partition(",")
    autor = primeiro.rstrip().removesuffix(".")
    return f"{autor} et al." if separador else autor


def _paragrafos_artigo(resumo: str) -> list[str]:
    sem_titulos = re.sub(
        r"(?is)<(h4|title)\b[^>]*>.*?</\1\s*>", "\n", resumo
    )
    separado = re.sub(r"(?i)</?p\b[^>]*>", "\n", sem_titulos)
    paragrafos = []
    for parte in separado.splitlines():
        texto = _normalizar(re.sub(r"<[A-Za-z/][^>]*>", "", parte))
        if texto:
            paragrafos.append(texto)
    return paragrafos


def _artigo(url: str, fonte: str, id: str, dados: dict | None = None) -> Fonte:
    if dados is None:
        base = os.environ.get(
            "ROTEIRISTA_EUROPEPMC",
            "https://www.ebi.ac.uk/europepmc/webservices/rest",
        ).rstrip("/")
        resposta = _pedir_json(
            f"{base}/search",
            {
                "query": f"EXT_ID:{id} AND SRC:{fonte}",
                "resultType": "core",
                "format": "json",
            },
        )
        resultados = resposta.get("resultList", {}).get("result", [])
        if not resultados:
            raise FonteNaoEncontrada(url)
        dados = resultados[0]
    resumo = dados.get("abstractText")
    if not isinstance(resumo, str) or not resumo.strip():
        raise FonteSemTexto(url)
    return Fonte(
        url=url,
        autor=_autor_artigo(str(dados.get("authorString", ""))),
        ano=str(dados.get("pubYear", "")),
        titulo=_normalizar(str(dados.get("title", ""))),
        paragrafos=_paragrafos_artigo(resumo),
    )


def artigo_de_dados(url: str, dados: dict) -> Fonte:
    """Monta uma fonte com um resultado já obtido em uma busca."""
    return _artigo(url, str(dados.get("source", "")), str(dados.get("id", "")), dados)


def _titulo_secao(linha: str) -> str | None:
    achado = re.fullmatch(r"\s*==+\s*(.*?)\s*==+\s*", linha)
    return achado.group(1).strip().casefold() if achado else None


def _paragrafos_wikipedia(extract: str) -> list[str]:
    finais = {"see also", "notes", "references", "further reading", "external links"}
    paragrafos = []
    for linha in extract.splitlines():
        secao = _titulo_secao(linha)
        if secao is not None:
            if secao in finais:
                break
            continue
        texto = _normalizar(linha)
        if texto:
            paragrafos.append(texto)
    return paragrafos


def _wikipedia(url: str, titulo: str) -> Fonte:
    base = os.environ.get(
        "ROTEIRISTA_WIKIPEDIA", "https://en.wikipedia.org/w/api.php"
    )
    resposta = _pedir_json(
        base,
        {
            "action": "query",
            "prop": "extracts",
            "explaintext": "1",
            "redirects": "1",
            "format": "json",
            "titles": titulo,
        },
    )
    paginas = resposta.get("query", {}).get("pages", {})
    if not isinstance(paginas, dict) or not paginas:
        raise FonteNaoEncontrada(url)
    pagina = next(iter(paginas.values()))
    if "missing" in pagina:
        raise FonteNaoEncontrada(url)
    extract = pagina.get("extract")
    if not isinstance(extract, str) or not extract.strip():
        raise FonteSemTexto(url)
    return Fonte(
        url=url,
        autor="Wikipedia",
        ano="—",
        titulo=_normalizar(str(pagina.get("title", titulo))),
        paragrafos=_paragrafos_wikipedia(extract),
    )


def carregar(url: str) -> Fonte:
    """Busca e transforma uma das URLs aceitas em uma fonte."""
    partes = parse.urlsplit(url)
    if partes.scheme == "https" and partes.netloc == "europepmc.org":
        achado = re.fullmatch(r"/(?:article|abstract)/([^/]+)/([^/]+)", partes.path)
        if achado:
            fonte, id = (parse.unquote(parte) for parte in achado.groups())
            return _artigo(url, fonte, id)
    if partes.scheme == "https" and partes.netloc == "en.wikipedia.org":
        achado = re.fullmatch(r"/wiki/(.+)", partes.path)
        if achado:
            titulo = parse.unquote(achado.group(1)).replace("_", " ")
            return _wikipedia(url, titulo)
    raise FonteNaoSuportada(url)
