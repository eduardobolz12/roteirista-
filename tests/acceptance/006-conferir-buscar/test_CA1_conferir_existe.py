"""CA-1: frase literal existe; a marca [nPP] no meio da frase e espaços repetidos não atrapalham."""


def test_CA1_conferir_existe(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r1 = livro("conferir", "teste", "a certidão sem examinar")
    assert r1.codigo == 0, f"código {r1.codigo}; stderr: {r1.erro}"
    assert r1.stdout == b"EXISTE 01.001\n"

    r2 = livro("conferir", "teste", "guardou uma   cópia")
    assert r2.codigo == 0, f"código {r2.codigo}; stderr: {r2.erro}"
    assert r2.stdout == b"EXISTE 01.002\n"
