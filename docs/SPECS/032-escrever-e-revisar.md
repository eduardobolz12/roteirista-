# SPEC 032 — /escrever e /revisar

**Estado:** skills escritas e testadas no Serpent pelo arquiteto em 2026-11-12; aguardando o roteiro
manual e o aceite do Decisor

## Intenção
Como Decisor, quero que cada capítulo saia escrito em português só a partir do briefing aprovado, com as
citações no original conferidas, e que o roteiro inteiro passe por uma revisão de clareza, coerência,
repetição, sustentação, curva e tempo antes de chegar a mim (D-009, D-011, D-028).

## Fronteira
- `.claude/skills/escrever/SKILL.md`, com os guias `capitulo-1.md` a `capitulo-6.md` (os do piloto,
  adaptados ao briefing e à D-028), chamada como `/escrever <slug> <n> <k>`. Saídas: `cap-<k>.md`,
  `cap-<k>-conferencia.md` e, depois do 6, `roteiro-pt.md`.
- `.claude/skills/revisar/SKILL.md`, chamada como `/revisar <slug> <n>`. Saída: `revisao.md`, com as
  correções aplicadas.

## Fora de escopo
- Tradução e humanização (lote 7).

## Aceite (D-019)
1. Cada capítulo passa em `livro contar <slug> cap-<k>.md --briefing briefing-<k>.md` com `0 problemas`
   (SPEC 022); cada apontamento de `livro revisar` (SPEC 042) está decidido na conferência.
2. Roteiro manual do Decisor: ler `livros/serpent/temas/1/roteiro-pt.md` e, por amostra, conferir duas
   citações e duas afirmações na conferência do capítulo.

## Teste do arquiteto (Serpent, tema 1, 2026-11-12)
- 6 capítulos, 1.722 palavras, 11,5 min, 10 citações, 0 problemas; verso de Emily Dickinson (1890)
  conferido no Wikisource, com duas alternativas.
- `livro revisar` na escrita: 18 apontamentos; 10 levaram a correção (atribuição, generalização, cena sem
  fonte, leitura sem marca); os outros caíam sobre o verso, sobre leituras já marcadas ou sobre o que estava
  sustentado em outro capítulo.
- `/revisar`: 15 problemas (1 grave, 10 médios, 4 leves); 13 corrigidos, 2 leves registrados.
