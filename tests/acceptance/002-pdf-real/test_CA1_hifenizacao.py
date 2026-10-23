"""CA-1: palavra partida no fim da linha volta inteira; hífen de composto conhecido fica."""


def test_CA1_hifenizacao(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"conversão falhou: código {novo.codigo}; stderr: {novo.erro}"

    r1 = livro("trecho", "teste", "01.001")
    assert r1.codigo == 0, f"código {r1.codigo}; stderr: {r1.erro}"
    assert r1.stdout == "A família pagou a construção do túmulo em duas parcelas.\n".encode("utf-8")

    r2 = livro("trecho", "teste", "01.002")
    assert r2.codigo == 0, f"código {r2.codigo}; stderr: {r2.erro}"
    assert r2.stdout == "Os vizinhos chamavam aquilo de guarda-chuva dos mortos, e riam.\n".encode("utf-8")
