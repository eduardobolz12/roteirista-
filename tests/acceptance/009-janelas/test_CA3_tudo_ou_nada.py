"""CA-3: se uma janela falha, o capítulo fica como estava."""


def test_CA3_tudo_ou_nada(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("indexar", "teste", "01", "--janela", "40").codigo == 0
    antes = livro("itens", "teste", "01").texto
    assert antes != ""

    ollama.grupo = "falha"
    r = livro("indexar", "teste", "01", "--janela", "40")
    assert r.codigo == 3, f"código {r.codigo}; stderr: {r.erro}"
    assert "modelo inacessível:" in r.erro
    assert livro("itens", "teste", "01").texto == antes
