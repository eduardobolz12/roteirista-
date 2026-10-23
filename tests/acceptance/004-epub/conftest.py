"""Fronteira da SPEC 004: o executável `livro`, chamado como processo."""
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"
EPUB = FIXTURES / "dois-capitulos.epub"


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


@pytest.fixture
def epub():
    """A fixture da tabela de CA: dois-capitulos.epub."""
    return EPUB


@pytest.fixture
def livros(tmp_path):
    pasta = tmp_path / "livros"
    pasta.mkdir()
    return pasta


@pytest.fixture
def livro(livros):
    """Roda `livro <args>` com ROTEIRISTA_LIVROS na pasta temporária do teste."""

    def rodar(*args: str) -> Saida:
        env = dict(os.environ, ROTEIRISTA_LIVROS=str(livros))
        try:
            r = subprocess.run(["livro", *args], capture_output=True, env=env, timeout=120)
        except FileNotFoundError:
            # executável ausente: o mundo vê "comando não encontrado"
            return Saida(127, b"", b"livro: comando nao encontrado")
        return Saida(r.returncode, r.stdout, r.stderr)

    return rodar
