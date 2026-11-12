---
name: temas
description: Propõe os temas de vídeo de um livro já indexado, a partir só do índice (nunca do livro inteiro), no formato M-003, conferido por `livro validar-temas`. Grava livros/<slug>/temas.md para o Decisor escolher até 4 temas, a ordem e as casas dos assuntos compartilhados.
disable-model-invocation: true
argument-hint: <slug>
---

# Temas

Argumento: o slug do livro (`$ARGUMENTS`). Saída: `livros/<slug>/temas.md`.

Antes de tudo, leia `docs/prompts/roteiro-regras.md`. Valem as regras de lá.

O Claude propõe e o Decisor escolhe (D-017). A skill mede o que o índice sustenta e apresenta os
candidatos com o material de cada um; não escolhe, não corta por gosto e não completa a lista com tema
fraco.

## Por que estas regras

Cada vídeo tem 6 capítulos de funções fixas (D-009). Três delas não admitem invenção, porque são feitas de
fato do livro: a **cena-enigma** do cap. 1 (uma coisa concreta, vista inteira, que o espectador não
consegue explicar), os **números** do cap. 3 (prazos, quantidades, durações que fazem o ciclo doer) e a
**rachadura** do cap. 4 (o lugar onde a fonte não fecha: duas afirmações que não encaixam, uma hesitação
do autor, uma divergência). Um tema sem essas três coisas no livro trava depois, na escrita. E o material
precisa estar em mais de um capítulo do livro: tema de um capítulo só é resumo, não vídeo.

## Pré-condições

`livro ficha <slug>` mostra a língua e os capítulos. Se `livro visao <slug>` vier vazio, o livro não foi
indexado: pare e diga isso.

## Passos

1. **Visão do livro.** Leia `livro visao <slug>` inteira (é curta): por capítulo, fichas, números,
   contradições, nomes e termos que se repetem.

2. **Candidatos.** Procure o que atravessa capítulos: uma pessoa ou um caso que aparece em vários
   (um **fio**), um ritual, uma instituição, uma ideia com cena. Para cada candidato, meça com
   `livro contar-tema <slug> <termos...>` (fichas, parágrafos, capítulos, números, contradições). Use os
   termos na língua do livro, com variações (`Bizango "secret society"`). A contagem por palavra
   subestima tema que ocupa um capítulo inteiro sem repetir o nome: confira com `livro itens`.
   Capítulos de apoio (glossário, notas, agradecimentos, sobre o autor) entram na contagem, mas não são
   cena, número nem rachadura: não use ids deles nas três funções, e não conte um deles como o
   "segundo capítulo" de um tema.

3. **Material das três funções.** Para cada candidato que parecer forte, nos capítulos onde ele se
   concentra, leia as fichas filtradas: `livro itens <slug> <cap> | grep -i -E "<termos>"`.
   - enigma: fichas `cena`, `caso` ou `informante` que se veem inteiras;
   - números: fichas `numero`;
   - rachadura: fichas `contradicao` e as hesitações do autor (`livro hesitacoes <slug> --julgadas`, ou
     sem a opção se nada foi julgado).

   Depois **confira cada id que vai usar** com `livro montar <slug> <ids...>` (um comando por tema): o
   parágrafo tem de dizer o que a sua linha vai dizer. Ficha torta do índice não entra. Para achar um
   número ou um nome num parágrafo longo:
   `livro trecho <slug> <id> | grep -o -i -E ".{0,80}<palavra>.{0,80}"`. Use `{0,80}` dos dois lados:
   com `{80}` exato, a palavra perto do começo ou do fim do parágrafo não aparece, e parece que ela não
   está lá (no teste do Serpent, "the four leaders", no fim de 16.088, quase foi descartado assim).
   Confira também **quem** diz e **quem** faz: no mesmo teste, "There is no poison" era fala de um
   primo, não de Narcisse, e quem cavava o túmulo era Jean, não Marcel. Na dúvida sobre quem fala, não
   dê nome ("a pergunta que fica", "quem deu o pó").

4. **Corte.** Fica de 3 a 8 candidatos. Entra só o tema com enigma, números e rachadura no livro, com os
   ids desses três itens em pelo menos 2 capítulos do livro. Livro fraco rende lista curta, até 1. Tema
   que não passou vai para "Descartado", com o motivo em uma frase.

5. **Assuntos compartilhados.** O que aparece em mais de um candidato (uma cena, um caso, um conceito)
   tem uma **casa**: o vídeo que o desenvolve; nos outros ele é menção (D-018). Proponha a casa de cada
   um: o tema em que o assunto é peça central. Um par de temas que divide mais da metade dos assuntos é
   o mesmo tema com outro título: junte ou diga a diferença.

6. **Gravar e conferir.** Escreva `livros/<slug>/temas.md` no formato abaixo e rode
   `livro validar-temas <slug> livros/<slug>/temas.md`. Corrija até sair `ok: <T> temas, <A> assuntos`.

## Formato de `temas.md`

O validador confere seções, ids, os três itens com id e a casa de cada assunto. Siga à risca:

```markdown
# Sugestão de temas — <título do livro> (<autor>, <ano>)

**Estado:** aguardando escolha do Decisor
**Pedido:** escolha até 4 temas e a ordem dos vídeos. Confirme ou troque as casas dos assuntos compartilhados.

## Resumo

| # | Tema | Pergunta do vídeo | Fio | Itens no livro | Viabilidade |
|---|---|---|---|---|---|
| 1 | <título curto> | <a pergunta que o enigma força> | <pessoa ou caso, ou "sem personagem"> | <fichas do contar-tema> | ✅ suficiente |
| 2 | ... | ... | ... | ... | ⚠ parcial: <o que falta> |

**Descartado:** *<tema>.* <motivo em uma frase, com ids se citar o livro>.

## Assuntos compartilhados e a casa de cada um

| Assunto | Ids principais | 1 | 2 |
|---|---|---|---|
| <assunto> | <ids> | **casa** | menção |

<uma ou duas frases sobre sobreposição entre temas>

## Detalhe de cada candidato

### 1 — <título curto>

- **Enigma de abertura (cap. 1):** <a cena, como acontecimento> [<id>].
- **O que explica (cap. 2):** <o sistema que a cena pede> [<ids>].
- **Números (cap. 3):** <os números, cada um com id> [<id>]; ...
- **Rachadura (cap. 4):** <o que não fecha> [<id>].
- **Falta:** <o que o livro não dá e onde buscar: web, ou nenhum lugar>. (omita se nada falta)
- **Teste dos 20 segundos:** "<o tema dito em voz alta, para quem nunca ouviu falar do livro>" **Sim.**

## Sua decisão

- Temas escolhidos, em ordem: 1º ___ · 2º ___ · 3º ___ · 4º ___
- Casas: ☐ aprovadas como propostas · ☐ trocar: <assunto → tema>
- Ajuste de título ou de pergunta: <escreva aqui>
```

Regras do formato:

- Ids entre colchetes, como no exemplo; num intervalo, todos os ids existem. **Todo id do arquivo é
  conferido**, inclusive os do descartado e os dos assuntos.
- A tabela de casas tem uma coluna por tema, na ordem do resumo, e exatamente uma célula `**casa**` por
  linha; nas outras, `menção` ou `—`.
- Título curto, que diga o assunto com algo concreto ("O tribunal da noite"), nunca um rótulo vago
  ("O vodu").
- Pergunta do vídeo: a que o enigma força e o material responde; não "o que é X?".
- Itens no livro: o número de fichas do `contar-tema`, com os termos usados entre parênteses se ajudar.
- Teste dos 20 segundos: **Sim**, **Com esforço** ou **Não**. Tema com **Não** não entra. A frase do
  teste também afirma coisas do livro: confira como as outras (no teste do Serpent, "gente rica
  comprava" saiu de um parágrafo que dizia "ricos e pobres, e quem não podia alugava").

## Resumo na conversa

- Quantos temas, quantos descartados.
- Os três mais fortes: número, título, fio e viabilidade.
- Alertas: tema com material num só lugar, fio disputado por dois temas, falta que depende de web.
- O que o Decisor faz: preencher "Sua decisão" em `livros/<slug>/temas.md` (ou dizer na conversa).
- Próximo passo: `/pesquisar <slug> <n>` para cada tema escolhido.
