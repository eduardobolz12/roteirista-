"""CA-1: palavras do texto narrado, citações conferidas pelas palavras e aviso de aspas sem id."""


def test_CA1_conta_e_confere(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('contar', 'teste', 'capitulo.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '7: citação não confere em 01.003: quis falar do enterro\n'
        '9: aviso: aspas sem id: tarde\n'
        '11: id inexistente: 02.009\n'
        '51 palavras, 0,3 min; 5 citações, 2 problemas\n'
    )
