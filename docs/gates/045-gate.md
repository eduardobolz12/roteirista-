# Gate 045 — correcao-das-conferencias

## Gate
- Data: 2026-11-12
- Commit: 9a04df10a3d65d288567ee1ac809dd08ef672b1d
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/045-correcao-das-conferencias --junitxml=relatorios/045-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_glossario_nos_dois_sentidos_e_i_curvo.py, CA-2 → test_CA2_inicial_e_titulo.py, CA-3 → test_CA3_numeros_pelo_valor.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/045-correcao-das-conferencias.md | d7ad2686da4678aa9d0186c7643fac6d05a522ed134af90082810c7afb886473 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/045-correcao-das-conferencias/conftest.py | 0f9e1eaf0f9fb95f73aa287168baa72a0755d40fe31712c247b3972fd45293b8 |
| tests/acceptance/045-correcao-das-conferencias/test_CA1_glossario_nos_dois_sentidos_e_i_curvo.py | ad20c211fe14b90078fe331bdfdfa6a3f93e3adcb9ee67bb061fcb7d41794168 |
| tests/acceptance/045-correcao-das-conferencias/test_CA2_inicial_e_titulo.py | 13c6487c644dc9247e592bb3d1366598431d289e98c94dee24c995ec99239aa9 |
| tests/acceptance/045-correcao-das-conferencias/test_CA3_numeros_pelo_valor.py | b819bb060a1314a2e60371b4c3d99318dc761a78fcccf583916206ef326ed0cb |
| tests/acceptance/045-correcao-das-conferencias/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/045-correcao-das-conferencias/fixtures/inicial-en-revisado.md | 2af4d34fe2e1904f71fcb4d3811585a80ae2322cf1a7a6b5098b88d21aa9a1e0 |
| tests/acceptance/045-correcao-das-conferencias/fixtures/inicial-en.md | 752b1ff5bc79d04a731364cf029a87d697c1c74c58b90ad2a262df60b44f5227 |
| tests/acceptance/045-correcao-das-conferencias/fixtures/nomes-en.md | 55c83b85c8477e88d3cdee20c3c87f3fc8aa80e63e65c4d61a8fb8c088f42c0f |
| tests/acceptance/045-correcao-das-conferencias/fixtures/nomes-pt.md | 30133f785499f7d146cd7a402037c0479ed865170dd75b1263dbaf629bcc13e4 |
| tests/acceptance/045-correcao-das-conferencias/fixtures/numeros-en.md | 5a220f726d2145fa4f0e658ca0a2aaf4bf99fc81918adfc3b187ebd8f383ee52 |
| tests/acceptance/045-correcao-das-conferencias/fixtures/numeros-fr.md | 025300a24e88de3391453b36f5b53c4eb2446532b75644d95de36a98c7505ba8 |
| tests/acceptance/045-correcao-das-conferencias/fixtures/numeros-pt.md | 68ee3fea1a492156ba8d6260e3ef58f5ab68d28cc043896c4efbb70d59ddba5c |
