"""Gera antigo/livro.sqlite, a fixture da SPEC 038.

Rodar da raiz do repositório:
    uv run --no-project python tests/acceptance/038-livro-antigo/fixtures/_gerar_banco.py

O livro de dois-capitulos.pdf (SPEC 001) gravado no formato do commit af7a1d3, o fim do bloco A:
só as tabelas ficha, capitulos, paragrafos, notas e bibliografia.
"""
import sqlite3
from pathlib import Path

CAPITULOS = {
    "Capítulo Um": [
        "O homem parou diante do túmulo e leu o próprio nome gravado no cimento.",
        "A irmã reconheceu o apelido de infância antes de reconhecer o rosto.",
        "Naquela tarde, ninguém na aldeia quis falar sobre o enterro.",
    ],
    "Capítulo Dois": [
        "O médico assinou a certidão às três horas da tarde.",
        "Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.",
    ],
}

saida = Path(__file__).with_name("antigo") / "livro.sqlite"
saida.parent.mkdir(exist_ok=True)
saida.unlink(missing_ok=True)
with sqlite3.connect(saida) as conexao:
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
        """
    )
    conexao.execute("INSERT INTO ficha (lingua) VALUES (NULL)")
    for numero, (titulo, paragrafos) in enumerate(CAPITULOS.items(), start=1):
        conexao.execute("INSERT INTO capitulos (numero, titulo) VALUES (?, ?)", (numero, titulo))
        for p, texto in enumerate(paragrafos, start=1):
            conexao.execute(
                "INSERT INTO paragrafos (id, capitulo, numero, texto) VALUES (?, ?, ?, ?)",
                (f"{numero:02d}.{p:03d}", numero, p, texto),
            )
conexao.close()
print(saida)
