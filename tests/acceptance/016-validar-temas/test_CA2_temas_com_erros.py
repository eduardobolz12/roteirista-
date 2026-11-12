"""CA-2: id inexistente, casas erradas, falta de rachadura e material num só capítulo."""


def test_CA2_temas_com_erros(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    r = livro('validar-temas', 'teste', 'temas-erros.md')
    assert r.codigo == 1, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        '16: assunto sem casa\n'
        '17: assunto com mais de uma casa\n'
        '25: id inexistente: 01.009\n'
        'tema 1: material num só capítulo do livro\n'
        'tema 2: falta a rachadura com id\n'
        '5 problemas\n'
    )
