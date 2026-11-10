"""Persistência e consulta dos livros convertidos."""

import os
from pathlib import Path
import sqlite3

from roteirista.pdf import Livro


def _caminho(slug: str) -> Path:
    raiz = Path(os.environ.get("ROTEIRISTA_LIVROS", "./livros"))
    return raiz / slug / "livro.sqlite"


def criar(slug: str, livro: Livro, lingua: str | None = None) -> None:
    caminho = _caminho(slug)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(caminho) as conexao:
        conexao.executescript(
            """
            CREATE TABLE ficha (
                lingua TEXT
            );
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
            CREATE TABLE itens (
                sequencia INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT NOT NULL REFERENCES paragrafos(id),
                tipo TEXT NOT NULL,
                ancora TEXT NOT NULL,
                afirmacao TEXT NOT NULL
            );
            CREATE TABLE sem_conteudo (
                id TEXT PRIMARY KEY REFERENCES paragrafos(id)
            );
            """
        )
        conexao.execute("INSERT INTO ficha (lingua) VALUES (?)", (lingua,))
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


def ficha(slug: str) -> tuple[str | None, int, int]:
    with sqlite3.connect(_caminho(slug)) as conexao:
        lingua = conexao.execute("SELECT lingua FROM ficha").fetchone()[0]
        capitulos = conexao.execute("SELECT COUNT(*) FROM capitulos").fetchone()[0]
        paragrafos = conexao.execute("SELECT COUNT(*) FROM paragrafos").fetchone()[0]
    return lingua, capitulos, paragrafos


def capitulos(slug: str) -> list[tuple[int, list[str]]]:
    with sqlite3.connect(_caminho(slug)) as conexao:
        linhas = conexao.execute(
            """
            SELECT capitulos.numero, paragrafos.texto
            FROM capitulos
            LEFT JOIN paragrafos ON paragrafos.capitulo = capitulos.numero
            ORDER BY capitulos.numero, paragrafos.numero
            """
        ).fetchall()
    resultado: list[tuple[int, list[str]]] = []
    for numero, texto in linhas:
        if not resultado or resultado[-1][0] != numero:
            resultado.append((numero, []))
        if texto is not None:
            resultado[-1][1].append(texto)
    return resultado


def textos(slug: str) -> list[tuple[str, str]]:
    with sqlite3.connect(_caminho(slug)) as conexao:
        return conexao.execute(
            """
            SELECT id, texto FROM (
                SELECT id, texto, capitulo, 0 AS tipo, numero FROM paragrafos
                UNION ALL
                SELECT id, texto, capitulo, 1 AS tipo, numero FROM notas
                UNION ALL
                SELECT id, texto, 2147483647 AS capitulo, 2 AS tipo, numero FROM bibliografia
            )
            ORDER BY capitulo, tipo, numero
            """
        ).fetchall()


def trecho(slug: str, id: str) -> str | None:
    with sqlite3.connect(_caminho(slug)) as conexao:
        for tabela in ("paragrafos", "notas", "bibliografia"):
            linha = conexao.execute(
                f"SELECT texto FROM {tabela} WHERE id = ?", (id,)
            ).fetchone()
            if linha:
                return linha[0]
    return None


def paragrafos_capitulo(slug: str, capitulo: str) -> list[tuple[str, str]] | None:
    with sqlite3.connect(_caminho(slug)) as conexao:
        existe = conexao.execute(
            "SELECT EXISTS(SELECT 1 FROM capitulos WHERE numero = ?)",
            (int(capitulo),),
        ).fetchone()[0]
        if not existe:
            return None
        return conexao.execute(
            """
            SELECT id, texto FROM paragrafos
            WHERE capitulo = ? ORDER BY numero
            """,
            (int(capitulo),),
        ).fetchall()


def existe_paragrafo(slug: str, id: str) -> bool:
    with sqlite3.connect(_caminho(slug)) as conexao:
        return bool(
            conexao.execute(
                "SELECT EXISTS(SELECT 1 FROM paragrafos WHERE id = ?)", (id,)
            ).fetchone()[0]
        )


def substituir_itens(
    slug: str, capitulo: str, itens: list[tuple[str, str, str, str]]
) -> None:
    with sqlite3.connect(_caminho(slug)) as conexao:
        conexao.execute(
            "DELETE FROM itens WHERE id IN (SELECT id FROM paragrafos WHERE capitulo = ?)",
            (int(capitulo),),
        )
        conexao.execute(
            """
            DELETE FROM sem_conteudo
            WHERE id IN (SELECT id FROM paragrafos WHERE capitulo = ?)
            """,
            (int(capitulo),),
        )
        conexao.executemany(
            "INSERT INTO itens (id, tipo, ancora, afirmacao) VALUES (?, ?, ?, ?)",
            itens,
        )


def itens(slug: str, capitulo: str) -> list[tuple[str, str, str, str]]:
    with sqlite3.connect(_caminho(slug)) as conexao:
        return conexao.execute(
            """
            SELECT itens.id, itens.tipo, itens.ancora, itens.afirmacao
            FROM itens
            JOIN paragrafos ON paragrafos.id = itens.id
            WHERE paragrafos.capitulo = ?
            ORDER BY paragrafos.numero, itens.sequencia
            """,
            (int(capitulo),),
        ).fetchall()


def lacunas(slug: str, capitulo: str) -> list[str]:
    with sqlite3.connect(_caminho(slug)) as conexao:
        linhas = conexao.execute(
            """
            SELECT paragrafos.id, paragrafos.texto
            FROM paragrafos
            LEFT JOIN itens ON itens.id = paragrafos.id
            LEFT JOIN sem_conteudo ON sem_conteudo.id = paragrafos.id
            WHERE paragrafos.capitulo = ?
              AND itens.sequencia IS NULL
              AND sem_conteudo.id IS NULL
            ORDER BY paragrafos.numero
            """,
            (int(capitulo),),
        ).fetchall()
    return [id for id, texto in linhas if any(caractere.isalnum() for caractere in texto)]


def gravar_repescagem(
    slug: str,
    itens: list[tuple[str, str, str, str]],
    sem_conteudo: list[str],
) -> None:
    with sqlite3.connect(_caminho(slug)) as conexao:
        conexao.executemany(
            "INSERT INTO itens (id, tipo, ancora, afirmacao) VALUES (?, ?, ?, ?)",
            itens,
        )
        conexao.executemany(
            "INSERT OR IGNORE INTO sem_conteudo (id) VALUES (?)",
            [(id,) for id in sem_conteudo],
        )
