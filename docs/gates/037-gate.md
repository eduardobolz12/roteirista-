# Gate 037 — juncao-de-linhas

## Gate
- Data: 2026-11-06
- Commit: 15068ec82f7b97e3b12af3d398a05bcbc3b5b7f6
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/037-juncao-de-linhas --junitxml=relatorios/037-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_travessao.py, CA-2 → test_CA2_hifen_fica.py, CA-3 → test_CA3_partes_do_livro.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/037-juncao-de-linhas.md | d5dcc6c70e62fad2ca0bf1457c03a3cc0e3ee7db16a1871ff14cea5598dc7623 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/037-juncao-de-linhas/conftest.py | aff3c0759d7717196d1c1bf287955e62a49d7c5aad5def12af4d8971ef600c7e |
| tests/acceptance/037-juncao-de-linhas/test_CA1_travessao.py | 226875f94511102febc21006e16d1829df99e098bab5b464522c7ed279ac1898 |
| tests/acceptance/037-juncao-de-linhas/test_CA2_hifen_fica.py | 802488a6003148893bf0c18b41034a72b8be799c7980f735f725dd355a478f99 |
| tests/acceptance/037-juncao-de-linhas/test_CA3_partes_do_livro.py | 46bf62bb05250c1f7fd88124aeac86ced7e891c45fa5a5dd98ad1cd035b03a81 |
| tests/acceptance/037-juncao-de-linhas/fixtures/juncao.pdf | 908e2da024766df6ec976c33361893e3173d27389fe10f32abfd531fe65a20e0 |
| tests/acceptance/037-juncao-de-linhas/fixtures/_gerar_pdf.py | dd70191aa2fb6f92dd3b22776c66b2c5857efdec8575ff3185330e90beb7a1af |

## Prova
- Data: 2026-11-06
- Commit: af3fbe631db59983c5e8ed3d7a593d6888491be7
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 034 verde, 035 verde, 036 verde
