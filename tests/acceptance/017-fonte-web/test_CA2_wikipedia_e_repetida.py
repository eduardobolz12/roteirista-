"""CA-2: uma página da Wikipédia vira a W02 sem as referências; a URL repetida não é pedida de novo."""


def test_CA2_wikipedia_e_repetida(pdf, livro, servidor):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("fonte", "teste", "https://europepmc.org/article/MED/11111111").codigo == 0

    r = livro("fonte", "teste", "https://en.wikipedia.org/wiki/Test_Book")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "W02 | Wikipedia | — | Test Book\n3 parágrafos\n"
    wiki = [p for p in servidor.api if p["caminho"] == "/w/api.php"]
    assert len(wiki) == 1, servidor.api
    assert wiki[0]["q"].get("titles", "").replace("_", " ") == "Test Book", wiki[0]
    assert wiki[0]["q"].get("prop") == "extracts" and wiki[0]["q"].get("explaintext") == "1", wiki[0]

    antes = len(servidor.api)
    d = livro("fonte", "teste", "https://europepmc.org/article/MED/11111111")
    assert d.codigo == 0, f"código {d.codigo}; stderr: {d.erro}"
    assert d.texto == "W01 | já gravada\n"
    assert len(servidor.api) == antes, "a URL já gravada não pode ser pedida de novo"

    f = livro("fontes", "teste")
    assert f.codigo == 0, f"código {f.codigo}; stderr: {f.erro}"
    assert f.texto == (
        "W01 | Silva A et al. | 2014 | Awareness under anaesthesia: a test record. | https://europepmc.org/article/MED/11111111\n"
        "W02 | Wikipedia | — | Test Book | https://en.wikipedia.org/wiki/Test_Book\n"
    )

    t = livro("trecho", "teste", "W02.003")
    assert t.codigo == 0 and t.texto == "It inspired a 1988 film.\n", (t.codigo, t.texto, t.erro)
    x = livro("trecho", "teste", "W02.004")
    assert x.codigo == 2 and x.texto == "" and "id inexistente: W02.004" in x.erro, (x.codigo, x.texto, x.erro)
