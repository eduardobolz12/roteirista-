"""CA-1: passagem desenvolvida que é casa de outro tema gera aviso, sem mudar o código."""


def test_CA1_aviso_de_casa(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('validar-briefing', 'teste', 'briefing-tema2.md', '--temas', 'temas-ok.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'aviso: 22: 01.001 é desenvolvido aqui, mas a casa de "O túmulo" é o tema 1\n'
        'ok: 2 momentos, 4 passagens, 0 citações, 0 dados da web\n'
    )
