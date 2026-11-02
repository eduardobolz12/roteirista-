"""CA-1: `livro novo` converte o EPUB; a capa sem título não conta."""


def test_CA1_novo_converte_epub(epub, livro):
    r = livro("novo", str(epub), "--slug", "teste")

    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto.rstrip("\n").split("\n")[-1] == "2 capítulos, 5 parágrafos"
