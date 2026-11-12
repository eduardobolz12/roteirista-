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
