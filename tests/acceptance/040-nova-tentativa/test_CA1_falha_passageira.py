"""CA-1: uma falha passageira é repetida e o capítulo sai completo."""


def test_CA1_falha_passageira(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    ollama.falhar = {1}

    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "3 itens gravados, 0 corrigidos, 0 rejeitados\n"
    assert "modelo falhou, nova tentativa (1 de 2)" in r.erro
    assert len(ollama.pedidos) == 2
    assert ollama.pedidos[0]["prompt"] == ollama.pedidos[1]["prompt"]
