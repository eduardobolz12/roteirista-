# SPEC 033 — /traduzir e /humanizar

**Estado:** rascunho testado no ensaio E-009 em 2026-11-12; o aceite vem depois da construção da 026 e da
027, com o roteiro manual

## Intenção
Como Decisor, quero que o roteiro aprovado em português vire o texto da narração em inglês ou francês,
fiel e simples de ouvir para quem não é nativo, e aprová-lo lendo em português, capítulo a capítulo, sem
gastar tokens na aprovação (D-011, D-012, D-029).

## Fronteira
- `.claude/skills/traduzir/SKILL.md`, chamada como `/traduzir <slug> <n> [en|fr]`. Saídas:
  `roteiro-<língua>.md`, `traducao.md` e os termos novos no glossário do livro, aprovados pelo Decisor.
- `.claude/skills/humanizar/SKILL.md`, chamada como `/humanizar <slug> <n> <en|fr>`. Saídas:
  `roteiro-<língua>-humanizado.md`, `humanizacao.md`, a retrotradução (`livro retraduzir`, SPEC 026) e a
  tela (`livro lado-a-lado`, SPEC 027).
- As regras comuns de `docs/prompts/roteiro-regras.md`, que passam a valer para as duas.

## Fora de escopo
- A narração gravada e a montagem do vídeo.

## Aceite (D-019)
1. A tradução passa em `livro glossario --conferir` e em `livro invariantes` (português → tradução) com 0
   alertas. O humanizado passa em `livro invariantes` (tradução → humanizado e português → humanizado) e
   no glossário com 0 alertas; a `livro legibilidade` dele tem menos palavras raras e expressões que a
   tradução, e o que sobrar tem motivo em `humanizacao.md`.
2. `livro retraduzir` e `livro lado-a-lado` rodam no humanizado, e a tela abre sem rede.
3. Roteiro manual do Decisor: ler a tela do tema 1 e decidir cada capítulo (aprovado, com sugestões ou
   refazer); as sugestões aplicadas e registradas em `decisoes.md`.

## Teste do arquiteto (Serpent, tema 1, 2026-11-12, E-009)
- Tradução (E-008, pelas regras da `/traduzir`): 62 parágrafos; glossário de 17 termos e invariantes com 0
  alertas.
- Humanização pela `/humanizar`: 15 parágrafos mexidos; invariantes e glossário com 0 alertas;
  legibilidade de 6 raras e 2 expressões para 1 rara ("conch", que o texto explica) e 0 expressões.
- Retrotradução (protótipo da 026, com o prompt novo): 409 s, nenhuma citação perdida, 0 alertas; na
  leitura, 2 parágrafos com erro de sentido da retrotradução, em capítulos diferentes.
- Tela (protótipo da 027): 62 parágrafos, 0 marcados.
