"""CA-3: id que não existe nunca devolve texto."""

def test_CA3_id_inexistente(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"conversão falhou: código {novo.codigo}; stderr: {novo.erro}"

    r = livro("trecho", "teste", "02.003")

    assert r.codigo == 2, f"código {r.codigo}; stderr: {r.erro}"
    assert r.stdout == b""
    assert "id inexistente: 02.003" in r.erro
