"""CA-3: o julgamento só vale para ids da lista e sai em --julgadas."""


def test_CA3_julgar(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "en", "--lingua", "en").codigo == 0

    r = livro("julgar", "en", "02.002", "nao", "só um modo de dizer")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    r = livro("julgar", "en", "01.002", "hesitacao", "o autor admite o erro")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"

    fora = livro("julgar", "en", "01.003", "nao", "x")
    assert fora.codigo == 2, f"código {fora.codigo}; stdout: {fora.texto!r}"
    assert "id fora da lista: 01.003" in fora.erro

    r = livro("hesitacoes", "en", "--julgadas")
    assert r.texto == "01.002 | hesitacao | o autor admite o erro\n02.002 | nao | só um modo de dizer\n"
