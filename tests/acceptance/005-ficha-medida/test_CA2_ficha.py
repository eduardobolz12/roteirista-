"""CA-2: a ficha mostra a língua; sem --lingua é 'não informada'; língua inválida não cria livro."""


def test_CA2_ficha(pdf, livro, livros):
    assert livro("novo", str(pdf), "--slug", "teste", "--lingua", "pt").codigo == 0
    assert livro("novo", str(pdf), "--slug", "outro").codigo == 0

    f1 = livro("ficha", "teste")
    assert f1.codigo == 0, f"código {f1.codigo}; stderr: {f1.erro}"
    assert f1.stdout == "língua: pt\ncapítulos: 2\nparágrafos: 5\n".encode("utf-8")

    f2 = livro("ficha", "outro")
    assert f2.codigo == 0, f"código {f2.codigo}; stderr: {f2.erro}"
    assert f2.texto.startswith("língua: não informada\n")

    erro = livro("novo", str(pdf), "--slug", "errado", "--lingua", "xx")
    assert erro.codigo == 2, f"código {erro.codigo}; stderr: {erro.erro}"
    assert "língua inválida: xx" in erro.erro
    assert not (livros / "errado").exists()
