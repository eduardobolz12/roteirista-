"""CA-1: `novo --lingua` mostra 3 parágrafos de conferência antes do resumo."""


def test_CA1_lingua_e_conferencia(pdf, livro):
    r = livro("novo", str(pdf), "--slug", "teste", "--lingua", "pt")

    assert r.codigo == 0, f"código {r.codigo}; stderr: {r.erro}"
    assert r.texto.rstrip("\n").split("\n")[-4:] == [
        "01.001 O homem parou diante do túmulo e leu o próprio nome gravado no cimento.",
        "02.001 O médico assinou a certidão às três horas da tarde.",
        "02.002 Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.",
        "2 capítulos, 5 parágrafos",
    ]
