"""CA-3: seção faltando, tema sem detalhe e arquivo que não existe."""


def test_CA3_incompleto_e_inexistente(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('validar-temas', 'teste', 'temas-incompleto.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'falta a seção: Assuntos compartilhados e a casa de cada um\n'
        'tema 3: falta o detalhe\n'
        '2 problemas\n'
    )
    s = livro('validar-temas', 'teste', 'nada.md')
    assert s.codigo == 2 and "arquivo inexistente: nada.md" in s.erro, (s.codigo, s.erro)
