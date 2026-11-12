"""CA-1: sugestão certa dá ok com o número de temas e de assuntos."""


def test_CA1_temas_ok(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('validar-temas', 'teste', 'temas-ok.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'ok: 2 temas, 2 assuntos\n'
    )
