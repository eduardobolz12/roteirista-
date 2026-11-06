# SPEC 037 — Junção de linhas: travessão, maiúscula e palavra composta

**Estado:** exemplos e limitação aprovados pelo Decisor em 2026-11-06; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que travessões e hífens saiam como o autor escreveu quando caem na quebra de
linha, para que uma citação literal do livro confira com `conferir`.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro novo` e `livro trecho`.

## Substitui
Esta spec não altera as SPECs anteriores; onde divergem, vale esta (D-020):

- SPEC 002, **Hifenização**: acrescenta os casos abaixo. A forma com hífen vista em outro ponto do
  livro continua mantendo o hífen.

## Fora de escopo
- Separar ou juntar palavras dentro da mesma linha.
- Dicionário externo: as regras olham só o próprio livro.

## Formatos
Valem os formatos das SPECs anteriores. Ao unir duas linhas do mesmo parágrafo, nesta ordem:

- **Travessão:** se a primeira termina, ou a segunda começa, em `—` ou `–`, elas se unem **sem
  espaço**.
- **Hífen antes de maiúscula:** se a primeira termina em letra + hífen e a segunda começa por
  maiúscula, o hífen fica e elas se unem sem espaço (`Mercedes-Benz`).
- **Hífen antes de minúscula:** a forma unida vence quando aparece no livro. Se não aparece, o hífen
  fica, sem espaço, em qualquer um destes casos; nos demais, ele sai:
  - a forma com hífen aparece inteira numa linha só, em outro ponto do livro;
  - a primeira parte já tem outro hífen (`dia-a-` + `dia`);
  - as duas partes aparecem como palavras inteiras em outro ponto do livro.
- **Palavra inteira:** a que não está partida numa quebra de linha com hífen.

## Tabela de CA

Fixture: `tests/acceptance/037-juncao-de-linhas/fixtures/juncao.pdf`, gerada por `_gerar_pdf.py` na
mesma pasta. PDF com o marcador "Capítulo Um" e nove parágrafos separados por espaço vertical. A
barra marca a quebra de linha:

1. `A família esperou em silêncio—` / `ninguém falou nada.`
2. `O padre saiu da igreja` / `—a chuva já tinha parado.`
3. `O carro era um velho Mercedes-` / `Benz da prefeitura.`
4. `O trabalho do dia-a-` / `dia pesava na aldeia.`
5. `Ela comprou uma saia-` / `calça na feira.`
6. `A saia e a calça ficaram no varal.`
7. `A testemu-` / `nha chegou cedo.`
8. `A sobre-` / `mesa veio fria.`
9. `Deixaram a sobremesa sobre a mesa.`

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `juncao.pdf` convertido com `--slug teste` | `livro trecho teste 01.001` e `01.002` | stdout exatamente `A família esperou em silêncio—ninguém falou nada.\n` e `O padre saiu da igreja—a chuva já tinha parado.\n` |
| CA-2 | o mesmo livro | `livro trecho teste 01.003` e `01.004` | stdout exatamente `O carro era um velho Mercedes-Benz da prefeitura.\n` e `O trabalho do dia-a-dia pesava na aldeia.\n` |
| CA-3 | o mesmo livro | `livro trecho teste 01.005`, `01.007`, `01.008` e `01.010` | `01.005`, `01.007` e `01.008` dão exatamente `Ela comprou uma saia-calça na feira.\n`, `A testemunha chegou cedo.\n` e `A sobremesa veio fria.\n`; `01.010` sai com código `2` |

## Limitação aceita
Composto cuja parte não aparece sozinha em nenhum outro ponto do livro perde o hífen. No Serpent são
4 casos (`midseventeenth`, `tightfitting`, `selffulfilling`, `halfintelligent`). Quem cita esses
trechos vê `NÃO EXISTE` em `conferir` com a grafia original e confere pelo `trecho`.

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/037-juncao-de-linhas --junitxml=relatorios/037-junit.xml
```

As suítes 001 a 007, 034, 035 e 036 têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/pdf.py`

## Arquivo-exemplo
`src/roteirista/pdf.py`: `_juntar_linhas`. Referência de comportamento: a função `juntar` do
`converter` em `ferramentas/livro.py` do piloto.

## Roteiro manual (3 passos)
1. Com o Serpent reconvertido, rode `livro conferir serpent "on the head—baskets of"`: `EXISTE`.
2. Rode `livro conferir serpent "Mercedes-Benz"` e `livro conferir serpent "hell-on-earth"`: `EXISTE`.
3. Rode `livro buscar serpent "self"` e abra um dos parágrafos com `trecho`: nenhum travessão com
   espaço sobrando.

## Decisões pendentes
nenhuma
