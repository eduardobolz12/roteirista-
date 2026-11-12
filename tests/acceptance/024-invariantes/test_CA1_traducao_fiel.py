"""CA-1: tradução fiel, com o nome traduzido pelo glossário, não dá alerta."""


def test_CA1_traducao_fiel(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'Barão', 'Baron').codigo == 0
    r = livro('invariantes', 'teste', 'roteiro-pt.md', 'roteiro-en.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '6 parágrafos, 0 alertas\n'
    )
