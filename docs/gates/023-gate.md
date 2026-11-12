# Gate 023 — glossario

## Gate
- Data: 2026-11-12
- Commit: b313c12fb01f207c541689960db70e0a995a5eac
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/023-glossario --junitxml=relatorios/023-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_grava_troca_e_lista.py, CA-2 → test_CA2_conferir_sem_alerta.py, CA-3 → test_CA3_conferir_com_alerta_e_lingua_invalida.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/023-glossario.md | f7391037fb8a976e2f5b186b4070a706dbe66f0b1317f0dd7894b0b93ee2d460 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/023-glossario/conftest.py | 98ce3819f12c4659dd91e30650f3955d275dad6ad60c803b072ac2ec00a715ff |
| tests/acceptance/023-glossario/test_CA1_grava_troca_e_lista.py | 6953f66c859d7dd9e933dff9d487d0b6efa61b8a6d1887dadd9c921cc777b75e |
| tests/acceptance/023-glossario/test_CA2_conferir_sem_alerta.py | be2656f3c51a296366a619892e948a118f6c8446b29497a3067584abfffcae24 |
| tests/acceptance/023-glossario/test_CA3_conferir_com_alerta_e_lingua_invalida.py | 896a90359e7b49779a0302a36fb6c32e214ba38be275c665f4fd58a27d18cee5 |
| tests/acceptance/023-glossario/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/023-glossario/fixtures/roteiro-en-glossario.md | 80f5f7fab97d3c53d76bb8bb7973acc0f83ddf330dab4721879d7be0507b1aaa |
| tests/acceptance/023-glossario/fixtures/roteiro-en.md | b5292c0727f9ce0259d5f92b3677f67fae6f122246dc4f2dc8fe593cf6d4bde3 |
| tests/acceptance/023-glossario/fixtures/roteiro-pt.md | d858e7baccc1ccb7f9a9cc71f143a87475f276dbcff21036c29352f8c18194f7 |
