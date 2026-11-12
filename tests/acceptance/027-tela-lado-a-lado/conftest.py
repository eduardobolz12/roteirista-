"""Fronteira da SPEC 027: o executável `livro`, chamado como processo numa pasta de trabalho, sem rede."""
import os
import shutil
import subprocess
from dataclasses import dataclass
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


@pytest.fixture
def pdf():
    return PDF


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
def livro(livros, pasta):
    """Roda `livro <args>` na pasta de trabalho, com ROTEIRISTA_LIVROS na pasta temporária."""

    def rodar(*args: str) -> Saida:
        env = dict(os.environ, ROTEIRISTA_LIVROS=str(livros))
        try:
            r = subprocess.run(["livro", *args], capture_output=True, env=env, cwd=pasta, timeout=120)
        except FileNotFoundError:
            # executável ausente: o mundo vê "comando não encontrado"
            return Saida(127, b"", b"livro: comando nao encontrado")
        return Saida(r.returncode, r.stdout, r.stderr)

    return rodar
