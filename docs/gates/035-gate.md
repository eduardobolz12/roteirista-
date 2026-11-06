# Gate 035 — paragrafos-por-recuo

## Gate
- Data: 2026-11-06
- Commit: 47f646008735c023903c36f2c10610eba049dba4
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/035-paragrafos-por-recuo --junitxml=relatorios/035-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_recuo_e_virada.py, CA-2 → test_CA2_citacao_e_dialogo.py, CA-3 → test_CA3_glossario.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/035-paragrafos-por-recuo.md | 753f3f1129a2286227a27dbbfeb315b7ab03c7522c88e118c510bcbee82286d8 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/035-paragrafos-por-recuo/conftest.py | 296e1a25e783d89f9bc38e1131b7f2eca85a5a04dcdb0a8ec8cc700daebb1731 |
| tests/acceptance/035-paragrafos-por-recuo/test_CA1_recuo_e_virada.py | 3905d752fd99e4fad0f78d7f5882666f96c76ce38a9ca3372276222b8a1ffd1d |
| tests/acceptance/035-paragrafos-por-recuo/test_CA2_citacao_e_dialogo.py | 954a439cb3d1cb2da30a7888b4054115b2e7328264964cdb649c914ed9954442 |
| tests/acceptance/035-paragrafos-por-recuo/test_CA3_glossario.py | 3725b77af6a1adc5c0b43caa847914db56b758e1d10cd3cb4c5e4ca066353a2e |
| tests/acceptance/035-paragrafos-por-recuo/fixtures/recuo.pdf | f5f05d27ca33c49a05da5cb9012b9002747a669cb5de4454ada08670b3a04f98 |
| tests/acceptance/035-paragrafos-por-recuo/fixtures/_gerar_pdf.py | 29fe6f88c181926cbc41d605898dde6fa8baabbe3f97b2b4455c587a80af68b0 |

## Prova
- Data: 2026-11-06
- Commit: 9a5295ab87b1603fece2d3449a3da624b1fda06d
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 034 verde

## Aceite
- Data: 2026-11-06
- Decisor: aceito
- Evidência: Serpent reconvertido em 2026-11-06 no commit 36a514c: 20 capítulos, 1489 parágrafos; 1.394 dos 1.433 parágrafos do piloto idênticos.
- Roteiro manual: as regras só valeram no livro real depois da fatia 036. Citação em bloco da página 106 é um parágrafo só (`10.087`). O `10.083` do roteiro é o `10.084`: `“Professor.”` é parágrafo próprio aqui.
