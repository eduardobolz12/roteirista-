# E-003 — Língua do índice

Rodado em 2026-11-10 pelo arquiteto, depois do aceite do lote 1, que mostrou o índice em português
perdendo números e detalhes. Mesmas condições do E-002 (`qwen3:14b`, temperatura 0, janelas de 2000
tokens). Saídas em `E-003/`. A conferência de âncora aqui é como palavra inteira na rodada C, e como
trecho de texto nas rodadas A e B.

## Rodadas

| Rodada | Fichas válidas | Recusadas | Cobertura | Números do gabarito (4) | Tamanho do índice | Tempo |
|---|---|---|---|---|---|---|
| Cap. 06, português (prompt do lote 1) | 61 | 5% | 33/38 | 1 | 20% do capítulo | 2 min 40 s |
| A — cap. 06, inglês, mesmas regras | 46 | 12% | 31/38 | 4 | 25% | 3 min 10 s |
| B — cap. 06, inglês, "todo número" | 90 | 13% | 32/38 | 4 | 52% | 6 min 10 s |
| **C — cap. 06, inglês ajustado** | **60** | **12%** | **35/38** | **4** | **37%** | **4 min 20 s** |
| **C — cap. 14, inglês ajustado** | **164** | **7%** | **59/59** | — | **29%** | **13 min 50 s** |

O gabarito são os 4 números do capítulo 06 que o Sonnet achou no piloto (E-001): as doses medidas em
horas (06.021), as duas ou três semanas (06.023), os 400 mil escravos (06.028) e as oito sementes
(06.033). O prompt da rodada C está em `docs/prompts/indexar-livro.txt`.

## O que mudou

Em inglês, o modelo deixa de resumir e passa a copiar a frase-chave do autor (89% das fichas na
rodada A). Por isso voltam os números e os detalhes, e some o erro de sentido do lote 1 (a pergunta
irônica de Schultes em 06.018). A rodada C também achou o "quite possibly" de Schultes (06.020).

## O que continua errado

- Frases longas: 25 de 60 (cap. 06) e 45 de 164 (cap. 14) passam de 25 palavras.
- Frases sem contexto, que começam por pronome: 7 e 19.
- A mesma frase no mesmo parágrafo: 4 e 7. A frase contida em outra: 2 e 3.
- Tipo errado: `South Station` como `numero`; o "quite wrong" de 06.038 como `caso`.
- Na primeira tentativa do cap. 14, o Ollama respondeu erro 500 e a rodada caiu. Na segunda, passou.
- A conferência como trecho de texto aceitou `six` dentro de `sixteenth` (rodada A).

## Conclusões

1. Índice na língua do livro, com o prompt da rodada C (SPEC 039).
2. Âncora como palavra inteira e a mesma frase juntada pelo sistema (SPEC 039).
3. Nova tentativa quando o Ollama falha (SPEC 040).
4. Pedir "todo número" não compensa: dobra o índice sem achar mais do gabarito.
