"""CA-2: o primeiro modelo falha e o segundo responde em eventos `data:`; `sem apoio (...)` vale `sem apoio`."""


def test_CA2_modelo_de_reserva(pdf, livro, servidor):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    servidor.modelos = {
        "m1": 429,
        "m2": ("sse", "Naquela noite, a aldeia inteira fez festa. | festa inventada | sem apoio (cf. 01.003)\n"),
    }

    r = livro("revisar", "teste", "texto.md", "01.001-01.003", modelos="m1,m2")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert "modelo falhou, próximo: m1" in r.erro, r.erro
    assert r.texto == (
        "sem apoio | Naquela noite, a aldeia inteira fez festa. | festa inventada\n"
        "1 apontamentos, 0 descartados — m2\n"
    )
    assert [p["model"] for p in servidor.nuvem] == ["m1", "m2"], servidor.nuvem
