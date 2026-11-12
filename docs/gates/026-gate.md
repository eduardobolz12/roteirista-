# Gate 026 — retrotraducao-local

## Gate
- Data: 2026-11-12
- Commit: 08f24806d7c5d0796723c28be46d90cdb19c536d
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/026-retrotraducao-local --junitxml=relatorios/026-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_retraduz_com_contexto_e_glossario.py, CA-2 → test_CA2_citacao_perdida.py, CA-3 → test_CA3_modelo_fora_do_ar_e_linguas.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/026-retrotraducao-local.md | 7cd943c4d4ad36e47381a5a6c181a79753fe1446a4199b5c7205e2b159f16e4b |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/026-retrotraducao-local/conftest.py | b64115ccb87b20774e78be6ac806e75c4e937f0a253a80f40aca0084bf2025f9 |
| tests/acceptance/026-retrotraducao-local/test_CA1_retraduz_com_contexto_e_glossario.py | e34dae8e9adce3d30d5bb7c0d803e6db44b774500f1ca92b6993ea632b922d37 |
| tests/acceptance/026-retrotraducao-local/test_CA2_citacao_perdida.py | b510bb9ffcd69641707dcbb6c22545062ba133101b820f61558e10663ef00239 |
| tests/acceptance/026-retrotraducao-local/test_CA3_modelo_fora_do_ar_e_linguas.py | 87c3256886d16888be6eee30abb5d8ee1a4cc54c81c37f2465a8fc510444ffe2 |
| tests/acceptance/026-retrotraducao-local/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/026-retrotraducao-local/fixtures/notas.md | 721ca08c7813d5a7e529ccd758678758df288b5bdb583f116e966596591a3090 |
| tests/acceptance/026-retrotraducao-local/fixtures/outro-en.md | d5038736d0d7c3b1bcff2e20ded01ffa41eb3e5c9789b2da33c1d70f363032ec |
| tests/acceptance/026-retrotraducao-local/fixtures/respostas.json | a56af65503deb024333aa4eb8d681cde5a6118578bf61306395d4bdc2b25c538 |
| tests/acceptance/026-retrotraducao-local/fixtures/roteiro-en.md | a7ab016a51e19fef9fa9dea8462542c46edc93f070c2d529ce201410ff199a61 |
| tests/acceptance/026-retrotraducao-local/fixtures/roteiro-pt.md | c382e36ad0ec99382e4037426f6609957b96f0f4d8592fade9f56da4cae7ecb7 |
