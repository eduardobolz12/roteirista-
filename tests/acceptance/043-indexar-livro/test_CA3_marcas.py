"""CA-3: capítulo pronto não é refeito; indexar um capítulo tira a marca; --refazer refaz tudo."""


def test_CA3_marcas(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("indexar-livro", "teste").codigo == 0
    ollama.pedidos.clear()

    r = livro("indexar-livro", "teste")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "01 | já indexado\n02 | já indexado\n0 capítulos indexados, 2 já estavam\n"
    assert ollama.pedidos == []

    assert livro("indexar", "teste", "01").codigo == 0
    r = livro("indexar-livro", "teste")
    assert r.texto == "01 | 3 itens gravados, 0 corrigidos, 0 rejeitados | 0 itens gravados, 0 sem conteúdo, 0 rejeitados | lacunas 0\n02 | já indexado\n1 capítulos indexados, 1 já estavam\n"

    r = livro("indexar-livro", "teste", "--refazer")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto.splitlines()[-1] == "2 capítulos indexados, 0 já estavam"
