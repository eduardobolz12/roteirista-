"""CA-1: lacuna é parágrafo sem item; parágrafo sem letra nem número não conta."""


def test_CA1_lacunas(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    antes = livro("lacunas", "teste", "01")
    assert antes.codigo == 0, f"código {antes.codigo}; stderr: {antes.erro}"
    assert antes.texto == "01.001\n01.003\n01.004\n01.005\n"

    assert livro("indexar", "teste", "01").codigo == 0
    depois = livro("lacunas", "teste", "01")
    assert depois.texto == "01.003\n01.004\n01.005\n"
