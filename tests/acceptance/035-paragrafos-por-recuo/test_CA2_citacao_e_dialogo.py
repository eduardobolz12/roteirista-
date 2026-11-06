"""CA-2: citação em bloco é um parágrafo só; cada fala curta é um parágrafo."""


def test_CA2_citacao_e_dialogo(pdf, livro):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0

    esperado = [
        "O legista escreveu ao bispo e descreveu o que tinha visto no corpo, dizendo apenas isto:\n",
        "O paciente estava pálido e consciente, com o pulso pequeno e intermitente, e a respiração "
        "foi ficando difícil até cessar.\n",
        "Depois disso, o bispo não respondeu a nenhuma carta do legista e o caso foi esquecido.\n",
        '"Professor."\n',
        '"Sim?"\n',
        '"O senhor leu a carta do legista antes de mandar buscar o livro?"\n',
    ]
    for numero, texto in enumerate(esperado, start=1):
        id_ = f"02.{numero:03d}"
        r = livro("trecho", "teste", id_)
        assert r.codigo == 0, f"{id_}: código {r.codigo}; stderr: {r.erro}"
        assert r.texto == texto, f"{id_}: {r.texto!r}"
