"""CA-2: o texto do capítulo aparece num id só; serviço e parte ficam fora do livro."""


def test_CA2_texto_em_um_lugar(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r1 = livro("conferir", "teste", "O homem leu")
    assert r1.codigo == 0, f"código {r1.codigo}; stderr: {r1.erro}"
    assert r1.stdout == b"EXISTE 03.001\n"

    r2 = livro("buscar", "teste", "certidão")
    assert r2.codigo == 0, f"código {r2.codigo}; stderr: {r2.erro}"
    assert r2.stdout == b"04.001\n"

    for termo in ["direitos", "costa"]:
        r = livro("buscar", "teste", termo)
        assert r.codigo == 1, f"{termo!r}: código {r.codigo}; stderr: {r.erro}"
        assert r.stdout == b"", f"{termo!r}: {r.stdout!r}"
