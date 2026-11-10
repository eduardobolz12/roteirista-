# Gate 011 — lacunas

## Gate
- Data: 2026-11-10
- Commit: a851cfd46aeef60844e239182df4f8df842857a8
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/011-lacunas --junitxml=relatorios/011-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_lacunas.py, CA-2 → test_CA2_repescar.py, CA-3 → test_CA3_regravar.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/011-lacunas.md | 88c2ae540b7b34d4edc93c80be334ba7997c5d5b64832fd86593bdaf76f5be8d |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| docs/prompts/indexar.txt | 59e8e427fbb16b135b50566949a299e10b7af654dc44eb6fa0faabb171833682 |
| docs/prompts/repescar.txt | 1a3c66ede5bcd009ad0601e6a4da06eab50a7bf0db846259d55b70640cbbc8dc |
| tests/acceptance/011-lacunas/conftest.py | 28e9368807f7f41ed5f2bf48b773f1f3221ff3bd62fa9652c0ccbd1bb8eeb25e |
| tests/acceptance/011-lacunas/test_CA1_lacunas.py | d4187412e9edf5a9c666a2f17fb3c7f7a82753aece82b568d0d3ef57f891ae1f |
| tests/acceptance/011-lacunas/test_CA2_repescar.py | c953d5eaff2d21e900a8bbfc40f1204df4df4c629945fca07050367bec556276 |
| tests/acceptance/011-lacunas/test_CA3_regravar.py | 982dc281992958ae8588e225be180a8bce710e66c9477d19dfd7c10fc5878327 |
| tests/acceptance/011-lacunas/fixtures/lacunas.pdf | 8387ed07d407a9d23c95467d575fd63b5663deb6475d73c9b6cf2c3689fbba2d |
| tests/acceptance/011-lacunas/fixtures/_gerar_pdf.py | 7bdb4933867ac75e772de1f0cfbf745acb836486a700b5f574792dac94c686ab |
| tests/acceptance/011-lacunas/fixtures/respostas/padrao/01.001.txt | 5aab4295ea14878b44a6265759825efca7ff744be1596d6944f0dcafaf5ca541 |
| tests/acceptance/011-lacunas/fixtures/respostas/padrao/01.003.txt | bd86c394fa5cae232be561e2365985abdfc8e063f747314085ba249e1dac595f |
| tests/acceptance/011-lacunas/fixtures/respostas/tudo/01.001.txt | c5474b5f76b0305f543346783f4b11243cc141131a91ee556413de637f17b737 |

## Prova
- Data: 2026-11-10
- Commit: 0348dd922147786551942badc38c94b600c65f86
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 034 verde, 035 verde, 036 verde, 037 verde, 008 verde, 009 verde, 010 verde

## Aceite
- Data: 2026-11-10
- Decisor: aceito, com ressalvas
- Evidência: Serpent reconvertido; capítulo 06 indexado com o qwen3:14b real em 2026-11-10 pelo Decisor e pelo arquiteto, com resultado idêntico nas duas rodadas: 57 itens gravados, 4 corrigidos, 3 rejeitados; 2 lacunas, fechadas pela repescagem.
- Roteiro manual: lacunas 06.019 e 06.020 fechadas pela repescagem em 18 s; o ornamento 06.016 não conta como lacuna.
- Ressalvas: o índice em português perde números e detalhes (1 de 4 números do gabarito) e o tipo do item não é confiável, sobretudo `contradicao`. Em teste: índice na língua do livro (E-003).
