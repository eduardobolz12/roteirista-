"""CA-2: `--wiki` busca na Wikipédia; `sem resposta` não é achado; fonte já gravada não se repete."""


def test_CA2_wiki_e_fonte_existente(pdf, livro, servidor):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    assert livro("fonte", "teste", "https://europepmc.org/article/MED/11111111").codigo == 0
    servidor.modelos = {"m1": ("json", "sem resposta\n")}

    r = livro("pesquisar", "teste", "Quando saiu?", "--busca", "Test Book", "--wiki")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == "fonte W02 | Wikipedia | — | Test Book\n0 achados, 0 recusados — m1\n"
    assert any(p["q"].get("list") == "search" and p["q"].get("srsearch") == "Test Book" for p in servidor.api), servidor.api

    s = livro("pesquisar", "teste", "Qual a incidência?", "--busca", "awareness anaesthesia")
    assert s.codigo == 0, f"código {s.codigo}; stderr: {s.erro}"
    assert s.texto.startswith(
        "fonte W01 | Silva A et al. | 2014 | Awareness under anaesthesia: a test record.\n"
        "fonte W03 | Costa D | 2004 | A second test record.\n"
    ), s.texto

    f = livro("fontes", "teste")
    linhas = f.texto.splitlines()
    assert [l.split(" | ")[0] for l in linhas] == ["W01", "W02", "W03"], f.texto
    assert linhas[2].endswith("| https://europepmc.org/article/MED/22222222"), f.texto
