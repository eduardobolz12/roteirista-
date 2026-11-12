# Gate 018 — pesquisa-gratuita

## Gate
- Data: 2026-11-11
- Commit: 10414600deca2c5347f517a5ec60804b35da1a17
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/018-pesquisa-gratuita --junitxml=relatorios/018-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_achados_conferidos.py, CA-2 → test_CA2_wiki_e_fonte_existente.py, CA-3 → test_CA3_busca_vazia_e_fora_do_ar.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/018-pesquisa-gratuita.md | 6ba1fa8593bb256148018f97eda24fbc21dd780ebc5cdf7eadc9820f7140cba1 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| docs/prompts/pesquisar.txt | 1cf8514b4f182b01ff61a7aa26b0dd70eeaf7ace468a38bfa7ce6c51ab9ffcfe |
| tests/acceptance/018-pesquisa-gratuita/conftest.py | 6ef0d9116219cb6ccf5524df7fa1288e915abb196b496469420af2dec99ec6db |
| tests/acceptance/018-pesquisa-gratuita/test_CA1_achados_conferidos.py | 9f87eace119a06d440128ee1a9dc12c40e800ff5c2604237ab1debb5a21f588f |
| tests/acceptance/018-pesquisa-gratuita/test_CA2_wiki_e_fonte_existente.py | 1c71446cda6ae8d4c52da1e9c95a82b3413d8bdbcab22bb2b1a9e82f9f96c6c7 |
| tests/acceptance/018-pesquisa-gratuita/test_CA3_busca_vazia_e_fora_do_ar.py | 9d8f5e8e778640f80d53fea2c2de360ea8d78a1b856ab6815d620a0cab18508c |
| tests/acceptance/018-pesquisa-gratuita/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/018-pesquisa-gratuita/fixtures/europepmc/11111111.json | 6334f6e2b91f54dc8452ebdece5a5bacc8b4b8716fe5d8be2aaceedf21ebaf76 |
| tests/acceptance/018-pesquisa-gratuita/fixtures/europepmc/33333333.json | 8c7e4678c9bd9c219b04a7f70ff7dc89f653a6455522769611fab79993572c52 |
| tests/acceptance/018-pesquisa-gratuita/fixtures/europepmc/busca/awareness_anaesthesia.json | d2a50db0cde84ee07b542271e3a7d5a98b87d993266f7b08ad814fedcb4d9f09 |
| tests/acceptance/018-pesquisa-gratuita/fixtures/wikipedia/Test_Book.json | 043231c0410ccb126d95b1d4b076594cc8deae700432a88eec9eca61be557226 |
| tests/acceptance/018-pesquisa-gratuita/fixtures/wikipedia/busca/Test_Book.json | 52cdf9e739267a113a800315f0277b74bc79c9823a11cb8c9263396872d662b0 |

## Prova
- Data: 2026-11-11
- Commit: 68cbd9e26551ccc610a6b8cd25bcca7103e36dd4
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 014 verde, 015 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 043 verde, 017 verde, 042 verde

## Aceite
- Data: 2026-11-11
- Decisor: aceito
- Evidência: roteiros manuais nas APIs reais e no 9Router em 2026-11-11, depois da entrega do Kimi.
- Roteiro manual: NAP5 com 1 achado conferido (`~1:8200`); o livro pela Wikipédia com 3 achados conferidos (1985, best-seller, críticas) e 1 recusado com razão (citação certa, parágrafo errado); citações conferidas com `livro trecho`.
- Ressalva: a busca do Europe PMC traz às vezes artigos fora do assunto (NAP7); viram fonte, não geram achado.
