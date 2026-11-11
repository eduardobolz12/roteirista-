"""CA-1: sem opção, só os parágrafos com marca forte."""


def test_CA1_fortes(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "en", "--lingua", "en").codigo == 0

    r = livro("hesitacoes", "en")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "01.002 | hypothesis, wrong\n02.001 | possibly\n"
