"""CA-2: a falha para o comando; a próxima chamada retoma do capítulo que faltou."""


def test_CA2_retoma(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    ollama.falhar = {2, 3, 4}

    r = livro("indexar-livro", "teste")
    assert r.codigo == 3, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto.startswith("01 | 3 itens gravados, 0 corrigidos, 0 rejeitados | 0 itens gravados, 0 sem conteúdo, 0 rejeitados | lacunas 0\n")
    assert "modelo inacessível:" in r.erro

    ollama.falhar = set()
    r = livro("indexar-livro", "teste")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "01 | já indexado\n02 | 2 itens gravados, 0 corrigidos, 0 rejeitados | 0 itens gravados, 0 sem conteúdo, 0 rejeitados | lacunas 0\n1 capítulos indexados, 1 já estavam\n"
