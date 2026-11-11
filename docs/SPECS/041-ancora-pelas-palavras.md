# SPEC 041 — Âncora pelas palavras

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que a ficha certa não seja recusada só porque o modelo tirou uma vírgula ou um "of" da
âncora, porque no Serpent isso derrubou cerca de 12% das fichas e deixou diálogos inteiros sem ficha.

## Fronteira testada
CLI `livro`: `livro indexar`, `livro repescar` e `livro itens`.

## Substitui
Esta spec não altera as SPECs anteriores; onde divergem, vale esta (D-026):

- SPEC 010, **Comparação**, e SPEC 039, **Âncora como palavra inteira**: a âncora passa a conferir pelas
  palavras, como abaixo. A procura nos vizinhos e as mensagens continuam as mesmas.

## Fora de escopo
- Aceitar palavra parecida (`awkward` não confere com `awkwardly`).
- Aceitar âncora traduzida.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Palavras:** o texto em NFC, sem diferenciar maiúsculas, sem as marcas `[nPP]`, cortado em sequências
  de letras e algarismos. Pontuação, aspas, apóstrofos e travessões só separam palavras
  (`That’s` são as palavras `that` e `s`).
- **Confere:** as palavras da âncora aparecem nas palavras do parágrafo na mesma ordem, e entre duas
  palavras seguidas da âncora há no máximo 2 palavras do parágrafo.
- **Âncora longa:** com mais de 4 palavras, a âncora confere se algum trecho de 4 palavras seguidas dela
  conferir pela regra acima (o modelo às vezes copia a frase inteira e troca uma palavra).
- Vale para o parágrafo apontado, para os vizinhos (SPEC 010) e para a repescagem (SPEC 011).

## Tabela de CA

Fixture: `tests/acceptance/041-ancora-pelas-palavras/fixtures/dois-capitulos.pdf`, cópia do PDF da SPEC
001 (capítulo 01: `O homem parou diante do túmulo e leu o próprio nome gravado no cimento.`, `A irmã
reconheceu o apelido de infância antes de reconhecer o rosto.`, `Naquela tarde, ninguém na aldeia quis
falar sobre o enterro.`).

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro convertido; o modelo aponta `homem parou túmulo`, `A irmã reconheceu o apelido da escola` (longa, com uma palavra trocada) e `Naquela tarde ninguém` | `livro indexar teste 01` e `livro itens teste 01` | stdout exatamente `3 itens gravados, 0 corrigidos, 0 rejeitados\n`; as três fichas ficam nos ids apontados |
| CA-2 | o mesmo livro; o modelo aponta `homem nome` (8 palavras no meio), `nome próprio` (fora de ordem), `home` e `homem viu o túmulo de pedra` (longa, sem trecho de 4 palavras que confira) em `01.001`, e `apelido infância` (uma palavra no meio) em `01.002` | `livro indexar teste 01` | stdout exatamente `rejeitado (âncora não encontrada): 01.001 \| caso \| homem nome \| Palavras longe demais.\nrejeitado (âncora não encontrada): 01.001 \| caso \| nome próprio \| Fora de ordem.\nrejeitado (âncora não encontrada): 01.001 \| caso \| home \| Pedaço de palavra.\nrejeitado (âncora não encontrada): 01.001 \| caso \| homem viu o túmulo de pedra \| Nenhum trecho de quatro palavras confere.\n1 itens gravados, 0 corrigidos, 4 rejeitados\n` |
| CA-3 | o mesmo livro; o modelo aponta `irmã apelido infância` e `próprio nome` em `01.001`; depois, na repescagem dos outros parágrafos, `aldeia quis falar` em `01.003` e `irmã apelido` em `01.003` | `livro indexar teste 01` e `livro repescar teste 01` | `indexar` dá `corrigido: 01.001 -> 01.002: irmã apelido infância\n2 itens gravados, 1 corrigidos, 0 rejeitados\n`; `repescar` dá `rejeitado (âncora não encontrada): 01.003 \| caso \| irmã apelido \| Âncora de outro parágrafo.\n1 itens gravados, 0 sem conteúdo, 1 rejeitados\n` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/041-ancora-pelas-palavras --junitxml=relatorios/041-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- O módulo que fala com o modelo

## Arquivo-exemplo
A conferência de âncora da SPEC 039.

## Roteiro manual (3 passos)
1. Rode `livro indexar serpent 07`. Na medição do arquiteto, a regra nova recuperou 30 das 36 fichas
   recusadas do capítulo 07 (e 19 de 32 no capítulo 10); espere bem menos linhas `rejeitado` que antes.
2. Leia três linhas `corrigido` com `livro trecho`: a âncora está no parágrafo novo?
3. Rode `livro lacunas serpent 05`: sobram menos parágrafos de diálogo que os 12 de antes.

## Decisões pendentes
nenhuma
