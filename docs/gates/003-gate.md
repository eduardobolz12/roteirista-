# Gate 003 — notas-bibliografia

## Gate
- Data: 2026-10-23
- Commit: 3bb74d953adf8433578decc243c3b5af65a9625c
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/003-notas-bibliografia --junitxml=relatorios/003-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_nota_tem_id_proprio.py, CA-2 → test_CA2_corpo_sem_nota.py, CA-3 → test_CA3_bibliografia_fora_do_corpo.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/003-notas-bibliografia.md | abe1a4c67c2dc8260effc083ebcdca261a10c120569502ff0ce99a4862a5da35 |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/003-notas-bibliografia/conftest.py | 5129dfb8fbd4dd13c52899733ec143cf67d5d19aed260a8acb34136e7c133126 |
| tests/acceptance/003-notas-bibliografia/test_CA1_nota_tem_id_proprio.py | a2f45190f16352c10a3ddc065aa2cbe824e7529dca823be151aafc99d0519aea |
| tests/acceptance/003-notas-bibliografia/test_CA2_corpo_sem_nota.py | 92209639f3513a794851716410309edf733bdb09396478ad780d8841921a75d8 |
| tests/acceptance/003-notas-bibliografia/test_CA3_bibliografia_fora_do_corpo.py | 0373f1978f724ce88cf03308ebe8ea6e58b42e0efb504228281d950c64f1ab54 |
| tests/acceptance/003-notas-bibliografia/fixtures/notas.pdf | 1d3315353c7b1b553e3819bcc735bbc78f88364d37b7d4614646d1eff16cbcf5 |
| tests/acceptance/003-notas-bibliografia/fixtures/_gerar_pdf.py | 1d75fb075e820705ccd8d81307355609eb9a924ae498471367992a0268f4d4f0 |
