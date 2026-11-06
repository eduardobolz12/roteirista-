# Gate 034 — estrutura-do-livro

## Gate
- Data: 2026-11-06
- Commit: 47f646008735c023903c36f2c10610eba049dba4
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/034-estrutura-do-livro --junitxml=relatorios/034-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_capitulos.py, CA-2 → test_CA2_texto_em_um_lugar.py, CA-3 → test_CA3_abertura_de_capitulo.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/034-estrutura-do-livro.md | eaf49c5f66e8ff9404b3c2ca491888e739cb3429ef59fc721d1df2fe91884f3a |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/034-estrutura-do-livro/conftest.py | 95f5c8b3653b6d46c870bfb615a98cf5d21ff45a72721cee05676accbff67d07 |
| tests/acceptance/034-estrutura-do-livro/test_CA1_capitulos.py | 5c2bfc556b65e738204afa6feb80ecb92da60c16da15a8fdc1704b76014e5645 |
| tests/acceptance/034-estrutura-do-livro/test_CA2_texto_em_um_lugar.py | 339ca853fcf7ff0e31011cf48d1f475baf9a58b97cabe0d201dbea23e7e1a0c7 |
| tests/acceptance/034-estrutura-do-livro/test_CA3_abertura_de_capitulo.py | a5f28d71b61aa99c0fd60c8842aebae24accce3ca91cd0395fe26c3f4519fe0f |
| tests/acceptance/034-estrutura-do-livro/fixtures/estrutura.pdf | 55f8d881f376f284383952525e725df391be193a35762952d4bf5abf48ef62e5 |
| tests/acceptance/034-estrutura-do-livro/fixtures/_gerar_pdf.py | 0282f706f662379de647f0240d28daae3301d8717ba6d64432abca48637fe870 |

## Prova
- Data: 2026-11-06
- Commit: 0ed7fcad69ca38508ae97d0f7b3f26f6fe8bcddf
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde
