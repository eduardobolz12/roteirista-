"""CA-3: nome que some (também no começo da frase), nome novo, citação traduzida, número trocado e parágrafo a mais."""


def test_CA3_humanizado_com_mudancas(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'Barão', 'Baron').codigo == 0
    r = livro('invariantes', 'teste', 'roteiro-en.md', 'roteiro-en-humanizado.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '1.1: nome sumiu: Benetier\n'
        '1.1: nome novo: Port-au-Prince\n'
        '1.2: citações: "leu o próprio nome gravado no cimento" [01.001] → "read his own name carved in the cement" [01.001]\n'
        '1.3: números: 2 → 3\n'
        'cap. 2: 2 parágrafos antes, 3 depois\n'
        '3.1: nome sumiu: Benetier\n'
        '4 parágrafos, 6 alertas\n'
    )
