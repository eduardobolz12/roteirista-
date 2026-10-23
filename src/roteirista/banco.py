"""Persistência e consulta dos livros convertidos."""

import os
from pathlib import Path
import sqlite3

from roteirista.pdf import Livro


def _caminho(slug: str) -> Path:
    raiz = Path(os.environ.get("ROTEIRISTA_LIVROS", "./livros"))
    return raiz / slug / "livro.sqlite"


def criar(slug: str, livro: Livro) -> None:
    caminho = _caminho(slug)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(caminho) as conexao:
        conexao.executescript(
            """
            CREATE TABLE capitulos (
                numero INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL
            );
            CREATE TABLE paragrafos (
                id TEXT PRIMARY KEY,
                capitulo INTEGER NOT NULL REFERENCES capitulos(numero),
                numero INTEGER NOT NULL,
                texto TEXT NOT NULL,
                UNIQUE (capitulo, numero)
            );
            CREATE TABLE notas (
                id TEXT PRIMARY KEY,
                capitulo INTEGER NOT NULL REFERENCES capitulos(numero),
                numero INTEGER NOT NULL,
                texto TEXT NOT NULL,
                UNIQUE (capitulo, numero)
            );
            CREATE TABLE bibliografia (
                id TEXT PRIMARY KEY,
                numero INTEGER NOT NULL UNIQUE,
                texto TEXT NOT NULL
            );
            """
        )
        for numero_capitulo, capitulo in enumerate(livro.capitulos, start=1):
            conexao.execute(
                "INSERT INTO capitulos (numero, titulo) VALUES (?, ?)",
                (numero_capitulo, capitulo.titulo),
            )
            conexao.executemany(
                "INSERT INTO paragrafos (id, capitulo, numero, texto) VALUES (?, ?, ?, ?)",
                [
                    (
                        f"{numero_capitulo:02d}.{numero_paragrafo:03d}",
                        numero_capitulo,
                        numero_paragrafo,
                        texto,
                    )
                    for numero_paragrafo, texto in enumerate(capitulo.paragrafos, start=1)
                ],
            )
            conexao.executemany(
                "INSERT INTO notas (id, capitulo, numero, texto) VALUES (?, ?, ?, ?)",
                [
                    (
                        f"{numero_capitulo:02d}.n{nota.numero:02d}",
                        numero_capitulo,
                        nota.numero,
                        nota.texto,
                    )
                    for nota in capitulo.notas
                ],
            )
        conexao.executemany(
            "INSERT INTO bibliografia (id, numero, texto) VALUES (?, ?, ?)",
            [
                (f"bib.{numero:03d}", numero, texto)
                for numero, texto in enumerate(livro.bibliografia, start=1)
            ],
        )


def trecho(slug: str, id: str) -> str | None:
    with sqlite3.connect(_caminho(slug)) as conexao:
        for tabela in ("paragrafos", "notas", "bibliografia"):
            linha = conexao.execute(
                f"SELECT texto FROM {tabela} WHERE id = ?", (id,)
            ).fetchone()
            if linha:
                return linha[0]
    return None
