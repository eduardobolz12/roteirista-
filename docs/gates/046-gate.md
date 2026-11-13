# Gate 046 — portugues-aprovado-legivel

## Gate
- Data: 2026-11-13
- Commit: 9fbbe5dbd6d5d5ddc2f064bb1f2c8be5b1a7ded3
- Comando: uv run --with pytest==8.3.4 pytest tests/acceptance/046-portugues-aprovado-legivel --junitxml=relatorios/046-junit.xml
- Junit: tests=3 failures=3 errors=0 skipped=0
- Rastreabilidade: CA-1 → test_CA1_portugues_aprovado_nas_duas_colunas.py, CA-2 → test_CA2_portugues_aprovado_embaixo_da_nota.py, CA-3 → test_CA3_portugues_aprovado_em_tela_estreita.py

| Arquivo | SHA-256 |
|---|---|
| docs/SPECS/046-portugues-aprovado-legivel.md | 87d1ad8480a4d9540c08bfff8c1eb48582298916a2b92837f0d53e6be53e790c |
| pytest.ini | 9095a2aa27c20d25118cc8ab1d727540272083ad2fc1a8f429f06ef0838d2f04 |
| tests/acceptance/046-portugues-aprovado-legivel/conftest.py | 9c5db2446699908eaf8788e4de0c8bc6fa56e438716b51cabdea1d59fcfd5bfa |
| tests/acceptance/046-portugues-aprovado-legivel/test_CA1_portugues_aprovado_nas_duas_colunas.py | d55c99775c52a3265375b348b335a78ed3d94b908daf6cbfe34c28b51ea21592 |
| tests/acceptance/046-portugues-aprovado-legivel/test_CA2_portugues_aprovado_embaixo_da_nota.py | d5eb41a7989387201951acd94edd0e5836587297170c0e2a273b1b5fd74aba31 |
| tests/acceptance/046-portugues-aprovado-legivel/test_CA3_portugues_aprovado_em_tela_estreita.py | 87e442b3961ce334a5b6469030356817f2822b1fc28d3b66242c1643776c4284 |
| tests/acceptance/046-portugues-aprovado-legivel/fixtures/dois-capitulos.pdf | c2f9bfbc214d074ecada1eb02d9123fd8a133ff0152c49760fa8199521b8513b |
| tests/acceptance/046-portugues-aprovado-legivel/fixtures/retro-pt-roteiro-en-humanizado.md | 457a741d6a8241db5743a576fdd2a5c4f36207c148c853f664886421ee22f525 |
| tests/acceptance/046-portugues-aprovado-legivel/fixtures/retro-pt-roteiro-en.md | 770066de6f116c51c7409dc345334b483b260eaecdc05e2f436b147c606a7cc1 |
| tests/acceptance/046-portugues-aprovado-legivel/fixtures/roteiro-en-humanizado.md | 2978da18dd0b38a8dd5d0d7cbacb6973748b03f38b9b60bcd23bf8ec6e61c5bd |
| tests/acceptance/046-portugues-aprovado-legivel/fixtures/roteiro-en.md | 5e80f96a24621452fe8663eb2955c422a0df836a1c8f704169db72df51a51c75 |
| tests/acceptance/046-portugues-aprovado-legivel/fixtures/roteiro-pt.md | e7db7226ef6f1a68b56930c75271d2b447830d28691322221cf736e6259db401 |

## Prova
- Data: 2026-11-13
- Commit: ae83662acd8c92ec39a982ac93b2c05ec2f78c4b
- Hashes: todos iguais ao gate
- Junit: tests=3 failures=0 errors=0 skipped=0
- Suítes anteriores: 001 verde, 002 verde, 003 verde, 004 verde, 005 verde, 006 verde, 007 verde, 008 verde, 009 verde, 010 verde, 011 verde, 014 verde, 015 verde, 016 verde, 017 verde, 018 verde, 020 verde, 021 verde, 022 verde, 023 verde, 024 verde, 025 verde, 026 verde, 027 verde, 034 verde, 035 verde, 036 verde, 037 verde, 038 verde, 039 verde, 040 verde, 041 verde, 042 verde, 043 verde, 044 verde, 045 verde
- Manual: 3 de 3 passos conformes: no navegador, sem rede, em janela larga o "Português aprovado" aberto fica embaixo do inglês e da retrotradução, na largura das duas colunas; em janela de 600 px, na largura toda; o resto da página não muda: 62 parágrafos em 6 capítulos, 0 marcados, página igual ao stdout.
