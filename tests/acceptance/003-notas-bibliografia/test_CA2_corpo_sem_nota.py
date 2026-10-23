"""CA-2: o corpo fica sem o texto da nota, e a chamada vira a marca [nPP]."""


def test_CA2_corpo_sem_nota(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"conversão falhou: código {novo.codigo}; stderr: {novo.erro}"

    r1 = livro("trecho", "teste", "01.001")
    assert r1.codigo == 0, f"código {r1.codigo}; stderr: {r1.erro}"
    assert r1.stdout == "O médico assinou a certidão sem examinar o corpo.[n01]\n".encode("utf-8")

    r2 = livro("trecho", "teste", "01.002")
    assert r2.codigo == 0, f"código {r2.codigo}; stderr: {r2.erro}"
    assert r2.stdout == "A família guardou uma cópia na igreja.\n".encode("utf-8")
