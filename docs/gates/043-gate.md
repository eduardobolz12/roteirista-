# Gate 043 — indexar-livro

## Gate
- Data: 2026-11-10
- Commit: 438cc92b11dcf072745d5e3029e5079a997efbb7
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/043-indexar-livro --junitxml=relatorios/043-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_livro_inteiro.py, CA-2 → test_CA2_retoma.py, CA-3 → test_CA3_marcas.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/043-indexar-livro.md | 4ce59c45c27c28bd6569a627532552837bbfd210bda58c22730964773b05b128 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/043-indexar-livro/conftest.py | 2cddbd1de99963d435e5122faebdfd6b8fc746b5ea60e45cb6e77bde5e6d8b80 |
| tests/acceptance/043-indexar-livro/test_CA1_livro_inteiro.py | 4b6445b9a1b721313ff842485ea78e19472f1b1d8ad6b6cd40410193903bdb2a |
| tests/acceptance/043-indexar-livro/test_CA2_retoma.py | 30714eac300de58303604bca265a06015740dc8e460762a4cb9952ee07b7097d |
| tests/acceptance/043-indexar-livro/test_CA3_marcas.py | aa298e652b981f258fee0e4d9cc814d5a5a7e96ab078a65d359fff76627d11ea |
| tests/acceptance/043-indexar-livro/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/043-indexar-livro/fixtures/respostas/padrao/01.001.txt | ae7ecf340fc52c839a2a75275859522eaf1c760250e40a512ea31cd8a73be15f |
| tests/acceptance/043-indexar-livro/fixtures/respostas/padrao/02.001.txt | 6be089a3cdb58006ed5c344d601d3ecc438ba1b5355ac57ed016311538bd252e |

## Prova
- Data: 2026-11-11
- Commit: ec58f6236db6f105636bbc6468cee482eba53da2
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde
