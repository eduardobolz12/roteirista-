"""CA-2: cada alerta diz se é da tradução ou da retrotradução, e o parágrafo com alerta fica marcado."""


def test_CA2_alertas_da_traducao_e_da_retrotraducao(pdf, livro, pasta):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'facão', 'machete').codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade|sociedades', 'society|societies').codigo == 0
    r = livro('lado-a-lado', 'teste', 'roteiro-pt.md', 'roteiro-en-humanizado.md', 'retro-pt-roteiro-en-humanizado.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '1.1: Tradução: números: 2, 1962 → 3, 1962\n'
        '1.1: Retrotradução: nome sumiu: Narcisse\n'
        '1.1: Retrotradução: nome novo: Narciso\n'
        '1.2: Retrotradução: machete não voltou como facão\n'
        '2.1: Retrotradução: frase marcada como ambígua\n'
        '3 parágrafos, 3 marcados: lado-a-lado-roteiro-en-humanizado.html\n'
    )
    h = (pasta / 'lado-a-lado-roteiro-en-humanizado.html').read_text(encoding='utf-8')
    assert '<div class="par suspeito" id="p-1-1">' in h
    assert '<span class="nota">⚠ Retrotradução: nome novo: Narciso</span>' in h
    assert (
        '<div class="meta">Inglês · 2 capítulos · 3 parágrafos · 3 marcados</div>'
    ) in h
