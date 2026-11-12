"""CA-2: no parágrafo com alerta, o português aprovado vem embaixo da última nota, na largura das duas colunas."""


def linhas_do_estilo(html):
    return [linha.strip() for linha in html.split("<style>", 1)[-1].split("</style>", 1)[0].splitlines()]


def test_CA2_portugues_aprovado_embaixo_da_nota(pdf, livro, pasta):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'facão', 'machete').codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade|sociedades', 'society|societies').codigo == 0
    r = livro('lado-a-lado', 'teste', 'roteiro-pt.md', 'roteiro-en-humanizado.md',
              'retro-pt-roteiro-en-humanizado.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    h = (pasta / 'lado-a-lado-roteiro-en-humanizado.html').read_text(encoding='utf-8')
    assert 'details { grid-column: 2 / 4; }' in linhas_do_estilo(h)
    assert ('⚠ Retrotradução: nome novo: Narciso</span><details><summary>Português aprovado</summary>'
            in h)
