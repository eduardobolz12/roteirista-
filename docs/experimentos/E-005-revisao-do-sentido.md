# E-005 — Revisão do sentido por modelo gratuito

**Data:** 2026-11-11 · **Decisão relacionada:** D-023 · **Fatia que mede:** 042

## Pergunta
Um modelo gratuito na nuvem, lendo o capítulo escrito junto com o material literal, acha as afirmações
que o livro não sustenta? Falso alarme no texto correto é tolerável?

## Montagem
- **Material:** `E-004/cap-1-material.md` (ids 15.073–15.091, 16.147, 20.001; cerca de 5,6 mil caracteres).
- **Rascunho:** o capítulo 1 aprovado (`E-004/cap-1.md`) com as 4 infidelidades do primeiro rascunho do
  E-004 reinseridas (`rascunho.md`):
  1. ordem trocada: o secretário lê a data antes de o caixão entrar;
  2. contraste inventado: "ninguém o chama de túmulo";
  3. detalhe sem apoio: Davis "com uma vela acesa nas mãos";
  4. generalização: "um povo inteiro" em vez da sociedade.
- **Controle:** o capítulo aprovado, sem as infidelidades (`final.md`).
- **Caminho:** 9Router local (`127.0.0.1:20128`) → OpenRouter, só modelos `:free`; temperatura 0;
  prompt em `revisar.py`. Saída em linhas `frase | motivo | id`.

## Resultado

| Modelo | Rascunho: infidelidades achadas | Correto: apontamentos |
|---|---|---|
| ERNIE 5.5 Flash (rodada 1) | **4 de 4** | 1 |
| ERNIE 5.5 Flash (rodada 2) | **4 de 4** (+1 falso) | 3 |
| Nemotron 3 Ultra | 1 de 4 (só a ordem) | 1 |
| Gemma 4 31B | limite de uso do provedor (429) | — |
| Inkling 2 Small | recusado: só para "agentic harnesses" | — |

Apontamentos no texto correto, julgados pelo arquiteto:
- "faz essas pessoas jurarem silêncio diante de um caixão" — o canto de silêncio vem **antes** de o
  caixão entrar (15.081–15.086), e é canto de advertência, não juramento. **Procedente**: o arquiteto
  não tinha visto. Apontado pelos dois modelos.
- "Dá a volta no terreiro" — o livro diz em volta do *poteau mitan*. **Procedente, menor.**
- "uma noite de março" — o livro não diz "noite" nesses trechos. **Discutível** (velas, sessão noturna).
- "Quem assistia era Wade Davis" — o narrador em primeira pessoa é Davis, mas o material não diz o nome.
  **Falso alarme.**

Custo: cerca de 4 mil tokens de entrada e 4 a 5 mil de saída (quase tudo raciocínio) por chamada, 20 a 70
segundos, de graça. Com menos de 20 mil tokens de saída permitidos, os modelos esgotam o raciocínio e
devolvem resposta vazia.

## Conclusão
1. **Funciona com o modelo certo.** O ERNIE achou as 4 infidelidades duas vezes; o Nemotron não serve.
2. **Acha coisas que o arquiteto perdeu.** O "juram silêncio diante do caixão" passou no ensaio aprovado.
3. **O ruído é pequeno e barato de julgar.** O Claude lê só as linhas apontadas (algumas centenas de
   tokens) e confere cada uma com `livro trecho`; o capítulo não volta inteiro para o Claude.
4. **O grátis é instável.** Em uma hora: 2 de 4 modelos indisponíveis, e o OpenCode Free inteiro fora
   do ar. A fatia 042 precisa de uma lista de modelos em ordem de preferência e de um erro claro quando
   nenhum responde, não silêncio.
5. Limite do OpenRouter grátis: cerca de 50 pedidos por dia; um vídeo usa 6 a 12 revisões.

**Aplicado em 2026-11-11, com aprovação do Decisor:** `E-004/cap-1.md` corrigido nas duas frases
procedentes ("poste central do terreiro"; "cantarem que engolem a língua se contarem").

## Para a SPEC 042
- Entrada: o capítulo escrito e os ids que ele cita; o comando monta o material literal pelos ids.
- Saída do modelo: `frase | motivo | id`; o script confere que a frase existe no capítulo e que o id
  existe no livro, e descarta o resto.
- Guarda as duas versões (D-023) e a lista apontada; não altera o capítulo.
- Modelos em ordem, com reserva; `max_tokens` alto; falha de todos vira erro com código.
