"""CA-3: fichas do mesmo parágrafo com a mesma frase ficam uma só."""


def test_CA3_mesma_frase(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "en", "--lingua", "en").codigo == 0
    ollama.grupo = "frase"

    r = livro("indexar", "en", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto.splitlines()[-1] == "2 itens gravados, 0 corrigidos, 0 rejeitados"
    assert livro("itens", "en", "01").texto == (
        "01.001 | cena | próprio nome | O homem lê o próprio nome no túmulo.\n"
        "01.002 | caso | apelido de infância | A irmã reconhece o apelido.\n"
    )
