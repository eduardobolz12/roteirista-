"""CA-3: termo traduzido de outro jeito vira alerta no parágrafo; língua fora de en/fr dá código 2."""


def test_CA3_conferir_com_alerta_e_lingua_invalida(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade', 'society|societies').codigo == 0
    assert livro('glossario', 'teste', 'en', 'túmulo|túmulos', 'tomb|tombs').codigo == 0
    assert livro('glossario', 'teste', 'en', 'Barão', 'Baron').codigo == 0
    r = livro('glossario', 'teste', 'en', '--conferir', 'roteiro-pt.md', 'roteiro-en-glossario.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '1.1: túmulo|túmulos sem tomb|tombs\n'
        '2.2: sociedade sem society|societies\n'
        '3 termos, 2 alertas\n'
    )
    s = livro('glossario', 'teste', 'de')
    assert s.codigo == 2 and 'língua inválida: de' in s.erro, (s.codigo, s.erro)
