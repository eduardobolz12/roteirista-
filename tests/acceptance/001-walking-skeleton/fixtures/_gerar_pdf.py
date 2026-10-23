"""Gera dois-capitulos.pdf, a fixture da SPEC 001.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 python tests/acceptance/001-walking-skeleton/fixtures/_gerar_pdf.py
"""
from pathlib import Path

from fpdf import FPDF

CAPITULOS = [
    ("Capítulo Um", [
        "O homem parou diante do túmulo e leu o próprio nome gravado no cimento.",
        "A irmã reconheceu o apelido de infância antes de reconhecer o rosto.",
        "Naquela tarde, ninguém na aldeia quis falar sobre o enterro.",
    ]),
    ("Capítulo Dois", [
        "O médico assinou a certidão às três horas da tarde.",
        "Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.",
    ]),
]

pdf = FPDF(format="A5")
pdf.set_auto_page_break(auto=True, margin=15)
for titulo, paragrafos in CAPITULOS:
    pdf.add_page()
    pdf.start_section(titulo, level=0)
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.multi_cell(0, 10, titulo)
    pdf.ln(6)
    pdf.set_font("Helvetica", size=11)
    for texto in paragrafos:
        # largura de 95 mm: o 2º parágrafo do cap. 2 quebra em duas linhas, sem hifenização
        pdf.multi_cell(95, 6, texto)
        pdf.ln(6)

saida = Path(__file__).with_name("dois-capitulos.pdf")
pdf.output(str(saida))
print(saida)
