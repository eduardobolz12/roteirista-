# SPEC 002 — PDF real: hifenização, cabeçalho, rodapé e virada de página

**Estado:** exemplos e limitação aprovados pelo Decisor em 2026-10-23; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que o texto de um PDF de livro de verdade saia como o autor escreveu, sem
palavras partidas, sem o título corrido e sem os números de página no meio dos parágrafos, para que
`trecho` e `conferir` encontrem a frase exata.

## Fronteira testada
CLI `livro`, como na SPEC 001: `livro novo <pdf> --slug <slug>` e `livro trecho <slug> <id>`, com
`ROTEIRISTA_LIVROS` apontando para a pasta dos livros.

## Fora de escopo
- Notas de rodapé e bibliografia (003).
- PDF sem marcadores, EPUB (004).
- Hífen suave (U+00AD) e travessão no fim da linha.
- Composto com hífen que aparece **uma única vez** no livro e cai partido no fim da linha (ex.:
  `tight-` / `fitting`): pela regra abaixo, ele sai unido (`tightfitting`). Limitação aceita nesta
  fatia; a âncora de citação continua sendo o id.
- Cabeçalho que aparece em menos de 3 páginas.

## Formatos
Valem todos os formatos da SPEC 001. Acrescentam-se:

- **Hifenização:** linha que termina em letra + hífen (`-`), seguida de linha que começa por letra
  minúscula: as duas partes se unem **sem o hífen e sem espaço**. Exceção: se a forma com hífen
  (`guarda-chuva`) aparece inteira, numa linha só, em outro ponto do livro, e a forma unida
  (`guardachuva`) não aparece, o hífen fica e as partes se unem sem espaço.
- **Cabeçalho e rodapé:** é removida toda linha que está na faixa superior ou inferior da página
  (14% da altura, cada uma) e que (a) se repete, com o mesmo texto, em 3 páginas ou mais, ou (b) é
  só um número (o número da página). Essas linhas nunca entram em parágrafo nem contam como
  parágrafo.
- **Virada de página:** o último parágrafo de uma página continua no primeiro da página seguinte
  quando a última linha da página **não** termina em `.`, `!`, `?` ou `…` (seguidos ou não de aspas
  de fechamento). As partes se unem com um espaço, aplicando a regra da hifenização.
- **Título do capítulo:** a linha com o texto do marcador do capítulo não é parágrafo (SPEC 001).

## Tabela de CA

Fixture: `tests/acceptance/002-pdf-real/fixtures/tres-paginas.pdf`, PDF A5 de 3 páginas. Em toda
página, no topo, o título corrido `O LIVRO DE TESTE`; no pé, o número impresso (`12`, `13`, `14`).
Marcadores: "Capítulo Um" (página 1) e "Capítulo Dois" (página 3). Linhas exatas no PDF:

- Página 1: `A família pagou a cons-` / `trução do túmulo em duas parcelas.` · `Os vizinhos chamavam aquilo de guarda-` / `chuva dos mortos, e riam.` · `Ninguém levou guarda-chuva ao enterro.` · `O padre chegou tarde e` (última linha da página)
- Página 2: `começou a missa sem esperar a família.` · `Depois da missa, o caixão foi levado em silêncio.`
- Página 3: `O cemitério fechou ao anoitecer.`

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `tres-paginas.pdf` convertido com `--slug teste` | `livro trecho teste 01.001` e `livro trecho teste 01.002` | stdout exatamente `A família pagou a construção do túmulo em duas parcelas.\n` e `Os vizinhos chamavam aquilo de guarda-chuva dos mortos, e riam.\n` |
| CA-2 | `tres-paginas.pdf`; `ROTEIRISTA_LIVROS` numa pasta vazia | `livro novo tres-paginas.pdf --slug teste`, depois `livro trecho` de `01.001` a `01.005` e `02.001` | última linha do `novo` é `2 capítulos, 6 parágrafos`; nenhum dos 6 trechos contém `O LIVRO DE TESTE`, `12`, `13` ou `14` |
| CA-3 | `tres-paginas.pdf` convertido com `--slug teste` | `livro trecho teste 01.004` e `livro trecho teste 01.005` | stdout exatamente `O padre chegou tarde e começou a missa sem esperar a família.\n` e `Depois da missa, o caixão foi levado em silêncio.\n` |

## Risco declarado
nenhum

## Como rodar os testes
Como na SPEC 001 (`pytest.ini` da raiz; executável `livro` no PATH; ausente = código `127`).

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/002-pdf-real --junitxml=relatorios/002-junit.xml
```

A suíte da 001 tem de continuar verde depois desta fatia.

## Arquivos que serão tocados (previsão)
- `src/roteirista/` (conversão de PDF)

## Arquivo-exemplo
O código da fatia 001 depois de aceito. Referência de comportamento: os passos "cabeçalhos, rodapés
e números impressos" e "vocabulário para decidir hifenização" do `converter` em
`ferramentas/livro.py` do piloto.

## Roteiro manual (3 passos)
1. Reconverta o Serpent e rode `livro trecho serpent 04.001`: nenhuma palavra partida com hífen e
   nenhum número de página no meio do parágrafo.
2. Procure no PDF uma página em que um parágrafo continua na seguinte, e confira com `trecho` que
   ele sai como um parágrafo só.
3. Confira, com `trecho`, um parágrafo que tenha `hell-on-earth` (cap. 08 do Serpent): o hífen do
   composto ficou.

## Decisões pendentes
nenhuma
