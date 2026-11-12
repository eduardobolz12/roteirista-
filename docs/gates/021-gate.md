# Gate 021 — casa-dos-assuntos

## Gate
- Data: 2026-11-11
- Commit: 6e8960279cca9de736aeda913d4b546b3d681ec7
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/021-casa-dos-assuntos --junitxml=relatorios/021-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_aviso_de_casa.py, CA-2 → test_CA2_sem_aviso.py, CA-3 → test_CA3_tema_inexistente_e_temas_com_erro.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/021-casa-dos-assuntos.md | 2431e7bd4c81328714a219b3b5cfbe21a12e248220d3b095a3b78dc5751cad64 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/021-casa-dos-assuntos/conftest.py | bcd691ba7463e9e721b974c9e8b8483f0e5b27fadfa65b4f933f990ecc188dbb |
| tests/acceptance/021-casa-dos-assuntos/test_CA1_aviso_de_casa.py | 0457ba30daea2af2c79809ce81648542e0d5aa290a0621ff2aaf972bbdafe04b |
| tests/acceptance/021-casa-dos-assuntos/test_CA2_sem_aviso.py | edc58b6610531e035455ec5837467b3043465f7737e582f4399bc962992b5017 |
| tests/acceptance/021-casa-dos-assuntos/test_CA3_tema_inexistente_e_temas_com_erro.py | 97dc11b20e24e98d71e1323bb0716a46644c531504de2c03a220ca8941711240 |
| tests/acceptance/021-casa-dos-assuntos/fixtures/briefing-tema1.md | 49c6cd9feff276dcf877fccd63283a4714626904f0c69f54fd9316319f3320d8 |
| tests/acceptance/021-casa-dos-assuntos/fixtures/briefing-tema2.md | 353feaaa3031b51826ce4c86ec15d6127cbe70de9ebd326378e581f3cdfc0f26 |
| tests/acceptance/021-casa-dos-assuntos/fixtures/briefing-tema3.md | 822040eb1ba022f5d265569b6c1982b4ee9bedecd8528e594f839e22d77cdd42 |
| tests/acceptance/021-casa-dos-assuntos/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/021-casa-dos-assuntos/fixtures/temas-erros.md | 92281094ce71363aea2ad449ecbccf18736afe52adaae154e0872de4e43b7b99 |
| tests/acceptance/021-casa-dos-assuntos/fixtures/temas-ok.md | e595ee273edba94ae93ba77c6e96114eb9c9b71afadbd912240c0db63e509015 |

## Prova
- Data: 2026-11-12
- Commit: 6da73d49049a3625208753be7632c864f48bc0b2
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 014 verde, 015 verde, 017 verde, 018 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 042 verde, 043 verde, 016 verde, 020 verde

## Aceite
- Data: 2026-11-12
- Decisor: aceito
- Evidência: roteiros manuais com os arquivos reais do Serpent em 2026-11-12, depois da entrega do Kimi.
- Roteiro manual: com `--temas`, o briefing real não avisa; com `Tema: 2`, quatro avisos nas passagens da sessão (casa do tema 1); com as passagens em `mencionar`, os avisos somem.
