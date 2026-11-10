"""CA-3: depois de indexar, o texto e a ficha do livro antigo são os mesmos."""


def test_CA3_nada_se_perde(antigo, livro):
    r = livro("indexar", antigo, "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"

    assert livro("trecho", antigo, "01.001").texto == "O homem parou diante do túmulo e leu o próprio nome gravado no cimento.\n"
    assert livro("trecho", antigo, "02.002").texto == (
        "Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.\n"
    )
    assert livro("ficha", antigo).texto == "língua: não informada\ncapítulos: 2\nparágrafos: 5\n"
