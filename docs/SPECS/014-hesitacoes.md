# SPEC 014 — Hesitações do autor

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero uma lista curta dos parágrafos em que o autor hesita, se corrige ou admite dúvida,
para que o Claude julgue só essa lista e nenhum "talvez" do autor vire certeza no roteiro (D-005).

## Fronteira testada
CLI `livro`:

- `livro hesitacoes <slug> [--todas | --julgadas]`
- `livro julgar <slug> <id> <hesitacao|nao> "<nota>"`

## Fora de escopo
- O modelo local julgar: o tipo `contradicao` das fichas não entra aqui.
- Línguas além de `en` e `fr`.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Palavras-marca**, procuradas no texto dos parágrafos do corpo, sem diferenciar maiúsculas, com
  aspas curvas tratadas como retas, cada uma no início de uma palavra (`speculat` acha `speculation`):
  - `en`, fortes: `conjecture`, `hypothesis`, `wrong`, `mistaken`, `uncertain`, `uncertainty`, `doubt`,
    `unclear`, `speculat`, `possibly`, `i suspect`, `not sure`, `no evidence`, `remains to be`;
  - `en`, fracas: `perhaps`, `probably`, `apparently`, `presumably`, `it seems`, `it appears`,
    `appears to`, `seemed to`, `may have`, `might have`, `could have`, `unknown`;
  - `fr`, fortes: `conjecture`, `hypothèse`, `erreur`, `je me trompais`, `incertain`, `incertitude`,
    `doute`, `douteux`, `spécul`, `possiblement`, `je soupçonne`, `pas sûr`, `aucune preuve`, `reste à`;
  - `fr`, fracas: `peut-être`, `probablement`, `sans doute`, `apparemment`, `vraisemblablement`,
    `il semble`, `il paraît`, `semblait`, `aurait pu`, `pourrait`.
- **`hesitacoes`:** um parágrafo por linha, na ordem do livro, `<id> | <marcas>`, com as marcas achadas
  separadas por `, `, na ordem da lista. Sem opção, só os parágrafos com marca forte, mostrando só as
  fortes; com `--todas`, fortes e fracas, nesta ordem. Livro de língua sem lista, ou sem língua: stderr
  `sem palavras-marca para a língua: <código>` (ou `não informada`), código `2`.
- **`julgar`:** grava o julgamento do Claude para um id da lista `--todas`. Id fora dela: stderr
  `id fora da lista: <id>`, código `2`. Julgar de novo substitui.
- **`--julgadas`:** `<id> | <julgamento> | <nota>`, na ordem do livro.

## Tabela de CA

Fixture: `tests/acceptance/014-hesitacoes/fixtures/ingles.pdf`, gerada pelo mesmo gerador da SPEC 015, convertida com
`--lingua en`. Os parágrafos são:

- `01.001` `Perhaps the ship from Saint Marc carried more cargo than the records show.`
- `01.002` `The author admits the hypothesis, though neat, was quite wrong.`
- `01.003` `Marcel Pierre sold the powder to Max Beauvoir in Saint Marc.`
- `02.001` `Schultes thought it quite possibly came from the Spaniards.`
- `02.002` `It seems the Bizango met at night in Saint Marc.`
- `02.003` `The Bizango judged Narcisse there.`

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro `en` convertido | `livro hesitacoes en` | stdout exatamente `01.002 \| hypothesis, wrong\n02.001 \| possibly\n` |
| CA-2 | o livro `en`; o mesmo PDF convertido como `pt`, sem `--lingua` | `livro hesitacoes en --todas` e `livro hesitacoes pt` | o primeiro dá exatamente `01.001 \| perhaps\n01.002 \| hypothesis, wrong\n02.001 \| possibly\n02.002 \| it seems\n`; o segundo sai com código `2` e stderr com `sem palavras-marca para a língua: não informada` |
| CA-3 | o livro `en` | `livro julgar en 02.002 nao "só um modo de dizer"`, `livro julgar en 01.002 hesitacao "o autor admite o erro"`, `livro julgar en 01.003 nao "x"` e `livro hesitacoes en --julgadas` | os dois primeiros saem com código `0`; o terceiro com código `2` e `id fora da lista: 01.003`; `--julgadas` dá exatamente `01.002 \| hesitacao \| o autor admite o erro\n02.002 \| nao \| só um modo de dizer\n` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/014-hesitacoes --junitxml=relatorios/014-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, `src/roteirista/banco.py`

## Arquivo-exemplo
O subcomando `buscar`.

## Roteiro manual (3 passos)
1. Rode `livro hesitacoes serpent`: cerca de 65 parágrafos, e entre eles `06.020`, `06.037` e `06.038`.
2. Rode com `--todas`: cerca de 184.
3. Leia `06.038` com `livro trecho` e julgue com `livro julgar serpent 06.038 hesitacao "..."`.

## Decisões pendentes
nenhuma
