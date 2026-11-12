"""CA-2: a tradução que usa o glossário passa sem alerta."""


def test_CA2_conferir_sem_alerta(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade', 'society|societies').codigo == 0
    assert livro('glossario', 'teste', 'en', 'túmulo|túmulos', 'tomb|tombs').codigo == 0
    assert livro('glossario', 'teste', 'en', 'Barão', 'Baron').codigo == 0
    r = livro('glossario', 'teste', 'en', '--conferir', 'roteiro-pt.md', 'roteiro-en.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '3 termos, 0 alertas\n'
    )
