"""CA-2: título corrido e número de página não viram parágrafo nem entram em parágrafo."""

IDS = ["01.001", "01.002", "01.003", "01.004", "01.005", "02.001"]
PROIBIDOS = ["O LIVRO DE TESTE", "12", "13", "14"]


def test_CA2_cabecalho_rodape(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"código {novo.codigo}; stderr: {novo.erro}"
    assert novo.texto.rstrip("\n").split("\n")[-1] == "2 capítulos, 6 parágrafos"

    for id_ in IDS:
        r = livro("trecho", "teste", id_)
        assert r.codigo == 0, f"{id_}: código {r.codigo}; stderr: {r.erro}"
        for proibido in PROIBIDOS:
            assert proibido not in r.texto, f"{id_} contém {proibido!r}: {r.texto!r}"
