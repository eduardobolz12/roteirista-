# SPEC 009 — Capítulo em janelas

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que o capítulo seja lido em pedaços pequenos, sem nenhum parágrafo de fora, porque
no Serpent a leitura em janelas rendeu mais que o dobro de itens que a leitura do capítulo inteiro.

## Fronteira testada
CLI `livro`: `livro indexar <slug> <CC> [--janela <tokens>]` e `livro itens <slug> <CC>`.

## Fora de escopo
- Dividir um parágrafo: um parágrafo maior que a janela vai sozinho, inteiro.
- Retomar uma indexação interrompida.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Janela:** `--janela` tem o limite em tokens; sem ela, `2000`. Tokens do parágrafo = arredondamento
  para cima de (caracteres do parágrafo) / 4, como em `medir`.
- **Montagem:** os parágrafos entram em ordem enquanto a soma couber no limite. Uma janela nunca fica
  vazia. A janela seguinte começa repetindo o último parágrafo da anterior, se ele couber junto com o
  próximo parágrafo; se não couber, começa pelo próximo.
- **Pedido:** um pedido por janela, em ordem, no formato da SPEC 008.
- **Duplicado:** itens com o mesmo id, o mesmo tipo e a mesma âncora, sem diferenciar maiúsculas, são
  um só: fica o primeiro. Duplicado não conta como gravado nem como rejeitado.
- **Tudo ou nada:** se uma janela falhar, nada é gravado, os itens que já existiam ficam como estavam e
  o erro é o `modelo inacessível` da SPEC 008.

## Tabela de CA

Fixture: `tests/acceptance/009-janelas/fixtures/dois-capitulos.pdf`, cópia do PDF da SPEC 001. O
capítulo 01 tem parágrafos de 18, 17 e 15 tokens.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `dois-capitulos.pdf` convertido | `livro indexar teste 01 --janela 40`, `livro indexar teste 01 --janela 5` e `livro indexar teste 01` | com `40`: 2 pedidos, o primeiro com `01.001` e `01.002`, o segundo com `01.002` e `01.003`; com `5`: 3 pedidos, um parágrafo em cada; sem `--janela`: 1 pedido com os 3 parágrafos |
| CA-2 | o mesmo livro; as duas janelas devolvem o mesmo item de `01.002`, com maiúsculas diferentes e outra afirmação, e a segunda devolve mais um item de `01.002` com outra âncora | `livro indexar teste 01 --janela 40` e `livro itens teste 01` | última linha `4 itens gravados, 0 corrigidos, 0 rejeitados`; `itens` dá 4 linhas, na ordem do livro, e o item repetido sai com a afirmação da primeira janela |
| CA-3 | o capítulo já indexado; o servidor responde erro na segunda janela | `livro indexar teste 01 --janela 40` e `livro itens teste 01` | código `3`, stderr com `modelo inacessível:`; `itens` igual ao que era antes |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/009-janelas --junitxml=relatorios/009-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py` e o módulo que fala com o modelo

## Arquivo-exemplo
O subcomando `indexar` da SPEC 008.

## Roteiro manual (3 passos)
1. Rode `livro indexar serpent 14` e espere uns 10 minutos: é o maior capítulo do livro.
2. Rode `livro itens serpent 14`: há itens do começo ao fim do capítulo.
3. Leia dez linhas perto do meio e confira se fazem sentido.

## Decisões pendentes
nenhuma
