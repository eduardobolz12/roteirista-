# Gate 009 — janelas

## Gate
- Data: 2026-11-10
- Commit: a851cfd46aeef60844e239182df4f8df842857a8
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/009-janelas --junitxml=relatorios/009-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_montagem.py, CA-2 → test_CA2_duplicados.py, CA-3 → test_CA3_tudo_ou_nada.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/009-janelas.md | 9793ebdb2122bf2b1ff6b4d5a0311ac2b6ab03d5c745b26792a5bdfbc7367150 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| docs/prompts/indexar.txt | 59e8e427fbb16b135b50566949a299e10b7af654dc44eb6fa0faabb171833682 |
| docs/prompts/repescar.txt | 1a3c66ede5bcd009ad0601e6a4da06eab50a7bf0db846259d55b70640cbbc8dc |
| tests/acceptance/009-janelas/conftest.py | b4f789ed4478073f6b41dce0c1c75ed6f9119663d32b484838d526b1477f6e1e |
| tests/acceptance/009-janelas/test_CA1_montagem.py | 9c6008bf1a1fc6c842c337d4de2fd9ad046aaf74eeade5e02709029b7e2b4b5b |
| tests/acceptance/009-janelas/test_CA2_duplicados.py | 2bba8e049a99dbdb3def3d55221b187cd5679e4a5b96976d9379cc4075538eda |
| tests/acceptance/009-janelas/test_CA3_tudo_ou_nada.py | c907e722e3b446e6a12479be76a5c447925bbcd3107d2d03db5fc1b4f9eb0e90 |
| tests/acceptance/009-janelas/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/009-janelas/fixtures/respostas/falha/01.001.txt | 0d15eb261d661687957b23034fc1192510c450df68916109f25d9ca3e2d70cd1 |
| tests/acceptance/009-janelas/fixtures/respostas/padrao/01.001.txt | 0d15eb261d661687957b23034fc1192510c450df68916109f25d9ca3e2d70cd1 |
| tests/acceptance/009-janelas/fixtures/respostas/padrao/01.002.txt | 65f659b9e3527b55b1ef3f8d79d0d679f9b1d2a8a1484101c2c12ed9b085ee07 |
| tests/acceptance/009-janelas/fixtures/respostas/padrao/01.003.txt | f4c7b76bb48e19a29659b517c0f1ef1aa0eae6a35a3327863cedb568c55664e4 |

## Prova
- Data: 2026-11-10
- Commit: b1f9633f4213dec282455c8903ccbf7adaadac44
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 034 verde, 035 verde, 036 verde, 037 verde, 008 verde
