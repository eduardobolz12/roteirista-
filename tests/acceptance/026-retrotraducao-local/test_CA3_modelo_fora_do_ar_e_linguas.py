"""CA-3: modelo fora do ar dá código 3 e não grava nada; roteiro em português ou sem língua dá código 2."""


def test_CA3_modelo_fora_do_ar_e_linguas(pdf, livro, pasta, porta_fechada):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro('glossario', 'teste', 'en', 'facão', 'machete').codigo == 0
    assert livro('glossario', 'teste', 'en', 'sociedade|sociedades', 'society|societies').codigo == 0
    r = livro('retraduzir', 'teste', 'roteiro-en.md', url=porta_fechada)
    assert r.codigo == 3 and 'modelo inacessível:' in r.erro, (r.codigo, r.erro)
    assert not (pasta / 'retro-pt-roteiro-en.md').exists()
    s = livro('retraduzir', 'teste', 'roteiro-pt.md')
    assert s.codigo == 2 and 'o roteiro já está em português: roteiro-pt.md' in s.erro, (s.codigo, s.erro)
    t = livro('retraduzir', 'teste', 'notas.md')
    assert t.codigo == 2 and 'língua desconhecida: notas.md' in t.erro, (t.codigo, t.erro)
