"""Persistência e consulta dos livros convertidos."""

import os
from pathlib import Path
import sqlite3

from roteirista.pdf import Capitulo


def _caminho(slug: str) -> Path:
    raiz = Path(os.environ.get("ROTEIRISTA_LIVROS", "./livros"))
    return raiz / slug / "livro.sqlite"


def criar(slug: str, capitulos: list[Capitulo]) -> None:
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
            """
        )
        for numero_capitulo, capitulo in enumerate(capitulos, start=1):
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


def trecho(slug: str, id: str) -> str | None:
    with sqlite3.connect(_caminho(slug)) as conexao:
        linha = conexao.execute(
            "SELECT texto FROM paragrafos WHERE id = ?", (id,)
        ).fetchone()
    return linha[0] if linha else None
