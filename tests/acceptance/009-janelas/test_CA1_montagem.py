"""CA-1: a janela decide os pedidos; a seguinte repete o último parágrafo quando ele cabe."""


def test_CA1_montagem(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r = livro("indexar", "teste", "01", "--janela", "40")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert ollama.trechos() == [["01.001", "01.002"], ["01.002", "01.003"]]

    ollama.pedidos.clear()
    r = livro("indexar", "teste", "01", "--janela", "5")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert ollama.trechos() == [["01.001"], ["01.002"], ["01.003"]]

    ollama.pedidos.clear()
    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert ollama.trechos() == [["01.001", "01.002", "01.003"]]
