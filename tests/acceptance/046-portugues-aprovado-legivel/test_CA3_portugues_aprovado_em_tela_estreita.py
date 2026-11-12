"""CA-3: em tela estreita, de uma coluna só, o português aprovado ocupa a largura toda."""


def linhas_do_estilo(html):
    return [linha.strip() for linha in html.split("<style>", 1)[-1].split("</style>", 1)[0].splitlines()]


def test_CA3_portugues_aprovado_em_tela_estreita(pdf, livro, pasta):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'facão', 'machete').codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade|sociedades', 'society|societies').codigo == 0
    r = livro('lado-a-lado', 'teste', 'roteiro-pt.md', 'roteiro-en.md', 'retro-pt-roteiro-en.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    h = (pasta / 'lado-a-lado-roteiro-en.html').read_text(encoding='utf-8')
    linhas = linhas_do_estilo(h)
    largura = 'details { grid-column: 2 / 4; }'
    estreita = '@media (max-width: 700px) { details { grid-column: 1; } }'
    assert largura in linhas and estreita in linhas, (largura in linhas, estreita in linhas)
    assert linhas.index(largura) < linhas.index(estreita)
