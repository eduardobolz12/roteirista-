# Gate 006 — conferir-buscar

## Gate
- Data: 2026-11-02
- Commit: dd0fc60431f12e74c6f35843be022d383c3909e6
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/006-conferir-buscar --junitxml=relatorios/006-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_conferir_existe.py, CA-2 → test_CA2_conferir_nao_existe.py, CA-3 → test_CA3_buscar.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/006-conferir-buscar.md | cd5c75ce8994eb3a371371c58e272766df66ec060ac4c57b307c76ebe12bf00e |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/006-conferir-buscar/conftest.py | a2272180d83684687a8a1d6cf1538d087e209f0c21b5d7faae7feacf5187c18f |
| tests/acceptance/006-conferir-buscar/test_CA1_conferir_existe.py | c38647ef228b129b987323df16d52bcc67b6730c8d960c992a68877102a66253 |
| tests/acceptance/006-conferir-buscar/test_CA2_conferir_nao_existe.py | db8acf4223f06a2051a53fc2637883d1bfd4b53702af2eaa3484c2cef560f428 |
| tests/acceptance/006-conferir-buscar/test_CA3_buscar.py | a5b54d8ddf1e57d4ca01d29cb401b09f8c3adbd78c7cd657d4d797b2e4c558ab |
| tests/acceptance/006-conferir-buscar/fixtures/nota-no-meio.pdf | c8b3658fd1d3c5fee6dae09b2857283fccb4bdfcb330de21caec701f26f2f59e |
| tests/acceptance/006-conferir-buscar/fixtures/_gerar_pdf.py | df9650c8b2533bd2150cb8e801bb3fbe271393d77d428a7fff734cf2e236b8d4 |

## Prova
- Data: 2026-11-02
- Commit: 88d589feac2ff05d6a8ed3363368436db7a95e1a
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 007 verde

## Aceite
- Data: 2026-11-06
- Decisor: aceito
- Evidência: Serpent reconvertido em 2026-11-06 no commit 36a514c: 20 capítulos, 1489 parágrafos; 1.394 dos 1.433 parágrafos do piloto idênticos.
- Roteiro manual: `conferir` dá `EXISTE 07.040` para a citação exata e `NÃO EXISTE` com uma letra trocada; `buscar "Narcisse"` lista os ids em vários capítulos.
