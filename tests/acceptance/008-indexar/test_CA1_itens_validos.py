"""CA-1: itens válidos são gravados, e o pedido segue o contrato com o Ollama."""


def test_CA1_itens_validos(pdf, livro, ollama, prompts):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "3 itens gravados, 0 corrigidos, 0 rejeitados\n"

    itens = livro("itens", "teste", "01")
    assert itens.codigo == 0, f"código {itens.codigo}; stderr: {itens.erro}"
    assert itens.texto == (
        "01.001 | cena | próprio nome | O homem vê o próprio nome num túmulo.\n"
        "01.002 | caso | apelido de infância | A irmã reconhece o homem pelo apelido.\n"
        "01.003 | marginal | aldeia | Ninguém na aldeia fala do enterro.\n"
    )

    assert len(ollama.pedidos) == 1
    pedido = ollama.pedidos[0]
    assert pedido["caminho"] == "/api/generate"
    assert pedido["model"] == "qwen3:14b"
    assert pedido["stream"] is False
    assert pedido["think"] is False
    assert pedido["options"] == {"temperature": 0, "num_ctx": 16384, "num_predict": 3000, "repeat_penalty": 1.1}
    assert pedido["prompt"] == (prompts / "indexar.txt").read_bytes().decode("utf-8") + (
        "[01.001] O homem parou diante do túmulo e leu o próprio nome gravado no cimento.\n\n"
        "[01.002] A irmã reconheceu o apelido de infância antes de reconhecer o rosto.\n\n"
        "[01.003] Naquela tarde, ninguém na aldeia quis falar sobre o enterro."
    )
