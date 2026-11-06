"""Gera recuo.pdf, a fixture da SPEC 035.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 python tests/acceptance/035-paragrafos-por-recuo/fixtures/_gerar_pdf.py

Imita a composição de um livro comercial: entrelinha constante, sem espaço entre parágrafos, linhas
justificadas até a margem direita. O que separa parágrafos é o recuo horizontal.
"""
from pathlib import Path

from fpdf import FPDF

LINHA = 6  # mm entre linhas, a mesma em toda a fixture
ESQ = 15  # margem esquerda
LARGURA = 118  # até a margem direita
RECUO = 6  # recuo de primeira linha, de citação e de continuação de glossário

M, R, C = "margem", "recuo", "citacao"

pdf = FPDF(format="A5")  # 148 x 210 mm
pdf.set_auto_page_break(auto=False)
pdf.set_left_margin(ESQ)


def capitulo(titulo):
    pdf.add_page()
    pdf.start_section(titulo, level=0)
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.set_xy(ESQ, 32)
    pdf.cell(LARGURA, 10, titulo)
    return 50


def linhas(y, itens):
    """Cada item: (posição, texto, cheia). Linha cheia é justificada até o fim da sua medida."""
    pdf.set_font("Helvetica", size=11)
    for posicao, texto, cheia in itens:
        x = ESQ if posicao == M else ESQ + RECUO
        fim = ESQ + LARGURA - (RECUO if posicao == C else 0)
        pdf.set_xy(x, y)
        if cheia:  # justifica com o espaço entre letras (cell não justifica linha solta)
            sobra_mm = fim - x - pdf.get_string_width(texto)
            pdf.set_char_spacing(sobra_mm * pdf.k / (len(texto) - 1))
        pdf.cell(fim - x, LINHA, texto)
        pdf.set_char_spacing(0)
        y += LINHA
    return y


# Capítulo Um: prosa com recuo de primeira linha e duas viradas de página
y = capitulo("Capítulo Um")
linhas(y, [
    (R, "O médico chegou à aldeia numa tarde de chuva e procurou", True),
    (M, "a casa do padre, onde esperava encontrar os registros da paróquia", True),
    (M, "e alguma notícia do morto.", False),
    (R, "A irmã do morto contou a história na manhã seguinte, à porta", True),
    (M, "da igreja, sem pressa, enquanto os vizinhos fingiam não ouvir nada", True),
    (M, "do que ela dizia. Ninguém na aldeia duvidou daquela versão.", True),
])
pdf.add_page()
linhas(35, [
    (M, "Os mais velhos lembravam o enterro e o nome gravado na cruz de", True),
    (M, "madeira do cemitério.", False),
    (R, "O padre guardou o livro dos óbitos numa caixa de folha, no", True),
    (M, "fundo da sacristia, e a chave ficou com o sacristão até o fim daquele", True),
    (M, "inverno longo em que a estrada ficou fechada por causa da neve e", True),
])
pdf.add_page()
linhas(35, [
    (R, "Na primavera, o bispo mandou buscar o livro e nunca o devolveu.", True),
])

# Capítulo Dois: citação em bloco e diálogo curto
y = capitulo("Capítulo Dois")
linhas(y, [
    (R, "O legista escreveu ao bispo e descreveu o que tinha visto no", True),
    (M, "corpo, dizendo apenas isto:", False),
    (C, "O paciente estava pálido e consciente, com o pulso", True),
    (C, "pequeno e intermitente, e a respiração foi ficando", True),
    (C, "difícil até cessar.", False),
    (M, "Depois disso, o bispo não respondeu a nenhuma carta do legista e", True),
    (M, "o caso foi esquecido.", False),
    (R, '"Professor."', False),
    (R, '"Sim?"', False),
    (R, '"O senhor leu a carta do legista antes de mandar buscar o livro?"', True),
])

# Glossário: a entrada começa na margem e a continuação é que tem recuo
y = capitulo("Glossário")
linhas(y, [
    (M, "ASSON Chocalho sagrado feito de cabaça e usado pelo sacerdote", True),
    (R, "nos ritos.", False),
    (M, "BOKOR Feiticeiro que trabalha com as duas mãos, a do bem e", True),
    (R, "a do mal.", False),
    (M, "CANARI Jarro de barro que guarda o espírito do morto depois do", True),
    (R, "enterro.", False),
    (M, "CANZO O rito do fogo.", False),
    (M, "HOUNFOUR O templo do vodu, com o seu pátio e os seus altares", True),
    (R, "de pedra.", False),
    (M, "LOA O espírito que desce e monta a pessoa durante a cerimônia", True),
    (R, "da noite.", False),
    (M, "MAMBO A sacerdotisa do vodu, que conduz a cerimônia e guarda", True),
    (R, "o asson.", False),
])

saida = Path(__file__).with_name("recuo.pdf")
pdf.output(str(saida))
print(saida)
