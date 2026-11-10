"""CA-1: âncora no parágrafo apontado, sem diferenciar maiúsculas e aspas, mantém o item."""


def test_CA1_ancora_literal(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    ollama.grupo = "literal"

    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto.splitlines()[-1] == "2 itens gravados, 0 corrigidos, 0 rejeitados"

    assert livro("itens", "teste", "01").texto == (
        "01.001 | cena | LIVERPOOL em março | O navio partiu na primavera.\n"
        "01.004 | caso | “governador” | O capitão escreveu à autoridade.\n"
    )
