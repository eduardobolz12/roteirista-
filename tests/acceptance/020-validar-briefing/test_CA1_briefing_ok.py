"""CA-1: briefing certo dá ok com momentos, passagens, citações e dados da web."""


def test_CA1_briefing_ok(pdf, livro, servidor):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("fonte", "teste", "https://europepmc.org/article/MED/11111111").codigo == 0
    r = livro('validar-briefing', 'teste', 'briefing-ok.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'ok: 3 momentos, 2 passagens, 1 citações, 1 dados da web\n'
    )
