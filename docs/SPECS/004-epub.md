# SPEC 004 — EPUB

**Estado:** testes vermelhos escritos a pedido do Decisor; **exemplos ainda não aprovados — não levar ao gate antes da aprovação**

## Intenção
Como Decisor, quero converter um livro em EPUB do mesmo jeito que um PDF, com os mesmos ids, para
não depender do formato em que comprei o livro.

## Fronteira testada
CLI `livro`: `livro novo <caminho.epub> --slug <slug>` e `livro trecho <slug> <id>`, com
`ROTEIRISTA_LIVROS`. O formato é escolhido pela extensão do arquivo (`.pdf` ou `.epub`, sem
diferenciar maiúsculas).

## Fora de escopo
- Notas, bibliografia e imagens em EPUB.
- EPUB com DRM.
- Capítulo dividido em vários arquivos do EPUB.
- Outros formatos (`.mobi`, `.docx`, `.txt`).

## Formatos
Valem os formatos das SPECs 001 a 003 (id, encoding, LF, resumo de `novo`). Acrescentam-se:

- **Capítulo:** cada documento da ordem de leitura do EPUB (o `spine`) que tem um título `h1` ou
  `h2` abre um capítulo, numerado na ordem do `spine`. Documento sem título (capa, folha de rosto)
  não abre capítulo e não tem parágrafos.
- **Título:** o texto do primeiro `h1`/`h2` do documento não é parágrafo.
- **Parágrafo:** cada elemento `<p>` com texto. Marcas internas (`<em>`, `<i>`, `<b>`, `<span>`)
  somem e o texto fica; entidades HTML viram o caractere (`&amp;` → `&`). Espaços e quebras de
  linha dentro do `<p>` viram um espaço.

## Tabela de CA

Fixture: `tests/acceptance/004-epub/fixtures/dois-capitulos.epub`, EPUB 3 com 3 documentos no
`spine`: capa sem título; `<h1>Capítulo Um</h1>` com os mesmos 3 parágrafos do PDF da SPEC 001;
`<h1>Capítulo Dois</h1>` com os mesmos 2 parágrafos, e o 1º deles escrito como
`<p>O médico assinou a certidão <em>às três horas</em> da tarde &amp; saiu.</p>`; o 2º com uma
quebra de linha no meio do código-fonte.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `dois-capitulos.epub`; `ROTEIRISTA_LIVROS` numa pasta vazia | `livro novo dois-capitulos.epub --slug teste` | código `0`; última linha do stdout `2 capítulos, 5 parágrafos` (a capa não conta) |
| CA-2 | o livro `teste` convertido do EPUB | `livro trecho teste 01.001` e `livro trecho teste 02.002` | stdout exatamente `O homem parou diante do túmulo e leu o próprio nome gravado no cimento.\n` e `Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.\n` |
| CA-3 | o livro `teste` convertido do EPUB | `livro trecho teste 02.001` | stdout exatamente `O médico assinou a certidão às três horas da tarde & saiu.\n` |

## Risco declarado
dep nova (biblioteca de leitura de EPUB/HTML, a escolher pelo programador)

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/004-epub --junitxml=relatorios/004-junit.xml
```

As suítes 001 a 003 têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/epub.py` (novo), `src/roteirista/cli.py`, `pyproject.toml`

## Arquivo-exemplo
`src/roteirista/pdf.py`: a conversão de PDF, que devolve capítulos com parágrafos para o banco.

## Roteiro manual (3 passos)
1. Converta um EPUB seu com `livro novo`: o número de capítulos bate com o sumário do livro.
2. Rode `livro trecho` no 1º parágrafo do 1º capítulo e compare com o leitor de EPUB.
3. Escolha um parágrafo com itálico no leitor de EPUB e confira que o `trecho` traz o texto sem
   marca nenhuma.

## Decisões pendentes
nenhuma
