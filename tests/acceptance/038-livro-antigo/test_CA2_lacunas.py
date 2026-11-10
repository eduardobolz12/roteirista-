"""CA-2: o livro antigo aceita lacunas e repescar."""


def test_CA2_lacunas(antigo, livro):
    r = livro("lacunas", antigo, "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "01.001\n01.002\n01.003\n"

    rep = livro("repescar", antigo, "01")
    assert rep.codigo == 0, f"código {rep.codigo}; stderr: {rep.erro}"
    assert rep.texto.splitlines()[-1] == "3 itens gravados, 0 sem conteúdo, 0 rejeitados"
