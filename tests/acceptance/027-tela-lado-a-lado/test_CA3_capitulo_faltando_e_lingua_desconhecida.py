"""CA-3: capítulo que falta na retrotradução vira aviso; arquivo sem língua no nome dá código 2."""


def test_CA3_capitulo_faltando_e_lingua_desconhecida(pdf, livro, pasta):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'facão', 'machete').codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade|sociedades', 'society|societies').codigo == 0
    r = livro('lado-a-lado', 'teste', 'roteiro-pt.md', 'roteiro-en.md', 'retro-pt-curto.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'Retrotradução: cap. 2: 1 parágrafos antes, 0 depois\n'
        '3 parágrafos, 0 marcados: lado-a-lado-roteiro-en.html\n'
    )
    h = (pasta / 'lado-a-lado-roteiro-en.html').read_text(encoding='utf-8')
    assert (
        '<div class="aviso">Retrotradução: cap. 2: 1 parágrafos antes, 0 depois</div>'
    ) in h
    assert '<p class="pt"></p>' in h
    s = livro('lado-a-lado', 'teste', 'roteiro-pt.md', 'notas.md', 'retro-pt-roteiro-en.md')
    assert s.codigo == 2 and 'língua desconhecida: notas.md' in s.erro, (s.codigo, s.erro)
