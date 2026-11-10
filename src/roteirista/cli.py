"""Interface de linha de comando do roteirista."""

import argparse
import math
from pathlib import Path
import re
import sys
import unicodedata

from roteirista import banco, modelo
from roteirista.epub import extrair as extrair_epub
from roteirista.pdf import Livro, extrair as extrair_pdf


_LINGUAS = {"en", "fr", "pt", "es", "de", "it"}
_INTERVALO = re.compile(r"^(\d{2})\.(\d{3})-(\d{2})\.(\d{3})$")


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

    montar = comandos.add_parser("montar")
    montar.add_argument("slug")
    montar.add_argument("ids", nargs="+")

    conferir = comandos.add_parser("conferir")
    conferir.add_argument("slug")
    conferir.add_argument("frase")

    buscar = comandos.add_parser("buscar")
    buscar.add_argument("slug")
    buscar.add_argument("termo")

    indexar = comandos.add_parser("indexar")
    indexar.add_argument("slug")
    indexar.add_argument("capitulo")
    indexar.add_argument("--janela", type=int, default=2000)

    itens = comandos.add_parser("itens")
    itens.add_argument("slug")
    itens.add_argument("capitulo")
    return parser


def _conferencia(livro: Livro) -> list[str]:
    numero_primeiro, primeiro = next(
        (numero, capitulo)
        for numero, capitulo in enumerate(livro.capitulos, start=1)
        if capitulo.paragrafos
    )
    ultimo = livro.capitulos[-1]
    numero = len(livro.capitulos)
    return [
        f"{numero_primeiro:02d}.001 {primeiro.paragrafos[0]}",
        f"{numero:02d}.001 {ultimo.paragrafos[0]}",
        f"{numero:02d}.{len(ultimo.paragrafos):03d} {ultimo.paragrafos[-1]}",
    ]


def _montar(slug: str, argumentos: list[str]) -> tuple[list[tuple[str, str]], str | None]:
    blocos = []
    for argumento in argumentos:
        ids = [argumento]
        if "-" in argumento:
            intervalo = _INTERVALO.fullmatch(argumento)
            if intervalo is None:
                return [], f"intervalo inválido: {argumento}"
            capitulo_inicial, inicio, capitulo_final, fim = intervalo.groups()
            if capitulo_inicial != capitulo_final or int(inicio) > int(fim):
                return [], f"intervalo inválido: {argumento}"
            ids = [
                f"{capitulo_inicial}.{numero:03d}"
                for numero in range(int(inicio), int(fim) + 1)
            ]
        for id in ids:
            texto = banco.trecho(slug, id)
            if texto is None:
                return [], f"id inexistente: {id}"
            blocos.append((id, texto))
    return blocos, None


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

    if args.comando == "conferir":
        frase = unicodedata.normalize("NFC", re.sub(r"\s+", " ", args.frase).strip())
        ids = []
        for id, texto in banco.textos(args.slug):
            texto = re.sub(r"\[n\d{2}\]", "", texto)
            texto = unicodedata.normalize("NFC", re.sub(r"\s+", " ", texto).strip())
            if frase in texto:
                ids.append(id)
        if not ids:
            sys.stdout.write("NÃO EXISTE\n")
            raise SystemExit(1)
        sys.stdout.write(f"EXISTE {' '.join(ids)}\n")
        return

    if args.comando == "buscar":
        termo = unicodedata.normalize("NFC", args.termo).casefold()
        ids = [
            id
            for id, texto in banco.textos(args.slug)
            if termo in unicodedata.normalize("NFC", texto).casefold()
        ]
        if not ids:
            raise SystemExit(1)
        sys.stdout.write("".join(f"{id}\n" for id in ids))
        return

    if args.comando == "indexar":
        try:
            resultado = modelo.indexar(args.slug, args.capitulo, args.janela)
        except modelo.CapituloInexistente:
            sys.stderr.write(f"capítulo inexistente: {args.capitulo}\n")
            raise SystemExit(2)
        except modelo.ModeloInacessivel as erro:
            sys.stderr.write(f"modelo inacessível: {erro.url}\n")
            raise SystemExit(3)
        for aviso in resultado.avisos:
            sys.stdout.write(f"{aviso}\n")
        sys.stdout.write(
            f"{len(resultado.itens)} itens gravados, 0 corrigidos, "
            f"{resultado.rejeitados} rejeitados\n"
        )
        return

    if args.comando == "itens":
        for id, tipo, ancora, afirmacao in banco.itens(args.slug, args.capitulo):
            sys.stdout.write(f"{id} | {tipo} | {ancora} | {afirmacao}\n")
        return

    if args.comando == "montar":
        blocos, erro = _montar(args.slug, args.ids)
        if erro is not None:
            sys.stderr.write(f"{erro}\n")
            raise SystemExit(2)
        saida = "\n\n".join(f"## {id}\n\n{texto}" for id, texto in blocos)
        sys.stdout.write(f"{saida}\n")
        return

    texto = banco.trecho(args.slug, args.id)
    if texto is None:
        sys.stderr.write(f"id inexistente: {args.id}\n")
        raise SystemExit(2)
    sys.stdout.write(f"{texto}\n")
