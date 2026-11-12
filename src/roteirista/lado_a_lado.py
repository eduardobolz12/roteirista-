"""Página local para comparar tradução, retrotradução e português aprovado."""

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
import re

from roteirista import banco, traducao


@dataclass(frozen=True)
class Resultado:
    conteudo: str
    mensagens: list[str]
    paragrafos: int
    marcados: int


@dataclass(frozen=True)
class Conferencia:
    capitulos: list[str]
    paragrafos: dict[tuple[int, int], list[str]]


def _escapar(texto: str) -> str:
    return (
        texto.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _ler_conferencia(resultado: traducao.Resultado, origem: str) -> Conferencia:
    capitulos = []
    paragrafos: dict[tuple[int, int], list[str]] = {}
    for linha in resultado.saida.splitlines():
        if re.match(r"^cap\. \d+: ", linha):
            capitulos.append(f"{origem}: {linha}")
            continue
        achado = re.match(r"^(\d+)\.(\d+): (.*)$", linha)
        if achado:
            numero = int(achado.group(1))
            indice = int(achado.group(2))
            alerta = f"{origem}: {achado.group(3)}"
            paragrafos.setdefault((numero, indice), []).append(alerta)
    return Conferencia(capitulos, paragrafos)


def _alertas_glossario_retro(
    termos: list[tuple[str, str]], traduzido: str, retraduzido: str
) -> list[str]:
    texto_traduzido = traducao.sem_citacoes(traduzido)
    texto_retraduzido = traducao.sem_citacoes(retraduzido)
    alertas = []
    for termo, esperado in sorted(termos, key=lambda item: item[0].casefold()):
        if traducao._contem_forma(
            texto_traduzido, esperado
        ) and not traducao._contem_forma(texto_retraduzido, termo):
            primeira_traducao = esperado.split("|")[0]
            primeiro_termo = termo.split("|")[0]
            alertas.append(
                f"Retrotradução: {primeira_traducao} não voltou como {primeiro_termo}"
            )
    return alertas


def _estilo() -> str:
    return (
        resources.files("roteirista")
        .joinpath("estilos", "lado-a-lado.css")
        .read_bytes()
        .decode("utf-8")
    )


def gerar(
    slug: str,
    portugues: Path,
    traduzido: Path,
    retraduzido: Path,
    lingua: str,
) -> Resultado:
    invariantes_traducao = _ler_conferencia(
        traducao.conferir_invariantes(slug, portugues, traduzido, "pt", lingua),
        "Tradução",
    )
    glossario_traducao = _ler_conferencia(
        traducao.conferir_glossario(slug, lingua, portugues, traduzido),
        "Tradução",
    )
    invariantes_retro = _ler_conferencia(
        traducao.conferir_invariantes(slug, traduzido, retraduzido, lingua, "pt"),
        "Retrotradução",
    )

    capitulos_pt = dict(traducao.ler_roteiro(portugues))
    capitulos_traduzidos = traducao.ler_roteiro(traduzido)
    capitulos_retro = dict(traducao.ler_roteiro(retraduzido))
    termos = banco.glossario(slug, lingua)
    avisos = (
        invariantes_traducao.capitulos
        + glossario_traducao.capitulos
        + invariantes_retro.capitulos
    )
    capitulos_com_aviso_retro = {
        int(achado.group(1))
        for aviso in invariantes_retro.capitulos
        if (achado := re.match(r"Retrotradução: cap\. (\d+):", aviso))
    }

    linhas = [
        "<!doctype html>",
        '<html lang="pt-BR">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        f"<title>Lado a lado — {_escapar(traduzido.name)}</title>",
        "<style>",
        _estilo().rstrip(),
        "</style>",
        "</head>",
        "<body>",
        "<header>",
        "<h1>Humanizado × retrotradução</h1>",
    ]
    total = sum(len(paragrafos) for _, paragrafos in capitulos_traduzidos)
    marcados = 0
    mensagens = list(avisos)
    corpo = []
    lingua_extensa = {"en": "Inglês", "fr": "Francês"}[lingua]

    for numero, paragrafos in capitulos_traduzidos:
        corpo.append(f'<h2 id="cap-{numero}">Capítulo {numero}</h2>')
        originais = capitulos_pt.get(numero, [])
        retraduzidos = capitulos_retro.get(numero, [])
        for indice, texto_traduzido in enumerate(paragrafos, start=1):
            posicao = (numero, indice)
            texto_retraduzido = (
                retraduzidos[indice - 1] if indice <= len(retraduzidos) else ""
            )
            alertas = list(invariantes_traducao.paragrafos.get(posicao, []))
            alertas.extend(glossario_traducao.paragrafos.get(posicao, []))
            if numero not in capitulos_com_aviso_retro:
                alertas.extend(invariantes_retro.paragrafos.get(posicao, []))
                alertas.extend(
                    _alertas_glossario_retro(
                        termos, texto_traduzido, texto_retraduzido
                    )
                )
                if "[ambíguo]" in texto_retraduzido:
                    alertas.append("Retrotradução: frase marcada como ambígua")
            if alertas:
                marcados += 1
                mensagens.extend(
                    f"{numero}.{indice}: {alerta}" for alerta in alertas
                )
            classe = "par suspeito" if alertas else "par"
            notas = "".join(
                f'<span class="nota">⚠ {_escapar(alerta)}</span>'
                for alerta in alertas
            ) or '<span class="ok">✓ sem alerta</span>'
            original = originais[indice - 1] if indice <= len(originais) else ""
            corpo.append(
                f'<div class="{classe}" id="p-{numero}-{indice}">'
                f'<span class="num">{numero}.{indice}</span>'
                f'<p class="{lingua}">{_escapar(texto_traduzido)}</p>'
                f'<p class="pt">{_escapar(texto_retraduzido)}</p>'
                f"{notas}"
                f'<details><summary>Português aprovado</summary>'
                f'<p>{_escapar(original)}</p></details></div>'
            )
        corpo.append(
            f'<div class="decisao"><b>Sua decisão sobre o capítulo {numero}</b><br>'
            "☐ Aprovado · ☐ Aprovado com sugestões (escreva na conversa, em "
            "português, citando o §) · ☐ Refazer</div>"
        )

    linhas.append(
        f'<div class="meta">{lingua_extensa} · {len(capitulos_traduzidos)} capítulos · '
        f"{total} parágrafos · {marcados} marcados</div>"
    )
    linhas.extend(f'<div class="aviso">{_escapar(aviso)}</div>' for aviso in avisos)
    linhas.extend(("</header>", "<main>"))
    linhas.append(
        f'<div class="cab"><span>§</span><span>{lingua_extensa} '
        "(vai para a narração)</span><span>Retrotradução para você ler</span></div>"
    )
    linhas.extend(corpo)
    linhas.extend(("</main>", "</body>", "</html>"))
    return Resultado("\n".join(linhas) + "\n", mensagens, total, marcados)
