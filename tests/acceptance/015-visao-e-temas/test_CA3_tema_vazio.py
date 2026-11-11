"""CA-3: tema sem nenhuma ficha dá zeros e código 1."""


def test_CA3_tema_vazio(indexado, livro):
    r = livro("contar-tema", indexado, "zumbi")
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "0 fichas, 0 parágrafos, 0 capítulos\n"
