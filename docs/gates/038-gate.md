# Gate 038 — livro-antigo

## Gate
- Data: 2026-11-10
- Commit: 7f880f0620731c4fe239f6124eef006845d17b7f
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/038-livro-antigo --junitxml=relatorios/038-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_indexar.py, CA-2 → test_CA2_lacunas.py, CA-3 → test_CA3_nada_se_perde.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/038-livro-antigo.md | da39cb65de3d124b9e07c2a775012b0e5ae60c70c20efac54c695d2c37a1c6da |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| docs/prompts/indexar-livro.txt | 4b3b75eaa313e92b9230a1808ae4e8b9fdc69129236ae2cada734b3004557a0a |
| docs/prompts/indexar.txt | 59e8e427fbb16b135b50566949a299e10b7af654dc44eb6fa0faabb171833682 |
| docs/prompts/repescar-livro.txt | 9710ec6bebe61e1fc7401ab01aa620e8c39cad757529b3a64c3bdd09e1d0297d |
| docs/prompts/repescar.txt | 1a3c66ede5bcd009ad0601e6a4da06eab50a7bf0db846259d55b70640cbbc8dc |
| tests/acceptance/038-livro-antigo/conftest.py | 11818f9d2d76086a61a61210ba116a881c352f9c59342c05592519fe1bc21b14 |
| tests/acceptance/038-livro-antigo/test_CA1_indexar.py | f5f46205bf5c57ee1e0f0f5a740f6938f296bf6f619815703bda545dd6b35b1d |
| tests/acceptance/038-livro-antigo/test_CA2_lacunas.py | 1c2ea69b7e1dec462c4955d4e09ce22d85f47b73af5f9b9dfbb83a94437cd210 |
| tests/acceptance/038-livro-antigo/test_CA3_nada_se_perde.py | 05b9ffcb830cc107c3b09a5bf4c86e6ff461afa8be0208993f91b25e7c4d244d |
| tests/acceptance/038-livro-antigo/fixtures/_gerar_banco.py | 98b5a684861d58f9c714119f0dc9562c0b3f7b5ae2d920e1f65766808e9ea3b2 |
| tests/acceptance/038-livro-antigo/fixtures/antigo/livro.sqlite | 64b75b874211ffa3c4dd4015978d7fb26d063862159c75937a0bb963f4099301 |
| tests/acceptance/038-livro-antigo/fixtures/respostas/padrao/01.001.txt | ae7ecf340fc52c839a2a75275859522eaf1c760250e40a512ea31cd8a73be15f |
| tests/acceptance/038-livro-antigo/fixtures/respostas/padrao/01.002.txt | 0441316a7c50773203238e0095ce81c020441ab134ba03e92c6ebaf9b56ecb7d |
