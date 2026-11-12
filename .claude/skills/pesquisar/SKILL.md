---
name: pesquisar
description: Busca na web gratuita (Europe PMC e Wikipédia, pela CLI) o que um tema escolhido precisa e o livro não dá — a obra e a recepção (cap. 1), o paralelo de hoje (cap. 3), as distorções na cultura popular (cap. 5) e as faltas da sugestão —, grava as fontes com ids W e escreve livros/<slug>/temas/<n>/pesquisa.md com achados conferidos e lacunas decididas.
disable-model-invocation: true
argument-hint: <slug> <número do tema>
---

# Pesquisar

Argumentos (`$ARGUMENTS`): o slug do livro e o número do tema em `livros/<slug>/temas.md`.
Saída: `livros/<slug>/temas/<n>/pesquisa.md`, e as fontes novas gravadas no livro (`W07`, `W08`...).

Antes de tudo, leia `docs/prompts/roteiro-regras.md`. Valem as regras de lá.

## Por que estas regras

O livro dá o sistema, as cenas e os números. Três funções do vídeo precisam de fora: o cap. 1 diz quem
escreveu, quando e o que a obra provocou; o cap. 3 põe ao lado da ideia incômoda uma cena de hoje em que
a mesma coisa acontece; o cap. 5 mostra o que a cultura popular fez com o material, com nome, obra e
ano. Tudo isso vem de fonte aberta e gratuita (D-027): Europe PMC para ciência e medicina, Wikipédia para
a obra, o autor, a recepção e a cultura popular. A busca e a leitura são da CLI e de modelos gratuitos; o
Claude escolhe as perguntas, lê só os achados e decide as lacunas. Busca paga e buscador comum ficam de
fora, e quem decide a lacuna que sobrar é o Claude, com o que já foi recortado (D-008).

## Pré-condições

- `livro validar-temas <slug> livros/<slug>/temas.md` dá `ok` e o tema `<n>` está no resumo.
- Se "Sua decisão" de `temas.md` já lista temas e `<n>` não está entre eles, pergunte ao Decisor antes
  de seguir.
- Crie `livros/<slug>/temas/<n>/` se não existir. Se `decisoes.md` existir, leia antes de tudo.

## Passos

1. **O que o tema precisa.** Leia em `temas.md` a linha do tema no resumo, o detalhe dele e as casas.
   Liste as necessidades, uma por linha, cada uma com o capítulo do vídeo:
   - cap. 1, a fonte: ano da obra, circunstância, recepção e críticas;
   - cap. 3, o paralelo: uma situação de hoje, reconhecível, em que a mesma coisa acontece, com um dado
     (frequência, número) que a sustente;
   - cap. 5, as distorções: filmes, séries, livros ou jogos que usaram o material, com obra e ano, e o
     que pegaram e descartaram;
   - cada **Falta** do detalhe do tema.

2. **O que já existe.** `livro fontes <slug>` lista as fontes gravadas. Reaproveite antes de buscar:
   leia só os parágrafos que servem, com `livro trecho <slug> W0X.00Y` (um por vez, até o comando dizer
   `id inexistente`, que marca o fim da fonte) ou `livro montar <slug> W0X.001-W0X.00Y` quando souber o
   tamanho. Filtre com `| grep -i -E "<palavras>"` quando a fonte for longa.

3. **Buscar o que falta.** Para cada necessidade sem resposta, rode
   `livro pesquisar <slug> "<pergunta>" --busca "<termos>"`, com `--wiki` para obra, autor, recepção,
   história e cultura popular, e sem `--wiki` para ciência e medicina (Europe PMC).
   - A pergunta é em inglês e autossuficiente: quem lê só a pergunta sabe o que procurar.
   - Os termos de busca são poucos e concretos, como num catálogo: `"The Serpent and the Rainbow film
     1988"`, não a pergunta inteira.
   - A saída lista as fontes gravadas e os achados conferidos (`<id> | <fato> | "<citação>"`); os
     `recusado` não servem. Se vier `0 fontes` ou nenhum achado, tente **uma** vez com outros termos.
     Se a busca cair (`busca falhou`, código 3), espere um pouco e tente de novo uma vez; se o
     modelo gratuito não responder, diga isso e siga com o que houver.

4. **Conferir cada achado.** O fato vem do modelo gratuito; só a citação foi conferida pelo script. Leia a
   citação do achado e reescreva o **Dado** para dizer só o que ela sustenta: número, data e quem disse,
   como estão lá. Achado que a citação não sustenta não entra. O modelo gratuito costuma acrescentar
   moldura: no teste do Serpent ele escreveu "hoje" onde a citação não tinha data, "o zumbi original"
   onde ela falava do folclore rural, e um número exato onde ela dizia "pelo menos". Estimativa tem
   dono: "segundo o sociólogo X, citado pelo jornal Y". Quando a citação for curta demais para saber
   quem fala ou de quando é, leia o parágrafo inteiro com `livro trecho`.
   Uma busca na Wikipédia grava as 3 páginas que achar, mesmo as que não servem; fonte gravada sem
   achado não atrapalha.

5. **Lacunas.** O que continuar sem resposta vira lacuna, com a criticidade e a saída:
   - **crítica:** o capítulo não existe sem ela; **importante:** fica mais fraco; **opcional:** enfeite;
   - **saída:** `outra busca` (os termos novos), `link do Decisor` (uma página da Wikipédia ou um artigo
     do Europe PMC que ele indique, gravado com `livro fonte <slug> <url>`), ou `sem fonte` (o briefing
     adapta a função e diz isso nas ressalvas). Notícia de jornal não tem fonte gratuita: é `sem fonte`
     ou `link do Decisor`.

6. **Gravar** `pesquisa.md` no formato abaixo e conferir que todo id de achado existe
   (`livro trecho <slug> <id>`).

## Formato de `pesquisa.md`

```markdown
# Pesquisa — Tema <n> <título>

**Fontes usadas:** W02, W05, W07 (nova), ...

## Achados

| Id | Dado | Para |
|---|---|---|
| W02.001 | O livro saiu em 1985 | cap. 1, a fonte |
| W07.003 | <o que a citação sustenta, em português> | cap. 3, o paralelo |

## Lacunas

| # | O que falta | Para | Criticidade | Saída |
|---|---|---|---|---|
| 1 | <a necessidade> | cap. 5 | importante | link do Decisor: <que página procurar> |

## Buscas feitas

- "<pergunta>" — `<termos>` — <N> achados
```

`Dado` é uma frase curta em português; o original fica na fonte, e o briefing cita pelo id.

## Resumo na conversa

- Achados por capítulo (cap. 1, 3, 5) e fontes novas gravadas.
- Lacunas críticas e importantes, com a saída de cada uma.
- O que o Decisor pode fazer: indicar um link para uma lacuna.
- Próximo passo: `/briefing <slug> <n>`.
