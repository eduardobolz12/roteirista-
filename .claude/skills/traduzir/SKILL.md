---
name: traduzir
description: Traduz o roteiro em português de um tema (os 6 capítulos) para o inglês ou o francês — pergunta qual —, parágrafo por parágrafo, com o glossário do livro, citações copiadas iguais, números, nomes e ressalvas exatos; faz a segunda passada por exatidão, fluência, estilo e termos; grava livros/<slug>/temas/<n>/roteiro-<língua>.md e confere com `livro glossario --conferir` e `livro invariantes` até 0 alertas.
disable-model-invocation: true
argument-hint: <slug> <número do tema> [en|fr]
---

# Traduzir

Argumentos (`$ARGUMENTS`): o slug, o número do tema e a língua (`en` ou `fr`). Sem a língua, pergunte ao
Decisor "Traduzir para o inglês (en) ou para o francês (fr)?" e espere. Pasta do tema:
`livros/<slug>/temas/<n>/` (nos comandos abaixo, `<pasta>`). Saída: `roteiro-<língua>.md`, `traducao-<língua>.md`
e os termos novos no glossário do livro.

Antes de tudo, leia `docs/prompts/roteiro-regras.md`. Valem as regras de lá.

## Por que assim

A tradução é fiel. Quem deixa o texto fácil de ouvir é a humanização, depois (D-011). Separadas, cada uma
pode ser conferida:
- aqui, o script confere que nada mudou (citação, número, nome, termo);
- lá, confere-se que o texto ficou simples sem mudar o que diz.

Bonito nunca vence fiel: se a frase fiel soa dura, ela fica dura, e a `/humanizar` cuida dela. Uma língua
por vez.

## Pré-condições

- `roteiro-pt.md` existe e `revisao.md` marca uma passada aplicada.
- Leia `decisoes.md`: o que ele protege (verso, texto fixado) passa para a tradução como foi decidido.
- Se `roteiro-<língua>.md` já existe, pare e pergunte ao Decisor se é para refazer.

## Passos

1. **Glossário.**
   - Rode `livro glossario <slug> <língua>` para ver os termos já gravados.
   - Leia `roteiro-pt.md` e anote os termos que se repetem e precisam de tradução fixa: conceitos do tema,
     cargos, instituições, objetos que voltam (`facão → machete`) e nomes que mudam de uma língua para outra
     (`Barão → Baron`). Nome de pessoa que não muda não entra.
   - Cada termo leva as formas (`sociedade|sociedades → society|societies`). Quando o português usa
     adjetivo para o mesmo nome, entram os dois (`Estados Unidos|americano|americana → United
     States|American`).
   - Mostre ao Decisor os termos novos numa tabela curta e grave os aprovados com
     `livro glossario <slug> <língua> "<termo>" "<tradução>"`.

2. **Tradução, parágrafo por parágrafo.** Um parágrafo traduzido para cada parágrafo do português, com os
   mesmos capítulos (`## <k>`): a tela lado a lado e as conferências casam os parágrafos pela ordem.
   - Citação `"..." [id]` copiada igual, caractere por caractere: ela já está na língua do livro (D-028).
   - Números, datas, nomes e atribuições exatos ("ambos" é "both"; "a família" não vira "the sisters").
   - Ressalvas com alcance exatas: "quase", "pelo menos", "até", "mais de", "segundo X". Tirar uma muda o
     fato (`docs/prompts/vicios-de-ia.md`, "Quando não mexer").
   - As marcas de leitura continuam marcas de leitura ("me parece" → "it seems to me"): a leitura do
     narrador nunca vira fato.
   - Frases de até 25 palavras. Se o português tem uma frase longa, divida na tradução.
   - O narrador se apresenta como no piloto: "I'm Alderick, and…".
   - Termo do glossário sempre pela tradução gravada.

3. **Segunda passada, parágrafo por parágrafo, contra o português.** Quatro critérios (E-010):
   - **Exatidão:** acréscimo, omissão, sentido trocado, nuance deslocada, trecho sem traduzir.
   - **Fluência:** gramática; ordem natural da língua de chegada; falso cognato, imagem ao pé da letra e
     regência (`falsos-cognatos.md`, nesta pasta).
   - **Estilo:** a voz do narrador; a leitura dita como leitura.
   - **Termos:** o glossário, e um nome só para cada coisa no roteiro inteiro.

   Depois, leia a tradução do começo ao fim, como quem vai ouvir: pronome com referente certo, frase que
   não pode ser entendida de dois jeitos.

   A passada não substitui as conferências nem a tela: o Claude avalia mal a própria tradução.

4. **Conferências.** Rode até as duas darem 0 alertas:
   - `livro glossario <slug> <língua> --conferir <pasta>/roteiro-pt.md <pasta>/roteiro-<língua>.md`;
   - `livro invariantes <slug> <pasta>/roteiro-pt.md <pasta>/roteiro-<língua>.md`.

   Alerta se corrige na tradução, nunca no português. Se for falso alarme da regra, anote em `traducao-<língua>.md`
   com o motivo, e o Decisor decide.

5. **Legibilidade.** Rode `livro legibilidade <slug> <pasta>/roteiro-<língua>.md` e anote os números. Não
   simplifique aqui: a lista é o ponto de partida da `/humanizar`.

6. **Gravar `traducao-<língua>.md`** no formato abaixo, com a data de modificação do `roteiro-pt.md` traduzido. Se o
   português mudar depois, a tradução fica desatualizada, e a `/humanizar` para.

## Formato de `traducao-<língua>.md`

```markdown
# Tradução — Tema <n> <título> (<língua>)

**Estado:** traduzido em <data>
**Fonte:** roteiro-pt.md de <data e hora de modificação>
**Conferências:** glossário <T> termos, 0 alertas; invariantes <P> parágrafos, 0 alertas.
**Legibilidade:** <F> frases longas, <R> palavras raras, <E> expressões.
**Termos novos no glossário:** <termo → tradução; ...> (ou "nenhum").
**Segunda passada:** <§: tipo: o que mudou> (ou "nada").
**Falsos alarmes:** <parágrafo: alerta: motivo> (ou "nenhum").
```

## No fim

Diga em poucas linhas: a língua, os parágrafos, os termos novos, as conferências com 0 alertas e a
legibilidade. Próximo passo: `/humanizar <slug> <n> <língua>`.
