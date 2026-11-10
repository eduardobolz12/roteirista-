# Gate 008 — indexar

## Gate
- Data: 2026-11-10
- Commit: a851cfd46aeef60844e239182df4f8df842857a8
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/008-indexar --junitxml=relatorios/008-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_itens_validos.py, CA-2 → test_CA2_rejeicoes.py, CA-3 → test_CA3_regravar_e_erros.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/008-indexar.md | b98b7f95d034e2a5a82353b135d34ed1ca8a7ae3ed85c841b16819c78910d8e2 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| docs/prompts/indexar.txt | 59e8e427fbb16b135b50566949a299e10b7af654dc44eb6fa0faabb171833682 |
| docs/prompts/repescar.txt | 1a3c66ede5bcd009ad0601e6a4da06eab50a7bf0db846259d55b70640cbbc8dc |
| tests/acceptance/008-indexar/conftest.py | 0bd951cc7be1b7f2b3b91aab729852ab7ca684e3aa6839c91ccde08ca59a3fbb |
| tests/acceptance/008-indexar/test_CA1_itens_validos.py | 5f36d434b2cd3f796a1a7d7b77190a5e21c49f1d6bd2b60902640f5dce62d38e |
| tests/acceptance/008-indexar/test_CA2_rejeicoes.py | 5dbf85f0be3be79c4f99547d76f496289cefd927bcf4af4ef73fc93f5e406ddc |
| tests/acceptance/008-indexar/test_CA3_regravar_e_erros.py | cf1b5181c127936a51663e135ceec9e1a037bae332e7b6caecb62511f120e7ad |
| tests/acceptance/008-indexar/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/008-indexar/fixtures/respostas/padrao/01.001.txt | 1d1f537e6424f8f526e18a128e6fb23e112dd40052430a44b76f06ebec40c88b |
| tests/acceptance/008-indexar/fixtures/respostas/padrao/02.001.txt | dee5e377adbd8fa8c8e9fcfc3c7b686c6e0c519ce3ab3ed07c52bf3cb92362c5 |
| tests/acceptance/008-indexar/fixtures/respostas/segunda/01.001.txt | 481803df4ad508ae0e57eb069744bdbcf17d75f90e127f1e1c148bcd385024b3 |

## Prova
- Data: 2026-11-10
- Commit: 8a0fc3466afce00916b67c06c08ec9283138e45d
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 034 verde, 035 verde, 036 verde, 037 verde
