"""CA-2: `livro trecho` devolve o parágrafo literal, com acentos e linhas unidas."""

def test_CA2_trecho_devolve_literal(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"conversão falhou: código {novo.codigo}; stderr: {novo.erro}"

    r1 = livro("trecho", "teste", "01.001")
    assert r1.codigo == 0, f"código {r1.codigo}; stderr: {r1.erro}"
    assert r1.stdout == (
        "O homem parou diante do túmulo e leu o próprio nome gravado no cimento.\n"
    ).encode("utf-8")

    r2 = livro("trecho", "teste", "02.002")
    assert r2.codigo == 0, f"código {r2.codigo}; stderr: {r2.erro}"
    assert r2.stdout == (
        "Ninguém soube dizer à família, naquela manhã de maio, "
        "quem tinha aberto a cova durante a noite.\n"
    ).encode("utf-8")
