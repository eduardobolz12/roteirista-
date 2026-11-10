"""CA-2: três falhas seguidas: modelo inacessível, e o capítulo fica como estava."""


def test_CA2_desiste(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("indexar", "teste", "01").codigo == 0
    antes = livro("itens", "teste", "01").texto
    ollama.pedidos.clear()
    ollama.falhar = {1, 2, 3}

    r = livro("indexar", "teste", "01")
    assert r.codigo == 3, f"código {r.codigo}; stderr: {r.erro}"
    assert "nova tentativa (1 de 2)" in r.erro
    assert "nova tentativa (2 de 2)" in r.erro
    assert "modelo inacessível:" in r.erro
    assert len(ollama.pedidos) == 3
    assert livro("itens", "teste", "01").texto == antes
