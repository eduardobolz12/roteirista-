# Gate 014 — hesitacoes

## Gate
- Data: 2026-11-10
- Commit: 438cc92b11dcf072745d5e3029e5079a997efbb7
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/014-hesitacoes --junitxml=relatorios/014-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_fortes.py, CA-2 → test_CA2_todas_e_lingua.py, CA-3 → test_CA3_julgar.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/014-hesitacoes.md | e87354a58b7a569383041fc0d48a8a6388a4177684e54e0dc85cb7bdf790e543 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/014-hesitacoes/conftest.py | ca5f5e795c1ddec9e16503b144c7aef1e5b903c58114d0e4ff470c8d17906e3f |
| tests/acceptance/014-hesitacoes/test_CA1_fortes.py | cded2c208d4d6d83e28ee1eca9bcea485ac971478f18147942f227a5170a9766 |
| tests/acceptance/014-hesitacoes/test_CA2_todas_e_lingua.py | 352e5d687c49808b18b5a28989be234e86f5908a08b72e1a02ce5a4bbbc3285e |
| tests/acceptance/014-hesitacoes/test_CA3_julgar.py | ab1762309105e68d39a413d65271fe3b8aeba98dcb1cf8cf215fcf68bb97caa5 |
| tests/acceptance/014-hesitacoes/fixtures/ingles.pdf | 616be2ae59ac056ff8254b56ac866bf6141df94eaf28cd199912582a8b293d40 |
| tests/acceptance/014-hesitacoes/fixtures/_gerar_pdf.py | 3a5b9347694036ee1873c82372622233d8034ea2f9c47370df3bdcd5fb7baee2 |

## Prova
- Data: 2026-11-11
- Commit: 3363c431c7b0f6e59742b173852ba0284984c01c
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 043 verde, 015 verde

## Aceite
- Data: 2026-11-11
- Decisor: aceito
- Evidência: Serpent reindexado inteiro com `livro indexar-livro serpent --refazer` em 2026-11-11 (retomado depois de queda do Ollama no capítulo 07): 2.035 fichas (antes 1.993), 19 de 1.489 parágrafos sem ficha (antes 57), 63 marcados sem conteúdo.
- Roteiro manual: 65 parágrafos com marca forte, entre eles 06.020, 06.037 e 06.038; 184 com `--todas`.
