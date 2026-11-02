"""Interface de linha de comando do roteirista."""

import argparse
import math
from pathlib import Path
import sys
import unicodedata

from roteirista import banco
from roteirista.epub import extrair as extrair_epub
from roteirista.pdf import Livro, extrair as extrair_pdf


_LINGUAS = {"en", "fr", "pt", "es", "de", "it"}


def _argumentos() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="livro")
    comandos = parser.add_subparsers(dest="comando", required=True)

    novo = comandos.add_parser("novo")
    novo.add_argument("arquivo", type=Path)
    novo.add_argument("--slug", required=True)
    novo.add_argument("--lingua")

    trecho = comandos.add_parser("trecho")
    trecho.add_argument("slug")
    trecho.add_argument("id")

    ficha = comandos.add_parser("ficha")
    ficha.add_argument("slug")

    medir = comandos.add_parser("medir")
    medir.add_argument("slug")
    return parser


def _conferencia(livro: Livro) -> list[str]:
    primeiro = livro.capitulos[0]
    ultimo = livro.capitulos[-1]
    numero = len(livro.capitulos)
    return [
        f"01.001 {primeiro.paragrafos[0]}",
        f"{numero:02d}.001 {ultimo.paragrafos[0]}",
        f"{numero:02d}.{len(ultimo.paragrafos):03d} {ultimo.paragrafos[-1]}",
    ]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    sys.stderr.reconfigure(encoding="utf-8", newline="\n")
    args = _argumentos().parse_args()

    if args.comando == "novo":
        if args.lingua is not None and args.lingua not in _LINGUAS:
            sys.stderr.write(f"língua inválida: {args.lingua}\n")
            raise SystemExit(2)
        extrair = extrair_epub if args.arquivo.suffix.casefold() == ".epub" else extrair_pdf
        livro = extrair(args.arquivo)
        banco.criar(args.slug, livro, args.lingua)
        total = sum(len(capitulo.paragrafos) for capitulo in livro.capitulos)
        for linha in _conferencia(livro):
            sys.stdout.write(f"{linha}\n")
        sys.stdout.write(f"{len(livro.capitulos)} capítulos, {total} parágrafos\n")
        return

    if args.comando == "ficha":
        lingua, capitulos, paragrafos = banco.ficha(args.slug)
        sys.stdout.write(f"língua: {lingua or 'não informada'}\n")
        sys.stdout.write(f"capítulos: {capitulos}\n")
        sys.stdout.write(f"parágrafos: {paragrafos}\n")
        return

    if args.comando == "medir":
        total_palavras = 0
        total_tokens = 0
        for numero, paragrafos in banco.capitulos(args.slug):
            palavras = sum(len(paragrafo.split()) for paragrafo in paragrafos)
            caracteres = sum(len(unicodedata.normalize("NFC", paragrafo)) for paragrafo in paragrafos)
            tokens = math.ceil(caracteres / 4)
            total_palavras += palavras
            total_tokens += tokens
            sys.stdout.write(f"{numero:02d} {palavras} palavras, {tokens} tokens\n")
        sys.stdout.write(f"total {total_palavras} palavras, {total_tokens} tokens\n")
        return

    texto = banco.trecho(args.slug, args.id)
    if texto is None:
        sys.stderr.write(f"id inexistente: {args.id}\n")
        raise SystemExit(2)
    sys.stdout.write(f"{texto}\n")
