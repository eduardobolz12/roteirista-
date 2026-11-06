"""CA-1: travessão na quebra de linha une sem espaço, no fim ou no início da linha."""


def test_CA1_travessao(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    esperado = {
        "01.001": "A família esperou em silêncio—ninguém falou nada.\n",
        "01.002": "O padre saiu da igreja—a chuva já tinha parado.\n",
    }
    for id_, texto in esperado.items():
        r = livro("trecho", "teste", id_)
        assert r.codigo == 0, f"{id_}: código {r.codigo}; stderr: {r.erro}"
        assert r.texto == texto, f"{id_}: {r.texto!r}"
