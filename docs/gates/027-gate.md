# Gate 027 — tela-lado-a-lado

## Gate
- Data: 2026-11-12
- Commit: 08f24806d7c5d0796723c28be46d90cdb19c536d
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/027-tela-lado-a-lado --junitxml=relatorios/027-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_tela_sem_alerta.py, CA-2 → test_CA2_alertas_da_traducao_e_da_retrotraducao.py, CA-3 → test_CA3_capitulo_faltando_e_lingua_desconhecida.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/027-tela-lado-a-lado.md | 0e9e1b9a7f55fa2d2608162f83a8b8cd311b9a28454aed40f0f06f7f7b349040 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/027-tela-lado-a-lado/conftest.py | 82d547586743b07a94e75a910764845cd8967a87aaf7913ccf57e8a0d02ecac8 |
| tests/acceptance/027-tela-lado-a-lado/test_CA1_tela_sem_alerta.py | bac8ce6633cd31359ca444070a0c51e186b4d003bef4b93684c9289a6197e0c3 |
| tests/acceptance/027-tela-lado-a-lado/test_CA2_alertas_da_traducao_e_da_retrotraducao.py | 8274d17e153fd2ff31cddefd289094c3ee3f00c4d0a3fbde3b09ae286a151567 |
| tests/acceptance/027-tela-lado-a-lado/test_CA3_capitulo_faltando_e_lingua_desconhecida.py | d1f6c35c2f7d30db51f6bc9b25019110c8f3189e9b43055773965f49494f84c6 |
| tests/acceptance/027-tela-lado-a-lado/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/027-tela-lado-a-lado/fixtures/notas.md | 721ca08c7813d5a7e529ccd758678758df288b5bdb583f116e966596591a3090 |
| tests/acceptance/027-tela-lado-a-lado/fixtures/retro-pt-curto.md | 77d0528e31650642f89e8c0bb6904cce47b58b060163834cce3953ba8203f3e2 |
| tests/acceptance/027-tela-lado-a-lado/fixtures/retro-pt-roteiro-en-humanizado.md | 457a741d6a8241db5743a576fdd2a5c4f36207c148c853f664886421ee22f525 |
| tests/acceptance/027-tela-lado-a-lado/fixtures/retro-pt-roteiro-en.md | 770066de6f116c51c7409dc345334b483b260eaecdc05e2f436b147c606a7cc1 |
| tests/acceptance/027-tela-lado-a-lado/fixtures/roteiro-en-humanizado.md | 2978da18dd0b38a8dd5d0d7cbacb6973748b03f38b9b60bcd23bf8ec6e61c5bd |
| tests/acceptance/027-tela-lado-a-lado/fixtures/roteiro-en.md | 5e80f96a24621452fe8663eb2955c422a0df836a1c8f704169db72df51a51c75 |
| tests/acceptance/027-tela-lado-a-lado/fixtures/roteiro-pt.md | e7db7226ef6f1a68b56930c75271d2b447830d28691322221cf736e6259db401 |
