"""CA-2: sem glossário, o nome traduzido some e aparece; arquivo sem língua no nome dá código 2."""


def test_CA2_sem_glossario_e_lingua_desconhecida(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('invariantes', 'teste', 'roteiro-pt.md', 'roteiro-en.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '2.1: nome sumiu: Barão\n'
        '2.1: nome novo: Baron\n'
        '6 parágrafos, 2 alertas\n'
    )
    s = livro('invariantes', 'teste', 'roteiro-pt.md', 'notas.md')
    assert s.codigo == 2 and 'língua desconhecida: notas.md' in s.erro, (s.codigo, s.erro)
