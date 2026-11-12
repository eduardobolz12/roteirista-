# SPEC 029 — /temas

**Estado:** skill escrita e testada no Serpent pelo arquiteto em 2026-11-12; aguardando o roteiro manual
e o aceite do Decisor

## Intenção
Como Decisor, quero receber a sugestão de temas de um livro já conferida, montada só a partir do índice,
para escolher até 4 vídeos sem que o Claude leia o livro inteiro (D-017, D-018).

## Fronteira
A skill `.claude/skills/temas/SKILL.md`, chamada como `/temas <slug>`, com as regras comuns de
`docs/prompts/roteiro-regras.md`. Saída: `livros/<slug>/temas.md`.

## Fora de escopo
- Escolher os temas: é do Decisor.
- Código: a skill só usa a CLI (`visao`, `contar-tema`, `itens`, `hesitacoes`, `buscar`, `montar`,
  `trecho`, `validar-temas`).

## Aceite (D-019)
1. O arquivo produzido passa em `livro validar-temas <slug> livros/<slug>/temas.md` (SPEC 016).
2. Roteiro manual do Decisor: ler `livros/serpent/temas.md` e conferir, por amostra, três ids do detalhe
   com `livro trecho serpent <id>`. O parágrafo diz o que a linha diz?

## Teste do arquiteto (Serpent, 2026-11-12)
- `ok: 5 temas, 4 assuntos`; 2 descartados com motivo.
- Na conferência pelo texto literal, três frases foram corrigidas antes de gravar: quem diz "There is no
  poison" (um primo, não Narcisse); quem cava o túmulo (Jean, não Marcel); "gente rica" num parágrafo que
  diz "ricos e pobres". As três viraram exemplos na skill.
- Ajustes da skill depois do teste: capítulos de apoio (glossário) não servem às três funções; o padrão de
  busca `{0,80}` dos dois lados.
