"""CA-3: capítulo certo, com aspas curvas, dá 0 problemas; arquivo que não existe dá código 2."""


def test_CA3_capitulo_certo_e_inexistente(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('contar', 'teste', 'capitulo-ok.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '18 palavras, 0,1 min; 2 citações, 0 problemas\n'
    )
    s = livro('contar', 'teste', 'nada.md')
    assert s.codigo == 2 and "arquivo inexistente: nada.md" in s.erro, (s.codigo, s.erro)
