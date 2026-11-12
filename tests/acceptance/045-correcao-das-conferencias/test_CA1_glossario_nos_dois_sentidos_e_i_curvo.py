"""CA-1: o glossário vale nos dois sentidos para termo minúsculo (haitiano → Haitian); I’m com apóstrofo curvo não é nome; nome que some ou aparece continua acusado."""


def test_CA1_glossario_nos_dois_sentidos_e_i_curvo(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'haitiano|haitiana', 'Haitian').codigo == 0
    assert livro('glossario', 'teste', 'en', 'presidente', 'President|president').codigo == 0
    r = livro('invariantes', 'teste', 'nomes-pt.md', 'nomes-en.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '1.2: nome sumiu: Clairvius\n'
        '1.2: nome novo: Narcisse\n'
        '1.3: nome novo: Haitian\n'
        '3 parágrafos, 3 alertas\n'
    )
