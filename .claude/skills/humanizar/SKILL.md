---
name: humanizar
description: Humaniza a tradução de um tema (roteiro-<língua>.md) para ser ouvida por quem não é nativo — frases curtas, palavras comuns, sem expressão idiomática e sem vícios de texto de IA — sem mudar fato, número, nome ou citação; grava roteiro-<língua>-humanizado.md, confere com `livro invariantes` e `livro legibilidade`, gera a retrotradução local e a tela lado a lado para o Decisor aprovar em português.
disable-model-invocation: true
argument-hint: <slug> <número do tema> <en|fr>
---

# Humanizar

Argumentos (`$ARGUMENTS`): o slug, o número do tema e a língua. Pasta: `livros/<slug>/temas/<n>/`.
Entrada: `roteiro-<língua>.md`. Saída: `roteiro-<língua>-humanizado.md`, `humanizacao.md`, a retrotradução
`retro-pt-roteiro-<língua>-humanizado.md` e a tela `lado-a-lado-roteiro-<língua>-humanizado.html`.

Antes de tudo, leia `docs/prompts/roteiro-regras.md`. Valem as regras de lá.

## Por que assim

A tradução é fiel, mas foi escrita para ser lida, e o vídeo é ouvido por quem fala a língua como segunda
língua. A humanização deixa o texto simples e natural de ouvir, sem mudar o que ele diz (D-011). O
Decisor não lê inglês nem francês: o modelo local retraduz o resultado para o português, sem tokens, e
ele aprova na tela lado a lado, capítulo a capítulo (D-012).

## Pré-condições

- `roteiro-<língua>.md` existe e `traducao.md` registra 0 alertas nas duas conferências.
- Leia `decisoes.md`: o que ele protege não muda.
- Se `roteiro-<língua>-humanizado.md` já existe, pare e pergunte: só se refaz a pedido do Decisor, ou para
  aplicar as sugestões dele (passo 7).

## Passos

1. **Medir.** `livro legibilidade <slug> roteiro-<língua>.md`: as frases longas, as palavras raras e as
   expressões, por parágrafo.

2. **Marcar.** Leia o texto inteiro uma vez e marque, por parágrafo:
   - cada item da legibilidade;
   - os vícios de texto de IA, mais fortes primeiro: contraste que só dá peso ("not X, but Y"); frase
     curta de efeito que fecha o parágrafo sem fato novo; frase que soa profunda e não diz nada; rodeio
     antes do ponto; resposta a uma objeção que ninguém fez; trio forçado; a mesma abertura de frase em
     sequência; travessão em toda parte; ressalva sobre ressalva; voz passiva que esconde quem fez;
     palavra inflada ("crucial", "pivotal", "testament", "delve"); importância inflada ("forever
     changed"); "-ing" solto no fim da frase ("…, highlighting the…"); linguagem de folheto sobre outra
     cultura; autoridade emprestada ("experts say"); explicar de novo o que o ouvinte já sabe.

   Um vício forte basta para mexer; um fraco só com outro no mesmo parágrafo. Dentro de citação, nome
   próprio e verso, nada se mexe.

3. **Reescrever, parágrafo por parágrafo.** Um parágrafo humanizado para cada parágrafo da tradução,
   nos mesmos capítulos.
   - **Fica igual:** cada fato, número, data, nome, atribuição e citação (`"..." [id]` caractere por
     caractere), as marcas de leitura do narrador e os termos do glossário.
   - **Fica simples:** frase de até 25 palavras; palavra rara pela comum que diz o mesmo (`unjustly →
     unfairly`, `accuser → the person who accused`); expressão idiomática pelo sentido literal (`up
     close → well`). Se a troca perde sentido, a palavra fica.
   - **Fica natural:** frases de tamanhos variados, a voz do narrador em primeira pessoa, sem os vícios do
     passo 2.

4. **Conferir.** Rode até as três darem 0 alertas:
   - `livro invariantes <slug> roteiro-<língua>.md roteiro-<língua>-humanizado.md`;
   - `livro invariantes <slug> roteiro-pt.md roteiro-<língua>-humanizado.md`;
   - `livro glossario <slug> <língua> --conferir roteiro-pt.md roteiro-<língua>-humanizado.md`.

   Depois, `livro legibilidade <slug> roteiro-<língua>-humanizado.md`. O que sobrar precisa de motivo
   (palavra sem troca fiel, expressão comum) anotado em `humanizacao.md`.

5. **Retrotradução e tela.** Rode `livro retraduzir <slug> roteiro-<língua>-humanizado.md` em segundo
   plano: o modelo local leva uns 8 a 10 minutos por tema. Depois rode
   `livro lado-a-lado <slug> roteiro-pt.md roteiro-<língua>-humanizado.md retro-pt-roteiro-<língua>-humanizado.md`.
   A tela marca os parágrafos com alerta; o que vier da retrotradução é erro dela, não do texto.

6. **Gravar `humanizacao.md`** no formato abaixo e diga ao Decisor para abrir a tela e decidir cada
   capítulo: aprovado, aprovado com sugestões (em português, citando o §) ou refazer.

7. **Sugestões do Decisor.** Aplique cada sugestão no texto humanizado, rode de novo os passos 4 e 5 e
   acrescente em `decisoes.md` o que ele aprovou (D-016).

## Formato de `humanizacao.md`

```markdown
# Humanização — Tema <n> <título> (<língua>)

**Estado:** humanizado em <data>; aguardando o Decisor na tela lado a lado
**Conferências:** invariantes (tradução → humanizado e português → humanizado) 0 alertas; glossário 0 alertas.
**Legibilidade:** antes <F> frases longas, <R> raras, <E> expressões; depois <F'>, <R'>, <E'>.
**O que ficou e por quê:** <parágrafo: palavra ou expressão: motivo> (ou "nada").
**Vícios corrigidos:** <tipo: quantidade; ...>
**Capítulos aprovados:** <k: aprovado | com sugestões | refazer> (o Decisor preenche na conversa)
```

## No fim

Diga em poucas linhas: as conferências com 0 alertas, a legibilidade antes e depois e o caminho da tela.
O Decisor decide cada capítulo.
