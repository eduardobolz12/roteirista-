"""CA-3: o próprio livro decide: partes conhecidas mantêm o hífen; palavra partida e forma unida não."""


def test_CA3_partes_do_livro(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    esperado = {
        "01.005": "Ela comprou uma saia-calça na feira.\n",
        "01.007": "A testemunha chegou cedo.\n",
        "01.008": "A sobremesa veio fria.\n",
    }
    for id_, texto in esperado.items():
        r = livro("trecho", "teste", id_)
        assert r.codigo == 0, f"{id_}: código {r.codigo}; stderr: {r.erro}"
        assert r.texto == texto, f"{id_}: {r.texto!r}"

    r = livro("trecho", "teste", "01.010")
    assert r.codigo == 2, f"código {r.codigo}; stdout: {r.texto!r}"
