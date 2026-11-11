"""Gera ingles.pdf, a fixture das SPECs 014 e 015.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 python tests/acceptance/015-visao-e-temas/fixtures/_gerar_pdf.py
"""
from pathlib import Path

from fpdf import FPDF

CAPITULOS = {
    "Chapter One": [
        "Perhaps the ship from Saint Marc carried more cargo than the records show.",
        "The author admits the hypothesis, though neat, was quite wrong.",
        "Marcel Pierre sold the powder to Max Beauvoir in Saint Marc.",
    ],
    "Chapter Two": [
        "Schultes thought it quite possibly came from the Spaniards.",
        "It seems the Bizango met at night in Saint Marc.",
        "The Bizango judged Narcisse there.",
    ],
}

pdf = FPDF(format="A4")  # 210 x 297 mm
pdf.set_auto_page_break(auto=False)
for titulo, paragrafos in CAPITULOS.items():
    pdf.add_page()
    pdf.start_section(titulo, level=0)
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.set_xy(20, 45)
    pdf.cell(170, 10, titulo)
    pdf.set_font("Helvetica", size=11)
    y = 65
    for texto in paragrafos:
        pdf.set_xy(20, y)
        pdf.cell(170, 6, texto)
        y += 16

saida = Path(__file__).with_name("ingles.pdf")
pdf.output(str(saida))
print(saida)
