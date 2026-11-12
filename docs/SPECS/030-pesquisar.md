# SPEC 030 — /pesquisar

**Estado:** skill escrita e testada no Serpent pelo arquiteto em 2026-11-12; aguardando o roteiro manual
e o aceite do Decisor

## Intenção
Como Decisor, quero que a pesquisa de fora do livro de cada tema escolhido (a obra e a recepção, o
paralelo de hoje, as distorções na cultura popular) venha de fontes gratuitas e com cada achado
conferido, para que nada da web entre no roteiro sem id (D-008, D-027).

## Fronteira
A skill `.claude/skills/pesquisar/SKILL.md`, chamada como `/pesquisar <slug> <n>`. Saídas: as fontes
gravadas no livro (`W..`) e `livros/<slug>/temas/<n>/pesquisa.md`.

## Fora de escopo
- PDFs externos (SPEC 019, na reserva): a lacuna que só um artigo fechado resolve vira "link do
  Decisor" ou "sem fonte".
- Busca paga e buscadores comuns (D-027).

## Aceite (D-019)
1. Todo id de "Achados" existe (`livro trecho <slug> <id>`), e o briefing que os usa passa no
   `livro validar-briefing` (SPEC 020).
2. Roteiro manual do Decisor: escolher dois achados de `livros/serpent/temas/1/pesquisa.md` e ler o
   parágrafo com `livro trecho`. O dado diz só o que o parágrafo sustenta?

## Teste do arquiteto (Serpent, tema 1, 2026-11-12)
- 3 buscas gratuitas: 22 achados conferidos pelo script, 1 recusado (citação que não batia); 9 fontes
  novas (W07 a W15); 14 achados gravados, todos com id existente; 2 lacunas opcionais.
- Na conferência dos dados, o modelo gratuito tinha acrescentado "hoje", "o zumbi original" e um número
  exato onde a fonte dizia "pelo menos"; os três foram corrigidos e viraram exemplo na skill.
