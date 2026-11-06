"""Gera recuo-escala.pdf, a fixture da SPEC 036.

Rodar da raiz do repositório:
    uv run --no-project --with fpdf2==2.8.3 --with pypdf==5.4.0 --with matplotlib==3.10.1 python tests/acceptance/036-medida-da-linha/fixtures/_gerar_pdf.py

Mesmo texto da fixture da SPEC 035, desenhado como num PDF comercial: fonte embutida, uma letra por
vez e a página inteira reduzida por uma escala (0,72). A justificação é feita nos espaços entre
palavras. O matplotlib entra só para fornecer uma fonte livre (DejaVu Serif).
"""
from pathlib import Path

import matplotlib
from fpdf import FPDF
from fpdf.enums import PDFResourceType
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

ESCALA = 0.72
K = 1 / ESCALA  # desenha ampliado; a escala da página devolve o tamanho final

LINHA = 6 * K  # mm entre linhas, a mesma em toda a fixture
ESQ = 15 * K  # margem esquerda
LARGURA = 118 * K  # até a margem direita
RECUO = 6 * K  # recuo de primeira linha, de citação e de continuação de glossário
CORPO = 10 * K  # pt
TITULO = 16 * K  # pt

M, R, C = "margem", "recuo", "citacao"

fonte = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSerif.ttf"
pdf = FPDF(format=(148 * K, 210 * K))
pdf.set_auto_page_break(auto=False)
pdf.add_font("Serifa", fname=fonte)


def letra_a_letra(x, y, texto, extra=0.0):
    """Um bloco de texto por linha, com cada letra posicionada por Td; `extra` vai em cada espaço."""
    fonte_atual = pdf.current_font
    pdf._resource_catalog.add(PDFResourceType.FONT, fonte_atual.i, pdf.page)  # o _out não registra
    partes = [f"BT /F{fonte_atual.i} {pdf.font_size_pt:.2f} Tf {x * pdf.k:.2f} {(pdf.h - y) * pdf.k:.2f} Td"]
    for indice, letra in enumerate(texto):
        partes.append(fonte_atual.encode_text(letra))
        avanco = pdf.get_string_width(letra) + (extra if letra == " " else 0)
        if indice + 1 < len(texto):
            partes.append(f"{avanco * pdf.k:.3f} 0 Td")
    partes.append("ET")
    pdf._out(" ".join(partes))


def capitulo(titulo):
    pdf.add_page()
    pdf.start_section(titulo, level=0)
    pdf.set_font("Serifa", size=TITULO)
    letra_a_letra(ESQ, 40 * K, titulo)
    return 56 * K


def linhas(y, itens):
    """Cada item: (posição, texto, cheia). Linha cheia é justificada até o fim da sua medida."""
    pdf.set_font("Serifa", size=CORPO)
    for posicao, texto, cheia in itens:
        x = ESQ if posicao == M else ESQ + RECUO
        fim = ESQ + LARGURA - (RECUO if posicao == C else 0)
        extra = (fim - x - pdf.get_string_width(texto)) / texto.count(" ") if cheia else 0.0
        letra_a_letra(x, y, texto, extra)
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
linhas(40 * K, [
    (M, "Os mais velhos lembravam o enterro e o nome gravado na cruz de", True),
    (M, "madeira do cemitério.", False),
    (R, "O padre guardou o livro dos óbitos numa caixa de folha, no", True),
    (M, "fundo da sacristia, e a chave ficou com o sacristão até o fim daquele", True),
    (M, "inverno longo em que a estrada ficou fechada por causa da neve e", True),
])
pdf.add_page()
linhas(40 * K, [
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

saida = Path(__file__).with_name("recuo-escala.pdf")
bruto = saida.with_suffix(".tmp")
pdf.output(str(bruto))

escrita = PdfWriter(clone_from=PdfReader(bruto))
for pagina in escrita.pages:
    largura, altura = float(pagina.mediabox.width), float(pagina.mediabox.height)
    pagina.add_transformation(Transformation().scale(ESCALA))
    caixa = RectangleObject((0, 0, largura * ESCALA, altura * ESCALA))
    pagina.mediabox = caixa
    pagina.cropbox = caixa
escrita.write(saida)
bruto.unlink()
print(saida)
