"""CA-1: um comando indexa e repesca todos os capítulos, em ordem."""


def test_CA1_livro_inteiro(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r = livro("indexar-livro", "teste")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "01 | 3 itens gravados, 0 corrigidos, 0 rejeitados | 0 itens gravados, 0 sem conteúdo, 0 rejeitados | lacunas 0\n02 | 2 itens gravados, 0 corrigidos, 0 rejeitados | 0 itens gravados, 0 sem conteúdo, 0 rejeitados | lacunas 0\n2 capítulos indexados, 0 já estavam\n"
    assert ollama.trechos() == [["01.001", "01.002", "01.003"], ["02.001", "02.002"]]
