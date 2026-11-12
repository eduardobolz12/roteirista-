"""CA-1: a busca grava as fontes com resumo; só passa o fato cuja citação está no parágrafo apontado."""

RESPOSTA = (
    'A incidência com bloqueio foi de ~1:8200. | "The incidence with neuromuscular block was ~1:8200" | W01.002\n'
    'A incidência geral foi de 0,13%. | "The incidence was 0.13%." | W02.001\n'
    'Pacientes acordam sempre. | "Patients often wake during surgery." | W01.001\n'
    'O estudo foi em 1990. | "The study ran in 1990." | W09.001\n'
)

ESPERADO = (
    "fonte W01 | Silva A et al. | 2014 | Awareness under anaesthesia: a test record.\n"
    "fonte W02 | Costa D | 2004 | A second test record.\n"
    'W01.002 | A incidência com bloqueio foi de ~1:8200. | "The incidence with neuromuscular block was ~1:8200"\n'
    'W02.001 | A incidência geral foi de 0,13%. | "The incidence was 0.13%."\n'
    'recusado (citação não confere): Pacientes acordam sempre. | "Patients often wake during surgery." | W01.001\n'
    'recusado (id fora das fontes): O estudo foi em 1990. | "The study ran in 1990." | W09.001\n'
    "2 achados, 2 recusados — m1\n"
)


def test_CA1_achados_conferidos(pdf, livro, servidor, prompts):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    servidor.modelos = {"m1": ("json", RESPOSTA)}

    r = livro("pesquisar", "teste", "Qual a incidência?", "--busca", "awareness anaesthesia")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == ESPERADO

    busca = [p for p in servidor.api if p["caminho"] == "/europepmc/search"]
    assert busca and busca[0]["q"].get("query") == "awareness anaesthesia", servidor.api
    assert busca[0]["q"].get("pageSize") == "10" and busca[0]["q"].get("resultType") == "core", busca[0]

    assert len(servidor.nuvem) == 1, servidor.nuvem
    conteudo = servidor.conteudo(0)
    inicio = (prompts / "pesquisar.txt").read_text(encoding="utf-8").split("{pergunta}")[0]
    assert conteudo.startswith(inicio), "o pedido tem de usar docs/prompts/pesquisar.txt"
    assert "Qual a incidência?" in conteudo and "## W02.001" in conteudo, conteudo
    assert "33333333" not in conteudo and "A record without abstract" not in conteudo, "resultado sem resumo não vira fonte"

    t = livro("trecho", "teste", "W02.001")
    assert t.codigo == 0 and t.texto == "The incidence was 0.13%.\n", (t.codigo, t.texto, t.erro)
