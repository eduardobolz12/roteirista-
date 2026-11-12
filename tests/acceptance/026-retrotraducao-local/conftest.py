"""Fronteira da SPEC 026: o executável `livro`, chamado como processo numa pasta de trabalho, e um Ollama
falso (D-013) que responde pelo texto do PARÁGRAFO do prompt, com as respostas de fixtures/respostas.json."""
import json
import os
import shutil
import socket
import subprocess
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
PDF = FIXTURES / "dois-capitulos.pdf"


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


class OllamaFalso:
    """Guarda cada pedido; responde o texto que respostas.json dá para o PARÁGRAFO; sem resposta, erro 500."""

    def __init__(self):
        self.pedidos = []
        respostas = json.loads((FIXTURES / "respostas.json").read_text(encoding="utf-8"))
        falso = self

        class Tratador(BaseHTTPRequestHandler):
            def do_POST(self):
                corpo = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                falso.pedidos.append(dict(corpo, caminho=self.path))
                paragrafo = corpo.get("prompt", "").rsplit("PARÁGRAFO:", 1)[-1].strip()
                if self.path != "/api/generate" or paragrafo not in respostas:
                    self.send_response(500)
                    self.end_headers()
                    return
                dados = json.dumps({"model": corpo.get("model"), "response": respostas[paragrafo],
                                    "done": True}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(dados)))
                self.end_headers()
                self.wfile.write(dados)

            def log_message(self, *args):
                pass

        self.servidor = ThreadingHTTPServer(("127.0.0.1", 0), Tratador)
        self.url = f"http://127.0.0.1:{self.servidor.server_address[1]}"
        threading.Thread(target=self.servidor.serve_forever, daemon=True).start()


@pytest.fixture
def pdf():
    return PDF


@pytest.fixture
def ollama():
    falso = OllamaFalso()
    yield falso
    falso.servidor.shutdown()


@pytest.fixture
def porta_fechada():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return f"http://127.0.0.1:{s.getsockname()[1]}"


@pytest.fixture
def pasta(tmp_path):
    """A pasta de trabalho: o processo roda aqui, com uma cópia dos .md de fixtures/."""
    p = tmp_path / "trabalho"
    p.mkdir()
    for md in FIXTURES.glob("*.md"):
        shutil.copyfile(md, p / md.name)
    return p


@pytest.fixture
def livros(tmp_path):
    p = tmp_path / "livros"
    p.mkdir()
    return p


@pytest.fixture
def livro(livros, ollama, pasta):
    """Roda `livro <args>` na pasta de trabalho, com o Ollama falso (ou `url`, para o modelo fora do ar)."""

    def rodar(*args: str, url: str | None = None) -> Saida:
        env = dict(os.environ, ROTEIRISTA_LIVROS=str(livros), ROTEIRISTA_OLLAMA=url or ollama.url)
        try:
            r = subprocess.run(["livro", *args], capture_output=True, env=env, cwd=pasta, timeout=120)
        except FileNotFoundError:
            # executável ausente: o mundo vê "comando não encontrado"
            return Saida(127, b"", b"livro: comando nao encontrado")
        return Saida(r.returncode, r.stdout, r.stderr)

    return rodar
