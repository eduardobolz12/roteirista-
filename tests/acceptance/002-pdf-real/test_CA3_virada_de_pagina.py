"""CA-3: parágrafo que continua na página seguinte sai como um parágrafo só."""


def test_CA3_virada_de_pagina(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"conversão falhou: código {novo.codigo}; stderr: {novo.erro}"

    r4 = livro("trecho", "teste", "01.004")
    assert r4.codigo == 0, f"código {r4.codigo}; stderr: {r4.erro}"
    assert r4.stdout == "O padre chegou tarde e começou a missa sem esperar a família.\n".encode("utf-8")

    r5 = livro("trecho", "teste", "01.005")
    assert r5.codigo == 0, f"código {r5.codigo}; stderr: {r5.erro}"
    assert r5.stdout == "Depois da missa, o caixão foi levado em silêncio.\n".encode("utf-8")
