"""CA-3: busca sem resultado não pede à nuvem (código 1); busca fora do ar não grava nada (código 3)."""


def test_CA3_busca_vazia_e_fora_do_ar(pdf, livro, servidor):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    servidor.modelos = {"m1": ("json", "sem resposta\n")}

    a = livro("pesquisar", "teste", "?", "--busca", "zumbi")
    assert a.codigo == 1, f"código {a.codigo}; stderr: {a.erro}"
    assert a.texto == "0 fontes\n"
    assert servidor.nuvem == [], "sem fonte, nenhum pedido à nuvem"

    servidor.falhar_api = True
    b = livro("pesquisar", "teste", "Qual a incidência?", "--busca", "awareness anaesthesia")
    assert b.codigo == 3, f"código {b.codigo}; stderr: {b.erro}"
    assert "busca falhou: europepmc" in b.erro, b.erro
    assert servidor.nuvem == [], servidor.nuvem

    servidor.falhar_api = False
    f = livro("fontes", "teste")
    assert f.codigo == 0 and f.texto == "", (f.codigo, f.texto, f.erro)
