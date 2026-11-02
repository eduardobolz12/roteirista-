"""CA-3: marcas internas do <p> somem e entidades HTML viram caractere."""


def test_CA3_marcas_e_entidades(epub, livro):
    novo = livro("novo", str(epub), "--slug", "teste")
    assert novo.codigo == 0, f"conversão falhou: código {novo.codigo}; stderr: {novo.erro}"

    r = livro("trecho", "teste", "02.001")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.stdout == "O médico assinou a certidão às três horas da tarde & saiu.\n".encode("utf-8")
