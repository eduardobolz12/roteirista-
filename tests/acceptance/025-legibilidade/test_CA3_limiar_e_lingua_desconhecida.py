"""CA-3: --limiar muda a fronteira da palavra rara; arquivo sem língua no nome dá código 2."""


def test_CA3_limiar_e_lingua_desconhecida(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'túmulo|túmulos', 'tomb|tombs').codigo == 0
    r = livro('legibilidade', 'teste', 'roteiro-en.md', '--limiar', '4.0')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '1.2: raras: eighteen\n'
        '2.1: raras: judged\n'
        '6 parágrafos, 0 frases longas, 2 palavras raras, 0 expressões\n'
    )
    s = livro('legibilidade', 'teste', 'notas.md')
    assert s.codigo == 2 and 'língua desconhecida: notas.md' in s.erro, (s.codigo, s.erro)
