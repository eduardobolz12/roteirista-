"""CA-3: âncora longe, inexistente ou vazia é rejeitada; a correção pode gerar duplicado."""


def test_CA3_rejeita(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    ollama.grupo = "rejeitar"

    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == (
        "rejeitado (âncora não encontrada): 01.002 | marginal | alfândega | Âncora longe demais.\n"
        "rejeitado (âncora não encontrada): 01.003 | doutrina | palavra que não existe | Âncora que não está no livro.\n"
        "rejeitado (âncora não encontrada): 01.004 | caso |  | Sem âncora.\n"
        "corrigido: 01.005 -> 01.003: 400,000 sacas\n"
        "1 itens gravados, 1 corrigidos, 3 rejeitados\n"
    )

    assert livro("itens", "teste", "01").texto == (
        "01.003 | numero | 400,000 sacas | Muito açúcar chegou ao porto.\n"
    )
