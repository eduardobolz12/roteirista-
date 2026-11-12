# Gate 020 — validar-briefing

## Gate
- Data: 2026-11-11
- Commit: 6e8960279cca9de736aeda913d4b546b3d681ec7
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/020-validar-briefing --junitxml=relatorios/020-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_briefing_ok.py, CA-2 → test_CA2_briefing_com_erros.py, CA-3 → test_CA3_briefing_incompleto.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/020-validar-briefing.md | 52e194db37f0197cc3a4773860f4dc28ecd967526a4d4a662b0485c93a870a84 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/020-validar-briefing/conftest.py | bcd691ba7463e9e721b974c9e8b8483f0e5b27fadfa65b4f933f990ecc188dbb |
| tests/acceptance/020-validar-briefing/test_CA1_briefing_ok.py | d12f5c4f851ba6c1cd8e8fdef3afacdc7675abdfb0fcfa990b47143757bca751 |
| tests/acceptance/020-validar-briefing/test_CA2_briefing_com_erros.py | ba87a494ae650463a5003073a603e6e2411aeae76176d2e68979b335ea878888 |
| tests/acceptance/020-validar-briefing/test_CA3_briefing_incompleto.py | b52459021a8fc7bd3795cf936ce4bdf712385c35986eefdce528c61fc16e796c |
| tests/acceptance/020-validar-briefing/fixtures/briefing-erros.md | 680ea25e26221af0894cce781ccde4241ffb3b83e7f43c909dec0ee60b3c7ba0 |
| tests/acceptance/020-validar-briefing/fixtures/briefing-incompleto.md | 43d2fc71c8795de4985bcdb6edd2cffbf52ddd33d239956e582d7547b00baead |
| tests/acceptance/020-validar-briefing/fixtures/briefing-ok.md | 8ca652ca1cb615c8606f44ee0a2ff9721594a97db6bf78fcba4e591fc17caeec |
| tests/acceptance/020-validar-briefing/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/020-validar-briefing/fixtures/europepmc/11111111.json | 6334f6e2b91f54dc8452ebdece5a5bacc8b4b8716fe5d8be2aaceedf21ebaf76 |
