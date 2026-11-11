"""CA-2: contar-tema conta fichas, parágrafos e capítulos de um ou mais termos."""


def test_CA2_contar_tema(indexado, livro):
    r = livro("contar-tema", indexado, "bizango")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "3 fichas, 2 parágrafos, 1 capítulos\ncapítulos: 02 (3)\nnumero 0, contradicao 0\n"

    r = livro("contar-tema", indexado, "saint marc", "powder")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "5 fichas, 4 parágrafos, 2 capítulos\ncapítulos: 01 (3), 02 (2)\nnumero 1, contradicao 0\n"
