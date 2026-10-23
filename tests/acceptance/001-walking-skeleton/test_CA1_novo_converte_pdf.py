"""CA-1: `livro novo` converte o PDF de 2 capítulos e cria o banco do livro."""

def test_CA1_novo_converte_pdf(pdf, livro, livros):
    r = livro("novo", str(pdf), "--slug", "teste")

    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto.rstrip("\n").split("\n")[-1] == "2 capítulos, 5 parágrafos"
    assert (livros / "teste" / "livro.sqlite").is_file()
