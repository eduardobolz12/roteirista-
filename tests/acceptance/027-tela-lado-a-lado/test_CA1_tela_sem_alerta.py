"""CA-1: tradução e retrotradução fiéis: a página tem os parágrafos lado a lado, o português aprovado recolhido e a caixa de decisão, sem rede."""


def test_CA1_tela_sem_alerta(pdf, livro, pasta):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'facão', 'machete').codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade|sociedades', 'society|societies').codigo == 0
    r = livro('lado-a-lado', 'teste', 'roteiro-pt.md', 'roteiro-en.md', 'retro-pt-roteiro-en.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == '3 parágrafos, 0 marcados: lado-a-lado-roteiro-en.html\n'
    h = (pasta / 'lado-a-lado-roteiro-en.html').read_text(encoding='utf-8')
    assert '<title>Lado a lado — roteiro-en.md</title>' in h
    assert (
        '<div class="meta">Inglês · 2 capítulos · 3 parágrafos · 0 marcados</div>'
    ) in h
    assert (
        '<div class="par" id="p-1-2"><span class="num">1.2</span><p class="en">The secretary raises the machete and reads the date: &quot;leu o próprio nome gravado no cimento&quot; [01.001].</p>'
    ) in h
    assert '<span class="ok">✓ sem alerta</span>' in h
    assert (
        '<details><summary>Português aprovado</summary><p>A sociedade julga a alma, não o corpo.</p></details>'
    ) in h
    assert '<b>Sua decisão sobre o capítulo 2</b>' in h
    assert 'http' not in h
    assert '<script' not in h
    assert '<link' not in h
