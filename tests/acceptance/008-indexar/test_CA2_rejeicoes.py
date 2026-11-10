"""CA-2: id errado, tipo errado e formato errado são rejeitados e listados."""


def test_CA2_rejeicoes(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r = livro("indexar", "teste", "02")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        "rejeitado (id inexistente): 02.009 | cena | médico | Item com id que não existe.\n"
        "rejeitado (id fora do capítulo): 01.001 | cena | homem | Item de outro capítulo.\n"
        "rejeitado (tipo inválido): 02.002 | afirmacao | família | Item com tipo que não existe.\n"
        "rejeitado (formato): texto solto sem separadores\n"
        "1 itens gravados, 0 corrigidos, 4 rejeitados\n"
    )

    itens = livro("itens", "teste", "02")
    assert itens.texto == "02.001 | cena | três horas | O médico assina a certidão à tarde.\n"
