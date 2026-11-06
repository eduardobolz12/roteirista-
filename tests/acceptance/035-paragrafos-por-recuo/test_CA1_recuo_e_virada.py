"""CA-1: o recuo separa parágrafos e decide a virada de página, não a pontuação."""


def test_CA1_recuo_e_virada(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"código {novo.codigo}; stderr: {novo.erro}"
    assert novo.texto.splitlines()[-1] == "3 capítulos, 17 parágrafos"

    r2 = livro("trecho", "teste", "01.002")
    assert r2.codigo == 0, f"código {r2.codigo}; stderr: {r2.erro}"
    assert r2.texto == (
        "A irmã do morto contou a história na manhã seguinte, à porta da igreja, sem pressa, "
        "enquanto os vizinhos fingiam não ouvir nada do que ela dizia. Ninguém na aldeia duvidou "
        "daquela versão. Os mais velhos lembravam o enterro e o nome gravado na cruz de madeira "
        "do cemitério.\n"
    )

    r3 = livro("trecho", "teste", "01.003")
    assert r3.codigo == 0, f"código {r3.codigo}; stderr: {r3.erro}"
    assert r3.texto.endswith("por causa da neve e\n"), r3.texto

    r4 = livro("trecho", "teste", "01.004")
    assert r4.codigo == 0, f"código {r4.codigo}; stderr: {r4.erro}"
    assert r4.texto == "Na primavera, o bispo mandou buscar o livro e nunca o devolveu.\n"

    r5 = livro("trecho", "teste", "01.005")
    assert r5.codigo == 2, f"código {r5.codigo}; stdout: {r5.texto!r}"
