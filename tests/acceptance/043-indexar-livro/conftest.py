"""Fronteira da SPEC 043: o executável `livro`, chamado como processo, e um Ollama falso (D-013)."""
import json
import os
import re
import socket
import subprocess
import threading
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


class OllamaFalso:
    """Devolve fixtures/respostas/<grupo>/<primeiro id do trecho>.txt; sem arquivo, responde erro 500."""

    def __init__(self):
        self.pedidos = []
        self.grupo = "padrao"
        self.falhar = set()
        falso = self

        class Tratador(BaseHTTPRequestHandler):
            def do_POST(self):
                corpo = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                falso.pedidos.append(dict(corpo, caminho=self.path))
                if len(falso.pedidos) in falso.falhar:
                    self.send_response(500)
                    self.end_headers()
                    return
                trecho = corpo.get("prompt", "").rsplit("TRECHO:", 1)[-1]
                achado = re.search(r"\[(\d\d\.\d{3})\]", trecho)
                arquivo = FIXTURES / "respostas" / falso.grupo / f"{achado.group(1) if achado else 'x'}.txt"
                if self.path != "/api/generate" or not arquivo.exists():
                    self.send_response(500)
                    self.end_headers()
                    return
                texto = arquivo.read_text(encoding="utf-8")
                dados = json.dumps({"model": corpo.get("model"), "response": texto, "done": True}).encode("utf-8")
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

    def trechos(self):
        """Os ids de cada pedido, na ordem, sem contar o exemplo do prompt."""
        return [re.findall(r"^\[(\d\d\.\d{3})\] ", p["prompt"].rsplit("TRECHO:", 1)[-1], re.M) for p in self.pedidos]


@pytest.fixture
def pdf():
    """A fixture da tabela de CA: dois-capitulos.pdf."""
    return PDF


@pytest.fixture
def prompts():
    return PROMPTS


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
def livros(tmp_path):
    pasta = tmp_path / "livros"
    pasta.mkdir()
    return pasta


@pytest.fixture
def livro(livros, ollama):
    """Roda `livro <args>` com ROTEIRISTA_LIVROS na pasta temporária e o Ollama falso."""

    def rodar(*args: str, url: str | None = None) -> Saida:
        env = dict(os.environ, ROTEIRISTA_LIVROS=str(livros), ROTEIRISTA_OLLAMA=url or ollama.url)
        try:
            r = subprocess.run(["livro", *args], capture_output=True, env=env, timeout=120)
        except FileNotFoundError:
            # executável ausente: o mundo vê "comando não encontrado"
            return Saida(127, b"", b"livro: comando nao encontrado")
        return Saida(r.returncode, r.stdout, r.stderr)

    return rodar
