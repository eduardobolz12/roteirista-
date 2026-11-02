"""CA-1: `livro montar` devolve os parágrafos na ordem dos argumentos."""


def test_CA1_ordem_pedida(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r = livro("montar", "teste", "02.002", "01.001")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.stdout == (
        "## 02.002\n\n"
        "Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.\n"
        "\n"
        "## 01.001\n\n"
        "O homem parou diante do túmulo e leu o próprio nome gravado no cimento.\n"
    ).encode("utf-8")
