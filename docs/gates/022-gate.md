# Gate 022 — contar-capitulo

## Gate
- Data: 2026-11-11
- Commit: 6e8960279cca9de736aeda913d4b546b3d681ec7
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/022-contar-capitulo --junitxml=relatorios/022-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_conta_e_confere.py, CA-2 → test_CA2_com_briefing.py, CA-3 → test_CA3_capitulo_certo_e_inexistente.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/022-contar-capitulo.md | a79e39ebe51fb033f54da71724bfa2c350fc4c327482a925deb43a2dcc030210 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/022-contar-capitulo/conftest.py | bcd691ba7463e9e721b974c9e8b8483f0e5b27fadfa65b4f933f990ecc188dbb |
| tests/acceptance/022-contar-capitulo/test_CA1_conta_e_confere.py | 19c95360b83a847a0c8fb01c985ab679e1d990f3869e0ec910ce3b609933a8d4 |
| tests/acceptance/022-contar-capitulo/test_CA2_com_briefing.py | c422acaa9d20534a4958de12049aa74f2cc7f76c210504b43954251e3175f4ae |
| tests/acceptance/022-contar-capitulo/test_CA3_capitulo_certo_e_inexistente.py | 6af64616d6ef50b65daceeb59024d34a3e3980281dba3ecc27c5ad2b43817637 |
| tests/acceptance/022-contar-capitulo/fixtures/briefing.md | 60c9eb018b5516bbd42cc1f1593884daa3542a75d0f129dd52342e5b28ee8c35 |
| tests/acceptance/022-contar-capitulo/fixtures/capitulo-ok.md | 415200eb7dd5c33f498146d219cb44d93c32bd8571e893b596dca299772f2c22 |
| tests/acceptance/022-contar-capitulo/fixtures/capitulo.md | 1b33a2938623c4376b4208a40c6705844a052d8230ea7367055d00acb64e5c53 |
| tests/acceptance/022-contar-capitulo/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
