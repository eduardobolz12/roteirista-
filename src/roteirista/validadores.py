"""Validadores determinísticos de temas, briefings e capítulos."""

from dataclasses import dataclass, field
from pathlib import Path
import re
import unicodedata

from roteirista import banco


_ID_SIMPLES = r"(?:\d{2}\.(?:\d{3}|n\d{2})|W\d{2}\.\d{3})"
_ID_NO_TEXTO = re.compile(
    rf"(?<![\w.]){_ID_SIMPLES}(?:[-–]{_ID_SIMPLES})?(?![\w.])"
)
_REFERENCIA = re.compile(
    r"^(\d{2}|W\d{2})\.(\d{3}|n\d{2})"
    r"(?:[-–](\d{2}|W\d{2})\.(\d{3}|n\d{2}))?$"
)
_SECOES_TEMAS = (
    "Resumo",
    "Assuntos compartilhados e a casa de cada um",
    "Detalhe de cada candidato",
    "Sua decisão",
)


@dataclass(frozen=True)
class LinhaTabela:
    numero: int
    celulas: list[str]


@dataclass(frozen=True)
class Assunto:
    nome: str
    ids: frozenset[str]
    casa: int


@dataclass
class ResultadoTemas:
    saida: str
    codigo: int
    temas: list[int] = field(default_factory=list)
    assuntos: list[Assunto] = field(default_factory=list)


def expandir(referencia: str) -> list[str] | None:
    """Expande um id ou intervalo; devolve None para uma forma inválida."""
    achado = _REFERENCIA.fullmatch(referencia.strip())
    if achado is None:
        return None
    capitulo, inicio, capitulo_final, fim = achado.groups()
    if capitulo_final is None:
        return [f"{capitulo}.{inicio}"]
    if (
        capitulo != capitulo_final
        or inicio.startswith("n") != fim.startswith("n")
        or int(inicio.removeprefix("n")) > int(fim.removeprefix("n"))
    ):
        return None
    largura = len(inicio.removeprefix("n"))
    prefixo = "n" if inicio.startswith("n") else ""
    return [
        f"{capitulo}.{prefixo}{numero:0{largura}d}"
        for numero in range(
            int(inicio.removeprefix("n")), int(fim.removeprefix("n")) + 1
        )
    ]


def ids_no_texto(texto: str):
    """Itera pelas referências e suas posições em um texto Markdown."""
    for achado in _ID_NO_TEXTO.finditer(texto):
        yield achado.group(), achado.start()


def _celulas(linha: str) -> list[str]:
    return [celula.strip() for celula in linha.strip().strip("|").split("|")]


def _separador(celulas: list[str]) -> bool:
    return all(re.fullmatch(r":?-+:?", celula.replace(" ", "")) for celula in celulas)


def ler_tabela(linhas: list[str], secao: str) -> tuple[list[str], list[LinhaTabela]]:
    """Lê o cabeçalho e as linhas de dados da tabela de uma seção."""
    try:
        inicio = next(i for i, linha in enumerate(linhas) if linha == f"## {secao}")
    except StopIteration:
        return [], []
    fim = next(
        (i for i in range(inicio + 1, len(linhas)) if linhas[i].startswith("## ")),
        len(linhas),
    )
    cabecalho_indice = next(
        (i for i in range(inicio + 1, fim) if linhas[i].strip().startswith("|")),
        None,
    )
    if cabecalho_indice is None:
        return [], []
    cabecalho = _celulas(linhas[cabecalho_indice])
    dados = []
    for i in range(cabecalho_indice + 1, fim):
        if not linhas[i].strip().startswith("|"):
            continue
        celulas = _celulas(linhas[i])
        if not _separador(celulas):
            dados.append(LinhaTabela(i + 1, celulas))
    return cabecalho, dados


def _palavras(texto: str) -> list[str]:
    return re.findall(r"[^\W_]+", unicodedata.normalize("NFC", texto).casefold())


def citacao_confere(citacao: str, textos: list[str]) -> bool:
    """Aplica a regra de citação da D-028, inclusive cortes por reticências."""
    palavras = _palavras(" ".join(textos))
    posicao = 0
    encontrou_parte = False
    for parte in re.split(r"\.\.\.|…", citacao):
        procuradas = _palavras(parte)
        if not procuradas:
            continue
        encontrou_parte = True
        limite = len(palavras) - len(procuradas)
        encontrada = next(
            (
                inicio
                for inicio in range(posicao, limite + 1)
                if palavras[inicio : inicio + len(procuradas)] == procuradas
            ),
            None,
        )
        if encontrada is None:
            return False
        posicao = encontrada + len(procuradas)
    return encontrou_parte


def textos_referencia(slug: str, referencia: str) -> tuple[list[str], list[str]]:
    """Devolve os textos existentes e os ids que faltam em uma referência."""
    ids = expandir(referencia) or []
    textos = []
    faltantes = []
    for id in ids:
        texto = banco.trecho(slug, id)
        if texto is None:
            faltantes.append(id)
        else:
            textos.append(texto)
    return textos, faltantes


def _secoes(linhas: list[str]) -> set[str]:
    return {linha[3:].strip() for linha in linhas if linha.startswith("## ")}


def _detalhes(linhas: list[str]) -> dict[int, dict[str, list[tuple[int, str]]]]:
    detalhes = {}
    atual = None
    tipos = {"Enigma": "enigma", "Números": "números", "Rachadura": "rachadura"}
    for numero, linha in enumerate(linhas, start=1):
        if linha.startswith("## "):
            atual = None
        achado = re.match(r"^###\s+(\d+)\s+—", linha)
        if achado:
            atual = int(achado.group(1))
            detalhes.setdefault(atual, {})
        if atual is not None:
            for marca, tipo in tipos.items():
                if linha.startswith(f"- **{marca}"):
                    detalhes[atual].setdefault(tipo, []).append((numero, linha))
    return detalhes


def _casas(slug: str, linhas: list[str], erros: list[tuple[int, int, str]]):
    cabecalho, dados = ler_tabela(linhas, "Assuntos compartilhados e a casa de cada um")
    assuntos = []
    for linha in dados:
        if len(linha.celulas) < 2:
            continue
        marcas = [
            i
            for i, celula in enumerate(linha.celulas[2:], start=2)
            if celula.replace("**", "").strip().casefold() == "casa"
        ]
        texto_linha = linhas[linha.numero - 1]
        if not marcas:
            erros.append((linha.numero, len(texto_linha), "assunto sem casa"))
            continue
        if len(marcas) > 1:
            erros.append(
                (linha.numero, len(texto_linha), "assunto com mais de uma casa")
            )
            continue
        try:
            casa = int(cabecalho[marcas[0]])
        except (IndexError, ValueError):
            continue
        ids = set()
        for referencia, _ in ids_no_texto(linha.celulas[1]):
            ids.update(expandir(referencia) or [])
        assuntos.append(Assunto(linha.celulas[0], frozenset(ids), casa))
    return assuntos


def validar_temas(slug: str, arquivo: Path) -> ResultadoTemas:
    linhas = arquivo.read_text(encoding="utf-8").splitlines()
    secoes = _secoes(linhas)
    problemas = [
        f"falta a seção: {secao}" for secao in _SECOES_TEMAS if secao not in secoes
    ]
    _, resumo = ler_tabela(linhas, "Resumo")
    temas = list(
        dict.fromkeys(
            int(linha.celulas[0])
            for linha in resumo
            if linha.celulas and linha.celulas[0].isdigit()
        )
    )
    erros = []
    for numero, linha in enumerate(linhas, start=1):
        for referencia, coluna in ids_no_texto(linha):
            _, faltantes = textos_referencia(slug, referencia)
            for id in faltantes:
                erros.append((numero, coluna, f"id inexistente: {id}"))
    assuntos = _casas(slug, linhas, erros)
    problemas.extend(
        f"{numero}: {mensagem}" for numero, _, mensagem in sorted(erros)
    )

    detalhes = _detalhes(linhas)
    nomes = {"enigma": "o enigma", "números": "os números", "rachadura": "a rachadura"}
    for tema in temas:
        if tema not in detalhes:
            problemas.append(f"tema {tema}: falta o detalhe")
            continue
        capitulos = set()
        for tipo in ("enigma", "números", "rachadura"):
            itens = detalhes[tema].get(tipo, [])
            referencias = [
                referencia
                for _, texto in itens
                for referencia, _ in ids_no_texto(texto)
            ]
            if not referencias:
                problemas.append(f"tema {tema}: falta {nomes[tipo]} com id")
            for referencia in referencias:
                for id in expandir(referencia) or []:
                    if not id.startswith("W"):
                        capitulos.add(id[:2])
        if len(capitulos) < 2:
            problemas.append(f"tema {tema}: material num só capítulo do livro")

    if problemas:
        problemas.append(f"{len(problemas)} problemas")
        codigo = 1
    else:
        problemas = [f"ok: {len(temas)} temas, {len(assuntos)} assuntos"]
        codigo = 0
    return ResultadoTemas("\n".join(problemas) + "\n", codigo, temas, assuntos)


@dataclass
class ResultadoBriefing:
    saida: str
    codigo: int


_CAMPOS_BRIEFING = (
    "Tema",
    "Capítulo",
    "Função do capítulo",
    "Ao fim, o espectador entende",
    "Duração estimada",
)
_SECOES_BRIEFING = (
    "O que será abordado",
    "Cenas e passagens do livro",
    "Citações literais previstas",
    "Dados da web",
    "O que fica de fora deste capítulo",
    "Ressalvas",
    "Sua decisão",
)


def _referencias_celula(celula: str) -> list[str]:
    referencias = [referencia for referencia, _ in ids_no_texto(celula)]
    return referencias or [celula.strip()]


def _conferir_ids(slug: str, celula: str) -> tuple[set[str], list[str], list[str]]:
    ids = set()
    textos = []
    faltantes = []
    for referencia in _referencias_celula(celula):
        ids.update(expandir(referencia) or [])
        encontrados, ausentes = textos_referencia(slug, referencia)
        textos.extend(encontrados)
        faltantes.extend(ausentes)
        if expandir(referencia) is None:
            faltantes.append(referencia)
    return ids, textos, faltantes


def validar_briefing(
    slug: str, arquivo: Path, temas: ResultadoTemas | None = None
) -> ResultadoBriefing:
    linhas = arquivo.read_text(encoding="utf-8").splitlines()
    campos = {}
    for linha in linhas:
        achado = re.match(r"^\*\*([^*]+):\*\*\s*(.*)$", linha)
        if achado:
            campos[achado.group(1)] = achado.group(2).strip()
    secoes = _secoes(linhas)
    problemas = [
        f"falta o campo: {campo}" for campo in _CAMPOS_BRIEFING if campo not in campos
    ]
    problemas.extend(
        f"falta a seção: {secao}" for secao in _SECOES_BRIEFING if secao not in secoes
    )

    tema = campos.get("Tema")
    tema_numero = int(tema) if tema and tema.isdigit() else tema
    tema_valido = temas is None or tema_numero in temas.temas
    if temas is not None and tema is not None and not tema_valido:
        problemas.append(f"tema {tema} não está no arquivo de temas")

    erros = []
    _, linhas_momentos = ler_tabela(linhas, "O que será abordado")
    momentos = {}
    for linha in linhas_momentos:
        if len(linha.celulas) < 4 or not linha.celulas[0].isdigit():
            continue
        numero = int(linha.celulas[0])
        origem = linha.celulas[3]
        momentos[numero] = origem
        if origem not in {"Livro", "Web", "Narrador"}:
            erros.append((linha.numero, 3, f"origem inválida: {origem}"))

    _, linhas_passagens = ler_tabela(linhas, "Cenas e passagens do livro")
    passagens = []
    passagens_por_momento = set()
    for linha in linhas_passagens:
        if len(linha.celulas) < 4:
            continue
        referencia = linha.celulas[0]
        ids, _, faltantes = _conferir_ids(slug, referencia)
        if faltantes:
            erros.append((linha.numero, 0, f"id inexistente: {referencia}"))
        numeros = [int(numero) for numero in re.findall(r"\d+", linha.celulas[2])]
        for numero in numeros:
            passagens_por_momento.add(numero)
            if numero not in momentos:
                erros.append(
                    (linha.numero, 2, f"momento inexistente: {numero}")
                )
        trato = linha.celulas[3]
        if trato not in {"desenvolver", "mencionar"}:
            erros.append((linha.numero, 3, f"trato inválido: {trato}"))
        passagens.append((linha.numero, referencia, ids, trato))

    _, linhas_citacoes = ler_tabela(linhas, "Citações literais previstas")
    for linha in linhas_citacoes:
        if len(linha.celulas) < 3:
            continue
        referencia = linha.celulas[0]
        _, textos, faltantes = _conferir_ids(slug, referencia)
        if faltantes:
            erros.append((linha.numero, 0, f"id inexistente: {referencia}"))
            continue
        citacao = linha.celulas[1].strip().strip('"“”«»')
        if not citacao_confere(citacao, textos):
            erros.append(
                (
                    linha.numero,
                    1,
                    f"citação não confere em {referencia}: {citacao}",
                )
            )

    _, linhas_dados = ler_tabela(linhas, "Dados da web")
    for linha in linhas_dados:
        if not linha.celulas:
            continue
        referencia = linha.celulas[0]
        _, _, faltantes = _conferir_ids(slug, referencia)
        if faltantes:
            erros.append((linha.numero, 0, f"id inexistente: {referencia}"))

    problemas.extend(
        f"{numero}: {mensagem}" for numero, _, mensagem in sorted(erros)
    )
    for numero in sorted(momentos):
        if momentos[numero] == "Livro" and numero not in passagens_por_momento:
            problemas.append(f"momento {numero}: origem Livro sem passagem")
        if momentos[numero] == "Web" and not linhas_dados:
            problemas.append(f"momento {numero}: origem Web sem dado")

    avisos = []
    if temas is not None and tema_valido:
        for numero, referencia, ids, trato in sorted(passagens):
            if trato != "desenvolver":
                continue
            for assunto in temas.assuntos:
                if assunto.casa != tema_numero and ids.intersection(assunto.ids):
                    avisos.append(
                        f'aviso: {numero}: {referencia} é desenvolvido aqui, '
                        f'mas a casa de "{assunto.nome}" é o tema {assunto.casa}'
                    )

    if problemas:
        finais = problemas + avisos + [f"{len(problemas)} problemas"]
        codigo = 1
    else:
        finais = avisos + [
            f"ok: {len(linhas_momentos)} momentos, {len(linhas_passagens)} passagens, "
            f"{len(linhas_citacoes)} citações, {len(linhas_dados)} dados da web"
        ]
        codigo = 0
    return ResultadoBriefing("\n".join(finais) + "\n", codigo)


@dataclass
class ResultadoContagem:
    saida: str
    codigo: int


_MARCA_ID = re.compile(
    rf"\[\s*({_ID_SIMPLES}(?:[-–]{_ID_SIMPLES})?)\s*\]"
)
_MARCA_ID_SEGUIDA = re.compile(
    rf"\s*\[\s*({_ID_SIMPLES}(?:[-–]{_ID_SIMPLES})?)\s*\]"
)
_ASPAS = re.compile(r'"([^"\n]*)"|“([^”\n]*)”|«([^»\n]*)»')


def _ids_previstos(arquivo: Path | None) -> set[str] | None:
    if arquivo is None:
        return None
    linhas = arquivo.read_text(encoding="utf-8").splitlines()
    previstos = set()
    for secao in ("Citações literais previstas", "Dados da web"):
        _, dados = ler_tabela(linhas, secao)
        previstos.update(
            linha.celulas[0] for linha in dados if linha.celulas
        )
    return previstos


def contar_capitulo(
    slug: str, arquivo: Path, briefing: Path | None = None
) -> ResultadoContagem:
    linhas = arquivo.read_text(encoding="utf-8").splitlines()
    previstos = _ids_previstos(briefing)
    palavras = []
    eventos = []
    citacoes = 0
    problemas = 0
    for numero, linha in enumerate(linhas, start=1):
        despojada = linha.strip()
        if not despojada or despojada.startswith("#"):
            continue
        if re.fullmatch(r"\[[^\]]*\]", despojada):
            continue
        narrado = _MARCA_ID.sub("", linha)
        palavras.extend(
            pedaco for pedaco in narrado.split() if any(c.isalnum() for c in pedaco)
        )
        for aspas in _ASPAS.finditer(linha):
            texto = next(grupo for grupo in aspas.groups() if grupo is not None)
            marca = _MARCA_ID_SEGUIDA.match(linha, aspas.end())
            if marca is None:
                eventos.append(
                    (numero, aspas.start(), f"{numero}: aviso: aspas sem id: {texto}")
                )
                continue
            citacoes += 1
            referencia = marca.group(1)
            mensagem = None
            ids = expandir(referencia)
            textos, faltantes = textos_referencia(slug, referencia)
            if ids is None or faltantes:
                mensagem = f"{numero}: id inexistente: {referencia}"
            elif not citacao_confere(texto, textos):
                mensagem = (
                    f"{numero}: citação não confere em {referencia}: {texto}"
                )
            elif previstos is not None and referencia not in previstos:
                mensagem = f"{numero}: citação fora do briefing: {referencia}"
            if mensagem is not None:
                eventos.append((numero, aspas.start(), mensagem))
                problemas += 1

    minutos = f"{len(palavras) / 150:.1f}".replace(".", ",")
    saida = [mensagem for _, _, mensagem in sorted(eventos)]
    saida.append(
        f"{len(palavras)} palavras, {minutos} min; "
        f"{citacoes} citações, {problemas} problemas"
    )
    return ResultadoContagem("\n".join(saida) + "\n", 1 if problemas else 0)
