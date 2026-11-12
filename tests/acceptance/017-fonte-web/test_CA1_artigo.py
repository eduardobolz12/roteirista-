"""CA-1: um artigo do Europe PMC vira a fonte W01, com um parágrafo por seção do resumo."""


def test_CA1_artigo(pdf, livro, servidor):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    r = livro("fonte", "teste", "https://europepmc.org/article/MED/11111111")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "W01 | Silva A et al. | 2014 | Awareness under anaesthesia: a test record.\n2 parágrafos\n"

    pedidos = [p for p in servidor.api if p["caminho"] == "/europepmc/search"]
    assert len(pedidos) == 1, servidor.api
    assert pedidos[0]["q"].get("query") == "EXT_ID:11111111 AND SRC:MED", pedidos[0]
    assert pedidos[0]["q"].get("resultType") == "core" and pedidos[0]["q"].get("format") == "json", pedidos[0]
    assert pedidos[0]["agente"] == "roteirista/0.1", pedidos[0]

    t = livro("trecho", "teste", "W01.002")
    assert t.codigo == 0, f"código {t.codigo}; stderr: {t.erro}"
    assert t.texto == "The incidence with neuromuscular block was ~1:8200 (p<0.001).\n"
