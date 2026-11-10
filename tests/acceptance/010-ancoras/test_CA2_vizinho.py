"""CA-2: âncora num vizinho corrige o id e avisa."""


def test_CA2_vizinho(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    ollama.grupo = "vizinho"

    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        "corrigido: 01.005 -> 01.003: 400,000 sacas\n"
        "corrigido: 01.007 -> 01.006: fechou\n"
        "2 itens gravados, 2 corrigidos, 0 rejeitados\n"
    )

    assert livro("itens", "teste", "01").texto == (
        "01.003 | numero | 400,000 sacas | Muito açúcar chegou ao porto.\n"
        "01.006 | cena | fechou | O inverno isolou a aldeia.\n"
    )
