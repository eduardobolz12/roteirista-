"""CA-1: aberto, o português aprovado ocupa as duas colunas de texto, como a nota de alerta."""


def linhas_do_estilo(html):
    return [linha.strip() for linha in html.split("<style>", 1)[-1].split("</style>", 1)[0].splitlines()]


def test_CA1_portugues_aprovado_nas_duas_colunas(pdf, livro, pasta):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'facão', 'machete').codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade|sociedades', 'society|societies').codigo == 0
    r = livro('lado-a-lado', 'teste', 'roteiro-pt.md', 'roteiro-en.md', 'retro-pt-roteiro-en.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    h = (pasta / 'lado-a-lado-roteiro-en.html').read_text(encoding='utf-8')
    assert 'details { grid-column: 2 / 4; }' in linhas_do_estilo(h)
