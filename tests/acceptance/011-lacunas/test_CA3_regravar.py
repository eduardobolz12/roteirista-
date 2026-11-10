"""CA-3: indexar de novo apaga as marcas; sem lacunas, repescar não chama o modelo."""


def test_CA3_regravar(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("indexar", "teste", "01").codigo == 0
    assert livro("repescar", "teste", "01").codigo == 0

    assert livro("indexar", "teste", "01").codigo == 0
    assert livro("lacunas", "teste", "01").texto == "01.003\n01.004\n01.005\n"

    ollama.grupo = "tudo"
    assert livro("indexar", "teste", "01").codigo == 0
    ollama.pedidos.clear()

    r = livro("repescar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "0 itens gravados, 0 sem conteúdo, 0 rejeitados\n"
    assert ollama.pedidos == []
