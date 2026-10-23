"""CA-3: a bibliografia não vira capítulo; cada entrada tem id bib.PPP."""


def test_CA3_bibliografia_fora_do_corpo(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"código {novo.codigo}; stderr: {novo.erro}"
    assert novo.texto.rstrip("\n").split("\n")[-1] == "2 capítulos, 3 parágrafos"

    b1 = livro("trecho", "teste", "bib.001")
    assert b1.codigo == 0, f"código {b1.codigo}; stderr: {b1.erro}"
    assert b1.stdout == "Davis, Wade. The Serpent and the Rainbow. 1985.\n".encode("utf-8")

    b2 = livro("trecho", "teste", "bib.002")
    assert b2.codigo == 0, f"código {b2.codigo}; stderr: {b2.erro}"
    assert b2.stdout == "Métraux, Alfred. Le Vaudou haïtien. 1958.\n".encode("utf-8")

    r = livro("trecho", "teste", "03.001")
    assert r.codigo == 2, f"código {r.codigo}; stderr: {r.erro}"
    assert r.stdout == b""
    assert "id inexistente: 03.001" in r.erro
