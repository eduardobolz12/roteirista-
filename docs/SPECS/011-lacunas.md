# SPEC 011 — Lacunas e repescagem

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero saber quais parágrafos ficaram sem item e fazer o modelo reler só esses, para que
nenhuma parte do livro fique invisível para o Claude sem ninguém perceber.

## Fronteira testada
CLI `livro`:

- `livro lacunas <slug> <CC>`
- `livro repescar <slug> <CC> [--janela <tokens>]`
- `livro indexar <slug> <CC>` e `livro itens <slug> <CC>`

## Fora de escopo
- Repescar duas vezes o mesmo parágrafo com outro prompt.
- Julgar se `sem-conteudo` foi uma resposta certa.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Lacuna:** parágrafo do capítulo sem nenhum item e sem marca `sem-conteudo`. Parágrafo sem letra nem
  número (`* * *`) nunca é lacuna.
- **`lacunas`:** um id por linha, na ordem do livro. Sem lacunas: stdout vazio. Código `0` nos dois casos.
- **`repescar`:** manda só as lacunas, em janelas como na SPEC 009, com o conteúdo de
  `docs/prompts/repescar.txt`, sem alteração, no lugar do prompt da SPEC 008. Sem lacunas, não faz
  pedido nenhum.
- **Linha do modelo:** a da SPEC 008, ou `id | sem-conteudo`, que marca o parágrafo.
- **Rejeição:** valem as da SPEC 008, com mais `id fora da lista` (id do capítulo que não é lacuna,
  verificado depois de `id fora do capítulo`). A âncora tem de estar no próprio parágrafo: aqui não há
  correção por vizinho, e o motivo é `âncora não encontrada`.
- **Saída de `repescar`:** as linhas `rejeitado` e, por último,
  `<N> itens gravados, <S> sem conteúdo, <M> rejeitados`. Os itens que já existiam ficam.
- **Regravar:** `indexar` apaga também as marcas `sem-conteudo` do capítulo.

## Tabela de CA

Fixture: `tests/acceptance/011-lacunas/fixtures/lacunas.pdf`, gerada por `_gerar_pdf.py` na mesma
pasta, com o marcador "Capítulo Um" e cinco parágrafos:

1. `O médico assinou a certidão.`
2. `* * *`
3. `A família guardou uma cópia.`
4. `Fim da primeira parte.`
5. `O caso chegou aos jornais.`

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `lacunas.pdf` convertido; o modelo devolve só um item de `01.001` | `livro lacunas teste 01` antes de indexar; `livro indexar teste 01`; `livro lacunas teste 01` | antes: `01.001\n01.003\n01.004\n01.005\n`; depois: `01.003\n01.004\n01.005\n` |
| CA-2 | o capítulo indexado; o modelo devolve um item de `01.003`, `01.004 \| sem-conteudo`, um item de `01.001` e um de `01.005` com âncora que não existe | `livro repescar teste 01`, `livro lacunas teste 01` e `livro itens teste 01` | o servidor recebeu um pedido, com o prompt de repescagem e só os parágrafos `01.003`, `01.004` e `01.005`; stdout com `rejeitado (id fora da lista): ...`, `rejeitado (âncora não encontrada): ...` e, por último, `1 itens gravados, 1 sem conteúdo, 2 rejeitados`; `lacunas` dá `01.005\n`; `itens` dá 2 linhas |
| CA-3 | o capítulo do CA-2 | `livro indexar teste 01` de novo, `livro lacunas teste 01`; depois uma indexação que cobre todos os parágrafos, `livro repescar teste 01` | depois de indexar de novo, `lacunas` volta a `01.003\n01.004\n01.005\n`; com tudo coberto, `repescar` dá `0 itens gravados, 0 sem conteúdo, 0 rejeitados\n` e nenhum pedido novo |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/011-lacunas --junitxml=relatorios/011-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, `src/roteirista/banco.py`, o módulo que fala com o modelo e o segundo prompt

## Arquivo-exemplo
O subcomando `indexar` das SPECs 008 a 010.

## Roteiro manual (3 passos)
1. Com o capítulo 06 indexado, rode `livro lacunas serpent 06`. Na medição do arquiteto foram 4 ou 5
   parágrafos.
2. Rode `livro repescar serpent 06`, em menos de um minuto, e `livro lacunas serpent 06` de novo: sobra
   quase nada.
3. Se sobrar algum id, leia com `livro trecho` e veja se é mesmo um parágrafo sem informação.

## Decisões pendentes
nenhuma
