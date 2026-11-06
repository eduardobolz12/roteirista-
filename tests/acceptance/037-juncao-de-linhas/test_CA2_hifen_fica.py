"""CA-2: o hífen fica antes de maiúscula e em composto que já tem outro hífen."""


def test_CA2_hifen_fica(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    esperado = {
        "01.003": "O carro era um velho Mercedes-Benz da prefeitura.\n",
        "01.004": "O trabalho do dia-a-dia pesava na aldeia.\n",
        "01.005": "Ela comprou uma saia-calça na feira.\n",
    }
    for id_, texto in esperado.items():
        r = livro("trecho", "teste", id_)
        assert r.codigo == 0, f"{id_}: código {r.codigo}; stderr: {r.erro}"
        assert r.texto == texto, f"{id_}: {r.texto!r}"
