# Gate 016 — validar-temas

## Gate
- Data: 2026-11-11
- Commit: 6e8960279cca9de736aeda913d4b546b3d681ec7
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/016-validar-temas --junitxml=relatorios/016-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_temas_ok.py, CA-2 → test_CA2_temas_com_erros.py, CA-3 → test_CA3_incompleto_e_inexistente.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/016-validar-temas.md | 858685a9fa34198a94fca73c6d47c0fd5d5da2ec13a28b6f66aa0cebeb1dc18d |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/016-validar-temas/conftest.py | bcd691ba7463e9e721b974c9e8b8483f0e5b27fadfa65b4f933f990ecc188dbb |
| tests/acceptance/016-validar-temas/test_CA1_temas_ok.py | d1da4dcd33ad198e85ba22cd0f0490202370dbd3543b6aff75d360b55e5085d3 |
| tests/acceptance/016-validar-temas/test_CA2_temas_com_erros.py | d1be00f43ae73082af00c3ebe30bebb581815520c63f213411252f8b23b47e77 |
| tests/acceptance/016-validar-temas/test_CA3_incompleto_e_inexistente.py | 232e5e0fe48b600bb26eaea7d3d61f23a97e8d06b340f8e1b690f96631a41ee0 |
| tests/acceptance/016-validar-temas/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/016-validar-temas/fixtures/temas-erros.md | 7b478c17f6989f1e19e6fcf6b89a97ce783538ae67a71184d1859f99a6ed0f00 |
| tests/acceptance/016-validar-temas/fixtures/temas-incompleto.md | 415c79241ae3d8668fe48ce291659a532989f99b1555b372d1fc8381b98773ec |
| tests/acceptance/016-validar-temas/fixtures/temas-ok.md | e595ee273edba94ae93ba77c6e96114eb9c9b71afadbd912240c0db63e509015 |

## Prova
- Data: 2026-11-12
- Commit: cba058f62b25b8db685a3eb05b28de14f63a46b7
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 014 verde, 015 verde, 017 verde, 018 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 042 verde, 043 verde

## Aceite
- Data: 2026-11-12
- Decisor: aceito
- Evidência: roteiros manuais com os arquivos reais do Serpent em 2026-11-12, depois da entrega do Kimi.
- Roteiro manual: a maquete M-003 deu 49 problemas, entre eles `03.038` inexistente; a sugestão real (Bizango e Narcisse) deu `ok: 2 temas, 2 assuntos`; sem a rachadura do tema 1, `tema 1: falta a rachadura com id`.
