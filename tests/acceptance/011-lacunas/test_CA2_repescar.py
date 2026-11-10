"""CA-2: a repescagem manda só as lacunas e aceita item ou sem-conteudo."""


def test_CA2_repescar(pdf, livro, ollama, prompts):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("indexar", "teste", "01").codigo == 0
    ollama.pedidos.clear()

    r = livro("repescar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        "rejeitado (id fora da lista): 01.001 | cena | médico | Parágrafo que não é lacuna.\n"
        "rejeitado (âncora não encontrada): 01.005 | caso | palavra que não existe | Âncora que não está no parágrafo.\n"
        "1 itens gravados, 1 sem conteúdo, 2 rejeitados\n"
    )

    assert ollama.trechos() == [["01.003", "01.004", "01.005"]]
    assert ollama.pedidos[0]["prompt"].startswith((prompts / "repescar.txt").read_bytes().decode("utf-8"))

    assert livro("lacunas", "teste", "01").texto == "01.005\n"
    assert livro("itens", "teste", "01").texto == (
        "01.001 | cena | certidão | O médico assinou o documento.\n"
        "01.003 | caso | uma cópia | A família guardou o documento.\n"
    )
