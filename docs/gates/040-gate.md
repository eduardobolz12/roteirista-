# Gate 040 — nova-tentativa

## Gate
- Data: 2026-11-10
- Commit: 7f880f0620731c4fe239f6124eef006845d17b7f
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/040-nova-tentativa --junitxml=relatorios/040-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_falha_passageira.py, CA-2 → test_CA2_desiste.py, CA-3 → test_CA3_cada_janela.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/040-nova-tentativa.md | 906f9565d6c2141df8be2ab487e93aecb6be337170cde69abd1fa80bea3dc11e |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| docs/prompts/indexar-livro.txt | 4b3b75eaa313e92b9230a1808ae4e8b9fdc69129236ae2cada734b3004557a0a |
| docs/prompts/indexar.txt | 59e8e427fbb16b135b50566949a299e10b7af654dc44eb6fa0faabb171833682 |
| docs/prompts/repescar-livro.txt | 9710ec6bebe61e1fc7401ab01aa620e8c39cad757529b3a64c3bdd09e1d0297d |
| docs/prompts/repescar.txt | 1a3c66ede5bcd009ad0601e6a4da06eab50a7bf0db846259d55b70640cbbc8dc |
| tests/acceptance/040-nova-tentativa/conftest.py | af3b04bd702aeeeafe5271564343bbb2a63890790a428b9c7a92e197eebce163 |
| tests/acceptance/040-nova-tentativa/test_CA1_falha_passageira.py | 092d672c85c43f2193deab0ccfcd7025b3f9c14da998d4e0adcad2c4c302eeef |
| tests/acceptance/040-nova-tentativa/test_CA2_desiste.py | 630c6fe1503c2809210abf5684f3b9b0228d1db93972a731ce213e9513ce5da1 |
| tests/acceptance/040-nova-tentativa/test_CA3_cada_janela.py | ff3f96707e48ce6b9e5d2a2d8421fbc2e18046b0d594bdc78f0462324a1e70f3 |
| tests/acceptance/040-nova-tentativa/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/040-nova-tentativa/fixtures/respostas/padrao/01.001.txt | ae7ecf340fc52c839a2a75275859522eaf1c760250e40a512ea31cd8a73be15f |
| tests/acceptance/040-nova-tentativa/fixtures/respostas/padrao/01.002.txt | 0441316a7c50773203238e0095ce81c020441ab134ba03e92c6ebaf9b56ecb7d |
| tests/acceptance/040-nova-tentativa/fixtures/respostas/pouco/01.001.txt | 6a616ac1ec1d6fd772580b4506a55a979e54ab3b3b0eb5ed6bc4875df071513a |
