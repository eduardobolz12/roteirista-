"""CA-3: todos os modelos falham (código 3, nada gravado); sem chave, nenhum pedido (código 2)."""


def test_CA3_nenhum_modelo(pdf, livro, servidor, pasta):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    servidor.modelos = {"m1": 429, "m2": 500}

    r = livro("revisar", "teste", "texto.md", "01.001-01.003", modelos="m1,m2")
    assert r.codigo == 3, f"código {r.codigo}; stderr: {r.erro}"
    assert "nenhum modelo gratuito respondeu" in r.erro, r.erro
    assert not (pasta / "texto.revisao.txt").exists(), "sem resposta, nada é gravado"
    assert len(servidor.nuvem) == 2, servidor.nuvem

    s = livro("revisar", "teste", "texto.md", "01.001-01.003", chave=False)
    assert s.codigo == 2, f"código {s.codigo}; stderr: {s.erro}"
    assert "chave da nuvem não informada: ROTEIRISTA_NUVEM_CHAVE" in s.erro, s.erro
    assert len(servidor.nuvem) == 2, "sem chave, nenhum pedido à nuvem"
