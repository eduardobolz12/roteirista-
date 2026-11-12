"""CA-2: a resposta sem a marca da citação gera aviso, e o parágrafo é gravado assim mesmo."""


def test_CA2_citacao_perdida(pdf, livro, pasta):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'facão', 'machete').codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade|sociedades', 'society|societies').codigo == 0
    r = livro('retraduzir', 'teste', 'outro-en.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '1.1: citação perdida na retrotradução\n'
        '1 parágrafos retraduzidos em retro-pt-outro-en.md\n'
    )
    assert (pasta / 'retro-pt-outro-en.md').read_text(encoding='utf-8') == (
        '# Retrotradução de outro-en.md (qwen3:14b)\n'
        '\n'
        '## 1\n'
        '\n'
        'Ele lê a data.\n'
        '\n'
    )
