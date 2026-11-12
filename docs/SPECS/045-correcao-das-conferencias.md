# SPEC 045 — Correção das conferências da tradução

**Estado:** exemplos aprovados pelo Decisor em 2026-11-12; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que as invariantes e a legibilidade sigam as regras das SPECs 024 e 025 também nos
casos que os testes não fixaram, e que o número escrito por extenso seja comparado pelo valor, para que a
conferência da tradução não dê alarme falso nem deixe passar nome ou número (correção do aceite das
SPECs 024 e 025, em 2026-11-12; revisão do D-029).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS` e `ROTEIRISTA_EXPRESSOES`: `livro invariantes <slug> <antes> <depois>` e
`livro legibilidade <slug> <roteiro>`.

## Fora de escopo
- O glossário (SPEC 023) e as citações: não mudam.
- Nome de várias palavras visto como um só: "W. B. Seabrook" continua dando `W`, `B` e `Seabrook`.
- Ano por extenso à moda inglesa (`nineteen sixty-two`) e frações (`meio`, `half`, `demi`).

## Formatos
Valem os formatos das SPECs 023, 024 e 025, com estas mudanças:

- **Fim da frase** (para os nomes e para as frases longas): o ponto não fecha a frase quando vem logo
  depois de uma letra maiúscula sozinha (`W. B.`), em qualquer lugar do parágrafo, ou de um destes
  títulos: `Dr`, `Dra`, `Sr`, `Sra`, `Mr`, `Mrs`, `Ms`, `Prof`, `St`.
- **Nomes:** os títulos da lista acima não são nome. `I` seguido de apóstrofo, reto (`'`) ou curvo (`’`),
  e de letras não é nome (`I'm`, `I’m`, `I’ll`).
- **Glossário nos dois sentidos**, entre línguas diferentes, para qualquer palavra, com ou sem maiúscula
  (palavra inteira, sem diferenciar maiúsculas):
  - um nome de `antes` passa quando ele, ou alguma palavra da tradução de um termo que o contém, está no
    parágrafo de `depois` (como já era: `Barão → Baron`);
  - um nome de `depois` passa quando ele, ou alguma palavra de um termo cuja tradução o contém, está no
    parágrafo de `antes`: com `haitiano|haitiana → Haitian`, "Haitian" passa se o português tem
    "haitiano".

  Com `depois` em português, termo e tradução trocam de papel.
- **Número por extenso, pelo valor:** palavras-número seguidas, ligadas por espaço, hífen ou pelo conector
  da língua (`e`, `and`, `et`), formam um número só, que vale o que se lê. A palavra seguinte entra no
  número quando cabe na casa que a anterior deixou livre (depois de uma dezena, uma unidade; no francês,
  depois de `soixante` e `quatre-vingt`, até 19; depois de uma centena, até 99; depois de mil, até 999),
  ou quando é multiplicadora (`hundred`, `cent`, `mil`, `thousand`, `mille`, `milhão`, `million`, `dúzia`,
  `dozen`, `douzaine` e os plurais) e multiplica o que veio antes; sem nada antes, a multiplicadora vale
  ela mesma (`mil` = 1000, `a hundred` = 100, `a dozen` = 12). Assim: `duzentos` = `two hundred` =
  `deux cents` = 200; `dezessete` = `seventeen` = `dix-sept` = 17; `oitenta` = `eighty` = `quatre-vingts`
  = 80; `mil e quinhentos` = `fifteen hundred` = `mille cinq cents` = 1500; `duas dúzias` = `two dozen` =
  `deux douzaines` = 24; `entre dois e três` dá 2 e 3.
  - `um`, `uma`, `one`, `un` e `une` valem 1 só dentro de um número (`vinte e um` = 21; `one hundred` =
    100); sozinhos não contam, porque também são artigo.
  - Multiplicadora no plural sem número antes não conta (`milhões de cruzes`, `millions of crosses`,
    `des millions`): quer dizer "muitos".
  - Algarismos como na SPEC 024 (`1.894` = `1,894` = 1894); uma multiplicadora logo depois multiplica
    (`8 milhões` = `8 million` = `eight million` = 8000000).
  - `ambos`, `ambas` e `both` continuam valendo 2.
- **Comparação dos números:** as duas listas têm de ter os mesmos números, as mesmas vezes, em qualquer
  ordem. A saída continua em ordem crescente.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`) e, em `fixtures/`:

- `nomes-pt.md` e `nomes-en.md`, três parágrafos: no 1, "haitiano" e "presidente" em minúscula no
  português, "Haitian" e "President" no inglês, "Duvalier" nos dois; no 2, "Clairvius" só no português,
  "Narcisse" e `I’m` (apóstrofo curvo) só no inglês; no 3, "Haitian" no inglês sem "haitiano" no
  português.
- `inicial-en.md`, um parágrafo com duas frases: a primeira, de 28 palavras, com "W. B. Seabrook" no meio;
  a segunda com "Dr. Douyon". `inicial-en-revisado.md`: o mesmo texto sem "W. B. Seabrook" e com "a
  doctor" no lugar de "Dr. Douyon".
- `numeros-pt.md`, `numeros-en.md` e `numeros-fr.md`, o mesmo texto nas três línguas, em cinco parágrafos:
  1962 e quatro, em outra ordem na tradução; duzentos, mil e quinhentos e 8 milhões; dezessete, vinte e
  um, setenta, oitenta e noventa e nove; dois milhões, "milhões de cruzes" e duas dúzias; 1950, dois
  irmãos e "um cavalo", que na tradução viram três irmãos.

`ROTEIRISTA_EXPRESSOES` aponta para uma pasta sem arquivo de expressões.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro com `haitiano\|haitiana → Haitian` e `presidente → President\|president` no glossário `en` | `livro invariantes teste nomes-pt.md nomes-en.md` | código `1`; stdout exatamente `1.2: nome sumiu: Clairvius\n1.2: nome novo: Narcisse\n1.3: nome novo: Haitian\n3 parágrafos, 3 alertas\n` |
| CA-2 | o livro | `livro invariantes teste inicial-en.md inicial-en-revisado.md` e `livro legibilidade teste inicial-en.md` | o primeiro com código `1` e stdout exatamente `1.1: nome sumiu: W\n1.1: nome sumiu: B\n1.1: nome sumiu: Seabrook\n1.1: nome sumiu: Douyon\n1 parágrafos, 4 alertas\n`; o segundo com código `0` e stdout exatamente `1.1: frase de 28 palavras\n1 parágrafos, 1 frases longas, 0 palavras raras, 0 expressões\n` |
| CA-3 | o livro | `livro invariantes teste numeros-pt.md numeros-en.md` e `livro invariantes teste numeros-pt.md numeros-fr.md` | os dois com código `1` e stdout exatamente `1.5: números: 2, 1950 → 3, 1950\n5 parágrafos, 1 alertas\n` |

## Risco declarado
No francês, `neuf` também quer dizer "novo" e conta como 9. Ano por extenso à moda inglesa dá dois números
(`nineteen sixty-two` = 19 e 62); os roteiros escrevem os anos em algarismos. Um título no fim da frase
(`St.`) junta duas frases.

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/045-correcao-das-conferencias --junitxml=relatorios/045-junit.xml
```

As suítes anteriores têm de continuar verdes, inclusive 023, 024 e 025.

## Arquivos que serão tocados (previsão)
- `src/roteirista/traducao.py`

## Arquivo-exemplo
O próprio módulo das conferências da tradução (SPECs 023, 024 e 025).

## Roteiro manual (3 passos)
1. Com o glossário de 17 termos já gravado no Serpent,
   `livro invariantes serpent livros/serpent/temas/1/roteiro-pt.md livros/serpent/temas/1/roteiro-en.md`:
   `62 parágrafos, 0 alertas` (Haitian e President passam pelo glossário).
2. Na cópia do inglês do passo 3 da SPEC 024 ("six cracks", "The boy tried" e uma citação traduzida): só
   `1.2: números: 7 → 6`, `2.6: nome sumiu: Isnard` e o alerta da citação; `62 parágrafos, 3 alertas`.
3. `livro legibilidade serpent livros/serpent/temas/1/roteiro-en.md`: as 6 palavras raras do E-008
   (conch, unjustly, accuser, peasantry, hesitates, henchman) e as 2 expressões, sem "seabrook".

## Decisões pendentes
nenhuma
