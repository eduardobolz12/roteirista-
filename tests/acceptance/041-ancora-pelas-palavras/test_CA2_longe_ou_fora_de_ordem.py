"""CA-2: palavras longe demais, fora de ordem ou pedaço de palavra não conferem; uma palavra omitida confere."""


def test_CA2_longe_ou_fora_de_ordem(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    ollama.grupo = "longe"

    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        "rejeitado (âncora não encontrada): 01.001 | caso | homem nome | Palavras longe demais.\n"
        "rejeitado (âncora não encontrada): 01.001 | caso | nome próprio | Fora de ordem.\n"
        "rejeitado (âncora não encontrada): 01.001 | caso | home | Pedaço de palavra.\n"
        "rejeitado (âncora não encontrada): 01.001 | caso | homem viu o túmulo de pedra | Nenhum trecho de quatro palavras confere.\n"
        "1 itens gravados, 0 corrigidos, 4 rejeitados\n"
    )
