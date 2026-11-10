"""Gera ancoras.pdf, a fixture da SPEC 010.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 python tests/acceptance/010-ancoras/fixtures/_gerar_pdf.py
"""
from pathlib import Path

from fpdf import FPDF

PARAGRAFOS = [
    "O navio partiu de Liverpool em março.",
    "A viagem durou quase dois meses.",
    "Chegaram 400,000 sacas de açúcar ao porto.",
    'O capitão escreveu ao "governador" sobre a carga.',
    "Ninguém respondeu à carta.",
    "O inverno fechou a estrada.",
    "A neve cobriu a alfândega.",
]

pdf = FPDF(format="A5")  # 148 x 210 mm
pdf.set_auto_page_break(auto=False)
pdf.add_page()
pdf.start_section("Capítulo Um", level=0)
pdf.set_font("Helvetica", style="B", size=16)
pdf.set_xy(15, 32)
pdf.cell(118, 10, "Capítulo Um")
pdf.set_font("Helvetica", size=11)
y = 50
for texto in PARAGRAFOS:
    pdf.set_xy(15, y)
    pdf.cell(118, 6, texto)
    y += 16

saida = Path(__file__).with_name("ancoras.pdf")
pdf.output(str(saida))
print(saida)
