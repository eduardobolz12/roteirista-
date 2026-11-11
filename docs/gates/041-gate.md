# Gate 041 — ancora-pelas-palavras

## Gate
- Data: 2026-11-10
- Commit: 438cc92b11dcf072745d5e3029e5079a997efbb7
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/041-ancora-pelas-palavras --junitxml=relatorios/041-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_palavras_proximas.py, CA-2 → test_CA2_longe_ou_fora_de_ordem.py, CA-3 → test_CA3_vizinho_e_repescagem.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/041-ancora-pelas-palavras.md | 7cd53b585f8f3faead43e954a5d606350f9c06c528e323371361797d22bb8d45 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/041-ancora-pelas-palavras/conftest.py | 2082aa17661a3dd202104295d099696661f7f76eb96e57ad39b3d41ece1f2365 |
| tests/acceptance/041-ancora-pelas-palavras/test_CA1_palavras_proximas.py | be1c5e1ec190a90e0865534dd9f25d81a57f6857df1695d3db8550dac0e73e44 |
| tests/acceptance/041-ancora-pelas-palavras/test_CA2_longe_ou_fora_de_ordem.py | 7115ea02430c6ccaebdfbf6cd422e2df93fcb83b719ae214b96d5c1b68636dc0 |
| tests/acceptance/041-ancora-pelas-palavras/test_CA3_vizinho_e_repescagem.py | e0f30fb4e93baadd619acf60ce8753cf4513e6353848de27d8bb2313bcef9e89 |
| tests/acceptance/041-ancora-pelas-palavras/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/041-ancora-pelas-palavras/fixtures/respostas/longe/01.001.txt | 241bcd9174992132e0fe9a2e9bb3db16be95495748e8b9dba2c3861ad874e3f8 |
| tests/acceptance/041-ancora-pelas-palavras/fixtures/respostas/perto/01.001.txt | c9b15e7c1f14080f79ca46d825cce5e8b968299c74346922162d3f2b29277085 |
| tests/acceptance/041-ancora-pelas-palavras/fixtures/respostas/vizinho/01.001.txt | 55acb955df3de6840ce8e2c1d0f352148bc8143266619ce329683ad7c19dd502 |
| tests/acceptance/041-ancora-pelas-palavras/fixtures/respostas/vizinho/01.003.txt | d2d7c199d52dd4db644aca044124fa3aebd983895c0fd5d4b2668f3b64a88f8f |

## Prova
- Data: 2026-11-11
- Commit: 6cb110a705b47af2be59526c199e1fe196185339
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde
