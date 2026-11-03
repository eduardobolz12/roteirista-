# Gate 007 — montar

## Gate
- Data: 2026-11-02
- Commit: e26ec71e8ca901f603767e8091acb91735fcbe9d
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/007-montar --junitxml=relatorios/007-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_ordem_pedida.py, CA-2 → test_CA2_intervalo.py, CA-3 → test_CA3_tudo_ou_nada.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/007-montar.md | a8b748302aed4042caeb2ddcbf18839b97ac76485d70d65ef58303db632a33c6 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/007-montar/conftest.py | 8e69496acbe99c070d7377537f8e423a2f99c21edd376570a910deb9601ed190 |
| tests/acceptance/007-montar/test_CA1_ordem_pedida.py | 54818d0b21947baa2ecc3c90cfe69db8ebf1d302c81c62a7cf95391da04f4d6e |
| tests/acceptance/007-montar/test_CA2_intervalo.py | f4630cb0148b0731b317580693972ec828dc903c91300989e59d24b18cb90272 |
| tests/acceptance/007-montar/test_CA3_tudo_ou_nada.py | 58a2326e028fabd56b930e69f3072b09ea9832a1aa751924e52b700a21d70324 |
| tests/acceptance/007-montar/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |

## Prova
- Data: 2026-11-02
- Commit: 6150930a8d6e731394f9f891a496d3eda826b56b
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde
