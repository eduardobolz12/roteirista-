# Gate 004 — epub

## Gate
- Data: 2026-11-02
- Commit: e26ec71e8ca901f603767e8091acb91735fcbe9d
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/004-epub --junitxml=relatorios/004-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_novo_converte_epub.py, CA-2 → test_CA2_mesmos_ids_do_pdf.py, CA-3 → test_CA3_marcas_e_entidades.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/004-epub.md | 93413f4e15f3aceff6880b7bddf96a8fb0671fdc2171c7f291e5370d8c10b99d |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/004-epub/conftest.py | ef4bbdf7ab8280b448f63e218c82c6182a7ff0ca9d590cac85137c6ffff74ba0 |
| tests/acceptance/004-epub/test_CA1_novo_converte_epub.py | 6d93516ae6af7774c9e811f559ee8aa63278cc3db803fa0210b76bb1f943bee5 |
| tests/acceptance/004-epub/test_CA2_mesmos_ids_do_pdf.py | b287dc512f72bc156dd5dbf1c60b2d6fbad9b397dc82b4072e53f3ccb6239b14 |
| tests/acceptance/004-epub/test_CA3_marcas_e_entidades.py | 2a9655143406ff78d5c7375bff3978768985b93c2140463181158df77e57bac5 |
| tests/acceptance/004-epub/fixtures/dois-capitulos.epub | dd184f6aa160356fbed267abde0cf8debccfa93828b016aee7dd94796f71e648 |
| tests/acceptance/004-epub/fixtures/_gerar_epub.py | be99a2977c47da7584ee5c8c362380cc7580094855186e6b99850c9932d87895 |

## Prova
- Data: 2026-11-02
- Commit: c277799f10d54812f4f202d84fac84281e3b8887
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde

## Aceite
- Data: 2026-11-06
- Decisor: pendente
- Evidência: Serpent reconvertido em 2026-11-06 no commit 36a514c: 20 capítulos, 1489 parágrafos; 1.394 dos 1.433 parágrafos do piloto idênticos.
- Roteiro manual: sem aceite: falta um EPUB do Decisor para o roteiro manual. A suíte da fatia segue verde.
