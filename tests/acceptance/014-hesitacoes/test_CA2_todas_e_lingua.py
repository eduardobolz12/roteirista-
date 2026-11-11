"""CA-2: --todas inclui as marcas fracas; livro sem lista de marcas é erro."""


def test_CA2_todas_e_lingua(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "en", "--lingua", "en").codigo == 0
    assert livro("novo", str(pdf), "--slug", "pt").codigo == 0

    r = livro("hesitacoes", "en", "--todas")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "01.001 | perhaps\n01.002 | hypothesis, wrong\n02.001 | possibly\n02.002 | it seems\n"

    r = livro("hesitacoes", "pt")
    assert r.codigo == 2, f"código {r.codigo}; stdout: {r.texto!r}"
    assert "sem palavras-marca para a língua: não informada" in r.erro
