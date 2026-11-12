"""CA-2: momento, passagem e citação com colunas faltando; o que a linha tem continua conferido."""


def test_CA2_linhas_curtas(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('validar-briefing', 'teste', 'briefing-linhas-curtas.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '15: faltam colunas: De onde vem\n'
        '22: faltam colunas: Momento, Trato\n'
        '28: citação não confere em 01.001: leu o nome próprio gravado no cimento\n'
        '28: faltam colunas: Uso\n'
        '4 problemas\n'
    )
