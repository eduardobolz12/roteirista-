# SPEC 031 — /briefing

**Estado:** skill escrita e testada no Serpent pelo arquiteto em 2026-11-12; aguardando o roteiro manual
e o aceite do Decisor

## Intenção
Como Decisor, quero receber o plano do vídeo e os 6 briefings de um tema já conferidos (ids que existem,
citações iguais ao livro, casas respeitadas, uma só pergunta sem resposta), para aprovar o conteúdo antes
de qualquer escrita (D-009, D-010, D-018).

## Fronteira
A skill `.claude/skills/briefing/SKILL.md`, chamada como `/briefing <slug> <n> [minutos]`. Saídas:
`plano.md` e `briefing-1.md` a `briefing-6.md` em `livros/<slug>/temas/<n>/`.

## Fora de escopo
- Escrever o roteiro.

## Aceite (D-019)
1. Os seis passam em `livro validar-briefing <slug> <briefing> --temas livros/<slug>/temas.md`
   (SPECs 020, 021 e 044), sem aviso de casa não explicado.
2. Roteiro manual do Decisor: ler `plano.md` e os seis briefings do tema 1 do Serpent e marcar "Sua
   decisão" em cada um.

## Teste do arquiteto (Serpent, tema 1, 2026-11-12)
- Os seis `ok` na primeira rodada, sem aviso de casa; conferência cruzada limpa (uma pergunta sem
  resposta, convite só no 4, âncora só no 1 e no 6, nenhum id em duas funções, 1.500 palavras).
- Na escrita e na revisão, três ids entraram nos briefings (16.096-16.102, 14.048, 15.087) e um dado da
  web (W11.009), para sustentar frases que o roteiro precisava; todos revalidados.
- Ajustes da skill: fala cortada pelo narrador do livro leva `...`; o cap. 6 pode trazer o elemento que
  divide.
