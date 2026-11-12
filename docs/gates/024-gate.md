# Gate 024 — invariantes

## Gate
- Data: 2026-11-12
- Commit: b313c12fb01f207c541689960db70e0a995a5eac
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/024-invariantes --junitxml=relatorios/024-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_traducao_fiel.py, CA-2 → test_CA2_sem_glossario_e_lingua_desconhecida.py, CA-3 → test_CA3_humanizado_com_mudancas.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/024-invariantes.md | d788d1535cf69c9ed228a883977f67e2d5bf2a43a09a094c78e847cc3a9870f6 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/024-invariantes/conftest.py | 98ce3819f12c4659dd91e30650f3955d275dad6ad60c803b072ac2ec00a715ff |
| tests/acceptance/024-invariantes/test_CA1_traducao_fiel.py | ef3a39cae11d132c66a539d6f79675b4d49f26485ed851c6843f585788ebfe43 |
| tests/acceptance/024-invariantes/test_CA2_sem_glossario_e_lingua_desconhecida.py | ecb2f402d8aec976d3208255abc880ffe81aac630f395aa248590b3ee54282f5 |
| tests/acceptance/024-invariantes/test_CA3_humanizado_com_mudancas.py | 63c90fd6850eb85318142385c4e4528ec00a103d7407ba37142cbcc0af58880c |
| tests/acceptance/024-invariantes/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/024-invariantes/fixtures/notas.md | 0d2b755b22f91d30c9dc9dc00e684588412b2af7c56fb59598bf51bef4c9d8d9 |
| tests/acceptance/024-invariantes/fixtures/roteiro-en-humanizado.md | 84236a89cae1c0dbf5ab75b1f4e6a27d827d2aa512ad2fa8983f2f238a119511 |
| tests/acceptance/024-invariantes/fixtures/roteiro-en.md | b5292c0727f9ce0259d5f92b3677f67fae6f122246dc4f2dc8fe593cf6d4bde3 |
| tests/acceptance/024-invariantes/fixtures/roteiro-pt.md | d858e7baccc1ccb7f9a9cc71f143a87475f276dbcff21036c29352f8c18194f7 |

## Prova
- Data: 2026-11-12
- Commit: 68792c579020c0e87ae05c834401126686b521d5
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 014 verde, 015 verde, 016 verde, 017 verde, 018 verde, 020 verde, 021 verde, 022 verde, 023 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 042 verde, 043 verde, 044 verde
- Manual: 2 de 3 passos conformes. Passo 1 não conforme: 3 alertas falsos de nome novo (4.3 e 5.4 Haitian; 4.6 President), porque o glossário não vale nos dois sentidos quando o termo em português é minúsculo. Passos 2 e 3 acusam o esperado (1.2 números 7 → 6; 2.6 nome sumiu: Isnard; citação em 2.12), com os mesmos 3 falsos. Em arquivos mínimos: números fora de ordem dão alerta com os dois lados iguais; I’m com apóstrofo curvo vira nome; nome depois de inicial no meio do parágrafo (W. B.) não é conferido; número por extenso não bate entre línguas (duzentos contra two hundred), limite da própria spec.

## Aceite
- Data: 2026-11-12
- Decisor: aceito com correção
- Evidência: roteiros manuais com os arquivos reais do Serpent em 2026-11-12, depois da entrega do Kimi.
- Roteiro manual: os passos 2 e 3 acusaram o esperado (`1.2: números: 7 → 6`; `2.6: nome sumiu: Isnard`, com o nome no começo da frase; a citação em 2.12).
- Ressalva: o passo 1 falhou, com 3 alertas falsos de nome novo (4.3 e 5.4 Haitian, 4.6 President): o glossário só valia para nome com maiúscula no português. Em arquivos mínimos, mais três desvios da spec: números fora de ordem davam alerta com os dois lados iguais; `I’m` com apóstrofo curvo virava nome; nome depois de inicial no meio do parágrafo (`W. B.`) não era conferido. E uma lacuna da própria SPEC 024: número por extenso contado palavra por palavra não bate entre línguas (`duzentos` contra `two hundred`). Correção na SPEC 045.
