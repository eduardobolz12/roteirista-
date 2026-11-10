"""CA-2: o item repetido na emenda fica um só, com a afirmação da primeira janela."""


def test_CA2_duplicados(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r = livro("indexar", "teste", "01", "--janela", "40")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto.splitlines()[-1] == "4 itens gravados, 0 corrigidos, 0 rejeitados"

    assert livro("itens", "teste", "01").texto == (
        "01.001 | cena | próprio nome | O homem vê o próprio nome.\n"
        "01.002 | caso | apelido de infância | Primeira versão do item.\n"
        "01.002 | cena | reconhecer o rosto | Outra âncora no mesmo parágrafo.\n"
        "01.003 | marginal | aldeia | Ninguém na aldeia fala do enterro.\n"
    )
