# SPEC 023 — Glossário por livro e língua

**Estado:** exemplos aprovados pelo Decisor em 2026-11-12; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que cada termo do roteiro tenha uma tradução fixa por livro e língua, conferida em
cada parágrafo, para que o mesmo termo não apareça traduzido de dois jeitos no vídeo (D-011, D-029).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro glossario <slug> <língua> [<termo> <tradução> | --conferir <português> <tradução>]`.

## Fora de escopo
- Escolher a tradução: é do Claude no `/traduzir`, com o Decisor.
- Conferir nomes e números: é a SPEC 024.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Língua:** `en` ou `fr`. Outra: stderr `língua inválida: <língua>`, código `2`.
- **Termo e tradução:** texto livre; formas alternativas separadas por `|` (`sociedade|sociedades`). O termo,
  como escrito, é a chave: gravar o mesmo termo de novo troca a tradução. O glossário fica no banco do
  livro, separado por língua.
- **Gravar** (`<termo> <tradução>`): stdout `gravado: <termo> → <tradução>`, ou, se o termo já existia,
  `trocado: <termo>: <tradução antiga> → <tradução nova>`; código `0`.
- **Listar** (sem mais argumentos): uma linha `<termo> → <tradução>` por termo, em ordem alfabética sem
  diferenciar maiúsculas; por fim `<N> termos (<língua>)`; código `0`.
- **Roteiro:** Markdown com capítulos `## <n>` e parágrafos separados por linha em branco; o título e as
  linhas que começam por `#` não contam. O texto das citações (`"..." [id]`, regra da SPEC 022) não conta.
- **Conferir** (`--conferir <português> <tradução>`): os capítulos são casados pelo número e os parágrafos
  pela ordem. Capítulo com número de parágrafos diferente: `cap. <n>: <a> parágrafos no português, <b> na
  tradução`, e ele não é conferido. Em cada par, para cada termo, em ordem alfabética: se alguma forma do
  termo aparece no parágrafo em português (palavra inteira, sem diferenciar maiúsculas) e nenhuma forma da
  tradução aparece no parágrafo traduzido: `<n>.<p>: <termo> sem <tradução>`. Por fim
  `<T> termos, <A> alertas`; código `1` se houver alerta, senão `0`. Arquivo que não existe: como na
  SPEC 016.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`) e, em `fixtures/`:

- `roteiro-pt.md`: três capítulos, seis parágrafos (`## 1`: o cemitério de Benetier e o túmulo; a citação
  `"leu o próprio nome gravado no cimento" [01.001]` e a sociedade; Alderick e os dois irmãos.
  `## 2`: a cruz do Barão Samedi e os quatro líderes em 1962; a sociedade que nunca esqueceu.
  `## 3`: "Benetier ainda espera.").
- `roteiro-en.md`: a tradução fiel, com "tomb", "society" e "Baron".
- `roteiro-en-glossario.md`: a mesma, com "grave" no lugar de "tomb" (1.1) e "association" no lugar de
  "society" (2.2).

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro | `livro glossario teste en sociedade "society\|societies"`, `livro glossario teste en Barão Baron`, `livro glossario teste en sociedade association` e `livro glossario teste en` | os três primeiros com código `0` e stdout exatamente `gravado: sociedade → society\|societies\n`, `gravado: Barão → Baron\n` e `trocado: sociedade: society\|societies → association\n`; o último exatamente `Barão → Baron\nsociedade → association\n2 termos (en)\n` |
| CA-2 | o livro com `sociedade → society\|societies`, `túmulo\|túmulos → tomb\|tombs` e `Barão → Baron` | `livro glossario teste en --conferir roteiro-pt.md roteiro-en.md` | código `0`; stdout exatamente `3 termos, 0 alertas\n` |
| CA-3 | o mesmo glossário | `livro glossario teste en --conferir roteiro-pt.md roteiro-en-glossario.md` e `livro glossario teste de` | o primeiro com código `1` e stdout exatamente `1.1: túmulo\|túmulos sem tomb\|tombs\n2.2: sociedade sem society\|societies\n3 termos, 2 alertas\n`; o segundo com código `2` e `língua inválida: de` no stderr |

## Risco declarado
nenhum

## Como rodar os testes
```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/023-glossario --junitxml=relatorios/023-junit.xml
```
As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, o banco do livro (tabela nova, criada sem perder livro antigo, SPEC 038) e um
  módulo para as conferências da tradução.

## Arquivo-exemplo
O subcomando `fonte` (gravar no banco do livro) e o validador da SPEC 022 (citações).

## Roteiro manual (3 passos)
1. Grave no Serpent os 17 termos do E-008 e rode `livro glossario serpent en`: a lista em ordem, `17 termos (en)`.
2. `livro glossario serpent en --conferir livros/serpent/temas/1/roteiro-pt.md livros/serpent/temas/1/roteiro-en.md`:
   `17 termos, 0 alertas`.
3. Numa cópia do inglês, troque um "society" por "association" e confira de novo: o alerta aparece no parágrafo certo.

## Decisões pendentes
nenhuma
