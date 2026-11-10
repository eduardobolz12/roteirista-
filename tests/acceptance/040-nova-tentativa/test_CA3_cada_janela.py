"""CA-3: cada janela e a repescagem têm as suas tentativas."""


def test_CA3_cada_janela(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    ollama.falhar = {2}

    r = livro("indexar", "teste", "01", "--janela", "40")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert len(ollama.pedidos) == 3
    assert ollama.trechos() == [["01.001", "01.002"], ["01.002", "01.003"], ["01.002", "01.003"]]

    ollama.grupo = "pouco"
    assert livro("indexar", "teste", "01").codigo == 0
    ollama.grupo = "padrao"
    ollama.pedidos.clear()
    ollama.falhar = {1}

    rep = livro("repescar", "teste", "01")
    assert rep.codigo == 0, f"código {rep.codigo}; stderr: {rep.erro}"
    assert len(ollama.pedidos) == 2
