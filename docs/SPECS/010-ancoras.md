# SPEC 010 — Conferência de âncoras

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que cada item do índice seja conferido no texto literal do livro, para que o
número apontado no parágrafo errado seja corrigido e o que não existe no livro não entre (D-003).

## Fronteira testada
CLI `livro`: `livro indexar <slug> <CC>` e `livro itens <slug> <CC>`.

## Substitui
Esta spec não altera as SPECs anteriores; onde divergem, vale esta (D-022):

- SPEC 008, **Saída de `indexar`**: `<C>` passa a contar as correções.

## Fora de escopo
- Conferir se a afirmação em português é fiel ao parágrafo: o script confere a âncora, não o sentido.
- Procurar a âncora em outro capítulo.

## Formatos
Valem os formatos das SPECs anteriores. Depois das verificações da SPEC 008:

- **Comparação:** a âncora é procurada no texto do parágrafo sem diferenciar maiúsculas, com os dois em
  NFC, espaços repetidos reduzidos a um, aspas curvas tratadas como retas e as marcas `[nPP]` ignoradas.
- **Âncora no parágrafo apontado:** o item fica como está.
- **Âncora num vizinho:** procura nos parágrafos do mesmo capítulo a distância 1, 2 e 3, nesta ordem;
  em cada distância, primeiro o anterior e depois o seguinte. Achou: o id do item passa a ser o do
  vizinho, e sai a linha `corrigido: <id antigo> -> <id novo>: <ancora>`.
- **Âncora vazia ou não encontrada:** `rejeitado (âncora não encontrada): <linha do modelo>`.
- **Ordem da saída:** as linhas `corrigido` e `rejeitado` saem na ordem da resposta do modelo.
- **Duplicado:** a regra da SPEC 009 vale depois da correção do id.

## Tabela de CA

Fixture: `tests/acceptance/010-ancoras/fixtures/ancoras.pdf`, gerada por `_gerar_pdf.py` na mesma
pasta, com o marcador "Capítulo Um" e sete parágrafos:

1. `O navio partiu de Liverpool em março.`
2. `A viagem durou quase dois meses.`
3. `Chegaram 400,000 sacas de açúcar ao porto.`
4. `O capitão escreveu ao "governador" sobre a carga.`
5. `Ninguém respondeu à carta.`
6. `O inverno fechou a estrada.`
7. `A neve cobriu a alfândega.`

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `ancoras.pdf` convertido; o modelo aponta `LIVERPOOL em março` em `01.001` e `“governador”`, com aspas curvas, em `01.004` | `livro indexar teste 01` e `livro itens teste 01` | última linha `2 itens gravados, 0 corrigidos, 0 rejeitados`; os dois itens ficam nos ids apontados, com a âncora como o modelo escreveu |
| CA-2 | o mesmo livro; o modelo aponta `400,000 sacas` em `01.005` e `fechou` em `01.007` | `livro indexar teste 01` e `livro itens teste 01` | stdout exatamente `corrigido: 01.005 -> 01.003: 400,000 sacas\ncorrigido: 01.007 -> 01.006: fechou\n2 itens gravados, 2 corrigidos, 0 rejeitados\n`; `itens` traz os dois nos ids novos |
| CA-3 | o mesmo livro; o modelo aponta `alfândega` em `01.002` (distância 5), `palavra que não existe` em `01.003`, uma âncora vazia em `01.004`, e `400,000 sacas` em `01.003` e em `01.005` | `livro indexar teste 01` e `livro itens teste 01` | as três primeiras linhas saem como `rejeitado (âncora não encontrada): ...`; há uma linha `corrigido: 01.005 -> 01.003: 400,000 sacas`; a última linha é `1 itens gravados, 1 corrigidos, 3 rejeitados`; `itens` dá uma linha só, a de `01.003` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/010-ancoras --junitxml=relatorios/010-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- O módulo que fala com o modelo, `src/roteirista/banco.py`

## Arquivo-exemplo
`src/roteirista/cli.py`: a comparação usada por `conferir`.

## Roteiro manual (3 passos)
1. Rode `livro indexar serpent 06`. Na medição do arquiteto foram 62 linhas, com cerca de 5 correções
   e 4 rejeições (o modelo pode variar um pouco).
2. Confira uma linha `corrigido` com `livro trecho`: a âncora está mesmo no parágrafo novo?
3. Conte quantas correções parecem certas. Se errar mais do que acerta, é o gatilho da D-003.

## Decisões pendentes
nenhuma
