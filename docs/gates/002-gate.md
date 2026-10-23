# Gate 002 — pdf-real

## Gate
- Data: 2026-10-23
- Commit: 6abf2be9f896c461052edff364e26d69dfcae4aa
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/002-pdf-real --junitxml=relatorios/002-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_hifenizacao.py, CA-2 → test_CA2_cabecalho_rodape.py, CA-3 → test_CA3_virada_de_pagina.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/002-pdf-real.md | 04c1fab07e2f8c77783b3c0b6e4d1d931e8b728854f1039975cfccfda5dbb1f1 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/002-pdf-real/conftest.py | 0713aaafd70e193a53dc29950349b2fb858df405ffa3496d5659d06960255efe |
| tests/acceptance/002-pdf-real/test_CA1_hifenizacao.py | 693422629954ac00975cb4e82b3a4d7ffc8ec49f544a6e5aa135e1bacc81bd0a |
| tests/acceptance/002-pdf-real/test_CA2_cabecalho_rodape.py | f7d03b10f9f75298886a8224148ce07535525088f7e973f9e04d66495c693d56 |
| tests/acceptance/002-pdf-real/test_CA3_virada_de_pagina.py | b4796de6320b3be78f769fe2bb533dc36487acc85f0ade50f1d6c2f4303802ed |
| tests/acceptance/002-pdf-real/fixtures/tres-paginas.pdf | dcf04a3507e692a16ee9aa88d13564ac295932b7d1c32f24549b6127dfc35eb1 |
| tests/acceptance/002-pdf-real/fixtures/_gerar_pdf.py | 47d84ec4cc8e06167e0a98a620c01cc5d241db5cc0a48d5b500f3b6b0035cafd |

## Prova
- Data: 2026-10-23
- Commit: 4af79ece26ad38d0f38664e7f84e81be6b1dad9d
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde
