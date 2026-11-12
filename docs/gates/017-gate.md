# Gate 017 — fonte-web

## Gate
- Data: 2026-11-11
- Commit: 10414600deca2c5347f517a5ec60804b35da1a17
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/017-fonte-web --junitxml=relatorios/017-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_artigo.py, CA-2 → test_CA2_wikipedia_e_repetida.py, CA-3 → test_CA3_erros.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/017-fonte-web.md | 4457f5be3d289221ee59622da2d4a74bd8e54796b90e1b0ba707700d8b0fa332 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/017-fonte-web/conftest.py | 6ef0d9116219cb6ccf5524df7fa1288e915abb196b496469420af2dec99ec6db |
| tests/acceptance/017-fonte-web/test_CA1_artigo.py | d439da1588040e651016d250f511c91c88db11d3e8cf7de223c7df63903f7770 |
| tests/acceptance/017-fonte-web/test_CA2_wikipedia_e_repetida.py | b6e2477ad7596ffa0b6b636fb272efeea252f364285a3278794194c0f4acdbe8 |
| tests/acceptance/017-fonte-web/test_CA3_erros.py | 683255d3b6e4b30428a189ec477b7a09b43bb27b2c444915d7a8ddb887513a9d |
| tests/acceptance/017-fonte-web/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/017-fonte-web/fixtures/europepmc/11111111.json | 6334f6e2b91f54dc8452ebdece5a5bacc8b4b8716fe5d8be2aaceedf21ebaf76 |
| tests/acceptance/017-fonte-web/fixtures/europepmc/33333333.json | 8c7e4678c9bd9c219b04a7f70ff7dc89f653a6455522769611fab79993572c52 |
| tests/acceptance/017-fonte-web/fixtures/wikipedia/Test_Book.json | 043231c0410ccb126d95b1d4b076594cc8deae700432a88eec9eca61be557226 |
