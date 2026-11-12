"""CA-2: palavra rara, expressão e frase longa apontadas; nomes e termos do glossário não contam."""


def test_CA2_texto_dificil(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'bokor', 'bokor').codigo == 0
    r = livro('legibilidade', 'teste', 'roteiro-en-dificil.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '1.1: raras: henchman\n'
        '1.1: expressão: the hard way\n'
        '1.2: frase de 33 palavras\n'
        '1.2: raras: peasantry\n'
        '2 parágrafos, 1 frases longas, 2 palavras raras, 1 expressões\n'
    )
