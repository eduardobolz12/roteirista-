---
name: briefing
description: Monta o plano de um tema escolhido (fio, linha do tempo, pergunta, escada, âncora, ciclo e segunda volta) e os 6 briefings de capítulo no formato M-001, a partir do índice, do texto literal dos ids escolhidos e da pesquisa web. Cada briefing é conferido por `livro validar-briefing --temas` antes de ir ao Decisor.
disable-model-invocation: true
argument-hint: <slug> <número do tema> [duração em minutos, padrão 10]
---

# Briefing

Argumentos (`$ARGUMENTS`): o slug, o número do tema em `livros/<slug>/temas.md` e, opcional, a
duração de referência em minutos (padrão 10). Pasta do tema: `livros/<slug>/temas/<n>/`.
Saída: `plano.md` e `briefing-1.md` a `briefing-6.md` nessa pasta.

Antes de tudo, leia `docs/prompts/roteiro-regras.md`. Valem as regras de lá.

O briefing distribui material; não escreve roteiro. Nada de prosa de narração nem frase de efeito: cada
linha diz o que entra, de onde vem e para quê. O Decisor aprova os 6 antes da escrita (D-010); depois
disso, escrita e revisão andam sem parar.

## As seis funções (D-009)

| Cap. | Função | Momentos, em ordem | O que precisa do material |
|---|---|---|---|
| 1 | O enigma | verso → cena do enigma → apresentação → âncora → pergunta do vídeo → fonte | uma cena concreta, vista inteira, que não se explica; a âncora; a fonte (obra, ano, circunstância, recepção) da web |
| 2 | O sistema como resposta | princípio → a peça que explica o enigma, com a chave de sedução → o ciclo completo, fechado | o sistema que torna o enigma inteligível, contado pelo fio; nada do que dá errado |
| 3 | O mesmo ciclo, quebrado | (reação pessoal) → segunda volta → ideia incômoda → paralelo de hoje → pergunta sem resposta | as mesmas etapas do cap. 2, na mesma ordem, agora com os números guardados; uma citação e um caso para a ideia incômoda; um dado da web para o paralelo |
| 4 | Onde não fecha | contradição → segunda camada (se houver) → detalhe que não grita → convite | a rachadura com as duas peças; a hesitação ou divergência; um detalhe pequeno que passou o vídeo inteiro sem drama |
| 5 | Nós | espelho → distorções → contraste com a fonte | o material com respeito antes de ser virado; obras da cultura popular com nome e ano (web); o que a fonte realmente diz |
| 6 | A volta | inversão → divisão → despedida → âncora | o elemento que divide os leitores, com as duas leituras; a âncora do cap. 1 de volta. Nada novo |

Regras que valem para o vídeo inteiro (são elas que dão a curva):

- **Uma só pergunta sem resposta**, no fim do cap. 3. Convite só no 4; despedida só no 6. Os caps. 1 e 2
  não terminam em pergunta nem em convite; a pergunta do vídeo entra no 1, mas não como o fim dele.
- **Âncora:** a imagem do cap. 1 volta no 6 e não aparece em nenhum outro. Nenhum outro item se repete
  entre funções: se um id serviria a duas, escolha uma e diga qual no "O que fica de fora".
- **Números guardados para o 3:** os prazos, quantidades e durações que fazem a segunda volta doer não
  são gastos no 2.
- **Casa (D-018):** passagem de um assunto cuja casa é outro tema entra como `mencionar`. Desenvolver a
  casa de outro vídeo só com o Decisor de acordo, dito em "Ressalvas".
- **Leitura é leitura:** o princípio do cap. 2 que a fonte não declara, o paralelo do 3, o espelho do 5
  e a inversão do 6 são leitura do narrador; diga "leitura:" no "O que entra".
- **Lacuna:** momento sem material sai da tabela e vira ressalva, com o que falta. Nunca se escreve
  "Livro" num momento que o livro não sustenta.
- **Orçamento:** total = duração × 150 palavras (D-028). Por capítulo: 16%, 27%, 19%, 14%, 14% e 10%.
  É referência de proporção, não teto: nada sai do vídeo para caber no tempo.

## Pré-condições

- `livros/<slug>/temas.md` passa no `livro validar-temas` e tem o tema `<n>`.
- `livros/<slug>/temas/<n>/pesquisa.md` existe (rode `/pesquisar` antes). Sem ela, os momentos `Web`
  ficam sem dado.
- Se `decisoes.md` existir, leia antes de tudo: o que ele protege não se reabre.

## Passos

1. **O que já se sabe.** Leia em `temas.md` o detalhe do tema e a tabela de casas; leia `pesquisa.md`
   inteira.

2. **Material.** `livro contar-tema <slug> <termos do tema>` mostra os capítulos. Nos 2 a 4 capítulos
   centrais, leia as fichas filtradas:
   `livro itens <slug> <cap> | grep -E "\| (cena|caso|informante|numero|contradicao|doutrina) \|" | grep -i -E "<termos>"`.
   Fora desses capítulos, use `livro buscar <slug> <termo>` para achar um parágrafo pontual.

3. **Plano.** Antes dos briefings, escreva `plano.md` (formato abaixo): o fio, a linha do tempo do fio
   com ids, a pergunta do vídeo, a escada (o que o espectador acredita ao fim de cada capítulo; cada
   degrau muda o anterior), a âncora e como ela volta no 6, o ciclo do cap. 2 com a segunda volta do 3
   lado a lado, e o excedente. Se dois degraus dizem o mesmo, a estrutura está errada: refaça antes de
   seguir.

4. **Texto literal.** Escolhidos os ids de cada capítulo, leia todos com `livro montar <slug> <ids...>`
   (um comando por capítulo). É daqui que saem o "O que é" de cada passagem e o trecho de cada
   citação. Confira quem faz e quem diz cada coisa; o índice erra.

5. **Os seis briefings**, no formato abaixo, um arquivo por capítulo.

6. **Conferir.** Para cada um:
   `livro validar-briefing <slug> livros/<slug>/temas/<n>/briefing-<k>.md --temas livros/<slug>/temas.md`.
   Corrija até sair `ok`. Um `aviso` de casa se resolve trocando a passagem para `mencionar`, ou fica,
   explicado nas ressalvas, para o Decisor decidir.

7. **Conferência cruzada**, lendo os seis juntos: uma só pergunta sem resposta (fim do 3); convite só no
   4; despedida só no 6; âncora só no 1 e no 6; nenhum id em duas funções; a segunda volta do 3 nas
   mesmas etapas e na mesma ordem do ciclo do 2; nenhum número guardado para o 3 aparece no 2; a soma
   das durações bate com o total.

## Formato de `plano.md`

```markdown
# Plano — Tema <n> <título>

**Duração de referência:** <N> min × 150 = <total> palavras (referência, não teto)

## Fio
<pessoa ou caso> — <por que este> [ids]. Alternativa descartada: <uma linha>.

## Linha do tempo do fio
1. <momento> — <acontecimento> [id]

## Pergunta do vídeo
<uma frase>

## Escada
| Ao fim do cap. | O espectador acredita que |
|---|---|
| 1 | ... |

## Âncora
<a imagem do cap. 1> [id]. Volta no cap. 6 como: <a forma exata>.

## O ciclo (cap. 2) e a segunda volta (cap. 3)
| Etapa | Cap. 2: funcionando | Cap. 3: o custo, com o número |
|---|---|---|
| 1 | ... [id] | ... [id] |

## Excedente
- [id] — <o que é> — <por que ficou de fora>
```

## Formato de cada `briefing-<k>.md`

O validador confere campos, seções, colunas, ids, momentos, tratos, origens e citações. Siga à risca:

```markdown
# Briefing — Tema <n> <título> · Capítulo <k> de 6

**Tema:** <n>
**Capítulo:** <k>
**Estado:** aguardando aprovação do Decisor
**Função do capítulo:** <nome da função>. <o que este capítulo faz neste tema, em uma frase>
**Ao fim, o espectador entende:** <o degrau <k> da escada>
**Duração estimada:** ~<palavras> palavras, ~<minutos> min (referência, não teto)

## O que será abordado

| # | Momento | O que entra | De onde vem |
|---|---|---|---|
| 1 | <nome do momento> | <o que entra> | Livro |

## Cenas e passagens do livro

| Id | O que é | Momento | Trato |
|---|---|---|---|
| <id ou intervalo> | <o que é, em poucas palavras> | <n, ou "1 e 2"> | desenvolver |

## Citações literais previstas

| Id | Trecho (original) | Uso |
|---|---|---|
| <id> | "<palavras do original, copiadas do montar>" | <momento> |

## Dados da web

| Id | Dado | Uso |
|---|---|---|
| <W..> | <o dado, da pesquisa.md> | <momento> |

## O que fica de fora deste capítulo

- <o que não entra, e para onde vai>

## Ressalvas

- <lacunas, leituras, casas, ou "Nenhuma.">

## Sua decisão

- [ ] Aprovado como está
- [ ] Aprovado com mudanças: <escreva aqui>
- [ ] Refazer: <o que não serve>
```

Regras do formato:

- `De onde vem` é `Livro`, `Web` ou `Narrador`. Momento `Livro` precisa de pelo menos uma passagem que o
  cite; momento `Web`, de pelo menos um dado da web. O verso, a apresentação, a pergunta, o convite, a
  despedida e as leituras são `Narrador`.
- `Trato` é `desenvolver` (o capítulo conta) ou `mencionar` (uma ou duas frases).
- Tabela vazia fica com o cabeçalho e a linha `|---|`. Toda linha tem todas as colunas.
- A citação é copiada do texto de `livro montar`, palavra por palavra; pontuação e maiúsculas podem
  variar, palavras não. Num intervalo, as palavras seguidas dos parágrafos juntos; `...` marca o corte.
  Prefira trechos curtos, que se digam em voz alta. Fala cortada pelo narrador do livro
  (`"They say we eat people," Jean continued, "and we do..."`) leva `...` no lugar das palavras dele.
- Cap. 1: a fonte é `Web` (o ano e a recepção da obra) e pode citar o livro pela página "sobre o autor"
  se houver. Cap. 6: nada novo além do elemento que divide, que é do pacote dele; a âncora é a mesma do
  cap. 1.

## Resumo na conversa

- Os seis briefings conferidos (`ok`), com a duração de cada um.
- O fio, a pergunta do vídeo e a âncora, em três linhas.
- Lacunas e ressalvas que pedem decisão (casas, leituras fortes).
- O que o Decisor faz: ler e marcar "Sua decisão" em cada briefing.
- Próximo passo, com os seis aprovados: `/escrever <slug> <n> 1`.
