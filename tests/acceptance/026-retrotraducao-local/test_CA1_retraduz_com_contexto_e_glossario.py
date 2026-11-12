"""CA-1: cada parágrafo vai ao modelo local com o capítulo como contexto, a citação como marca e só os termos do glossário que ele usa; a resposta volta com a citação no lugar."""


def test_CA1_retraduz_com_contexto_e_glossario(pdf, livro, pasta, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'facão', 'machete').codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade|sociedades', 'society|societies').codigo == 0
    r = livro('retraduzir', 'teste', 'roteiro-en.md')
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == '3 parágrafos retraduzidos em retro-pt-roteiro-en.md\n'
    assert (pasta / 'retro-pt-roteiro-en.md').read_text(encoding='utf-8') == (
        '# Retrotradução de roteiro-en.md (qwen3:14b)\n'
        '\n'
        '## 1\n'
        '\n'
        'O secretário ergue o facão e lê a data: "leu o próprio nome gravado no cimento" [01.001].\n'
        '\n'
        'Em 1962, dois médicos assinaram a certidão.\n'
        '\n'
        '## 2\n'
        '\n'
        'A sociedade julga a alma, não o corpo.\n'
        '\n'
    )
    assert [q['model'] for q in ollama.pedidos] == ['qwen3:14b'] * 3
    assert (
        '  machete → facão\n'
        '- Escreva só a tradução do PARÁGRAFO.'
    ) in ollama.pedidos[0]['prompt']
    assert (
        'CAPÍTULO:\n'
        '\n'
        'The secretary raises the machete and reads the date: ⟦c⟧.\n'
        '\n'
        'In 1962, two doctors signed the certificate.\n'
        '\n'
        'PARÁGRAFO:\n'
        '\n'
        'The secretary raises the machete and reads the date: ⟦1⟧.'
    ) in ollama.pedidos[0]['prompt']
    assert 'Use estas traduções' not in ollama.pedidos[1]['prompt']
    assert '  society, societies → sociedade, sociedades\n' in ollama.pedidos[2]['prompt']
