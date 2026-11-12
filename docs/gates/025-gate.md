# Gate 025 — legibilidade

## Gate
- Data: 2026-11-12
- Commit: b313c12fb01f207c541689960db70e0a995a5eac
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/025-legibilidade --junitxml=relatorios/025-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_texto_simples.py, CA-2 → test_CA2_texto_dificil.py, CA-3 → test_CA3_limiar_e_lingua_desconhecida.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/025-legibilidade.md | 27939c64db5c0852f9df936ba4c87ab87800ac42d719e391a67f26f5bbaa021e |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/025-legibilidade/conftest.py | 00fc3561cbea28911d509a44a33ced06eef969432d13e30705a671b958cff23e |
| tests/acceptance/025-legibilidade/test_CA1_texto_simples.py | e337db3878dd79c8c5f203636d68f87bbb0d85e2483f50c90547f67d151cb3c6 |
| tests/acceptance/025-legibilidade/test_CA2_texto_dificil.py | 05cb5ba048de34263b48a035b21e64d1ee31f3fef195bc8f2fe1584ee8c70769 |
| tests/acceptance/025-legibilidade/test_CA3_limiar_e_lingua_desconhecida.py | 603473471d850c2227ae3b06d35fa2d001a63dc0b1c6356e8d84cf8ccb052b26 |
| tests/acceptance/025-legibilidade/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/025-legibilidade/fixtures/notas.md | 0d2b755b22f91d30c9dc9dc00e684588412b2af7c56fb59598bf51bef4c9d8d9 |
| tests/acceptance/025-legibilidade/fixtures/roteiro-en-dificil.md | ed1c2649f36a5736da221ca78f0ec93e0109c7e429cdd79f0c8fca1855170459 |
| tests/acceptance/025-legibilidade/fixtures/roteiro-en.md | b5292c0727f9ce0259d5f92b3677f67fae6f122246dc4f2dc8fe593cf6d4bde3 |
| tests/acceptance/025-legibilidade/fixtures/expressoes/en.txt | 96f2e1fbac8a834a6aea0329b242aff6518c911d6cdf179a3e4404407cb4a6fe |

## Prova
- Data: 2026-11-12
- Commit: 0e21df2b59fbf3fc827361e8d08d9f14d6858da9
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 014 verde, 015 verde, 016 verde, 017 verde, 018 verde, 020 verde, 021 verde, 022 verde, 023 verde, 024 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 042 verde, 043 verde, 044 verde
- Manual: 1 de 3 passos conforme (o 2: some "peasantry" e volta a frase de 27 palavras em 2.14). Passos 1 e 3 não conformes: "seabrook", nome de pessoa depois de "W. B.", contado como palavra rara em 5.3; o resto igual ao E-008.
