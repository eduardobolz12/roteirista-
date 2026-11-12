"""CA-3: tema fora do arquivo de temas é problema; arquivo de temas com problemas para tudo."""


def test_CA3_tema_inexistente_e_temas_com_erro(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('validar-briefing', 'teste', 'briefing-tema3.md', '--temas', 'temas-ok.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'tema 3 não está no arquivo de temas\n'
        '1 problemas\n'
    )
    s = livro('validar-briefing', 'teste', 'briefing-tema2.md', '--temas', 'temas-erros.md')
    assert s.codigo == 2 and s.texto == "", (s.codigo, s.texto)
    assert "o arquivo de temas tem problemas: rode livro validar-temas" in s.erro, s.erro
