"""CA-3: linha só com o id dá todas as colunas que faltam; o briefing completo continua ok."""


def test_CA3_so_id_e_briefing_certo(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('validar-briefing', 'teste', 'briefing-so-id.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '22: id inexistente: 01.009\n'
        '22: faltam colunas: O que é, Momento, Trato\n'
        '2 problemas\n'
    )
    s = livro('validar-briefing', 'teste', 'briefing-ok.md')
    assert s.codigo == 0, f"código {s.codigo}; stderr: {s.erro}"
    assert s.texto == (
        'ok: 2 momentos, 2 passagens, 1 citações, 0 dados da web\n'
    )
