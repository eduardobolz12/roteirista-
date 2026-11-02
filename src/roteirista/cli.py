"""Interface de linha de comando do roteirista."""

import argparse
from pathlib import Path
import sys

from roteirista import banco
from roteirista.epub import extrair as extrair_epub
from roteirista.pdf import extrair as extrair_pdf


def _argumentos() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="livro")
    comandos = parser.add_subparsers(dest="comando", required=True)

    novo = comandos.add_parser("novo")
    novo.add_argument("arquivo", type=Path)
    novo.add_argument("--slug", required=True)

    trecho = comandos.add_parser("trecho")
    trecho.add_argument("slug")
    trecho.add_argument("id")
    return parser


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    sys.stderr.reconfigure(encoding="utf-8", newline="\n")
    args = _argumentos().parse_args()

    if args.comando == "novo":
        extrair = extrair_epub if args.arquivo.suffix.casefold() == ".epub" else extrair_pdf
        livro = extrair(args.arquivo)
        banco.criar(args.slug, livro)
        total = sum(len(capitulo.paragrafos) for capitulo in livro.capitulos)
        sys.stdout.write(f"{len(livro.capitulos)} capítulos, {total} parágrafos\n")
        return

    texto = banco.trecho(args.slug, args.id)
    if texto is None:
        sys.stderr.write(f"id inexistente: {args.id}\n")
        raise SystemExit(2)
    sys.stdout.write(f"{texto}\n")
