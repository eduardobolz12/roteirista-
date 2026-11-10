"""Gera lacunas.pdf, a fixture da SPEC 011.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 python tests/acceptance/011-lacunas/fixtures/_gerar_pdf.py
"""
from pathlib import Path

from fpdf import FPDF

PARAGRAFOS = [
    "O médico assinou a certidão.",
    "* * *",
    "A família guardou uma cópia.",
    "Fim da primeira parte.",
    "O caso chegou aos jornais.",
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

saida = Path(__file__).with_name("lacunas.pdf")
pdf.output(str(saida))
print(saida)
