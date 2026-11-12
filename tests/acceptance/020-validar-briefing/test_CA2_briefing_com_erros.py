"""CA-2: campo faltando, momento e id inexistentes, trato inválido, citação que não confere e origem sem material."""


def test_CA2_briefing_com_erros(pdf, livro, servidor):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("fonte", "teste", "https://europepmc.org/article/MED/11111111").codigo == 0
    r = livro('validar-briefing', 'teste', 'briefing-erros.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        'falta o campo: Função do capítulo\n'
        '21: momento inexistente: 4\n'
        '22: id inexistente: 01.002-01.009\n'
        '22: trato inválido: aprofundar\n'
        '28: citação não confere em 01.001: leu o nome próprio gravado no cimento\n'
        'momento 1: origem Livro sem passagem\n'
        'momento 3: origem Web sem dado\n'
        '7 problemas\n'
    )
