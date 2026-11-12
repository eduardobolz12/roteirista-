"""CA-3: seções faltando e id de fonte que não existe."""


def test_CA3_briefing_incompleto(pdf, livro, servidor):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("fonte", "teste", "https://europepmc.org/article/MED/11111111").codigo == 0
    r = livro('validar-briefing', 'teste', 'briefing-incompleto.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'falta a seção: Citações literais previstas\n'
        'falta a seção: Ressalvas\n'
        '29: id inexistente: W05.001\n'
        '3 problemas\n'
    )
