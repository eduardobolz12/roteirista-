# SPEC 018 — Pesquisa gratuita

**Estado:** exemplos aprovados pelo Decisor em 2026-11-11; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero fazer uma pergunta de fora do livro e receber só os fatos com citação conferida na
fonte, para que a pesquisa web não gaste nada e o Claude leia algumas linhas em vez de páginas
(D-008, D-027, E-006).

## Fronteira testada
CLI `livro`, com as variáveis das SPECs 017 e 042:
`livro pesquisar <slug> "<pergunta>" --busca "<termos>" [--wiki]`.

## Fora de escopo
- Buscadores comuns e notícias de jornal (D-027): o que não estiver no Europe PMC ou na Wikipédia vira
  lacuna para o Claude.
- Escrever a busca: os termos vêm de quem chama.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Busca:**
  - sem `--wiki`: `<ROTEIRISTA_EUROPEPMC>/search` com `query=<termos>`, `resultType=core`,
    `format=json`, `pageSize=10`; os 3 primeiros resultados com `abstractText` viram fonte pela URL
    `https://europepmc.org/article/<source>/<id>`, com os dados que já vieram na busca;
  - com `--wiki`: `<ROTEIRISTA_WIKIPEDIA>` com `action=query`, `list=search`, `srsearch=<termos>`,
    `srlimit=3`, `format=json`; cada título vira fonte como na SPEC 017, com a página inteira (no
    teste real, três páginas grandes, 117 mil caracteres, foram lidas em 11 segundos, com 4 de 4 citações
    conferidas).
  - As fontes são gravadas como na SPEC 017; uma URL já gravada usa a fonte existente.
- **Pedido:** à nuvem, como na SPEC 042 (modelos em ordem, mesmas mensagens e códigos), com o prompt
  `docs/prompts/pesquisar.txt`: `{pergunta}` trocado pela pergunta e `{fontes}` pelos parágrafos das
  fontes desta busca, no formato de `livro montar`.
- **Resposta do modelo:** linhas `<fato> | "<citação>" | <id de parágrafo>`; linhas fora do formato e
  `sem resposta` são ignoradas.
- **Conferência:** o id é de um parágrafo das fontes desta busca, e a citação está nele, comparando em
  NFKC, sem diferenciar maiúsculas, com espaços repetidos como um e aspas e travessões curvos como retos.
- **Saída:** primeiro uma linha por fonte da busca, `fonte <W> | <autor> | <ano> | <título>`; depois,
  em ordem, os fatos conferidos, `<id> | <fato> | "<citação>"`, e os outros como
  `recusado (id fora das fontes): <linha>` ou `recusado (citação não confere): <linha>` (o id é
  conferido antes da citação); por fim `<N> achados, <R> recusados — <modelo>`.
- **Nada achado:** a busca sem resultado com texto dá stdout `0 fontes`, código `1`, sem pedido à nuvem.
  **Busca fora do ar** ou resposta diferente de 200: stderr `busca falhou: <europepmc|wikipedia> (<motivo>)`,
  código `3`, nada gravado.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`) e um servidor falso para as APIs e para a nuvem:

- busca no Europe PMC por `awareness anaesthesia`: três resultados, `33333333` (sem resumo, o mesmo da SPEC 017), `11111111` (o mesmo da SPEC 017) e
  `22222222` (autores `Costa D.`, ano `2004`, título `A second test record.`, resumo
  `The incidence was 0.13%.`);
- busca na Wikipédia por `Test Book`: um título, `Test Book` (o mesmo da SPEC 017).

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro; `m1` responde `A incidência com bloqueio foi de ~1:8200. \| "The incidence with neuromuscular block was ~1:8200" \| W01.002`, `A incidência geral foi de 0,13%. \| "The incidence was 0.13%." \| W02.001`, `Pacientes acordam sempre. \| "Patients often wake during surgery." \| W01.001` e `O estudo foi em 1990. \| "The study ran in 1990." \| W09.001` | `livro pesquisar teste "Qual a incidência?" --busca "awareness anaesthesia"` | código `0`; stdout exatamente `fonte W01 \| Silva A et al. \| 2014 \| Awareness under anaesthesia: a test record.\nfonte W02 \| Costa D \| 2004 \| A second test record.\nW01.002 \| A incidência com bloqueio foi de ~1:8200. \| "The incidence with neuromuscular block was ~1:8200"\nW02.001 \| A incidência geral foi de 0,13%. \| "The incidence was 0.13%."\nrecusado (citação não confere): Pacientes acordam sempre. \| "Patients often wake during surgery." \| W01.001\nrecusado (id fora das fontes): O estudo foi em 1990. \| "The study ran in 1990." \| W09.001\n2 achados, 2 recusados — m1\n`; o pedido levou a pergunta e `## W02.001`; `livro trecho teste W02.001` dá `The incidence was 0.13%.\n` |
| CA-2 | o livro com só a W01, gravada por `livro fonte teste https://europepmc.org/article/MED/11111111`; `m1` responde `sem resposta` | `livro pesquisar teste "Quando saiu?" --busca "Test Book" --wiki`; depois a busca da CA-1 de novo | o primeiro dá exatamente `fonte W02 \| Wikipedia \| — \| Test Book\n0 achados, 0 recusados — m1\n`; o segundo começa por `fonte W01 \| Silva A et al.` e grava só a `W03`, para o `22222222` |
| CA-3 | o livro | `livro pesquisar teste "?" --busca "zumbi"` (busca vazia); a busca da CA-1 com o Europe PMC respondendo 500 | o primeiro dá `0 fontes\n`, código `1`, sem pedido à nuvem; o segundo sai com código `3` e `busca falhou: europepmc`, e `livro fontes teste` fica vazio |

## Risco declarado
A qualidade depende das palavras da busca (E-006: a pergunta P2 só achou o artigo na segunda busca).

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/018-pesquisa-gratuita --junitxml=relatorios/018-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, os módulos das SPECs 017 e 042, `docs/prompts/pesquisar.txt` (do arquiteto)

## Arquivo-exemplo
Os subcomandos `fonte` (SPEC 017) e `revisar` (SPEC 042).

## Roteiro manual (3 passos)
1. `livro pesquisar serpent "What is the incidence of awareness with neuromuscular block in NAP5?" --busca "NAP5 accidental awareness general anaesthesia summary main findings"`:
   um achado com `~1:8200`.
2. `livro pesquisar serpent "When was the book published and how was it received?" --busca "The Serpent and the Rainbow Wade Davis" --wiki`:
   achados com `1985` e com as críticas.
3. Leia dois achados com `livro trecho`: a citação está lá?

## Decisões pendentes
nenhuma
