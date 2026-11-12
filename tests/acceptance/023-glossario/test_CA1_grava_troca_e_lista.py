"""CA-1: grava termo com formas, troca a tradução e lista em ordem."""


def test_CA1_grava_troca_e_lista(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    a = livro('glossario', 'teste', 'en', 'sociedade', 'society|societies')
    assert a.codigo == 0, f"código {a.codigo}; stderr: {a.erro}"
    assert a.texto == (
        'gravado: sociedade → society|societies\n'
    )
    b = livro('glossario', 'teste', 'en', 'Barão', 'Baron')
    assert b.codigo == 0, f"código {b.codigo}; stderr: {b.erro}"
    assert b.texto == (
        'gravado: Barão → Baron\n'
    )
    c = livro('glossario', 'teste', 'en', 'sociedade', 'association')
    assert c.codigo == 0, f"código {c.codigo}; stderr: {c.erro}"
    assert c.texto == (
        'trocado: sociedade: society|societies → association\n'
    )
    r = livro('glossario', 'teste', 'en')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'Barão → Baron\n'
        'sociedade → association\n'
        '2 termos (en)\n'
    )
