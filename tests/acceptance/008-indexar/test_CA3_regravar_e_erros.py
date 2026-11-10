"""CA-3: indexar de novo substitui; modelo fora do ar não apaga nada; capítulo inexistente é erro."""


def test_CA3_regravar_e_erros(pdf, livro, ollama, porta_fechada):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("indexar", "teste", "01").codigo == 0

    ollama.grupo = "segunda"
    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    esperado = "01.003 | termo | enterro | Outra leitura do mesmo capítulo.\n"
    assert livro("itens", "teste", "01").texto == esperado

    fora = livro("indexar", "teste", "01", url=porta_fechada)
    assert fora.codigo == 3, f"código {fora.codigo}; stderr: {fora.erro}"
    assert f"modelo inacessível: {porta_fechada}" in fora.erro
    assert livro("itens", "teste", "01").texto == esperado

    errado = livro("indexar", "teste", "09")
    assert errado.codigo == 2, f"código {errado.codigo}; stderr: {errado.erro}"
    assert "capítulo inexistente: 09" in errado.erro
