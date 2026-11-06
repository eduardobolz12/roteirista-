"""Gera juncao.pdf, a fixture da SPEC 037.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 --with matplotlib==3.10.1 python tests/acceptance/037-juncao-de-linhas/fixtures/_gerar_pdf.py

Um capítulo com nove parágrafos separados por espaço vertical. O matplotlib entra só para fornecer
uma fonte livre com travessão (DejaVu Serif).
"""
from pathlib import Path

import matplotlib
from fpdf import FPDF

LINHA = 6  # mm entre linhas
PARAGRAFO = 12  # mm entre parágrafos

PARAGRAFOS = [
    ["A família esperou em silêncio—", "ninguém falou nada."],
    ["O padre saiu da igreja", "—a chuva já tinha parado."],
    ["O carro era um velho Mercedes-", "Benz da prefeitura."],
    ["O trabalho do dia-a-", "dia pesava na aldeia."],
    ["Ela comprou uma saia-", "calça na feira."],
    ["A saia e a calça ficaram no varal."],
    ["A testemu-", "nha chegou cedo."],
    ["A sobre-", "mesa veio fria."],
    ["Deixaram a sobremesa sobre a mesa."],
]

fonte = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSerif.ttf"
pdf = FPDF(format="A4")  # 210 x 297 mm
pdf.set_auto_page_break(auto=False)
pdf.add_font("Serifa", fname=fonte)
pdf.add_page()
pdf.start_section("Capítulo Um", level=0)
pdf.set_font("Serifa", size=16)
pdf.set_xy(20, 45)
pdf.cell(170, 10, "Capítulo Um")

pdf.set_font("Serifa", size=11)
y = 62
for linhas in PARAGRAFOS:
    for linha in linhas:
        pdf.set_xy(20, y)
        pdf.cell(170, LINHA, linha)
        y += LINHA
    y += PARAGRAFO

saida = Path(__file__).with_name("juncao.pdf")
pdf.output(str(saida))
print(saida)
