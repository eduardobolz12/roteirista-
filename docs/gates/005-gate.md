# Gate 005 — ficha-medida

## Gate
- Data: 2026-11-02
- Commit: e26ec71e8ca901f603767e8091acb91735fcbe9d
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/005-ficha-medida --junitxml=relatorios/005-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_lingua_e_conferencia.py, CA-2 → test_CA2_ficha.py, CA-3 → test_CA3_medir.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/005-ficha-medida.md | 3c4564aa00d1e9f3b0ebf2f16e0af483501ed79dc6410762fc5a1377ba439310 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/005-ficha-medida/conftest.py | a77041617da0208d147f16239369ad1689b71353ad7a737ef403a9fb44714d77 |
| tests/acceptance/005-ficha-medida/test_CA1_lingua_e_conferencia.py | 2d4eb58eb32307c9833438f1df49f4edbac3690f359730e3c807581244a6b61b |
| tests/acceptance/005-ficha-medida/test_CA2_ficha.py | 18e1edc34dc311f5276a51d3ef43abbafff29e91a48548c18f9e275a0d3c7eeb |
| tests/acceptance/005-ficha-medida/test_CA3_medir.py | 28f8ad15c14a09c00ad7d63bf9a6f9ac83607c606ab447295324549d5c71a9f3 |
| tests/acceptance/005-ficha-medida/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |

## Prova
- Data: 2026-11-02
- Commit: 79a20a873efdecf7f9d956655c85fab210274c0f
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde
