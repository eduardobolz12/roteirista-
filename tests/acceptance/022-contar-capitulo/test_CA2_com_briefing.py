"""CA-2: com --briefing, citação que confere mas não estava prevista é problema."""


def test_CA2_com_briefing(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('contar', 'teste', 'capitulo.md', '--briefing', 'briefing.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '7: citação fora do briefing: 01.002\n'
        '7: citação não confere em 01.003: quis falar do enterro\n'
        '9: citação fora do briefing: 02.001\n'
        '9: aviso: aspas sem id: tarde\n'
        '11: id inexistente: 02.009\n'
        '51 palavras, 0,3 min; 5 citações, 4 problemas\n'
    )
