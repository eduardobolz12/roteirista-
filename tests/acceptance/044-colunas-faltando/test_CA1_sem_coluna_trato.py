"""CA-1: tabela de passagens sem a coluna Trato: cada linha acusa, e o id continua conferido."""


def test_CA1_sem_coluna_trato(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('validar-briefing', 'teste', 'briefing-sem-trato.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '21: faltam colunas: Trato\n'
        '22: id inexistente: 01.009\n'
        '22: faltam colunas: Trato\n'
        '3 problemas\n'
    )
