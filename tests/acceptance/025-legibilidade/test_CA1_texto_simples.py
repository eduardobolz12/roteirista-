"""CA-1: texto simples não dá frase longa, palavra rara nem expressão."""


def test_CA1_texto_simples(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('legibilidade', 'teste', 'roteiro-en.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '6 parágrafos, 0 frases longas, 0 palavras raras, 0 expressões\n'
    )
