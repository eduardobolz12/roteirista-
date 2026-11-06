"""CA-3: no glossário, a entrada começa na margem e a linha recuada continua a entrada."""


def test_CA3_glossario(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    esperado = {
        "03.001": "ASSON Chocalho sagrado feito de cabaça e usado pelo sacerdote nos ritos.\n",
        "03.004": "CANZO O rito do fogo.\n",
        "03.007": "MAMBO A sacerdotisa do vodu, que conduz a cerimônia e guarda o asson.\n",
    }
    for id_, texto in esperado.items():
        r = livro("trecho", "teste", id_)
        assert r.codigo == 0, f"{id_}: código {r.codigo}; stderr: {r.erro}"
        assert r.texto == texto, f"{id_}: {r.texto!r}"

    r = livro("trecho", "teste", "03.008")
    assert r.codigo == 2, f"código {r.codigo}; stdout: {r.texto!r}"
