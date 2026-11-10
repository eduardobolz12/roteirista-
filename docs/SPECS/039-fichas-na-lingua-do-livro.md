# SPEC 039 — Fichas na língua do livro, âncora como palavra inteira

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que o índice guarde os números e os detalhes concretos do livro, sem parágrafo
apontado por engano e sem a mesma ficha repetida, porque é desse material que saem as cenas e os
enigmas dos vídeos (E-003).

## Fronteira testada
CLI `livro`: `livro novo ... --lingua <código>`, `indexar`, `repescar`, `itens`.

## Substitui
Esta spec não altera as SPECs anteriores; onde divergem, vale esta (D-024):

- SPEC 008, **Prompt**: livro com língua informada usa outro prompt.
- SPEC 010, **Comparação**: a âncora tem de aparecer como palavra inteira.
- SPEC 011, **`repescar`**: livro com língua informada usa outro prompt.

## Fora de escopo
- Conferir o sentido da afirmação.
- Juntar ficha cuja frase está contida na de outra ficha (raro no E-003: 2 em 60 e 3 em 164).

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Prompt na língua do livro:** livro com língua informada na ficha usa `docs/prompts/indexar-livro.txt`
  em `indexar` e `docs/prompts/repescar-livro.txt` em `repescar`, sem alteração e com os mesmos bytes
  dentro do pacote. Livro sem língua informada continua com os prompts das SPECs 008 e 011.
- **Âncora como palavra inteira:** além da comparação da SPEC 010, o caractere antes da âncora no texto
  e o caractere depois dela não podem ser letra nem número. `six` não confere com `sixteenth`.
- **Mesma frase:** fichas do mesmo parágrafo com a mesma afirmação são uma só: fica a primeira. A
  comparação ignora maiúsculas, espaços repetidos e o ponto final. Vale depois da correção do id e
  junto com a regra de duplicado da SPEC 009; a ficha descartada não conta como gravada nem como
  rejeitada.

## Tabela de CA

Fixture: `tests/acceptance/039-fichas-na-lingua-do-livro/fixtures/dois-capitulos.pdf`, cópia do PDF
da SPEC 001 (capítulo 01: `O homem parou diante do túmulo e leu o próprio nome gravado no cimento.`,
`A irmã reconheceu o apelido de infância antes de reconhecer o rosto.`, `Naquela tarde, ninguém na
aldeia quis falar sobre o enterro.`).

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o PDF convertido duas vezes: `en`, com `--lingua en`, e `pt`, sem `--lingua` | `livro indexar en 01`, `livro repescar en 01` e `livro indexar pt 01` | o pedido de `indexar en` tem o prompt de `indexar-livro.txt` seguido dos parágrafos; o de `repescar en` começa por `repescar-livro.txt`; o de `indexar pt` tem o prompt de `indexar.txt` |
| CA-2 | `en` convertido; o modelo aponta `nome`, `home` e `rosto` em `01.001`, e `ar` em `01.003` | `livro indexar en 01` e `livro itens en 01` | stdout exatamente `rejeitado (âncora não encontrada): 01.001 \| caso \| home \| Âncora dentro de outra palavra.\ncorrigido: 01.001 -> 01.002: rosto\nrejeitado (âncora não encontrada): 01.003 \| marginal \| ar \| Âncora curta dentro de palavras.\n2 itens gravados, 1 corrigidos, 2 rejeitados\n`; `itens` dá `nome` em `01.001` e `rosto` em `01.002` |
| CA-3 | `en` convertido; o modelo devolve duas fichas de `01.001` com a mesma afirmação, mudando só maiúsculas, espaços e o ponto final, e uma de `01.002` | `livro indexar en 01` e `livro itens en 01` | última linha `2 itens gravados, 0 corrigidos, 0 rejeitados`; `itens` dá 2 linhas, e a de `01.001` é a primeira que o modelo escreveu |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/039-fichas-na-lingua-do-livro --junitxml=relatorios/039-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- O módulo que fala com o modelo e os dois prompts novos dentro do pacote

## Arquivo-exemplo
A conferência de âncora da SPEC 010.

## Roteiro manual (3 passos)
1. Com o Serpent convertido com `--lingua en`, rode `livro indexar serpent 06`. No E-003 foram 60 fichas
   e cerca de 12% de recusas; o modelo pode variar um pouco.
2. Rode `livro itens serpent 06` e procure as oito sementes, as duas ou três semanas e os 400 mil
   escravos: os três aparecem.
3. Rode `livro buscar serpent "sixteenth"` e confira que nenhuma ficha com âncora `six` aponta para
   esse parágrafo.

## Decisões pendentes
nenhuma
