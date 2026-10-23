"""Gera tres-paginas.pdf, a fixture da SPEC 002.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 python tests/acceptance/002-pdf-real/fixtures/_gerar_pdf.py

Cada linha é escrita exatamente como na tabela de CA da spec (quebras de linha e hífens manuais).
"""
from pathlib import Path

from fpdf import FPDF

CABECALHO = "O LIVRO DE TESTE"
LINHA = 6  # mm entre linhas de um parágrafo
PARAGRAFO = 12  # mm entre parágrafos

# (marcador do capítulo ou None, número impresso, parágrafos como listas de linhas)
PAGINAS = [
    ("Capítulo Um", "12", [
        ["A família pagou a cons-", "trução do túmulo em duas parcelas."],
        ["Os vizinhos chamavam aquilo de guarda-", "chuva dos mortos, e riam."],
        ["Ninguém levou guarda-chuva ao enterro."],
        ["O padre chegou tarde e"],
    ]),
    (None, "13", [
        ["começou a missa sem esperar a família."],
        ["Depois da missa, o caixão foi levado em silêncio."],
    ]),
    ("Capítulo Dois", "14", [
        ["O cemitério fechou ao anoitecer."],
    ]),
]

pdf = FPDF(format="A5")  # 148 x 210 mm; faixas de 14% = 29,4 mm
pdf.set_auto_page_break(auto=False)
for marcador, numero, paragrafos in PAGINAS:
    pdf.add_page()
    pdf.set_font("Helvetica", size=9)
    pdf.set_xy(15, 8)
    pdf.cell(118, 5, CABECALHO, align="C")
    y = 40
    if marcador:
        pdf.start_section(marcador, level=0)
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.set_xy(15, y)
        pdf.cell(118, 10, marcador)
        y += 10 + PARAGRAFO
    pdf.set_font("Helvetica", size=11)
    for linhas in paragrafos:
        for linha in linhas:
            pdf.set_xy(15, y)
            pdf.cell(118, LINHA, linha)
            y += LINHA
        y += PARAGRAFO - LINHA
    pdf.set_font("Helvetica", size=9)
    pdf.set_xy(15, 195)
    pdf.cell(118, 5, numero, align="C")

saida = Path(__file__).with_name("tres-paginas.pdf")
pdf.output(str(saida))
print(saida)
