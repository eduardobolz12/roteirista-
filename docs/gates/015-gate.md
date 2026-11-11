# Gate 015 — visao-e-temas

## Gate
- Data: 2026-11-10
- Commit: 438cc92b11dcf072745d5e3029e5079a997efbb7
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/015-visao-e-temas --junitxml=relatorios/015-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_visao.py, CA-2 → test_CA2_contar_tema.py, CA-3 → test_CA3_tema_vazio.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/015-visao-e-temas.md | 41c09d66f8402cbc43c2c09b8996e43d0478c875093c720fed538bd86f521962 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/015-visao-e-temas/conftest.py | bf3eb247edba509f09226ab49a5d76c7be45c8ecd6dda68366a94783dcbcc53d |
| tests/acceptance/015-visao-e-temas/test_CA1_visao.py | 07a466281aa63df1acc24ecc1779e9b96b988b23f7c0ef4f5abe1d59c440d514 |
| tests/acceptance/015-visao-e-temas/test_CA2_contar_tema.py | bd9d6404f111f1253cd2f6ecb2bc73ce90dccba419be620d4c1bfa4ef05ff8dd |
| tests/acceptance/015-visao-e-temas/test_CA3_tema_vazio.py | cfdc43103f0bb0c5215e20b3e9ab08a9afd2c3cf02d43aeefb830201663c64ed |
| tests/acceptance/015-visao-e-temas/fixtures/ingles.pdf | cea70bbe64863092f299fb29601ee92bc11c575bd2b63a86e424afcb876c48db |
| tests/acceptance/015-visao-e-temas/fixtures/_gerar_pdf.py | 760d902669bd22b4b3a407e93cb0d32043749fe6bccc3204c06a54a887d61ef4 |
| tests/acceptance/015-visao-e-temas/fixtures/respostas/padrao/01.001.txt | 7c3d5e499bcd195f45455d4300c5867a6f1e3ccdcb7c753209eae8a1622b2ac2 |
| tests/acceptance/015-visao-e-temas/fixtures/respostas/padrao/02.001.txt | 2d4f5ee27534d3139b29de9a927ff2da9cb9c7b1ea0f0621a8f80a8d780ab4f9 |

## Prova
- Data: 2026-11-11
- Commit: f063285b74809e46e0ba8ee7f1a89dcb0ef04be1
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 043 verde

## Aceite
- Data: 2026-11-11
- Decisor: aceito
- Evidência: Serpent reindexado inteiro com `livro indexar-livro serpent --refazer` em 2026-11-11 (retomado depois de queda do Ollama no capítulo 07): 2.035 fichas (antes 1.993), 19 de 1.489 parágrafos sem ficha (antes 57), 63 marcados sem conteúdo.
- Roteiro manual: `visao` com 6.808 caracteres; Bizango (`bizango shanpwel "secret societ"`) 95 fichas em 8 capítulos; `zumbi` nada.
- Ressalva: `The (2)` aparece entre os nomes da visão. Ruído pequeno; fica para uma fatia futura se incomodar.
