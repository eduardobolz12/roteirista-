"""CA-3: número e título impressos não são parágrafo; a bibliografia não recebe o índice."""


def test_CA3_abertura_de_capitulo(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    esperado = {
        "03.001": "O homem leu o próprio nome gravado no cimento.\n",
        "03.002": "A irmã reconheceu o apelido de infância.\n",
        "bib.001": "Davis, Wade. The Serpent and the Rainbow. 1985.\n",
    }
    for id_, texto in esperado.items():
        r = livro("trecho", "teste", id_)
        assert r.codigo == 0, f"{id_}: código {r.codigo}; stderr: {r.erro}"
        assert r.texto == texto, f"{id_}: {r.texto!r}"

    for id_ in ["03.003", "bib.002"]:
        r = livro("trecho", "teste", id_)
        assert r.codigo == 2, f"{id_}: código {r.codigo}; stdout: {r.texto!r}"

    r = livro("buscar", "teste", "túmulo")
    assert r.codigo == 1, f"código {r.codigo}; stdout: {r.texto!r}"
    assert r.stdout == b""
