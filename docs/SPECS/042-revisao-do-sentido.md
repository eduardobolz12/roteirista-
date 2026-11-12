# SPEC 042 — Revisão do sentido por modelo gratuito

**Estado:** exemplos aprovados pelo Decisor em 2026-11-11; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que um modelo gratuito leia o capítulo escrito junto com o material literal e aponte
o que o livro não sustenta, para que infidelidades como as do ensaio E-004 sejam pegas antes de mim, sem
gastar tokens do Claude (D-023, D-027, E-005).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`, `ROTEIRISTA_NUVEM`, `ROTEIRISTA_NUVEM_CHAVE` e `ROTEIRISTA_MODELOS`:
`livro revisar <slug> <texto> <ids>...`.

## Fora de escopo
- Corrigir o texto: o modelo só aponta; quem corrige é o Claude.
- Julgar estilo.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Nuvem:** `POST <ROTEIRISTA_NUVEM>/v1/chat/completions` (padrão `http://127.0.0.1:20128`, o
  9Router), cabeçalho `Authorization: Bearer <ROTEIRISTA_NUVEM_CHAVE>`, corpo `model`,
  `messages` com uma mensagem `user`, `temperature` 0, `max_tokens` 20000, `stream` false. A resposta
  vale como JSON (`choices[0].message.content`) ou como eventos `data:` (soma dos `delta.content`).
- **Modelos:** `ROTEIRISTA_MODELOS`, nomes separados por vírgula, tentados em ordem, uma vez cada.
  Padrão: `openrouter/baidu/ernie-5.5-flash-preview:free,openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`.
  Falha de um modelo (conexão, resposta diferente de 200, conteúdo vazio): stderr
  `modelo falhou, próximo: <modelo> (<motivo>)` e passa ao seguinte, sem esperar. Todos falharam:
  stderr `nenhum modelo gratuito respondeu`, código `3`. Sem `ROTEIRISTA_NUVEM_CHAVE`: stderr
  `chave da nuvem não informada: ROTEIRISTA_NUVEM_CHAVE`, código `2`, sem pedido.
- **Material:** os `<ids>`, com os intervalos e o formato de `livro montar` (SPEC 007); aceita também
  ids de fonte (`W01.002`, `W01.001-W01.003`). Id inexistente: como na SPEC 007.
- **Pedido:** o prompt `docs/prompts/revisar.txt`, com `{material}` trocado pelo material e `{texto}`
  pelo conteúdo do arquivo `<texto>`.
- **Resposta do modelo:** linhas `<frase> | <motivo> | <id ou "sem apoio">`; linhas fora desse formato
  e a palavra `nada` são ignoradas.
- **Conferência:** a frase tem de estar no texto, comparando em NFKC, sem diferenciar maiúsculas, com
  espaços repetidos como um, aspas curvas como retas e sem aspas nas pontas da frase.
  Campo do id que começa por `sem apoio` vale `sem apoio`, com o que vier depois ignorado
  (`sem apoio (cf. 15.089)`). Nos outros, valem todos os ids que aparecem no campo, em qualquer
  separação (`15.086, 15.089`, `15.086 / 15.089`, `15.081–15.085`): tem de haver pelo menos um, e todos
  têm de ser ids do material. (No E-005, 10 de 18 apontamentos vieram assim.)
- **Saída:** em ordem, um apontamento conferido por linha, `<ids> | <frase> | <motivo>`, com os ids
  achados separados por `, `, ou `sem apoio`; os outros
  como `descartado (frase fora do texto): <linha>` ou `descartado (id fora do material): <linha>`
  (a frase é conferida antes do id); por fim `<N> apontamentos, <D> descartados — <modelo>`.
  O stdout também é gravado em `<texto sem extensão>.revisao.txt`, ao lado do texto. O arquivo
  `<texto>` não muda.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`; capítulo 01: `O homem parou diante do túmulo e leu o próprio
nome gravado no cimento.`, `A irmã reconheceu o apelido de infância antes de reconhecer o rosto.`,
`Naquela tarde, ninguém na aldeia quis falar sobre o enterro.`) e `fixtures/texto.md`:
`Um homem leu o próprio nome num túmulo. A irmã o reconheceu pelo rosto. Naquela noite, a aldeia inteira fez festa.`
Um servidor falso faz o papel do 9Router; modelos `m1` e `m2`.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro; `m1` responde `A irmã o reconheceu pelo rosto. \| o livro diz que ela reconheceu o apelido antes do rosto \| 01.002`, `Naquela noite, a aldeia inteira fez festa. \| o livro diz que ninguém quis falar do enterro \| 01.003 / 01.001`, `Um homem chorou no túmulo. \| detalhe acrescentado \| sem apoio` e `Um homem leu o próprio nome num túmulo. \| ordem \| 02.001` | `livro revisar teste texto.md 01.001-01.003` | código `0`; stdout exatamente `01.002 \| A irmã o reconheceu pelo rosto. \| o livro diz que ela reconheceu o apelido antes do rosto\n01.003, 01.001 \| Naquela noite, a aldeia inteira fez festa. \| o livro diz que ninguém quis falar do enterro\ndescartado (frase fora do texto): Um homem chorou no túmulo. \| detalhe acrescentado \| sem apoio\ndescartado (id fora do material): Um homem leu o próprio nome num túmulo. \| ordem \| 02.001\n2 apontamentos, 2 descartados — m1\n`; `texto.revisao.txt` igual ao stdout; o pedido levou `## 01.002` e o texto; `texto.md` igual ao de antes |
| CA-2 | o livro; `m1` responde 429; `m2` responde, em eventos `data:`, `Naquela noite, a aldeia inteira fez festa. \| festa inventada \| sem apoio (cf. 01.003)` | `livro revisar teste texto.md 01.001-01.003` com `ROTEIRISTA_MODELOS=m1,m2` | código `0`; stderr com `modelo falhou, próximo: m1`; stdout exatamente `sem apoio \| Naquela noite, a aldeia inteira fez festa. \| festa inventada\n1 apontamentos, 0 descartados — m2\n`; 2 pedidos, o segundo com `model` `m2` |
| CA-3 | o livro; `m1` responde 429 e `m2` responde 500 | `livro revisar` como na CA-2; e de novo sem `ROTEIRISTA_NUVEM_CHAVE` | o primeiro sai com código `3`, `nenhum modelo gratuito respondeu` e sem `texto.revisao.txt`; o segundo com código `2`, `chave da nuvem não informada: ROTEIRISTA_NUVEM_CHAVE`, sem pedido |

## Risco declarado
Os modelos gratuitos mudam (E-005): a lista padrão pode envelhecer. Por isso ela vem de
`ROTEIRISTA_MODELOS`.

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/042-revisao-do-sentido --junitxml=relatorios/042-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, um módulo novo para a nuvem, `docs/prompts/revisar.txt` (do arquiteto)

## Arquivo-exemplo
O subcomando `montar`.

## Roteiro manual (3 passos)
1. Com o 9Router aberto, rode `livro revisar serpent docs/experimentos/E-005/rascunho.md 15.073-15.091 16.147 20.001`:
   aparecem as 4 infidelidades do E-005 (ordem, túmulo, vela, povo inteiro).
2. Rode com `docs/experimentos/E-004/cap-1.md`: poucos apontamentos (0 a 3), nenhum dos quatro.
3. Feche o 9Router e rode de novo: `nenhum modelo gratuito respondeu`, código 3.

## Decisões pendentes
nenhuma
