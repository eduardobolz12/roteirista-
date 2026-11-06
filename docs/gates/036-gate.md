# Gate 036 — medida-da-linha

## Gate
- Data: 2026-11-06
- Commit: 15068ec82f7b97e3b12af3d398a05bcbc3b5b7f6
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/036-medida-da-linha --junitxml=relatorios/036-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_recuo_e_virada.py, CA-2 → test_CA2_citacao_e_dialogo.py, CA-3 → test_CA3_glossario.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/036-medida-da-linha.md | 5fa7199de12ead6d398866e264e765a69de6b1c5e027facaf92e47035a0f3c2a |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/036-medida-da-linha/conftest.py | d6b07dc2e8685842339652333986f86f6b6ea90ec118bba672848e8c1dcfb269 |
| tests/acceptance/036-medida-da-linha/test_CA1_recuo_e_virada.py | d175acae0e98760c4db416fc71132b5f7caafcb1f0f16944d1e0e06edfe8e0fd |
| tests/acceptance/036-medida-da-linha/test_CA2_citacao_e_dialogo.py | 0c1193ea6b68faa55892bc310003e320cfd588fe8155dca3d5997ba0b849ed69 |
| tests/acceptance/036-medida-da-linha/test_CA3_glossario.py | 2696c62e4333c3dc75ca4f5139f3f220dfa2deccdeb3f0908feb177cd45c761d |
| tests/acceptance/036-medida-da-linha/fixtures/recuo-escala.pdf | d16af2a79dccc2a12a13a701073c232792493c40d6ec746c4f812a03808b8e28 |
| tests/acceptance/036-medida-da-linha/fixtures/_gerar_pdf.py | 8394860840de8c6a3a8c2ebb343fb9988d32cde96b15c636d5ce1b9a1bc39e47 |
