"""CA-1: partes e páginas de serviço não são capítulo; capa sem texto mantém o número."""


def test_CA1_capitulos(pdf, livro):
    novo = livro("novo", str(pdf), "--slug", "teste")
    assert novo.codigo == 0, f"código {novo.codigo}; stderr: {novo.erro}"
    assert novo.texto.splitlines()[-4:] == [
        "02.001 Aos meus pais.",
        "04.001 O médico assinou a certidão às três horas.",
        "04.001 O médico assinou a certidão às três horas.",
        "4 capítulos, 4 parágrafos",
    ]

    medir = livro("medir", "teste")
    assert medir.codigo == 0, f"código {medir.codigo}; stderr: {medir.erro}"
    assert medir.texto.startswith("01 0 palavras, 0 tokens\n")
    assert len(medir.texto.splitlines()) == 5
