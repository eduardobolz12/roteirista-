"""Gera dois-capitulos.epub, a fixture da SPEC 004.

Rodar da raiz do repositório:
    uv run --no-project python tests/acceptance/004-epub/fixtures/_gerar_epub.py

EPUB 3 mínimo, montado com zipfile: capa sem título + dois capítulos com <h1>.
"""
import zipfile
from pathlib import Path

CONTAINER = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""

OPF = """<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="id">roteirista-fixture-004</dc:identifier>
    <dc:title>Livro de teste</dc:title>
    <dc:language>pt</dc:language>
    <meta property="dcterms:modified">2026-11-02T00:00:00Z</meta>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="capa" href="capa.xhtml" media-type="application/xhtml+xml"/>
    <item id="cap1" href="cap1.xhtml" media-type="application/xhtml+xml"/>
    <item id="cap2" href="cap2.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine>
    <itemref idref="capa"/>
    <itemref idref="cap1"/>
    <itemref idref="cap2"/>
  </spine>
</package>
"""


def xhtml(corpo: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Livro de teste</title></head>
<body>
{corpo}
</body>
</html>
"""


NAV = xhtml("""<nav epub:type="toc"><ol>
<li><a href="cap1.xhtml">Capítulo Um</a></li>
<li><a href="cap2.xhtml">Capítulo Dois</a></li>
</ol></nav>""")

CAPA = xhtml("""<div class="capa"><p class="autor">Livro de teste</p></div>""")

CAP1 = xhtml("""<h1>Capítulo Um</h1>
<p>O homem parou diante do túmulo e leu o próprio nome gravado no cimento.</p>
<p>A irmã reconheceu o apelido de infância antes de reconhecer o rosto.</p>
<p>Naquela tarde, ninguém na aldeia quis falar sobre o enterro.</p>""")

CAP2 = xhtml("""<h1>Capítulo Dois</h1>
<p>O médico assinou a certidão <em>às três horas</em> da tarde &amp; saiu.</p>
<p>Ninguém soube dizer à família, naquela manhã de maio, quem tinha
aberto a cova durante a noite.</p>""")

saida = Path(__file__).with_name("dois-capitulos.epub")
with zipfile.ZipFile(saida, "w") as z:
    # o mimetype vem primeiro e sem compressão (regra do EPUB)
    z.writestr(zipfile.ZipInfo("mimetype", date_time=(2026, 11, 2, 0, 0, 0)), "application/epub+zip",
               compress_type=zipfile.ZIP_STORED)
    for nome, texto in [("META-INF/container.xml", CONTAINER), ("OEBPS/content.opf", OPF),
                        ("OEBPS/nav.xhtml", NAV), ("OEBPS/capa.xhtml", CAPA),
                        ("OEBPS/cap1.xhtml", CAP1), ("OEBPS/cap2.xhtml", CAP2)]:
        info = zipfile.ZipInfo(nome, date_time=(2026, 11, 2, 0, 0, 0))
        z.writestr(info, texto.encode("utf-8"), compress_type=zipfile.ZIP_DEFLATED)
print(saida)
