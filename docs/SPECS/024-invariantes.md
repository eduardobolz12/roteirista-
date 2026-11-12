# SPEC 024 — Invariantes entre versões

**Estado:** exemplos aprovados pelo Decisor em 2026-11-12; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que a tradução e a humanização sejam conferidas contra a versão anterior, parágrafo
por parágrafo, para que nenhuma citação, número ou nome mude ou suma no caminho (D-011, D-029).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro invariantes <slug> <antes> <depois>`.

## Fora de escopo
- Conferir o sentido: é a SPEC 042.
- Conferir termos que não são nome: é a SPEC 023.

## Formatos
Valem os formatos das SPECs anteriores e o **roteiro** da SPEC 023. Acrescentam-se:

- **Língua de cada arquivo:** o primeiro pedaço do nome, sem `.md` e separado por `-`, que seja `pt`, `en` ou
  `fr` (`roteiro-en-humanizado.md` é `en`). Sem isso: stderr `língua desconhecida: <nome do arquivo>`,
  código `2`.
- **Casamento:** os capítulos pelo número, os parágrafos pela ordem. Capítulo com número de parágrafos
  diferente, ou que falta em `depois`: `cap. <n>: <a> parágrafos antes, <b> depois`, e ele não é conferido.
- **Em cada par de parágrafos**, nesta ordem:
  - **citações:** a lista de citações (texto e id, regra da SPEC 022) tem de ser igual, caractere por
    caractere, em NFC. Senão: `<n>.<p>: citações: <antes> → <depois>`, cada lado com as citações como
    `"<texto>" [<id>]` separadas por ` · `, ou `nenhuma`.
  - **números:** fora das citações e das marcas de id, os algarismos (pontos e vírgulas de dentro ignorados:
    `1.894` = `1,894` = `1894`) e as palavras-número da língua, contadas palavra por palavra
    (`vinte e quatro` dá 20 e 4; `twenty-four` dá 20 e 4). A lista, com repetições, tem de ser igual.
    Senão: `<n>.<p>: números: <antes> → <depois>`, em ordem crescente, separados por `, `, ou `nenhum`.
  - **nomes:** palavra que começa por maiúscula e não é a primeira da frase, fora das citações, sem o `'s`
    final; `I` e suas contrações (`I'm`) não contam. A primeira palavra da frase também é nome quando,
    no mesmo arquivo, ela aparece como nome em outro lugar e nunca aparece em minúscula ("Isnard"
    conta; "The" não, porque "the" aparece). A frase acaba em `.`, `!` ou `?` seguido de espaço, menos
    depois de uma inicial (`W. B.`); uma citação que termina em `.`, `!` ou `?` também acaba a frase.
    Cada nome de `antes` tem de estar no parágrafo de `depois` (palavra inteira, sem diferenciar
    maiúsculas); senão `<n>.<p>: nome sumiu: <nome>`. Cada nome de `depois` tem de estar no de `antes`;
    senão `<n>.<p>: nome novo: <nome>`. Entre línguas diferentes, vale também qualquer palavra da
    tradução de um termo do glossário que contém o nome (`Barão → Baron`), nos dois sentidos. Cada nome uma
    vez por parágrafo, na ordem em que aparece.
- **Glossário:** o do livro na língua que não é `pt`; entre duas versões da mesma língua, nenhum.
- **Palavras-número:** 2 a 20, as dezenas, as centenas, mil/thousand/mille, milhão/million, dúzia/dozen/
  douzaine, e `ambos`, `ambas` e `both` valendo 2. `um`, `uma`, `one`, `un` e `une` não contam, porque
  também são artigo.
- **Saída:** os alertas na ordem dos capítulos e dos parágrafos; por fim `<P> parágrafos, <A> alertas`,
  com `P` os parágrafos conferidos. Código `1` se houver alerta, senão `0`. Arquivo que não existe: como na
  SPEC 016.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`), `roteiro-pt.md` e `roteiro-en.md` da SPEC 023, e em `fixtures/`:

- `roteiro-en-humanizado.md`: o inglês com quatro mudanças no cap. 1 ("Benetier" saiu e "Port-au-Prince"
  entrou em 1.1; a citação traduzida em 1.2; "both" virou "three" em 1.3), um parágrafo a mais no cap. 2
  e, no cap. 3, "The village is still waiting." no lugar de "Benetier is still waiting." (nome no começo da
  frase);
- `notas.md`: um arquivo sem língua no nome.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro com `Barão → Baron` no glossário `en` | `livro invariantes teste roteiro-pt.md roteiro-en.md` | código `0`; stdout exatamente `6 parágrafos, 0 alertas\n` |
| CA-2 | o livro sem glossário | `livro invariantes teste roteiro-pt.md roteiro-en.md` e `livro invariantes teste roteiro-pt.md notas.md` | o primeiro com código `1` e stdout exatamente `2.1: nome sumiu: Barão\n2.1: nome novo: Baron\n6 parágrafos, 2 alertas\n`; o segundo com código `2` e `língua desconhecida: notas.md` no stderr |
| CA-3 | o livro com `Barão → Baron` | `livro invariantes teste roteiro-en.md roteiro-en-humanizado.md` | código `1`; stdout exatamente `1.1: nome sumiu: Benetier\n1.1: nome novo: Port-au-Prince\n1.2: citações: "leu o próprio nome gravado no cimento" [01.001] → "read his own name carved in the cement" [01.001]\n1.3: números: 2 → 3\ncap. 2: 2 parágrafos antes, 3 depois\n3.1: nome sumiu: Benetier\n4 parágrafos, 6 alertas\n` |

## Risco declarado
nenhum

## Como rodar os testes
```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/024-invariantes --junitxml=relatorios/024-junit.xml
```
As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py` e o módulo das conferências da tradução (SPEC 023).

## Arquivo-exemplo
A conferência do glossário (SPEC 023) e o validador da SPEC 022 (citações).

## Roteiro manual (3 passos)
1. Com o glossário do E-008 gravado, `livro invariantes serpent livros/serpent/temas/1/roteiro-pt.md livros/serpent/temas/1/roteiro-en.md`:
   `62 parágrafos, 0 alertas`.
2. Numa cópia do inglês, troque "seven cracks" por "six cracks" e rode de novo: `1.2: números: 7 → 6`.
3. Na mesma cópia, traduza uma citação e troque "Isnard tried" por "The boy tried" (2.6, nome no começo
   da frase): `2.6: nome sumiu: Isnard` e o alerta de citação, nos parágrafos certos.

## Decisões pendentes
nenhuma
