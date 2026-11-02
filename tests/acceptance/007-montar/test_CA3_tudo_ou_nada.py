"""CA-3: um id inexistente ou intervalo entre capítulos não devolve nada."""


def test_CA3_tudo_ou_nada(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r1 = livro("montar", "teste", "01.001", "02.009")
    assert r1.codigo == 2, f"código {r1.codigo}; stderr: {r1.erro}"
    assert r1.stdout == b""
    assert "id inexistente: 02.009" in r1.erro

    r2 = livro("montar", "teste", "01.003-02.001")
    assert r2.codigo == 2, f"código {r2.codigo}; stderr: {r2.erro}"
    assert r2.stdout == b""
    assert "intervalo inválido: 01.003-02.001" in r2.erro
