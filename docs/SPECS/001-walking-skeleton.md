# SPEC 001 — Walking skeleton: PDF → banco → trecho

**Estado:** exemplos aprovados pelo Decisor em 2026-10-23; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero dar um PDF ao sistema e receber de volta o texto exato de qualquer parágrafo
pelo id, para que nenhuma citação do roteiro dependa de memória de modelo.

## Fronteira testada
CLI `livro`, executável do projeto, chamado como processo:

- `livro novo <caminho-do-pdf> --slug <slug>`
- `livro trecho <slug> <id>`

Diretório dos livros: variável de ambiente `ROTEIRISTA_LIVROS` (padrão: `./livros`). O livro
`<slug>` fica em `$ROTEIRISTA_LIVROS/<slug>/`, com um único arquivo de banco `livro.sqlite` (D-007).

## Fora de escopo
- Hifenização, cabeçalhos e rodapés (002); notas e bibliografia (003); EPUB (004).
- Ficha, língua do livro e medida (005); `conferir`, `buscar` (006); `montar` e intervalos de ids (007).
- PDF sem marcadores (bookmarks): nesta fatia, só PDF com marcadores.
- Reconverter um slug que já existe.
- Vários ids numa chamada de `trecho`.

## Formatos
- **Capítulo:** cada marcador de primeiro nível do PDF abre um capítulo, numerado na ordem dos
  marcadores: `01`, `02`... O título do capítulo (o texto do marcador) não é parágrafo.
- **Parágrafo:** bloco de texto separado do seguinte por linha em branco ou recuo vertical. Linhas
  do mesmo parágrafo são unidas com um espaço; espaços repetidos viram um.
- **Id:** `CC.PPP`: capítulo com 2 dígitos, ponto, parágrafo com 3 dígitos, começando em `001` em
  cada capítulo.
- **Encoding:** stdout e stderr em UTF-8 (também no Windows, qualquer que seja o código de página do
  console). A saída de `trecho` é normalizada em NFC, terminada por uma única quebra de linha LF
  (`
`, nunca `
`), sem espaço no início ou no fim do texto. Toda linha de stdout termina em LF.
- **Resumo de `novo`:** última linha do stdout exatamente `<N> capítulos, <M> parágrafos`.
- **Erro:** id que não existe → stdout vazio, stderr `id inexistente: <id>`, código de saída `2`.

## Tabela de CA

Fixture: `tests/acceptance/001-walking-skeleton/fixtures/dois-capitulos.pdf`, PDF com 2 marcadores:

- **"Capítulo Um"**, com 3 parágrafos; o 1º é: `O homem parou diante do túmulo e leu o próprio nome gravado no cimento.`
- **"Capítulo Dois"**, com 2 parágrafos; o 2º ocupa duas linhas no PDF e, unido, é: `Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.`

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `dois-capitulos.pdf`; `ROTEIRISTA_LIVROS` aponta para uma pasta vazia | `livro novo dois-capitulos.pdf --slug teste` | código `0`; última linha do stdout `2 capítulos, 5 parágrafos`; existe `<pasta>/teste/livro.sqlite` |
| CA-2 | o livro `teste` convertido no CA-1 | `livro trecho teste 01.001` e depois `livro trecho teste 02.002` | código `0` nas duas; stdout é exatamente `O homem parou diante do túmulo e leu o próprio nome gravado no cimento.\n` e `Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.\n` |
| CA-3 | o livro `teste` convertido no CA-1 | `livro trecho teste 02.003` (o cap. 2 só tem 2 parágrafos) | código `2`; stdout vazio; stderr contém `id inexistente: 02.003` |

## Risco declarado
nenhum

## Como rodar os testes
Pré-requisitos da máquina: `uv` e Python 3.12.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/001-walking-skeleton --junitxml=relatorios/001-junit.xml
```

A configuração do runner é o `pytest.ini` da raiz (protegido, como os testes). Os testes chamam o executável `livro` pelo PATH, cada um com `ROTEIRISTA_LIVROS` numa pasta
temporária própria. Executável ausente é tratado como código `127`, e o teste falha por asserção.

**Tarefa de ambiente para o Kimi (antes do build):** criar o `pyproject.toml` do projeto
(`requires-python = ">=3.12"`, gerenciado por `uv`) com o script de console `livro`, de modo que,
depois de `uv sync`, o comando acima encontre `livro` no PATH do `.venv`. Os testes e a fixture não
mudam.

## Arquivos que serão tocados (previsão)
- `pyproject.toml`, `uv.lock`
- `src/roteirista/` (CLI, conversão de PDF, banco)
- `.gitignore` (`livros/*/`, `.venv/`, `relatorios/`)

## Arquivo-exemplo
Nenhum ainda: esta é a primeira fatia. Como referência de comportamento (não de código), o
`converter` e o `trecho` de `ferramentas/livro.py` do piloto `roteiros-youtube`.

## Roteiro manual (3 passos)
1. Rode `livro novo` no PDF do Serpent, em `livros/` (fora do git): o resumo mostra um número de
   capítulos coerente com o sumário do livro. Hifenização e notas ainda saem imperfeitas, porque são
   das fatias 002 e 003.
2. Rode `livro trecho serpent 04.001` e compare, a olho, com a primeira frase do capítulo
   "The Calabar Hypothesis" no PDF ("I ENJOY TRAINS...").
3. Abra `livros/serpent/` e confira que há um único arquivo de banco e nenhuma cópia do texto
   espalhada em outros arquivos.

## Decisões pendentes
nenhuma
