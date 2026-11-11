"""CA-3: a regra vale na correção por vizinho e na repescagem, que não corrige."""


def test_CA3_vizinho_e_repescagem(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    ollama.grupo = "vizinho"

    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "corrigido: 01.001 -> 01.002: irmã apelido infância\n2 itens gravados, 1 corrigidos, 0 rejeitados\n"

    r = livro("repescar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        "rejeitado (âncora não encontrada): 01.003 | caso | irmã apelido | Âncora de outro parágrafo.\n"
        "1 itens gravados, 0 sem conteúdo, 1 rejeitados\n"
    )
