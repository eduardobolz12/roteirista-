"""CA-1: a nota de rodapé tem id próprio e sai sem o número inicial."""


def test_CA1_nota_tem_id_proprio(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"conversão falhou: código {novo.codigo}; stderr: {novo.erro}"

    r = livro("trecho", "teste", "01.n01")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.stdout == "A certidão foi encontrada em 1981 nos arquivos do hospital.\n".encode("utf-8")
