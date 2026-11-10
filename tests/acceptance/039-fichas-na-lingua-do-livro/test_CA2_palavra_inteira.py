"""CA-2: a âncora só confere como palavra inteira."""


def test_CA2_palavra_inteira(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "en", "--lingua", "en").codigo == 0
    ollama.grupo = "palavra"

    r = livro("indexar", "en", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        "rejeitado (âncora não encontrada): 01.001 | caso | home | Âncora dentro de outra palavra.\n"
        "corrigido: 01.001 -> 01.002: rosto\n"
        "rejeitado (âncora não encontrada): 01.003 | marginal | ar | Âncora curta dentro de palavras.\n"
        "2 itens gravados, 1 corrigidos, 2 rejeitados\n"
    )
    assert livro("itens", "en", "01").texto == (
        "01.001 | cena | nome | O homem leu o nome.\n"
        "01.002 | caso | rosto | A irmã reconhece o rosto.\n"
    )
