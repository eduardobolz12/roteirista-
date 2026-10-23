# SPEC 005 — Ficha do livro e medida

**Estado:** testes vermelhos escritos a pedido do Decisor; **exemplos ainda não aprovados — não levar ao gate antes da aprovação**

## Intenção
Como Decisor, quero informar a língua do livro na conversão, conferir de relance três parágrafos e
saber o tamanho de cada capítulo, para confirmar que a conversão saiu certa e planejar a leitura
pelo modelo local.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`:

- `livro novo <arquivo> --slug <slug> [--lingua <código>]`
- `livro ficha <slug>`
- `livro medir <slug>`

## Fora de escopo
- Detectar a língua sozinho.
- Contar tokens com o tokenizador real do modelo: a contagem é uma estimativa.
- Medir notas e bibliografia (só o corpo).
- Editar a ficha depois da conversão.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Língua:** `--lingua` é opcional; aceita só `en`, `fr`, `pt`, `es`, `de`, `it`. Código fora da
  lista → stderr `língua inválida: <código>`, código de saída `2`, nenhum livro criado.
- **Conferência em `novo`:** antes da linha de resumo, três linhas, nesta ordem: o 1º parágrafo do
  1º capítulo, o 1º parágrafo do último capítulo e o último parágrafo do último capítulo, cada uma
  no formato `<id> <texto>`. A linha de resumo continua sendo a última.
- **Ficha:** `livro ficha <slug>` imprime exatamente três linhas: `língua: <código>` (ou
  `língua: não informada`), `capítulos: <N>`, `parágrafos: <M>`.
- **Medida:** `livro medir <slug>` imprime uma linha por capítulo,
  `<CC> <palavras> palavras, <tokens> tokens`, e por fim `total <palavras> palavras, <tokens> tokens`.
  Palavras = pedaços separados por espaço em cada parágrafo. Tokens do capítulo = arredondamento
  para cima de (caracteres dos parágrafos do capítulo, em NFC, sem contar separadores) / 4. O total
  é a soma das linhas.

## Tabela de CA

Fixture: `tests/acceptance/005-ficha-medida/fixtures/dois-capitulos.pdf`, cópia do PDF da SPEC 001
(cap. 1 com 3 parágrafos, 36 palavras e 199 caracteres; cap. 2 com 2 parágrafos, 27 palavras e 146
caracteres).

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `dois-capitulos.pdf`; pasta vazia | `livro novo dois-capitulos.pdf --slug teste --lingua pt` | código `0`; as quatro últimas linhas do stdout são exatamente `01.001 O homem parou diante do túmulo e leu o próprio nome gravado no cimento.`, `02.001 O médico assinou a certidão às três horas da tarde.`, `02.002 Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.` e `2 capítulos, 5 parágrafos` |
| CA-2 | o livro `teste` do CA-1; e um segundo livro `outro`, convertido do mesmo PDF sem `--lingua`; e uma tentativa com `--lingua xx` e slug `errado` | `livro ficha teste`, `livro ficha outro` e `livro novo dois-capitulos.pdf --slug errado --lingua xx` | `ficha teste` dá exatamente `língua: pt\ncapítulos: 2\nparágrafos: 5\n`; `ficha outro` começa por `língua: não informada\n`; o `novo` com `xx` sai com código `2`, stderr com `língua inválida: xx`, e não existe a pasta `errado` |
| CA-3 | o livro `teste` do CA-1 | `livro medir teste` | stdout exatamente `01 36 palavras, 50 tokens\n02 27 palavras, 37 tokens\ntotal 63 palavras, 87 tokens\n` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/005-ficha-medida --junitxml=relatorios/005-junit.xml
```

As suítes anteriores têm de continuar verdes (elas chamam `novo` sem `--lingua` e leem só a última
linha do resumo).

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, `src/roteirista/banco.py`

## Arquivo-exemplo
`src/roteirista/cli.py`: os subcomandos `novo` e `trecho`.

## Roteiro manual (3 passos)
1. Reconverta o Serpent com `--lingua en` e leia as três linhas de conferência contra o PDF.
2. Rode `livro ficha serpent`: língua `en`.
3. Rode `livro medir serpent` e veja qual capítulo é o maior em tokens (ele será lido em janelas
   pelo modelo local, na fatia 009).

## Decisões pendentes
nenhuma
