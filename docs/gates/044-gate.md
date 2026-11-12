# Gate 044 — colunas-faltando

## Gate
- Data: 2026-11-12
- Commit: 6913d36855d4ffbef3a41dac45e560eea8320a17
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/044-colunas-faltando --junitxml=relatorios/044-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_sem_coluna_trato.py, CA-2 → test_CA2_linhas_curtas.py, CA-3 → test_CA3_so_id_e_briefing_certo.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/044-colunas-faltando.md | d6afddae2e6d56828eaf97914a0b9f2abd4e23891c7690eab5782cba18e3b579 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/044-colunas-faltando/conftest.py | 4307437acbe82bfbba79189bce4aeeecd29cb7ee41d34a70b5a9150ad163e9b7 |
| tests/acceptance/044-colunas-faltando/test_CA1_sem_coluna_trato.py | fef744ed711bd9fce1ec5755bfdfde6f1359bc128113952efdd05b7e341fef39 |
| tests/acceptance/044-colunas-faltando/test_CA2_linhas_curtas.py | bb4221208d9acd90e5340612a26346f11527c996c6e65e5511a928c4a4027cdb |
| tests/acceptance/044-colunas-faltando/test_CA3_so_id_e_briefing_certo.py | 93af4e9cee0231e025b58143cc8f5a49634085337ab3e8c0a05281e93a8f5254 |
| tests/acceptance/044-colunas-faltando/fixtures/briefing-linhas-curtas.md | 4f93b2d366f7f0af1bb35df83a8fc814e52365d4d2dc5bfcce8c5e111923400e |
| tests/acceptance/044-colunas-faltando/fixtures/briefing-ok.md | 02570a253f5620bb994306a7ca39df2c5b877ad2c85c867c2a6bd44eb71f3b1b |
| tests/acceptance/044-colunas-faltando/fixtures/briefing-sem-trato.md | 4a1621d56e37b4e0df1b96b08cdd814bcfc41a8f9b14335f3e0a0c7eed10a8a4 |
| tests/acceptance/044-colunas-faltando/fixtures/briefing-so-id.md | 2001eb0facecc36d3a0cc4698e231d7237bf115a191ef70afe12d979cfe12af6 |
| tests/acceptance/044-colunas-faltando/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |

## Prova
- Data: 2026-11-12
- Commit: 2a7e09d80f5354eb07791acd015bcf9d32557912
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 014 verde, 015 verde, 016 verde, 017 verde, 018 verde, 020 verde, 021 verde, 022 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 042 verde, 043 verde
- Manual: 3 de 3 passos conformes (maquete com 9 "faltam colunas: Trato" e 03.038 acusado; briefing real ok; briefing real sem Trato acusa as linhas 22 a 25).

## Aceite
- Data: 2026-11-12
- Decisor: aceito
- Evidência: roteiros manuais com os arquivos reais do Serpent em 2026-11-12, depois da entrega do Kimi.
- Roteiro manual: a maquete M-001 deu 9 `faltam colunas: Trato` e acusou `03.038` e os outros ids do piloto; o briefing real do Bizango continua `ok` (também com `--temas`); sem a coluna `Trato`, acusa as linhas 22 a 25. Fecha a ressalva do aceite da 020.
