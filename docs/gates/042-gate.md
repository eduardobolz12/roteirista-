# Gate 042 — revisao-do-sentido

## Gate
- Data: 2026-11-11
- Commit: 10414600deca2c5347f517a5ec60804b35da1a17
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/042-revisao-do-sentido --junitxml=relatorios/042-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_aponta_e_descarta.py, CA-2 → test_CA2_modelo_de_reserva.py, CA-3 → test_CA3_nenhum_modelo.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/042-revisao-do-sentido.md | 526309f1747e065f3e557f34ac3c0f5a2559f5874ed1a5335c6c2be6f7949049 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| docs/prompts/revisar.txt | 919d949e4ca98839c72576875212d0cc8a7476b656efb8201d37ca7638f9277c |
| tests/acceptance/042-revisao-do-sentido/conftest.py | 6ef0d9116219cb6ccf5524df7fa1288e915abb196b496469420af2dec99ec6db |
| tests/acceptance/042-revisao-do-sentido/test_CA1_aponta_e_descarta.py | 9aa937354a135bdd988ca67c1c508e039c0f1f02b5dba4cc3aa65c77f8e9e090 |
| tests/acceptance/042-revisao-do-sentido/test_CA2_modelo_de_reserva.py | 9985dc2b9557c9953354d8c1be780d24ae419498c27aa5bcac75d40ab3a38b07 |
| tests/acceptance/042-revisao-do-sentido/test_CA3_nenhum_modelo.py | 8d6e82bfea191e1f8b80e13664380d16081e3e2e82b4a973c2e3f34bb4a94f74 |
| tests/acceptance/042-revisao-do-sentido/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/042-revisao-do-sentido/fixtures/texto.md | 381d73324d30e68ccdde5bccb39ac9738c3c35a99440a9256d58d43f4a8d6a0a |

## Prova
- Data: 2026-11-11
- Commit: 2679a1968fe76d92eb5c826f8f1b0ef9827967e4
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 014 verde, 015 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 043 verde, 017 verde
