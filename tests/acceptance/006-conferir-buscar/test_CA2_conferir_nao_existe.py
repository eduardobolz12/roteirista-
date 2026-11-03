"""CA-2: palavra trocada ou maiúscula diferente não confere."""


def test_CA2_conferir_nao_existe(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    for frase in ["sem examinar o cadáver", "O MÉDICO assinou"]:
        r = livro("conferir", "teste", frase)
        assert r.codigo == 1, f"{frase!r}: código {r.codigo}; stderr: {r.erro}"
        assert r.stdout == "NÃO EXISTE\n".encode("utf-8"), f"{frase!r}: {r.stdout!r}"
