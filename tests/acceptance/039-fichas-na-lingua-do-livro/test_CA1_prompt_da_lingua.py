"""CA-1: livro com língua informada usa os prompts novos; sem língua, os antigos."""

PARAGRAFOS = (
    "[01.001] O homem parou diante do túmulo e leu o próprio nome gravado no cimento.\n\n"
    "[01.002] A irmã reconheceu o apelido de infância antes de reconhecer o rosto.\n\n"
    "[01.003] Naquela tarde, ninguém na aldeia quis falar sobre o enterro."
)


def test_CA1_prompt_da_lingua(pdf, livro, ollama, prompts):
    assert livro("novo", str(pdf), "--slug", "en", "--lingua", "en").codigo == 0
    assert livro("novo", str(pdf), "--slug", "pt").codigo == 0
    ler = lambda nome: (prompts / nome).read_bytes().decode("utf-8")

    r = livro("indexar", "en", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert ollama.pedidos[-1]["prompt"] == ler("indexar-livro.txt") + PARAGRAFOS

    r = livro("repescar", "en", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert ollama.pedidos[-1]["prompt"].startswith(ler("repescar-livro.txt"))

    r = livro("indexar", "pt", "01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert ollama.pedidos[-1]["prompt"] == ler("indexar.txt") + PARAGRAFOS
