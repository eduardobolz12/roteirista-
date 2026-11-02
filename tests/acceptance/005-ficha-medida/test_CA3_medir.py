"""CA-3: `livro medir` dá palavras e tokens estimados por capítulo e o total."""


def test_CA3_medir(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste", "--lingua", "pt").codigo == 0

    r = livro("medir", "teste")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.stdout == (
        "01 36 palavras, 50 tokens\n"
        "02 27 palavras, 37 tokens\n"
        "total 63 palavras, 87 tokens\n"
    ).encode("utf-8")
