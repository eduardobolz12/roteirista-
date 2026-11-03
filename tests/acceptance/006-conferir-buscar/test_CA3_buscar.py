"""CA-3: buscar sem diferenciar maiúsculas, na ordem do livro; nada achado = código 1."""


def test_CA3_buscar(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r1 = livro("buscar", "teste", "CERTIDÃO")
    assert r1.codigo == 0, f"código {r1.codigo}; stderr: {r1.erro}"
    assert r1.stdout == b"01.001\n01.n01\n"

    r2 = livro("buscar", "teste", "serpent")
    assert r2.codigo == 0, f"código {r2.codigo}; stderr: {r2.erro}"
    assert r2.stdout == b"bib.001\n"

    r3 = livro("buscar", "teste", "zumbi")
    assert r3.codigo == 1, f"código {r3.codigo}; stderr: {r3.erro}"
    assert r3.stdout == b""
