# Gate 039 — fichas-na-lingua-do-livro

## Gate
- Data: 2026-11-10
- Commit: 7f880f0620731c4fe239f6124eef006845d17b7f
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/039-fichas-na-lingua-do-livro --junitxml=relatorios/039-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_prompt_da_lingua.py, CA-2 → test_CA2_palavra_inteira.py, CA-3 → test_CA3_mesma_frase.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/039-fichas-na-lingua-do-livro.md | 274fcf352b5acf9f792d71099e47db8378fe6293c6222efeca298b0336b053d4 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| docs/prompts/indexar-livro.txt | 4b3b75eaa313e92b9230a1808ae4e8b9fdc69129236ae2cada734b3004557a0a |
| docs/prompts/indexar.txt | 59e8e427fbb16b135b50566949a299e10b7af654dc44eb6fa0faabb171833682 |
| docs/prompts/repescar-livro.txt | 9710ec6bebe61e1fc7401ab01aa620e8c39cad757529b3a64c3bdd09e1d0297d |
| docs/prompts/repescar.txt | 1a3c66ede5bcd009ad0601e6a4da06eab50a7bf0db846259d55b70640cbbc8dc |
| tests/acceptance/039-fichas-na-lingua-do-livro/conftest.py | ea4a269212f65fffec319cc4d1e45d248b217f2424ceed91b75a411201cca8c5 |
| tests/acceptance/039-fichas-na-lingua-do-livro/test_CA1_prompt_da_lingua.py | 47bb07847210c7a54d42794ef3dd0b74b47da7de9fe624e47b41176b54d174ed |
| tests/acceptance/039-fichas-na-lingua-do-livro/test_CA2_palavra_inteira.py | 0ce00499a36736cb6085b8b718ed9fb0f0c148663598467fb259875bdc967c6b |
| tests/acceptance/039-fichas-na-lingua-do-livro/test_CA3_mesma_frase.py | f302a70a41ab78e8c1316e29b337c159f384ce3bb6069d42d4118fa4d93b1563 |
| tests/acceptance/039-fichas-na-lingua-do-livro/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/039-fichas-na-lingua-do-livro/fixtures/respostas/frase/01.001.txt | c18199cf43af317af0d0bcbc00b010e4a985dbab7104f19653f8439710f25ab5 |
| tests/acceptance/039-fichas-na-lingua-do-livro/fixtures/respostas/padrao/01.001.txt | 6a616ac1ec1d6fd772580b4506a55a979e54ab3b3b0eb5ed6bc4875df071513a |
| tests/acceptance/039-fichas-na-lingua-do-livro/fixtures/respostas/padrao/01.002.txt | fbd74214a2775f51f616e1e2a7749074ae9ed425accac0d13bafad32272481fd |
| tests/acceptance/039-fichas-na-lingua-do-livro/fixtures/respostas/palavra/01.001.txt | 8960d80c77c1ba8a0c22534fa54231cfa03308a354e3ccbbda02a026ada10b24 |

## Prova
- Data: 2026-11-10
- Commit: 7761383f78bf3336c86c117853c5a5950afc5696
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde

## Aceite
- Data: 2026-11-10
- Decisor: aceito
- Evidência: Serpent indexado inteiro em inglês em 2026-11-10 (19:49 a 22:06): 1.993 fichas, índice com 32% do tamanho do livro, 57 de 1.489 parágrafos sem ficha, cerca de 12% de fichas recusadas por âncora.
- Roteiro manual: capítulo 06 com o código real: 55 fichas + 2 corrigidas, 8 recusadas, 4 de 4 números do gabarito, nenhuma âncora como pedaço de palavra.
- Observação para o lote 3: a âncora exata recusa fichas certas quando o modelo tira vírgulas e palavras curtas (`make somebody lot money`); concentra-se nos diálogos e nos capítulos 07, 10, 12 e no Epílogo. Regra da SPEC 010, não deste lote.
