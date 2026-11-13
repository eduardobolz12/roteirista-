---
name: humanizar
description: Humaniza a tradução de um tema (roteiro-<língua>.md) para ser ouvida por quem não é nativo — frases curtas, palavras comuns, sem expressão idiomática e sem vícios de texto de IA — sem mudar fato, número, nome, ressalva ou citação; confere o sentido contra o português, roda `livro invariantes`, `livro glossario --conferir` e `livro legibilidade`, gera a retrotradução local e a tela lado a lado para o Decisor aprovar em português.
disable-model-invocation: true
argument-hint: <slug> <número do tema> <en|fr>
---

# Humanizar

Argumentos (`$ARGUMENTS`): o slug, o número do tema e a língua. Pasta do tema: `livros/<slug>/temas/<n>/`
(nos comandos abaixo, `<pasta>`). Entrada: `roteiro-<língua>.md`. Saída: `roteiro-<língua>-humanizado.md`,
`humanizacao.md`, a retrotradução `retro-pt-roteiro-<língua>-humanizado.md` e a tela
`lado-a-lado-roteiro-<língua>-humanizado.html`.

Antes de tudo, leia `docs/prompts/roteiro-regras.md` e `docs/prompts/vicios-de-ia.md`. Valem os dois.

## Por que assim

A tradução é fiel, mas foi escrita para ser lida, e o vídeo é ouvido por quem fala a língua como segunda
língua. A humanização deixa o texto simples e natural de ouvir sem mudar o que ele diz (D-011). A meta é
clareza e fidelidade para quem ouve, não passar em detector de IA (E-010).

O Decisor não lê inglês nem francês. O modelo local retraduz o resultado para o português, sem tokens, e o
Decisor aprova na tela lado a lado, capítulo a capítulo (D-012). O Claude avalia mal o próprio texto (E-010):
por isso a conferência é dos scripts, do modelo local e do Decisor, e nenhuma nota é dada aqui.

## Pré-condições

- `roteiro-<língua>.md` existe, e `traducao.md` registra 0 alertas nas duas conferências e a data do
  `roteiro-pt.md` traduzido. Se o `roteiro-pt.md` mudou depois dessa data, a tradução está desatualizada:
  pare e avise o Decisor.
- Leia `decisoes.md`: o que ele protege não muda.
- Se `roteiro-<língua>-humanizado.md` já existe, pare e pergunte. Só se refaz a pedido do Decisor, ou para
  aplicar as sugestões dele (passo 8).

## Passos

1. **Medir.** Rode `livro legibilidade <slug> <pasta>/roteiro-<língua>.md`: as frases longas, as palavras
   raras e as expressões, por parágrafo.

2. **Marcar.** Leia o texto inteiro uma vez e marque, por parágrafo:
   - cada item da legibilidade;
   - os vícios de `vicios-de-ia.md`, pelo número, os fortes primeiro;
   - o que atrapalha quem ouve: frase que pode ser entendida de dois jeitos, pronome com referente
     duvidoso, o mesmo assunto com dois nomes (V19), mais de uma ideia por frase.

   Um vício forte basta para mexer; um fraco, só com outro no mesmo parágrafo. Vale a lista "Quando não
   mexer". Texto que já está bom fica: mexer demais é falha.

3. **Reescrever, parágrafo por parágrafo.** Um parágrafo humanizado para cada parágrafo da tradução, nos
   mesmos capítulos. Reescreva o parágrafo em volta da ideia; não remende palavra por palavra.
   - **Fica igual:**
     - cada fato, número, data, nome e atribuição;
     - as citações (`"..." [id]`, caractere por caractere);
     - as ressalvas com alcance ("almost", "at least", "up to", "according to");
     - as marcas de leitura e a dúvida do narrador;
     - os termos do glossário.
   - **Fica simples, para o ouvido:**
     - frases de 15 palavras em média, nunca acima de 25;
     - o fato principal antes da oração subordinada;
     - uma ideia por frase, sem dupla negação;
     - o substantivo repetido quando o pronome deixar dúvida, e um nome só para cada coisa;
     - palavra rara trocada pela comum que diz o mesmo (`unjustly → unfairly`), e expressão idiomática
       trocada pelo sentido literal (`up close → well`). Se a troca perde sentido, a palavra fica.
   - **Fica natural:**
     - frases de tamanhos variados;
     - a voz do narrador em primeira pessoa;
     - sem os vícios marcados.
   - **Não invente.** Se a frase pede um dado que o português não dá, ela fica mais simples. Nada entra
     para "dar vida".

4. **Passada de sentido.** Para cada parágrafo, compare o humanizado com o `roteiro-pt.md`, não com a
   tradução.
   - **Sentido.** Procure: acréscimo, omissão, sentido trocado, nuance deslocada ("devagar" virando
     "gently") e termo diferente do glossário.
   - **Fluência.** Procure tradução literal: imagem ao pé da letra, ordem de palavras do português, falso
     cognato e regência (`.claude/skills/traduzir/falsos-cognatos.md`).
   - **Leitura em voz alta.** Leia o capítulo como quem ouve pela primeira vez. Frase que pode ser entendida
     de dois jeitos muda.

5. **Conferir.** Rode até as três darem 0 alertas:
   - `livro invariantes <slug> <pasta>/roteiro-<língua>.md <pasta>/roteiro-<língua>-humanizado.md`;
   - `livro invariantes <slug> <pasta>/roteiro-pt.md <pasta>/roteiro-<língua>-humanizado.md`;
   - `livro glossario <slug> <língua> --conferir <pasta>/roteiro-pt.md <pasta>/roteiro-<língua>-humanizado.md`.

   Depois, rode `livro legibilidade <slug> <pasta>/roteiro-<língua>-humanizado.md`. O que sobrar precisa de
   motivo (palavra sem troca fiel, expressão comum) anotado em `humanizacao.md`.

6. **Retrotradução e tela.**
   - Rode `livro retraduzir <slug> <pasta>/roteiro-<língua>-humanizado.md` em segundo plano: o modelo local
     leva de 6 a 10 minutos por tema.
   - Depois, rode `livro lado-a-lado <slug> <pasta>/roteiro-pt.md <pasta>/roteiro-<língua>-humanizado.md <pasta>/retro-pt-roteiro-<língua>-humanizado.md`.
   - Leia a retrotradução parágrafo por parágrafo. O modelo local faz o papel de um ouvinte de teste (E-010).
     Quando ele entende errado, pergunte primeiro se o texto humanizado permite aquela leitura:
     - se permite, o humanizado muda, e os passos 4 a 6 rodam de novo para aquele parágrafo;
     - se não permite, o erro é do modelo. Anote em `humanizacao.md`, para o Decisor saber o que não é do
       texto.

7. **Gravar `humanizacao.md`** no formato abaixo. Diga ao Decisor para abrir a tela e decidir cada
   capítulo: aprovado, aprovado com sugestões (em português, citando o §) ou refazer. Diga também as
   escolhas que são dele.

8. **Sugestões do Decisor.** Aplique cada sugestão no texto humanizado e rode de novo os passos 4 a 6.
   Acrescente em `decisoes.md` o que ele aprovou (D-016).

## Formato de `humanizacao.md`

```markdown
# Humanização — Tema <n> <título> (<língua>)

**Estado:** humanizado em <data>; aguardando o Decisor na tela lado a lado
**Conferências:** invariantes (tradução → humanizado e português → humanizado) 0 alertas; glossário <T> termos, 0 alertas.
**Legibilidade:** antes <F> frases longas, <R> raras, <E> expressões; depois <F'>, <R'>, <E'>.
**O que ficou e por quê:** <§: palavra ou expressão: motivo> (ou "nada").
**Vícios corrigidos:** <V<n>: quantidade; ...> (ou "nenhum").
**Passada de sentido:** <§: tipo (acréscimo, omissão, sentido trocado, nuance, literal, ambíguo): o que mudou> (ou "nada").
**Erros da retrotradução (o texto está certo):** <§: o que ela diz> (ou "nenhum").
**Escolhas para o Decisor:** <§: a questão e as opções> (ou "nenhuma").
**Capítulos aprovados:** <k: aprovado | com sugestões | refazer> (o Decisor preenche na conversa)
```

## No fim

Diga em poucas linhas:
- as conferências com 0 alertas;
- a legibilidade antes e depois;
- o que a passada de sentido mudou;
- os erros da retrotradução que não são do texto;
- as escolhas do Decisor;
- o caminho da tela.

O Decisor decide cada capítulo.
