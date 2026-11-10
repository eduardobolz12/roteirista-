# Gate 010 — ancoras

## Gate
- Data: 2026-11-10
- Commit: a851cfd46aeef60844e239182df4f8df842857a8
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/010-ancoras --junitxml=relatorios/010-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_ancora_literal.py, CA-2 → test_CA2_vizinho.py, CA-3 → test_CA3_rejeita.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/010-ancoras.md | 03f5c7be4d78a068b58e9cf0c9e0f624a44eb7da0f1ba16766757dbcbd38d5fb |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| docs/prompts/indexar.txt | 59e8e427fbb16b135b50566949a299e10b7af654dc44eb6fa0faabb171833682 |
| docs/prompts/repescar.txt | 1a3c66ede5bcd009ad0601e6a4da06eab50a7bf0db846259d55b70640cbbc8dc |
| tests/acceptance/010-ancoras/conftest.py | 90e4cd166a34d99695717f6c58a4d55ebda305dc0247ae717c857bcd843da71e |
| tests/acceptance/010-ancoras/test_CA1_ancora_literal.py | 441d15ee050ca31c83138f2f88a534f352015f241b462ad179601aa79ae78a68 |
| tests/acceptance/010-ancoras/test_CA2_vizinho.py | 084571bbf6fd65e4f44ad9e1e0dd8fa6c79b47cc23fdc04b35545ad0b86d9bf9 |
| tests/acceptance/010-ancoras/test_CA3_rejeita.py | 2df6b5856f127b3eb0132e126739f9c400c380c395f1cf5b3cc7ab17199eedc9 |
| tests/acceptance/010-ancoras/fixtures/ancoras.pdf | 4ec30fbd93b0426e3839b6b2f9a4ced13014d7661d06000294369dd8e55036bd |
| tests/acceptance/010-ancoras/fixtures/_gerar_pdf.py | b2683f13484832c48dade06297d93c99abb370d0b174d2d57ad8c3d3387a1e17 |
| tests/acceptance/010-ancoras/fixtures/respostas/literal/01.001.txt | 43a0ac272534e9e88e64a16b8251d96741dbf218ba9ce19a673f731efb1fe9ce |
| tests/acceptance/010-ancoras/fixtures/respostas/rejeitar/01.001.txt | 4c60f93811e9a15173a00265c99a87f20812f84fbbe2edc0a7975c826c30ca45 |
| tests/acceptance/010-ancoras/fixtures/respostas/vizinho/01.001.txt | 534cde9c7e6d6f2fc56f3543afdf7b716409530f31dc66e1ba229c4ced57ef90 |
