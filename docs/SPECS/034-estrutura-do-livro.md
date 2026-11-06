# SPEC 034 — Estrutura do livro: partes, páginas de serviço e abertura de capítulo

**Estado:** exemplos aprovados pelo Decisor em 2026-11-06; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que um PDF de livro comercial saia com os capítulos que o autor escreveu, sem
partes engolindo capítulos, sem páginas de serviço e sem texto repetido, para que cada id aponte
para um lugar só do livro.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro novo`, `trecho`, `medir`, `conferir` e `buscar`.

## Substitui
Esta spec não altera as SPECs anteriores; onde divergem, vale esta (D-020):

- SPEC 001, **Capítulo**: "cada marcador de primeiro nível abre um capítulo".
- SPEC 002, **Título do capítulo**: passa a valer também o título impresso diferente do marcador.
- SPEC 005, **Conferência em `novo`**: "1º capítulo" passa a ser o 1º capítulo que tem parágrafos.

## Fora de escopo
- Parágrafos por recuo (SPEC 035).
- EPUB: partes e páginas de serviço em EPUB ficam para quando um EPUB real pedir.
- Guardar o texto da parte ou das páginas de serviço em outro lugar.
- PDF sem marcadores.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Capítulo:** cada marcador **sem filhos**, em qualquer nível, abre um capítulo, numerado na ordem
  dos marcadores.
- **Parte:** marcador com filhos não é capítulo. O texto das páginas dele, antes do primeiro filho,
  não entra no livro.
- **Página de serviço:** marcador sem filhos cujo texto, sem diferenciar maiúsculas, é um destes:
  `Copyright`, `Copyright Page`, `Direitos Autorais`, `Contents`, `Table of Contents`, `Sumário`,
  `Sommaire`, `Table des matières`, `Index`, `Índice`, `Índice Remissivo`. Não recebe número, não
  conta no resumo e o seu texto não entra no livro.
- **Capítulo sem texto:** um marcador cujas páginas não têm texto (capa em imagem) é capítulo com
  zero parágrafos. Ele mantém o seu número.
- **Título do capítulo:** as linhas em fonte maior que a do corpo, antes do primeiro parágrafo do
  capítulo, não são parágrafo, mesmo quando o texto impresso difere do marcador (`1` e `O Túmulo`
  para o marcador `1: O Túmulo`).
- **Cada linha pertence a um capítulo só.** Quando o título do próximo capítulo não aparece
  impresso igual ao marcador, a página do marcador inteira é do próximo capítulo.
- **Conferência em `novo`:** a primeira linha usa o 1º capítulo que tem parágrafos.

## Tabela de CA

Fixture: `tests/acceptance/034-estrutura-do-livro/fixtures/estrutura.pdf`, gerada por `_gerar_pdf.py`
na mesma pasta. PDF A5 de 9 páginas, uma por marcador:

| Página | Marcador (nível) | Texto |
|---|---|---|
| 1 | Title Page (1) | nenhum |
| 2 | Copyright Page (1) | `Todos os direitos reservados.` |
| 3 | Contents (1) | `O Túmulo` · `A Certidão` |
| 4 | Dedication (1) | `Aos meus pais.` |
| 5 | Parte Um (1) | `PARTE UM` e `O Veneno` em fonte maior · `Esta parte reúne os casos da costa.` |
| 6 | 1: O Túmulo (2) | `1` e `O Túmulo` em fonte maior · `O homem leu o próprio nome gravado no cimento.` · `A irmã reconheceu o apelido de infância.` |
| 7 | 2: A Certidão (2) | `2` e `A Certidão` em fonte maior · `O médico assinou a certidão às três horas.` |
| 8 | Annotated Bibliography (1) | `Davis, Wade. The Serpent and the Rainbow. 1985.` |
| 9 | Index (1) | `certidão, 12` · `túmulo, 3` |

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `estrutura.pdf`; pasta vazia | `livro novo estrutura.pdf --slug teste` e `livro medir teste` | código `0`; as quatro últimas linhas do `novo` são exatamente `02.001 Aos meus pais.`, `04.001 O médico assinou a certidão às três horas.`, `04.001 O médico assinou a certidão às três horas.` e `4 capítulos, 4 parágrafos`; o `medir` começa por `01 0 palavras, 0 tokens\n` e tem 5 linhas |
| CA-2 | o mesmo livro | `livro conferir teste "O homem leu"`, `livro buscar teste "certidão"`, `livro buscar teste "direitos"` e `livro buscar teste "costa"` | stdout `EXISTE 03.001\n` (um id só), `04.001\n`, vazio e vazio; códigos `0`, `0`, `1` e `1` |
| CA-3 | o mesmo livro | `livro trecho teste 03.001`, `03.002`, `03.003`, `bib.001`, `bib.002` e `livro buscar teste "túmulo"` | `03.001` e `03.002` dão exatamente `O homem leu o próprio nome gravado no cimento.\n` e `A irmã reconheceu o apelido de infância.\n`; `bib.001` dá `Davis, Wade. The Serpent and the Rainbow. 1985.\n`; `03.003` e `bib.002` saem com código `2`; o `buscar` dá stdout vazio e código `1` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/034-estrutura-do-livro --junitxml=relatorios/034-junit.xml
```

As suítes 001 a 007 têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/pdf.py`, `src/roteirista/cli.py`

## Arquivo-exemplo
`src/roteirista/pdf.py`: a montagem dos capítulos em `extrair`.

## Roteiro manual (3 passos)
1. Apague `livros\serpent`, reconverta o Serpent com `--lingua en` e rode `livro ficha serpent`:
   20 capítulos.
2. Rode `livro trecho serpent 02.001` e `livro trecho serpent 06.001`: a dedicatória e um texto que
   começa por "I ENJOY TRAINS".
3. Rode `livro buscar serpent "Rockefeller Center"`: nenhum resultado, porque o copyright saiu.

## Decisões pendentes
nenhuma
