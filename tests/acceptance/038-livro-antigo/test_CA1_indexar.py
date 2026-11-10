"""CA-1: o livro antigo aceita itens e indexar."""


def test_CA1_indexar(antigo, livro):
    vazio = livro("itens", antigo, "01")
    assert vazio.codigo == 0, f"código {vazio.codigo}; stderr: {vazio.erro}"
    assert vazio.stdout == b""

    r = livro("indexar", antigo, "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "3 itens gravados, 0 corrigidos, 0 rejeitados\n"
    assert len(livro("itens", antigo, "01").texto.splitlines()) == 3
