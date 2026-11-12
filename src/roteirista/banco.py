"""Persistência e consulta dos livros convertidos."""

import os
from pathlib import Path
import sqlite3

from roteirista.pdf import Livro


def _caminho(slug: str) -> Path:
    raiz = Path(os.environ.get("ROTEIRISTA_LIVROS", "./livros"))
    return raiz / slug / "livro.sqlite"


def _abrir(slug: str) -> sqlite3.Connection:
    conexao = sqlite3.connect(_caminho(slug))
    conexao.executescript(
        """
        CREATE TABLE IF NOT EXISTS itens (
            sequencia INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT NOT NULL REFERENCES paragrafos(id),
            tipo TEXT NOT NULL,
            ancora TEXT NOT NULL,
            afirmacao TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sem_conteudo (
            id TEXT PRIMARY KEY REFERENCES paragrafos(id)
        );
        CREATE TABLE IF NOT EXISTS capitulos_indexados (
            capitulo INTEGER PRIMARY KEY REFERENCES capitulos(numero)
        );
        CREATE TABLE IF NOT EXISTS hesitacoes_julgadas (
            id TEXT PRIMARY KEY REFERENCES paragrafos(id),
            julgamento TEXT NOT NULL,
            nota TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS fontes (
            sequencia INTEGER PRIMARY KEY AUTOINCREMENT,
            id TEXT NOT NULL UNIQUE,
            autor TEXT NOT NULL,
            ano TEXT NOT NULL,
            titulo TEXT NOT NULL,
            url TEXT NOT NULL,
            chave_url TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS fontes_paragrafos (
            id TEXT PRIMARY KEY,
            fonte_id TEXT NOT NULL REFERENCES fontes(id),
            numero INTEGER NOT NULL,
            texto TEXT NOT NULL,
            UNIQUE (fonte_id, numero)
        );
        """
    )
    return conexao


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
    with _abrir(slug) as conexao:
        lingua = conexao.execute("SELECT lingua FROM ficha").fetchone()[0]
        capitulos = conexao.execute("SELECT COUNT(*) FROM capitulos").fetchone()[0]
        paragrafos = conexao.execute("SELECT COUNT(*) FROM paragrafos").fetchone()[0]
    return lingua, capitulos, paragrafos


def capitulos(slug: str) -> list[tuple[int, list[str]]]:
    with _abrir(slug) as conexao:
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
    with _abrir(slug) as conexao:
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


def paragrafos_livro(slug: str) -> list[tuple[str, str]]:
    with _abrir(slug) as conexao:
        return conexao.execute(
            "SELECT id, texto FROM paragrafos ORDER BY capitulo, numero"
        ).fetchall()


def julgar_hesitacao(slug: str, id: str, julgamento: str, nota: str) -> None:
    with _abrir(slug) as conexao:
        conexao.execute(
            """
            INSERT INTO hesitacoes_julgadas (id, julgamento, nota) VALUES (?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET julgamento = excluded.julgamento, nota = excluded.nota
            """,
            (id, julgamento, nota),
        )


def hesitacoes_julgadas(slug: str) -> list[tuple[str, str, str]]:
    with _abrir(slug) as conexao:
        return conexao.execute(
            """
            SELECT hesitacoes_julgadas.id, julgamento, nota
            FROM hesitacoes_julgadas
            JOIN paragrafos ON paragrafos.id = hesitacoes_julgadas.id
            ORDER BY paragrafos.capitulo, paragrafos.numero
            """
        ).fetchall()


def fontes(slug: str) -> list[tuple[str, str, str, str, str]]:
    with _abrir(slug) as conexao:
        return conexao.execute(
            "SELECT id, autor, ano, titulo, url FROM fontes ORDER BY sequencia"
        ).fetchall()


def fonte_por_url(slug: str, chave_url: str) -> tuple[str, str, str, str, str] | None:
    with _abrir(slug) as conexao:
        return conexao.execute(
            """
            SELECT id, autor, ano, titulo, url FROM fontes
            WHERE chave_url = ?
            """,
            (chave_url,),
        ).fetchone()


def gravar_fonte(slug: str, fonte, chave_url: str) -> tuple[str, str, str, str, str]:
    """Grava a ficha e todos os parágrafos em uma única transação."""
    with _abrir(slug) as conexao:
        sequencia = conexao.execute(
            "SELECT COALESCE(MAX(sequencia), 0) + 1 FROM fontes"
        ).fetchone()[0]
        id = f"W{sequencia:02d}"
        conexao.execute(
            """
            INSERT INTO fontes (sequencia, id, autor, ano, titulo, url, chave_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sequencia,
                id,
                fonte.autor,
                fonte.ano,
                fonte.titulo,
                fonte.url,
                chave_url,
            ),
        )
        conexao.executemany(
            """
            INSERT INTO fontes_paragrafos (id, fonte_id, numero, texto)
            VALUES (?, ?, ?, ?)
            """,
            [
                (f"{id}.{numero:03d}", id, numero, texto)
                for numero, texto in enumerate(fonte.paragrafos, start=1)
            ],
        )
    return id, fonte.autor, fonte.ano, fonte.titulo, fonte.url


def trecho(slug: str, id: str) -> str | None:
    with _abrir(slug) as conexao:
        for tabela in ("paragrafos", "notas", "bibliografia", "fontes_paragrafos"):
            linha = conexao.execute(
                f"SELECT texto FROM {tabela} WHERE id = ?", (id,)
            ).fetchone()
            if linha:
                return linha[0]
    return None


def paragrafos_capitulo(slug: str, capitulo: str) -> list[tuple[str, str]] | None:
    with _abrir(slug) as conexao:
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
    with _abrir(slug) as conexao:
        return bool(
            conexao.execute(
                "SELECT EXISTS(SELECT 1 FROM paragrafos WHERE id = ?)", (id,)
            ).fetchone()[0]
        )


def substituir_itens(
    slug: str, capitulo: str, itens: list[tuple[str, str, str, str]]
) -> None:
    with _abrir(slug) as conexao:
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
    with _abrir(slug) as conexao:
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


def itens_livro(slug: str) -> list[tuple[int, str, str, str, str, str]]:
    with _abrir(slug) as conexao:
        return conexao.execute(
            """
            SELECT capitulos.numero, capitulos.titulo, itens.id,
                   itens.tipo, itens.ancora, itens.afirmacao
            FROM capitulos
            JOIN paragrafos ON paragrafos.capitulo = capitulos.numero
            JOIN itens ON itens.id = paragrafos.id
            ORDER BY capitulos.numero, paragrafos.numero, itens.sequencia
            """
        ).fetchall()


def lacunas(slug: str, capitulo: str) -> list[str]:
    with _abrir(slug) as conexao:
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
    with _abrir(slug) as conexao:
        conexao.executemany(
            "INSERT INTO itens (id, tipo, ancora, afirmacao) VALUES (?, ?, ?, ?)",
            itens,
        )
        conexao.executemany(
            "INSERT OR IGNORE INTO sem_conteudo (id) VALUES (?)",
            [(id,) for id in sem_conteudo],
        )


EstadoCapitulo = tuple[list[tuple[int, str, str, str, str]], list[str], bool]


def capitulos_prontos(slug: str) -> set[int]:
    with _abrir(slug) as conexao:
        linhas = conexao.execute("SELECT capitulo FROM capitulos_indexados").fetchall()
    return {capitulo for (capitulo,) in linhas}


def marcar_capitulo(slug: str, capitulo: str) -> None:
    with _abrir(slug) as conexao:
        conexao.execute(
            "INSERT OR REPLACE INTO capitulos_indexados (capitulo) VALUES (?)",
            (int(capitulo),),
        )


def desmarcar_capitulo(slug: str, capitulo: str) -> None:
    with _abrir(slug) as conexao:
        conexao.execute(
            "DELETE FROM capitulos_indexados WHERE capitulo = ?", (int(capitulo),)
        )


def capturar_capitulo(slug: str, capitulo: str) -> EstadoCapitulo:
    with _abrir(slug) as conexao:
        itens = conexao.execute(
            """
            SELECT itens.sequencia, itens.id, itens.tipo, itens.ancora, itens.afirmacao
            FROM itens
            JOIN paragrafos ON paragrafos.id = itens.id
            WHERE paragrafos.capitulo = ?
            ORDER BY itens.sequencia
            """,
            (int(capitulo),),
        ).fetchall()
        sem_conteudo = conexao.execute(
            """
            SELECT sem_conteudo.id FROM sem_conteudo
            JOIN paragrafos ON paragrafos.id = sem_conteudo.id
            WHERE paragrafos.capitulo = ?
            ORDER BY paragrafos.numero
            """,
            (int(capitulo),),
        ).fetchall()
        pronto = conexao.execute(
            "SELECT EXISTS(SELECT 1 FROM capitulos_indexados WHERE capitulo = ?)",
            (int(capitulo),),
        ).fetchone()[0]
    return itens, [id for (id,) in sem_conteudo], bool(pronto)


def restaurar_capitulo(slug: str, capitulo: str, estado: EstadoCapitulo) -> None:
    itens, sem_conteudo, pronto = estado
    with _abrir(slug) as conexao:
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
            "INSERT INTO itens (sequencia, id, tipo, ancora, afirmacao) VALUES (?, ?, ?, ?, ?)",
            itens,
        )
        conexao.executemany(
            "INSERT INTO sem_conteudo (id) VALUES (?)",
            [(id,) for id in sem_conteudo],
        )
        conexao.execute(
            "DELETE FROM capitulos_indexados WHERE capitulo = ?", (int(capitulo),)
        )
        if pronto:
            conexao.execute(
                "INSERT INTO capitulos_indexados (capitulo) VALUES (?)",
                (int(capitulo),),
            )
