"""CA-1: a visão compacta dá, por capítulo, fichas, nomes repetidos e termos."""


def test_CA1_visao(indexado, livro):
    r = livro("visao", indexado)
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        "01 Chapter One — 4 fichas; numero 1, contradicao 1\n"
        "   nomes: Saint Marc (2), Max Beauvoir (2)\n"
        "   termos: powder\n"
        "02 Chapter Two — 4 fichas; numero 0, contradicao 0\n"
        "   nomes: Bizango (3), Saint Marc (2)\n"
        "   termos: Bizango\n"
    )
