# Gate 001 — walking-skeleton

## Gate
- Data: 2026-10-23
- Commit: f509ec9aa73df35f468d20d2173bb0753f58597e
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/001-walking-skeleton --junitxml=relatorios/001-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_novo_converte_pdf.py, CA-2 → test_CA2_trecho_devolve_literal.py, CA-3 → test_CA3_id_inexistente.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/001-walking-skeleton.md | 2ce06259b1c3e339605e9abd731d63ac4ce7923af48eb74835380a73d848e3fa |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/001-walking-skeleton/conftest.py | b24fd44ea8109d89248bc1bb33400317483f540a88a478f7a521c793790cd6c5 |
| tests/acceptance/001-walking-skeleton/test_CA1_novo_converte_pdf.py | 55b3c7ea8f1c5b374f95c7a07906399b318b5b52527ae156bf0ca3ab08bef8b2 |
| tests/acceptance/001-walking-skeleton/test_CA2_trecho_devolve_literal.py | ebecdc2e3410cb81195af51479164574c58f9bc4774700bac35ffdb7b749a138 |
| tests/acceptance/001-walking-skeleton/test_CA3_id_inexistente.py | 1d134b85a16827180e2a0b32d80706db265c75661f9512868732437b48bb1f0f |
| tests/acceptance/001-walking-skeleton/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/001-walking-skeleton/fixtures/_gerar_pdf.py | f65f1348af7834ea5722add1c53151aab1646a7042fef55c6cfa562d30fb6f1c |

## Prova
- Data: 2026-10-23
- Commit: d29c881b2cd2800fc9dc12dd1453225418afcfc8
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: nenhuma (001 é a primeira)
