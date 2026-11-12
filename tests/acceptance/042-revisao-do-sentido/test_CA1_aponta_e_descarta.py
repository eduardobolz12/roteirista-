"""CA-1: o apontamento conferido sai com os ids; frase fora do texto e id fora do material são descartados."""

RESPOSTA = (
    "A irmã o reconheceu pelo rosto. | o livro diz que ela reconheceu o apelido antes do rosto | 01.002\n"
    "Naquela noite, a aldeia inteira fez festa. | o livro diz que ninguém quis falar do enterro | 01.003 / 01.001\n"
    "Um homem chorou no túmulo. | detalhe acrescentado | sem apoio\n"
    "Um homem leu o próprio nome num túmulo. | ordem | 02.001\n"
)

ESPERADO = (
    "01.002 | A irmã o reconheceu pelo rosto. | o livro diz que ela reconheceu o apelido antes do rosto\n"
    "01.003, 01.001 | Naquela noite, a aldeia inteira fez festa. | o livro diz que ninguém quis falar do enterro\n"
    "descartado (frase fora do texto): Um homem chorou no túmulo. | detalhe acrescentado | sem apoio\n"
    "descartado (id fora do material): Um homem leu o próprio nome num túmulo. | ordem | 02.001\n"
    "2 apontamentos, 2 descartados — m1\n"
)


def test_CA1_aponta_e_descarta(pdf, livro, servidor, pasta, prompts):
    assert livro("novo", str(pdf), "--slug", "teste").codigo == 0
    servidor.modelos = {"m1": ("json", RESPOSTA)}
    texto_antes = (pasta / "texto.md").read_bytes()

    r = livro("revisar", "teste", "texto.md", "01.001-01.003")
    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto == ESPERADO

    revisao = pasta / "texto.revisao.txt"
    assert revisao.exists(), "a revisão tem de ficar gravada ao lado do texto"
    assert revisao.read_bytes() == r.stdout
    assert (pasta / "texto.md").read_bytes() == texto_antes, "o texto não pode mudar"

    assert len(servidor.nuvem) == 1, servidor.nuvem
    pedido = servidor.nuvem[0]
    assert pedido["caminho"] == "/v1/chat/completions" and pedido["model"] == "m1", pedido
    assert pedido["chave"] == "Bearer chave-teste", pedido["chave"]
    assert pedido.get("temperature") == 0 and pedido.get("stream") is False and pedido.get("max_tokens") == 20000, pedido
    conteudo = servidor.conteudo(0)
    inicio = (prompts / "revisar.txt").read_text(encoding="utf-8").split("{material}")[0]
    assert conteudo.startswith(inicio), "o pedido tem de usar docs/prompts/revisar.txt"
    assert "## 01.002" in conteudo and "A irmã reconheceu o apelido de infância" in conteudo, conteudo
    assert "A irmã o reconheceu pelo rosto." in conteudo, conteudo
