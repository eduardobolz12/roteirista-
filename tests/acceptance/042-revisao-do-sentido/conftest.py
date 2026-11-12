"""Fronteira das SPECs 017, 042 e 018: o executável `livro`, chamado como processo, e um servidor falso
que faz o papel do Europe PMC, da Wikipédia e da nuvem (9Router), com respostas de arquivos reais."""
import json
import os
import shutil
import subprocess
import threading
import urllib.parse
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
PDF = FIXTURES / "dois-capitulos.pdf"
PROMPTS = Path(__file__).parents[3] / "docs" / "prompts"


@dataclass
class Saida:
    codigo: int
    stdout: bytes
    stderr: bytes

    @property
    def texto(self) -> str:
        return self.stdout.decode("utf-8")

    @property
    def erro(self) -> str:
        return self.stderr.decode("utf-8", errors="replace")


class ServidorFalso:
    """Europe PMC em /europepmc/search, Wikipédia em /w/api.php e a nuvem em /v1/chat/completions.

    - Europe PMC: `query=EXT_ID:<id> AND SRC:<fonte>` devolve fixtures/europepmc/<id>.json; outra query
      devolve fixtures/europepmc/busca/<query com espaços trocados por _>.json; sem arquivo, lista vazia.
    - Wikipédia: `prop=extracts` devolve fixtures/wikipedia/<título com _>.json, ou a página `missing`;
      `list=search` devolve fixtures/wikipedia/busca/<srsearch com _>.json, ou busca vazia.
    - `falhar_api = True`: as duas APIs respondem 500.
    - Nuvem: `modelos[<nome>]` é ("json", texto), ("sse", texto) ou um código HTTP de erro.
    """

    def __init__(self):
        self.api = []
        self.nuvem = []
        self.falhar_api = False
        self.modelos = {}
        falso = self

        class Tratador(BaseHTTPRequestHandler):
            def _enviar(self, codigo, corpo=b"", tipo="application/json"):
                self.send_response(codigo)
                self.send_header("Content-Type", tipo)
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)

            def _json(self, dados):
                self._enviar(200, json.dumps(dados).encode("utf-8"))

            def do_GET(self):
                partes = urllib.parse.urlsplit(self.path)
                q = dict(urllib.parse.parse_qsl(partes.query))
                falso.api.append({"caminho": partes.path, "q": q, "agente": self.headers.get("User-Agent")})
                if falso.falhar_api:
                    return self._enviar(500)
                if partes.path == "/europepmc/search":
                    consulta = q.get("query", "")
                    if consulta.startswith("EXT_ID:"):
                        arq = FIXTURES / "europepmc" / f"{consulta.split()[0].split(':', 1)[1]}.json"
                    else:
                        arq = FIXTURES / "europepmc" / "busca" / f"{consulta.replace(' ', '_')}.json"
                    if arq.exists():
                        return self._enviar(200, arq.read_bytes())
                    return self._json({"hitCount": 0, "resultList": {"result": []}})
                if partes.path == "/w/api.php":
                    if q.get("list") == "search":
                        arq = FIXTURES / "wikipedia" / "busca" / f"{q.get('srsearch', '').replace(' ', '_')}.json"
                        if arq.exists():
                            return self._enviar(200, arq.read_bytes())
                        return self._json({"query": {"search": []}})
                    titulo = q.get("titles", "")
                    arq = FIXTURES / "wikipedia" / f"{titulo.replace(' ', '_')}.json"
                    if arq.exists():
                        return self._enviar(200, arq.read_bytes())
                    return self._json({"query": {"pages": {"-1": {"ns": 0, "title": titulo, "missing": ""}}}})
                return self._enviar(404)

            def do_POST(self):
                corpo = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                falso.nuvem.append(dict(corpo, caminho=self.path, chave=self.headers.get("Authorization")))
                comportamento = falso.modelos.get(corpo.get("model"), 404)
                if self.path != "/v1/chat/completions" or isinstance(comportamento, int):
                    return self._enviar(comportamento if isinstance(comportamento, int) else 404,
                                        b'{"error":{"message":"falso"}}')
                modo, texto = comportamento
                if modo == "json":
                    return self._json({"id": "x", "model": corpo["model"],
                                       "choices": [{"index": 0, "message": {"role": "assistant", "content": texto},
                                                    "finish_reason": "stop"}]})
                metade = len(texto) // 2
                eventos = ""
                for pedaco in (texto[:metade], texto[metade:]):
                    eventos += "data: " + json.dumps({"id": "x", "model": corpo["model"],
                                                      "choices": [{"index": 0, "delta": {"content": pedaco}}]}) + "\n\n"
                eventos += "data: [DONE]\n\n"
                return self._enviar(200, eventos.encode("utf-8"), "text/event-stream")

            def log_message(self, *args):
                pass

        self.servidor = ThreadingHTTPServer(("127.0.0.1", 0), Tratador)
        self.url = f"http://127.0.0.1:{self.servidor.server_address[1]}"
        threading.Thread(target=self.servidor.serve_forever, daemon=True).start()

    def conteudo(self, i):
        """O texto da mensagem do pedido i à nuvem."""
        return self.nuvem[i]["messages"][0]["content"]


@pytest.fixture
def pdf():
    return PDF


@pytest.fixture
def prompts():
    return PROMPTS


@pytest.fixture
def servidor():
    falso = ServidorFalso()
    yield falso
    falso.servidor.shutdown()


@pytest.fixture
def pasta(tmp_path):
    """A pasta de trabalho: o processo roda aqui, e aqui fica o texto revisado."""
    p = tmp_path / "trabalho"
    p.mkdir()
    texto = FIXTURES / "texto.md"
    if texto.exists():
        shutil.copyfile(texto, p / "texto.md")
    return p


@pytest.fixture
def livros(tmp_path):
    p = tmp_path / "livros"
    p.mkdir()
    return p


@pytest.fixture
def livro(livros, servidor, pasta):
    """Roda `livro <args>` com as APIs e a nuvem no servidor falso."""

    def rodar(*args: str, chave: bool = True, modelos: str = "m1,m2") -> Saida:
        env = dict(os.environ)
        for nome in ("ROTEIRISTA_NUVEM_CHAVE", "ROTEIRISTA_MODELOS"):
            env.pop(nome, None)
        env.update(ROTEIRISTA_LIVROS=str(livros),
                   ROTEIRISTA_EUROPEPMC=f"{servidor.url}/europepmc",
                   ROTEIRISTA_WIKIPEDIA=f"{servidor.url}/w/api.php",
                   ROTEIRISTA_NUVEM=servidor.url,
                   ROTEIRISTA_MODELOS=modelos)
        if chave:
            env["ROTEIRISTA_NUVEM_CHAVE"] = "chave-teste"
        try:
            r = subprocess.run(["livro", *args], capture_output=True, env=env, cwd=pasta, timeout=120)
        except FileNotFoundError:
            # executável ausente: o mundo vê "comando não encontrado"
            return Saida(127, b"", b"livro: comando nao encontrado")
        return Saida(r.returncode, r.stdout, r.stderr)

    return rodar
