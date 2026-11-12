"""CA-3: URL não suportada, artigo inexistente, artigo sem resumo e API fora do ar não gravam nada."""


def test_CA3_erros(pdf, livro, servidor):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    a = livro("fonte", "teste", "https://example.com/x")
    assert a.codigo == 2 and "fonte não suportada: https://example.com/x" in a.erro, (a.codigo, a.erro)

    b = livro("fonte", "teste", "https://europepmc.org/article/MED/99999999")
    assert b.codigo == 2 and "fonte não encontrada: https://europepmc.org/article/MED/99999999" in b.erro, (b.codigo, b.erro)

    c = livro("fonte", "teste", "https://europepmc.org/article/MED/33333333")
    assert c.codigo == 2 and "fonte sem texto: https://europepmc.org/article/MED/33333333" in c.erro, (c.codigo, c.erro)

    servidor.falhar_api = True
    d = livro("fonte", "teste", "https://europepmc.org/article/MED/11111111")
    assert d.codigo == 3 and "fonte inacessível: https://europepmc.org/article/MED/11111111" in d.erro, (d.codigo, d.erro)

    f = livro("fontes", "teste")
    assert f.codigo == 0 and f.texto == "", (f.codigo, f.texto, f.erro)
