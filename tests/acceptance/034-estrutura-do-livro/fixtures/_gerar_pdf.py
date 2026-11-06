"""Gera estrutura.pdf, a fixture da SPEC 034.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 python tests/acceptance/034-estrutura-do-livro/fixtures/_gerar_pdf.py

Imita a estrutura de um livro comercial: capa sem texto, páginas de serviço, uma parte com capítulos
dentro e abertura de capítulo com número e título em fonte maior.
"""
from pathlib import Path

from fpdf import FPDF

LINHA = 6  # mm entre linhas
PARAGRAFO = 12  # mm entre parágrafos

pdf = FPDF(format="A5")  # 148 x 210 mm
pdf.set_auto_page_break(auto=False)
pdf.set_left_margin(15)


def pagina(marcador, nivel=0):
    pdf.add_page()
    pdf.start_section(marcador, level=nivel)


def grande(texto, y):
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.set_xy(15, y)
    pdf.cell(118, 10, texto)


def corpo(texto, y):
    pdf.set_font("Helvetica", size=11)
    pdf.set_xy(15, y)
    pdf.write(LINHA, texto)
    return y + PARAGRAFO


# Capa: só o marcador, nenhum texto (nos livros reais é uma imagem)
pagina("Title Page")

pagina("Copyright Page")
corpo("Todos os direitos reservados.", 40)

pagina("Contents")
y = corpo("O Túmulo", 40)
corpo("A Certidão", y)

pagina("Dedication")
corpo("Aos meus pais.", 40)

pagina("Parte Um")
grande("PARTE UM", 35)
grande("O Veneno", 50)
corpo("Esta parte reúne os casos da costa.", 70)

pagina("1: O Túmulo", nivel=1)
grande("1", 35)
grande("O Túmulo", 50)
y = corpo("O homem leu o próprio nome gravado no cimento.", 70)
corpo("A irmã reconheceu o apelido de infância.", y)

pagina("2: A Certidão", nivel=1)
grande("2", 35)
grande("A Certidão", 50)
corpo("O médico assinou a certidão às três horas.", 70)

pagina("Annotated Bibliography")
corpo("Davis, Wade. The Serpent and the Rainbow. 1985.", 40)

pagina("Index")
y = corpo("certidão, 12", 40)
corpo("túmulo, 3", y)

saida = Path(__file__).with_name("estrutura.pdf")
pdf.output(str(saida))
print(saida)
