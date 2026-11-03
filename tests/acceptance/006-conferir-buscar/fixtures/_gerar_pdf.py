"""Gera nota-no-meio.pdf, a fixture da SPEC 006.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 python tests/acceptance/006-conferir-buscar/fixtures/_gerar_pdf.py

Igual à notas.pdf da SPEC 003, exceto que a chamada da nota fica no meio do 1º parágrafo.
"""
from pathlib import Path

from fpdf import FPDF

LINHA = 6  # mm entre linhas
PARAGRAFO = 12  # mm entre parágrafos

pdf = FPDF(format="A5")  # 148 x 210 mm
pdf.set_auto_page_break(auto=False)
pdf.set_left_margin(15)


def titulo(texto, y):
    pdf.start_section(texto, level=0)
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.set_xy(15, y)
    pdf.cell(118, 10, texto)
    return y + 10 + PARAGRAFO


def corpo(texto, y, chamada=None, depois=""):
    pdf.set_font("Helvetica", size=11)
    pdf.set_xy(15, y)
    pdf.write(LINHA, texto)
    if chamada:
        pdf.char_vpos = "SUP"
        pdf.write(LINHA, chamada)
        pdf.char_vpos = "LINE"
        pdf.write(LINHA, depois)
    return y + PARAGRAFO


# Página 1: dois parágrafos e uma nota de rodapé
pdf.add_page()
y = titulo("Capítulo Um", 30)
y = corpo("O médico assinou a certidão", y, chamada="1", depois=" sem examinar o corpo.")
y = corpo("A família guardou uma cópia na igreja.", y)
pdf.set_font("Helvetica", size=8)
pdf.set_xy(15, 185)
pdf.cell(118, 4, "1 A certidão foi encontrada em 1981 nos arquivos do hospital.")

# Página 2: um parágrafo
pdf.add_page()
y = titulo("Capítulo Dois", 30)
corpo("O caso chegou aos jornais da capital.", y)

# Página 3: bibliografia
pdf.add_page()
y = titulo("Bibliografia", 30)
y = corpo("Davis, Wade. The Serpent and the Rainbow. 1985.", y)
corpo("Métraux, Alfred. Le Vaudou haïtien. 1958.", y)

saida = Path(__file__).with_name("nota-no-meio.pdf")
pdf.output(str(saida))
print(saida)
