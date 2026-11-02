"""CA-2: intervalo do mesmo capítulo é expandido, inclusive, na ordem do livro."""


def test_CA2_intervalo(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r = livro("montar", "teste", "01.002-01.003")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.stdout == (
        "## 01.002\n\n"
        "A irmã reconheceu o apelido de infância antes de reconhecer o rosto.\n"
        "\n"
        "## 01.003\n\n"
        "Naquela tarde, ninguém na aldeia quis falar sobre o enterro.\n"
    ).encode("utf-8")
