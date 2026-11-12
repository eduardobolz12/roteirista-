"""CA-2: o ponto da inicial no meio do parágrafo (W. B.) e o do título (Dr.) não fecham a frase: os nomes seguintes são conferidos, o título não é nome e a frase longa aparece inteira."""


def test_CA2_inicial_e_titulo(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('invariantes', 'teste', 'inicial-en.md', 'inicial-en-revisado.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '1.1: nome sumiu: W\n'
        '1.1: nome sumiu: B\n'
        '1.1: nome sumiu: Seabrook\n'
        '1.1: nome sumiu: Douyon\n'
        '1 parágrafos, 4 alertas\n'
    )
    s = livro('legibilidade', 'teste', 'inicial-en.md')
    assert s.codigo == 0, f"código {s.codigo}; stderr: {s.erro}"
    assert s.texto == (
        '1.1: frase de 28 palavras\n'
        '1 parágrafos, 1 frases longas, 0 palavras raras, 0 expressões\n'
    )
