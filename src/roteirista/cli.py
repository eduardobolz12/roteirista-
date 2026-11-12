"""Interface de linha de comando do roteirista."""

import argparse
from collections import Counter
import math
from pathlib import Path
import re
import sys
import unicodedata

from roteirista import banco, modelo, nuvem, pesquisa, revisao, traducao, validadores, web
from roteirista.epub import extrair as extrair_epub
from roteirista.pdf import Livro, extrair as extrair_pdf


_LINGUAS = {"en", "fr", "pt", "es", "de", "it"}
_INTERVALO = re.compile(
    r"^((?:\d{2}|W\d{2}))\.(\d{3})-((?:\d{2}|W\d{2}))\.(\d{3})$"
)
_MARCAS_HESITACAO = {
    "en": (
        (
            "conjecture", "hypothesis", "wrong", "mistaken", "uncertain",
            "uncertainty", "doubt", "unclear", "speculat", "possibly",
            "i suspect", "not sure", "no evidence", "remains to be",
        ),
        (
            "perhaps", "probably", "apparently", "presumably", "it seems",
            "it appears", "appears to", "seemed to", "may have", "might have",
            "could have", "unknown",
        ),
    ),
    "fr": (
        (
            "conjecture", "hypothèse", "erreur", "je me trompais", "incertain",
            "incertitude", "doute", "douteux", "spécul", "possiblement",
            "je soupçonne", "pas sûr", "aucune preuve", "reste à",
        ),
        (
            "peut-être", "probablement", "sans doute", "apparemment",
            "vraisemblablement", "il semble", "il paraît", "semblait",
            "aurait pu", "pourrait",
        ),
    ),
}


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

    fonte = comandos.add_parser("fonte")
    fonte.add_argument("slug")
    fonte.add_argument("url")

    fontes = comandos.add_parser("fontes")
    fontes.add_argument("slug")

    ficha = comandos.add_parser("ficha")
    ficha.add_argument("slug")

    medir = comandos.add_parser("medir")
    medir.add_argument("slug")

    montar = comandos.add_parser("montar")
    montar.add_argument("slug")
    montar.add_argument("ids", nargs="+")

    validar_temas = comandos.add_parser("validar-temas")
    validar_temas.add_argument("slug")
    validar_temas.add_argument("arquivo", type=Path)

    validar_briefing = comandos.add_parser("validar-briefing")
    validar_briefing.add_argument("slug")
    validar_briefing.add_argument("arquivo", type=Path)
    validar_briefing.add_argument("--temas", type=Path)

    contar = comandos.add_parser("contar")
    contar.add_argument("slug")
    contar.add_argument("capitulo", type=Path)
    contar.add_argument("--briefing", type=Path)

    glossario = comandos.add_parser("glossario")
    glossario.add_argument("slug")
    glossario.add_argument("lingua")
    glossario.add_argument("termo", nargs="?")
    glossario.add_argument("traducao", nargs="?")
    glossario.add_argument("--conferir", type=Path, nargs=2)

    invariantes = comandos.add_parser("invariantes")
    invariantes.add_argument("slug")
    invariantes.add_argument("antes", type=Path)
    invariantes.add_argument("depois", type=Path)

    revisar = comandos.add_parser("revisar")
    revisar.add_argument("slug")
    revisar.add_argument("texto", type=Path)
    revisar.add_argument("ids", nargs="+")

    pesquisar = comandos.add_parser("pesquisar")
    pesquisar.add_argument("slug")
    pesquisar.add_argument("pergunta")
    pesquisar.add_argument("--busca", required=True)
    pesquisar.add_argument("--wiki", action="store_true")

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

    indexar_livro = comandos.add_parser("indexar-livro")
    indexar_livro.add_argument("slug")
    indexar_livro.add_argument("--janela", type=int, default=2000)
    indexar_livro.add_argument("--refazer", action="store_true")

    itens = comandos.add_parser("itens")
    itens.add_argument("slug")
    itens.add_argument("capitulo")

    lacunas = comandos.add_parser("lacunas")
    lacunas.add_argument("slug")
    lacunas.add_argument("capitulo")

    repescar = comandos.add_parser("repescar")
    repescar.add_argument("slug")
    repescar.add_argument("capitulo")
    repescar.add_argument("--janela", type=int, default=2000)

    visao = comandos.add_parser("visao")
    visao.add_argument("slug")

    contar_tema = comandos.add_parser("contar-tema")
    contar_tema.add_argument("slug")
    contar_tema.add_argument("termos", nargs="+")

    hesitacoes = comandos.add_parser("hesitacoes")
    hesitacoes.add_argument("slug")
    opcoes = hesitacoes.add_mutually_exclusive_group()
    opcoes.add_argument("--todas", action="store_true")
    opcoes.add_argument("--julgadas", action="store_true")

    julgar = comandos.add_parser("julgar")
    julgar.add_argument("slug")
    julgar.add_argument("id")
    julgar.add_argument("julgamento", choices=("hesitacao", "nao"))
    julgar.add_argument("nota")
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


def _resumo_indexacao(resultado: modelo.Resultado) -> str:
    corrigidos = sum(aviso.startswith("corrigido:") for aviso in resultado.avisos)
    return (
        f"{len(resultado.itens)} itens gravados, {corrigidos} corrigidos, "
        f"{resultado.rejeitados} rejeitados"
    )


def _resumo_repescagem(resultado: modelo.ResultadoRepescagem) -> str:
    return (
        f"{len(resultado.itens)} itens gravados, "
        f"{len(resultado.sem_conteudo)} sem conteúdo, "
        f"{resultado.rejeitados} rejeitados"
    )


def _indexar_livro(slug: str, janela: int, refazer: bool) -> int:
    prontos = set() if refazer else banco.capitulos_prontos(slug)
    indexados = 0
    ja_estavam = 0
    for numero, paragrafos in banco.capitulos(slug):
        capitulo = f"{numero:02d}"
        if numero in prontos:
            sys.stdout.write(f"{capitulo} | já indexado\n")
            ja_estavam += 1
            continue
        if not paragrafos:
            sys.stdout.write(f"{capitulo} | sem parágrafos\n")
            continue
        estado = banco.capturar_capitulo(slug, capitulo)
        try:
            indexacao = modelo.indexar(slug, capitulo, janela)
            repescagem = modelo.repescar(slug, capitulo, janela)
        except modelo.ModeloInacessivel as erro:
            banco.restaurar_capitulo(slug, capitulo, estado)
            sys.stderr.write(f"modelo inacessível: {erro.url}\n")
            return 3
        banco.marcar_capitulo(slug, capitulo)
        lacunas = len(banco.lacunas(slug, capitulo))
        sys.stdout.write(
            f"{capitulo} | {_resumo_indexacao(indexacao)} | "
            f"{_resumo_repescagem(repescagem)} | lacunas {lacunas}\n"
        )
        indexados += 1
    sys.stdout.write(f"{indexados} capítulos indexados, {ja_estavam} já estavam\n")
    return 0


def _nomes_afirmacao(texto: str) -> list[str]:
    sequencias: list[tuple[int, list[str]]] = []
    sequencia: list[str] = []
    inicio = 0
    fim_anterior = None
    for achado in re.finditer(r"[^\W\d_]+", texto):
        palavra = achado.group()
        seguida = bool(
            sequencia
            and fim_anterior is not None
            and texto[fim_anterior : achado.start()].isspace()
        )
        valida = len(palavra) >= 2 and palavra[0].isupper()
        if valida and (not sequencia or seguida):
            if not sequencia:
                inicio = achado.start()
            sequencia.append(palavra)
        else:
            if sequencia:
                sequencias.append((inicio, sequencia))
            sequencia = [palavra] if valida else []
            if valida:
                inicio = achado.start()
        fim_anterior = achado.end()
    if sequencia:
        sequencias.append((inicio, sequencia))

    nomes = []
    for inicio, palavras in sequencias:
        prefixo = texto[:inicio].rstrip()
        if not prefixo or prefixo[-1] in ".!?:;“‘\"'(«":
            palavras = palavras[1:]
        if palavras:
            nomes.append(" ".join(palavras))
    return nomes


def _visao(slug: str) -> None:
    capitulos: dict[int, tuple[str, list[tuple[str, str, str, str]]]] = {}
    for numero, titulo, id, tipo, ancora, afirmacao in banco.itens_livro(slug):
        capitulos.setdefault(numero, (titulo, []))[1].append(
            (id, tipo, ancora, afirmacao)
        )
    for numero, (titulo, fichas) in capitulos.items():
        tipos = Counter(ficha[1] for ficha in fichas)
        sys.stdout.write(
            f"{numero:02d} {titulo} — {len(fichas)} fichas; "
            f"numero {tipos['numero']}, contradicao {tipos['contradicao']}\n"
        )
        nomes = Counter(
            nome
            for ficha in fichas
            for nome in _nomes_afirmacao(ficha[3])
        )
        frequentes = sorted(
            ((nome, vezes) for nome, vezes in nomes.items() if vezes >= 2),
            key=lambda item: -item[1],
        )[:10]
        listagem = ", ".join(f"{nome} ({vezes})" for nome, vezes in frequentes)
        sys.stdout.write(f"   nomes: {listagem or '—'}\n")
        termos = Counter(ficha[2] for ficha in fichas if ficha[1] == "termo")
        ordenados = sorted(termos, key=lambda termo: -termos[termo])[:8]
        sys.stdout.write(f"   termos: {', '.join(ordenados) or '—'}\n")


def _palavras_tema(texto: str) -> list[str]:
    return re.findall(r"[^\W_]+", unicodedata.normalize("NFC", texto).casefold())


def _tema_confere(texto: str, termos: list[list[str]]) -> bool:
    palavras = _palavras_tema(texto)
    for termo in termos:
        for inicio in range(len(palavras) - len(termo) + 1):
            if all(
                palavras[inicio + deslocamento].startswith(procurada)
                for deslocamento, procurada in enumerate(termo)
            ):
                return True
    return False


def _contar_tema(slug: str, termos: list[str]) -> int:
    procurados = [palavras for termo in termos if (palavras := _palavras_tema(termo))]
    fichas = [
        ficha
        for ficha in banco.itens_livro(slug)
        if _tema_confere(ficha[4], procurados)
        or _tema_confere(ficha[5], procurados)
    ]
    paragrafos = {ficha[2] for ficha in fichas}
    por_capitulo = Counter(ficha[0] for ficha in fichas)
    sys.stdout.write(
        f"{len(fichas)} fichas, {len(paragrafos)} parágrafos, "
        f"{len(por_capitulo)} capítulos\n"
    )
    if not fichas:
        return 1
    ordenados = sorted(por_capitulo, key=lambda capitulo: -por_capitulo[capitulo])
    listagem = ", ".join(
        f"{capitulo:02d} ({por_capitulo[capitulo]})" for capitulo in ordenados
    )
    sys.stdout.write(f"capítulos: {listagem}\n")
    tipos = Counter(ficha[3] for ficha in fichas)
    sys.stdout.write(
        f"numero {tipos['numero']}, contradicao {tipos['contradicao']}\n"
    )
    return 0


def _marcas_livro(slug: str) -> tuple[tuple[str, ...], tuple[str, ...]] | None:
    lingua = banco.ficha(slug)[0]
    if lingua not in _MARCAS_HESITACAO:
        sys.stderr.write(
            f"sem palavras-marca para a língua: {lingua or 'não informada'}\n"
        )
        return None
    return _MARCAS_HESITACAO[lingua]


def _lista_hesitacoes(
    slug: str, marcas: tuple[tuple[str, ...], tuple[str, ...]], todas: bool
) -> list[tuple[str, list[str]]]:
    fortes, fracas = marcas
    procuradas = fortes + fracas if todas else fortes
    resultado = []
    for id, texto in banco.paragrafos_livro(slug):
        normalizado = unicodedata.normalize("NFC", texto).casefold()
        normalizado = normalizado.translate(
            str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})
        )
        achadas = []
        for marca in procuradas:
            expressao = re.escape(marca).replace(r"\ ", r"\s+")
            if re.search(rf"(?<!\w){expressao}", normalizado):
                achadas.append(marca)
        if achadas:
            resultado.append((id, achadas))
    return resultado


def _prompt_documento(nome: str) -> str:
    caminho = Path(__file__).resolve().parents[2] / "docs" / "prompts" / nome
    return caminho.read_text(encoding="utf-8")


def _revisar(slug: str, arquivo: Path, argumentos: list[str]) -> int:
    blocos, erro = _montar(slug, argumentos)
    if erro is not None:
        sys.stderr.write(f"{erro}\n")
        return 2
    texto = arquivo.read_text(encoding="utf-8")
    material = "\n\n".join(f"## {id}\n\n{conteudo}" for id, conteudo in blocos)
    prompt = _prompt_documento("revisar.txt").replace("{material}", material)
    prompt = prompt.replace("{texto}", texto)
    try:
        modelo_usado, resposta = nuvem.responder(prompt)
    except nuvem.ChaveNaoInformada:
        sys.stderr.write("chave da nuvem não informada: ROTEIRISTA_NUVEM_CHAVE\n")
        return 2
    except nuvem.NenhumModeloRespondeu:
        sys.stderr.write("nenhum modelo gratuito respondeu\n")
        return 3
    linhas, apontamentos, descartados = revisao.conferir(
        texto, resposta, {id for id, _ in blocos}
    )
    linhas.append(
        f"{apontamentos} apontamentos, {descartados} descartados — {modelo_usado}"
    )
    saida = "\n".join(linhas) + "\n"
    arquivo.with_suffix(".revisao.txt").write_text(saida, encoding="utf-8", newline="\n")
    sys.stdout.write(saida)
    return 0


def _pesquisar(slug: str, pergunta: str, termos: str, wiki: bool) -> int:
    try:
        encontradas = web.buscar(termos, wiki)
    except web.BuscaFalhou as erro:
        sys.stderr.write(f"busca falhou: {erro.fonte} ({erro.motivo})\n")
        return 3
    if not encontradas:
        sys.stdout.write("0 fontes\n")
        return 1

    registros = []
    for fonte in encontradas:
        chave = web.chave_url(fonte.url)
        registro = banco.fonte_por_url(slug, chave)
        if registro is None:
            registro = banco.gravar_fonte(slug, fonte, chave)
        registros.append(registro)

    blocos = [
        bloco
        for registro in registros
        for bloco in banco.paragrafos_fonte(slug, registro[0])
    ]
    fontes = "\n\n".join(f"## {id}\n\n{texto}" for id, texto in blocos)
    prompt = _prompt_documento("pesquisar.txt").replace("{pergunta}", pergunta)
    prompt = prompt.replace("{fontes}", fontes)
    try:
        modelo_usado, resposta = nuvem.responder(prompt)
    except nuvem.ChaveNaoInformada:
        sys.stderr.write("chave da nuvem não informada: ROTEIRISTA_NUVEM_CHAVE\n")
        return 2
    except nuvem.NenhumModeloRespondeu:
        sys.stderr.write("nenhum modelo gratuito respondeu\n")
        return 3

    linhas = [
        f"fonte {id} | {autor} | {ano} | {titulo}"
        for id, autor, ano, titulo, _ in registros
    ]
    conferidos, achados, recusados = pesquisa.conferir(resposta, dict(blocos))
    linhas.extend(conferidos)
    linhas.append(f"{achados} achados, {recusados} recusados — {modelo_usado}")
    sys.stdout.write("\n".join(linhas) + "\n")
    return 0


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    sys.stderr.reconfigure(encoding="utf-8", newline="\n")
    args = _argumentos().parse_args()

    if args.comando == "glossario":
        if args.lingua not in {"en", "fr"}:
            sys.stderr.write(f"língua inválida: {args.lingua}\n")
            raise SystemExit(2)
        if args.conferir is not None:
            try:
                resultado = traducao.conferir_glossario(
                    args.slug, args.lingua, *args.conferir
                )
            except FileNotFoundError as erro:
                sys.stderr.write(f"arquivo inexistente: {erro.filename}\n")
                raise SystemExit(2)
            sys.stdout.write(resultado.saida)
            raise SystemExit(resultado.codigo)
        if (args.termo is None) != (args.traducao is None):
            sys.stderr.write("termo e tradução devem ser informados juntos\n")
            raise SystemExit(2)
        if args.termo is None:
            termos = banco.glossario(args.slug, args.lingua)
            for termo, traduzido in termos:
                sys.stdout.write(f"{termo} → {traduzido}\n")
            sys.stdout.write(f"{len(termos)} termos ({args.lingua})\n")
            return
        anterior = banco.gravar_termo(
            args.slug, args.lingua, args.termo, args.traducao
        )
        if anterior is None:
            sys.stdout.write(f"gravado: {args.termo} → {args.traducao}\n")
        else:
            sys.stdout.write(
                f"trocado: {args.termo}: {anterior} → {args.traducao}\n"
            )
        return

    if args.comando == "invariantes":
        linguas = []
        for arquivo in (args.antes, args.depois):
            lingua = traducao.lingua_arquivo(arquivo)
            if lingua is None:
                sys.stderr.write(f"língua desconhecida: {arquivo.name}\n")
                raise SystemExit(2)
            linguas.append(lingua)
        try:
            resultado = traducao.conferir_invariantes(
                args.slug, args.antes, args.depois, *linguas
            )
        except FileNotFoundError as erro:
            sys.stderr.write(f"arquivo inexistente: {erro.filename}\n")
            raise SystemExit(2)
        sys.stdout.write(resultado.saida)
        raise SystemExit(resultado.codigo)

    if args.comando == "validar-temas":
        try:
            resultado = validadores.validar_temas(args.slug, args.arquivo)
        except FileNotFoundError:
            sys.stderr.write(f"arquivo inexistente: {args.arquivo}\n")
            raise SystemExit(2)
        sys.stdout.write(resultado.saida)
        raise SystemExit(resultado.codigo)

    if args.comando == "validar-briefing":
        temas = None
        if args.temas is not None:
            try:
                temas = validadores.validar_temas(args.slug, args.temas)
            except FileNotFoundError:
                sys.stderr.write(f"arquivo inexistente: {args.temas}\n")
                raise SystemExit(2)
            if temas.codigo != 0:
                sys.stderr.write(
                    "o arquivo de temas tem problemas: rode livro validar-temas\n"
                )
                raise SystemExit(2)
        try:
            resultado = validadores.validar_briefing(args.slug, args.arquivo, temas)
        except FileNotFoundError:
            sys.stderr.write(f"arquivo inexistente: {args.arquivo}\n")
            raise SystemExit(2)
        sys.stdout.write(resultado.saida)
        raise SystemExit(resultado.codigo)

    if args.comando == "contar":
        try:
            resultado = validadores.contar_capitulo(
                args.slug, args.capitulo, args.briefing
            )
        except FileNotFoundError as erro:
            sys.stderr.write(f"arquivo inexistente: {erro.filename}\n")
            raise SystemExit(2)
        sys.stdout.write(resultado.saida)
        raise SystemExit(resultado.codigo)

    if args.comando == "fonte":
        chave = web.chave_url(args.url)
        existente = banco.fonte_por_url(args.slug, chave)
        if existente is not None:
            sys.stdout.write(f"{existente[0]} | já gravada\n")
            return
        try:
            fonte = web.carregar(args.url)
        except web.FonteNaoSuportada:
            sys.stderr.write(f"fonte não suportada: {args.url}\n")
            raise SystemExit(2)
        except web.FonteNaoEncontrada:
            sys.stderr.write(f"fonte não encontrada: {args.url}\n")
            raise SystemExit(2)
        except web.FonteSemTexto:
            sys.stderr.write(f"fonte sem texto: {args.url}\n")
            raise SystemExit(2)
        except web.FonteInacessivel:
            sys.stderr.write(f"fonte inacessível: {args.url}\n")
            raise SystemExit(3)
        gravada = banco.gravar_fonte(args.slug, fonte, chave)
        sys.stdout.write(
            f"{gravada[0]} | {gravada[1]} | {gravada[2]} | {gravada[3]}\n"
            f"{len(fonte.paragrafos)} parágrafos\n"
        )
        return

    if args.comando == "fontes":
        for id, autor, ano, titulo, url in banco.fontes(args.slug):
            sys.stdout.write(f"{id} | {autor} | {ano} | {titulo} | {url}\n")
        return

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
        banco.desmarcar_capitulo(args.slug, args.capitulo)
        for aviso in resultado.avisos:
            sys.stdout.write(f"{aviso}\n")
        sys.stdout.write(f"{_resumo_indexacao(resultado)}\n")
        return

    if args.comando == "indexar-livro":
        raise SystemExit(_indexar_livro(args.slug, args.janela, args.refazer))

    if args.comando == "itens":
        for id, tipo, ancora, afirmacao in banco.itens(args.slug, args.capitulo):
            sys.stdout.write(f"{id} | {tipo} | {ancora} | {afirmacao}\n")
        return

    if args.comando == "lacunas":
        for id in banco.lacunas(args.slug, args.capitulo):
            sys.stdout.write(f"{id}\n")
        return

    if args.comando == "repescar":
        try:
            resultado = modelo.repescar(args.slug, args.capitulo, args.janela)
        except modelo.CapituloInexistente:
            sys.stderr.write(f"capítulo inexistente: {args.capitulo}\n")
            raise SystemExit(2)
        except modelo.ModeloInacessivel as erro:
            sys.stderr.write(f"modelo inacessível: {erro.url}\n")
            raise SystemExit(3)
        for aviso in resultado.avisos:
            sys.stdout.write(f"{aviso}\n")
        sys.stdout.write(f"{_resumo_repescagem(resultado)}\n")
        return

    if args.comando == "visao":
        _visao(args.slug)
        return

    if args.comando == "contar-tema":
        raise SystemExit(_contar_tema(args.slug, args.termos))

    if args.comando == "hesitacoes":
        marcas = _marcas_livro(args.slug)
        if marcas is None:
            raise SystemExit(2)
        if args.julgadas:
            for id, julgamento, nota in banco.hesitacoes_julgadas(args.slug):
                sys.stdout.write(f"{id} | {julgamento} | {nota}\n")
            return
        for id, achadas in _lista_hesitacoes(args.slug, marcas, args.todas):
            sys.stdout.write(f"{id} | {', '.join(achadas)}\n")
        return

    if args.comando == "julgar":
        marcas = _marcas_livro(args.slug)
        if marcas is None:
            raise SystemExit(2)
        ids = {
            id
            for id, _ in _lista_hesitacoes(args.slug, marcas, todas=True)
        }
        if args.id not in ids:
            sys.stderr.write(f"id fora da lista: {args.id}\n")
            raise SystemExit(2)
        banco.julgar_hesitacao(args.slug, args.id, args.julgamento, args.nota)
        return

    if args.comando == "pesquisar":
        raise SystemExit(
            _pesquisar(args.slug, args.pergunta, args.busca, args.wiki)
        )

    if args.comando == "revisar":
        raise SystemExit(_revisar(args.slug, args.texto, args.ids))

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
