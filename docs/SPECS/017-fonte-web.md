# SPEC 017 — Fonte web com ids

**Estado:** exemplos aprovados pelo Decisor em 2026-11-11; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que um artigo ou uma página da Wikipédia vire uma fonte do livro, com parágrafos de
id próprio, para que todo dado de fora entre no roteiro do mesmo jeito que o livro: citado por id e
conferido no texto literal, sem gasto (D-008, D-027, E-006).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`, `ROTEIRISTA_EUROPEPMC` e `ROTEIRISTA_WIKIPEDIA`:

- `livro fonte <slug> <url>`
- `livro fontes <slug>`
- `livro trecho <slug> <id>`, que passa a aceitar ids de fonte

## Fora de escopo
- Outros sites, PDFs da web e Wikipédia em outra língua que não o inglês.
- Texto completo de artigo: do Europe PMC vem só o resumo.
- Buscar: é a SPEC 018.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Endereços das APIs:** `ROTEIRISTA_EUROPEPMC`, padrão `https://www.ebi.ac.uk/europepmc/webservices/rest`;
  `ROTEIRISTA_WIKIPEDIA`, padrão `https://en.wikipedia.org/w/api.php`. Pedidos com o cabeçalho
  `User-Agent: roteirista/0.1`.
- **URLs aceitas:**
  - `https://europepmc.org/article/<FONTE>/<ID>` ou `.../abstract/<FONTE>/<ID>`: pede
    `<ROTEIRISTA_EUROPEPMC>/search` com `query=EXT_ID:<ID> AND SRC:<FONTE>`, `resultType=core`,
    `format=json`, e usa o primeiro resultado;
  - `https://en.wikipedia.org/wiki/<Título>`: pede `<ROTEIRISTA_WIKIPEDIA>` com `action=query`,
    `prop=extracts`, `explaintext=1`, `redirects=1`, `format=json`, `titles=<Título>` (sem o
    percent-encoding da URL).
  - Outra URL: stderr `fonte não suportada: <url>`, código `2`.
- **Id da fonte:** `W` e 2 dígitos, na ordem em que as fontes são gravadas no livro: `W01`, `W02`...
  **Id de parágrafo:** `<fonte>.<PPP>`, por exemplo `W01.002`.
- **Ficha da fonte:**
  - Europe PMC: autor = o `authorString` até a primeira vírgula, mais ` et al.` se houver vírgula, sem o
    ponto final; ano = `pubYear`; título = `title`.
  - Wikipédia: autor `Wikipedia`; ano `—`; título = o `title` da página devolvida.
- **Parágrafos:**
  - Europe PMC: o `abstractText`, cortado a cada `<h4>...</h4>` e `<title>...</title>` (o título
    sai) e a cada `<p>`; depois saem as marcas, que são só `<` seguido de letra ou `/`, até o `>`
    (`p<0.001` e `BIS <50` ficam); entidades HTML viram o caractere; sem cortes, um parágrafo só.
    Sem `abstractText`: stderr `fonte sem texto: <url>`, código `2` (no E-006, 7 de 25 resultados reais
    vieram assim).
  - Wikipédia: cada linha não vazia do `extract`; as linhas `== ... ==` saem; tudo a partir da seção
    `See also`, `Notes`, `References`, `Further reading` ou `External links` sai.
  - Em todos: NFC, espaços repetidos viram um, sem espaço nas pontas.
- **`fonte`:** stdout `<W> | <autor> | <ano> | <título>` e `<N> parágrafos`. URL já gravada:
  `<W> | já gravada`, código `0`, sem pedido; a URL é comparada sem o `#...` do fim e com o
  percent-encoding desfeito (`%28book%29` é `(book)`). Resultado vazio, ou página com `missing`: stderr `fonte não encontrada: <url>`,
  código `2`. API fora do ar ou resposta diferente de 200: stderr `fonte inacessível: <url>`, código `3`.
  Nos erros, nada é gravado.
- **`fontes`:** uma linha por fonte, em ordem: `<W> | <autor> | <ano> | <título> | <url>`, com a URL
  como foi dada (para a Wikipédia, `https://en.wikipedia.org/wiki/` e o título com `_` no lugar dos
  espaços). Sem fontes: stdout vazio, código `0`.
- **`trecho`** com id de fonte: o parágrafo literal, como na SPEC 001; id inexistente, como na SPEC 001.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`); um servidor falso faz o papel das duas APIs com os arquivos
de `fixtures/`:

- `europepmc/11111111.json`: autores `Silva A, Souza B, Lima C.`, ano `2014`, título
  `Awareness under anaesthesia: a test record.`, resumo
  `<h4>Background</h4>Patients may wake during surgery.<h4>Results</h4>The incidence with <i>neuromuscular</i> block was ~1:8200 (p<0.001).`
- `wikipedia/Test_Book.json`: título `Test Book`, texto
  `Test Book is a 1985 book.` / `== Overview ==` / `The book tells a story.` / `It inspired a 1988 film.` /
  `== References ==` / `Ref one.`

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro convertido | `livro fonte teste https://europepmc.org/article/MED/11111111` e `livro trecho teste W01.002` | o primeiro dá exatamente `W01 \| Silva A et al. \| 2014 \| Awareness under anaesthesia: a test record.\n2 parágrafos\n`; o segundo `The incidence with neuromuscular block was ~1:8200 (p<0.001).\n`; o pedido levou `EXT_ID:11111111 AND SRC:MED` |
| CA-2 | o livro com a W01 | `livro fonte teste https://en.wikipedia.org/wiki/Test_Book`, `livro fonte teste https://europepmc.org/article/MED/11111111` e `livro fontes teste` | o primeiro dá `W02 \| Wikipedia \| — \| Test Book\n3 parágrafos\n`; o segundo `W01 \| já gravada\n`, sem pedido; `fontes` dá exatamente as duas linhas com a URL no fim; `livro trecho teste W02.003` dá `It inspired a 1988 film.\n` e `W02.004` sai com `id inexistente: W02.004` |
| CA-3 | o livro convertido | `livro fonte teste https://example.com/x`; `livro fonte teste https://europepmc.org/article/MED/99999999` (resultado vazio); `.../MED/33333333` (resultado sem resumo); a mesma URL da CA-1 com a API respondendo 500 | códigos `2`, `2`, `2` e `3`, com `fonte não suportada: https://example.com/x`, `fonte não encontrada: https://europepmc.org/article/MED/99999999`, `fonte sem texto: https://europepmc.org/article/MED/33333333` e `fonte inacessível: https://europepmc.org/article/MED/11111111`; `livro fontes teste` fica vazio |

## Risco declarado
As APIs reais podem mudar o formato. A medição E-006 usou os mesmos campos em 2026-11-11.

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/017-fonte-web --junitxml=relatorios/017-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, `src/roteirista/banco.py`, um módulo novo para as APIs

## Arquivo-exemplo
O subcomando `trecho`.

## Roteiro manual (3 passos)
1. `livro fonte serpent https://europepmc.org/article/MED/25204697`: `W01 | Pandit JJ et al. | 2014 | 5th National Audit Project (NAP5)...`.
2. `livro trecho serpent W01.001`: o resumo contém `~1:8200`.
3. `livro fonte serpent "https://en.wikipedia.org/wiki/The_Serpent_and_the_Rainbow_(book)"` e
   `livro fontes serpent`: a W02 tem 5 parágrafos (medido em 2026-11-11), o último sobre as críticas, sem a seção de
   referências.

## Decisões pendentes
nenhuma
