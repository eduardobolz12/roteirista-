"""CA-3: número por extenso lido pelo valor em português, inglês e francês, comparado em qualquer ordem; só a troca de verdade é acusada."""


def test_CA3_numeros_pelo_valor(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('invariantes', 'teste', 'numeros-pt.md', 'numeros-en.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '1.5: números: 2, 1950 → 3, 1950\n'
        '5 parágrafos, 1 alertas\n'
    )
    s = livro('invariantes', 'teste', 'numeros-pt.md', 'numeros-fr.md')
    assert s.codigo == 1, f"código {s.codigo}; stderr: {s.erro}"
    assert s.texto == (
        '1.5: números: 2, 1950 → 3, 1950\n'
        '5 parágrafos, 1 alertas\n'
    )
