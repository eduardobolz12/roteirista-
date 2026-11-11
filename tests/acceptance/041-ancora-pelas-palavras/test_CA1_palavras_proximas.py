"""CA-1: a âncora confere sem a pontuação, com palavras omitidas e, se longa, por um trecho de quatro palavras."""


def test_CA1_palavras_proximas(pdf, livro, ollama):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    ollama.grupo = "perto"

    r = livro("indexar", "teste", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "3 itens gravados, 0 corrigidos, 0 rejeitados\n"
    assert livro("itens", "teste", "01").texto == (
        "01.001 | cena | homem parou túmulo | O homem para diante do túmulo.\n"
        "01.002 | caso | A irmã reconheceu o apelido da escola | A irmã reconhece o apelido.\n"
        "01.003 | cena | Naquela tarde ninguém | Ninguém fala do enterro.\n"
    )
