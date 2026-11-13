# E-010 — Verificação do tema 1 e pesquisa de skills de humanização e tradução

Feito em 2026-11-13 pelo arquiteto, a pedido do Decisor, depois do lote 8. Perguntas:

1. Há erros no tema 1 do Serpent (português aprovado → inglês humanizado → retrotradução) e nas skills
   `/traduzir` e `/humanizar` que os scripts não pegam?
2. O que as skills e os guias que existem hoje têm de bom para as nossas?

Continua o E-007, que leu o humanizer e o stop-slop para o lote 6. Desta vez foram lidos os originais mais
novos e fontes de tradução, de escrita para o ouvido e de voz sintética.

## 1. Verificação do tema 1

**Scripts:** tudo com 0 alertas. Invariantes português → tradução, tradução → humanizado e português →
humanizado: 62 parágrafos, 0 alertas. Glossário: 19 termos, 0 alertas. Legibilidade do humanizado: 0 frases
longas, 0 raras, 0 expressões (a tradução tinha 5 raras e 2 expressões).

**Leitura parágrafo por parágrafo** (português, inglês e retrotradução lado a lado). Os scripts não pegam
estes erros:

| § | Tipo | O que está no inglês | Proposta |
|---|---|---|---|
| 3.3 | ambíguo para quem ouve | "bringing the emperor, the founding president…, a small deposit of money, the person's name and the complaint" soa como uma lista de cinco coisas levadas, o imperador entre elas | "All it takes is to take a small deposit of money, the person's name and the complaint to the emperor, the founding president of the society." |
| 6.1 | ambíguo para quem ouve | "I thought that was obvious too" (a retrotradução entendeu "isso também era óbvio") | "I, too, thought that was obvious." (como em 5.8) |
| 3.8 | ambíguo para quem ouve | "over his parents' land" (a retrotradução entendeu "sobre a terra") | "because of their parents' land" |
| 5.7 | sentido partido | a ironia do português ("Justo o tribunal que exige prova") virou dois fatos soltos | "…cinema judged vodou without any proof. It judged the one court that demands proof." |
| 1.11 | nuance trocada | "criticized for scientific errors": o português diz "imprecisão" | "criticized as scientifically inaccurate" |
| 1.6 | nuance trocada | "gently": o português diz "devagar" | "slowly" |
| 4.5 | acréscimo | "everything Isnard told them": o "them" não está no português | "everything Isnard said" |
| 2.9 | tradução literal | "A song came into his mouth" não soa inglês | "A song came to him, saying he was innocent." |
| 5.2 | tradução literal | "the version with drums of something we do here" segue a ordem do português; "courts without robes" fica obscuro | "a version, with drums, of something we do here without naming it"; "courts without judges' robes" |
| 4.8 × 5.7 | termo variando | "the court of the night" e "the night court" para a mesma coisa | um só: "the court of the night" |

**Escolhas para o Decisor** (não são erros):

- **2.2:** "the hard way" virou "from a bad experience", para tirar a expressão idiomática, mas o tom mudou
  (a noite de Isnard acaba bem). "The hard way" é das expressões mais conhecidas por quem aprende inglês.
- **4.9:** "write to me" é literal de "me escreve"; no YouTube, o pedido é comentar.
- **5.3:** "magician" vem de "mágico", no português aprovado. No filme, o vilão é um feiticeiro do vodu;
  "sorcerer" e "feiticeiro" seriam mais exatos, nas duas línguas.

**Ressalvas conferidas à mão:** todo "quase", "pelo menos", "até", "mais de", "me parece", "segundo",
"talvez" e "às vezes" do português chegou ao inglês. Nenhum script confere isso hoje (ver 4.14).

**Retrotradução:** além do "cegado" (2.9) e do "soldado comum" (4.7) do E-009, o modelo local errou em 3.8
("sobre a terra"), 6.1 ("isso também era óbvio"), 1.5 ("atrás delas") e 1.10 ("Em Haiti", "parece ter nada
a ver"). Em 3.8 e 6.1, o erro dele apontou uma ambiguidade real do inglês: se o modelo de 14B entendeu
errado, um ouvinte não nativo também pode entender.

**Registros que faltam:** o tema 1 não tem `traducao.md` nem `humanizacao.md`, porque os ensaios E-008 e
E-009 produziram os textos fora das skills. O aceite da 033 (item 1) pede o `humanizacao.md`.

**Nas skills:**

- Os comandos usam o nome do arquivo sem a pasta (`roteiro-pt.md`). Rodados da raiz do projeto, como a CLI
  roda, não acham o arquivo. Têm de levar `livros/<slug>/temas/<n>/`.
- A `/humanizar` diz que a retrotradução leva de 8 a 10 minutos. Medido: 6 a 6,5 minutos por tema.
- A `/humanizar` diz que o erro da retrotradução "é erro dela, não do texto". Nem sempre: ver 3.8 e 6.1.

## 2. O que foi lido

| Fonte | O que é |
|---|---|
| humanizer 4.0.0 (blader) | 26 padrões tirados da Wikipédia, do mais forte ao mais fraco; os 5 primeiros bastam sozinhos e os marcados "fraco sozinho" só contam com outro; "quando não mexer"; conferir fato, nome, número, data, citação, ordem e simultaneidade |
| stop-slop (hardikpandya) | 8 regras, checagem rápida, nota de 1 a 10 em 5 eixos (revisar abaixo de 35 de 50) |
| unslop (Cursor, pstack) | 28 regras com número fixo, que outras skills citam; corta a frase que "poderia aparecer igual em qualquer outro texto" |
| slopkit / slopbeth (ehmo) | "travar os fatos primeiro"; manter a ressalva que tem alcance; mexer demais em texto bom é falha; comparativo honesto: empate com as outras em 23 de 25 casos |
| Comparativo de skills anti-slop (flaviocopes) | ordena as skills por tarefa; recomenda a passada como revisão separada, depois do rascunho |
| Wikipedia: Signs of AI writing (en), a adaptação em português e a página francesa | catálogo de sinais por época, com o aviso de que não se trata de esconder sinais |
| Artigos franceses sobre tiques do ChatGPT em francês | "il est important de noter", "crucial", "essentiel", "par ailleurs", "en outre", "dans un monde où" |
| translation-agent (Andrew Ng) | traduzir → criticar → melhorar, com 4 critérios: exatidão, fluência, estilo e termos |
| translation (kostja94/marketing-skills) | termos com variantes permitidas e proibidas; versão da fonte; tradução que fica desatualizada |
| Princípios da ISPOR para tradução e adaptação (Wild et al., 2005) | 10 passos; a revisão da retrotradução contra a fonte é "um dos componentes mais importantes"; teste com 5 a 8 pessoas da língua de chegada |
| Estudos com modelos de linguagem: MT Summit 2025, Lost in Translation (arXiv 2604.12911) | o modelo avalia mal a própria tradução; a ida e volta é boa para achar problema, fraca como nota |
| VOA Learning English, Media Helping Media, Simple English Wikipedia | escrever para quem ouve na segunda língua |
| Azure e Google (SSML) | como a voz sintética lê números, datas, siglas e nomes |

## 3. Onde as fontes concordam, e o que já temos

- As listas de vícios convergem: contraste encenado ("not X but Y"), frase de efeito que fecha o parágrafo,
  tríade forçada, vocabulário inflado, "-ing" solto no fim, "serves as" no lugar de "is", autoridade vaga,
  travessão em toda parte. A `/humanizar` já tem quase tudo, vindo do E-007.
- Nenhuma skill ganha clara das outras. No comparativo do slopkit, 23 de 25 casos empataram. O valor está
  na lista, no modo de trabalhar e na trava dos fatos, não na ferramenta.
- A Wikipédia avisa: os sinais não são o problema, e escondê-los só dificulta achá-los. Para nós, a meta
  é clareza e fidelidade para quem ouve, não passar em detector.

## 4. O que é novo e vale trazer

**Para a `/humanizar`:**

1. **Número fixo para cada vício** (unslop): `V1`, `V2`… O `humanizacao.md` conta por número, e o Decisor
   pode citar.
2. **Lista atualizada** (humanizer 4.0, Wikipédia 2026). Entram:
   - conexão vaga ("associated with", "linked to");
   - "serves as", "boasts" e "features" no lugar de "is" e "has";
   - "Y rather than X" e a correção encenada ("should not be confused with"), dos modelos de 2026;
   - o vocabulário de 2026 ("quietly", "steady", "matters", "leverage", "multifaceted");
   - sinônimo trocado para a mesma coisa (confunde quem ouve; em 4.8 × 5.7);
   - dois-pontos como conector.

   O travessão continua: a adaptação portuguesa registra que, em julho de 2026, o Claude ainda usava mais
   travessões que os escritores profissionais.
3. **Quando não mexer** (humanizer, slopkit). Nada se mexe em:
   - detalhe específico e estranho;
   - dúvida não resolvida do narrador;
   - ressalva com alcance ("almost", "at least", "up to", "according to", "it seems to me");
   - escolha em primeira pessoa.

   Texto que já está bom fica: mexer demais é falha.
4. **Reescrever o parágrafo em volta da ideia**, não remendar palavra por palavra (humanizer).
5. **Não inventar detalhe:** se a frase pede um dado que o português não dá, a frase fica mais simples
   (humanizer).
6. **Para o ouvido** (VOA, Media Helping Media, Simple English):
   - frases de 15 palavras em média, e no máximo 25;
   - o fato principal antes da oração subordinada;
   - sem dupla negação;
   - uma ideia por frase;
   - repetir o substantivo quando o pronome deixar dúvida;
   - palavra nova explicada logo depois;
   - ler em voz alta.
7. **Passada de sentido, contra o português, parágrafo por parágrafo** (translation-agent; tipos de erro
   do MQM): acréscimo, omissão, sentido trocado, nuance deslocada e termo. Na fluência, a tradução literal:
   imagem ao pé da letra, ordem de palavras do português, falso cognato e regência. Foi o que achou 1.11,
   1.6, 4.5, 2.9 e 5.2.
8. **A retrotradução como ouvinte de teste.** A ISPOR testa a tradução com pessoas da língua de chegada.
   Nós não temos essas pessoas sem custo, mas o modelo local cumpre parte do papel. Quando ele entende
   errado, a primeira pergunta é se o inglês está ambíguo; se estiver, o inglês muda. Foi o que achou 3.8
   e 6.1. A ISPOR também recomenda retrotradução mais literal, e o nosso prompt já pede isso.

**Para a `/traduzir`:**

9. **A segunda passada com os 4 critérios** do translation-agent:
   - exatidão: acréscimo, sentido trocado, omissão, trecho sem traduzir;
   - fluência;
   - estilo;
   - termos.
10. **Falsos cognatos e regência** (adaptação portuguesa da Wikipédia): uma lista curta de pt → en e pt →
    fr para conferir ("atualmente" ≠ "actually", "eventualmente" ≠ "eventually", "pretender" ≠ "pretend").
11. **Versão da fonte** (kostja94): o `traducao.md` grava a data do `roteiro-pt.md` traduzido. Se o
    português mudar depois, a tradução fica desatualizada.
12. **Nada de nota dada pelo próprio Claude.** O modelo avalia mal a própria tradução (MT Summit 2025), e a
    nota de 35 de 50 do stop-slop não diz como é dada. A conferência continua independente: scripts,
    modelo local e Decisor.

**Para a `/revisar`, no português:**

13. O tema 1 tem três "não é X. É Y." (2.11, 3.9 e 5.6) e várias frases de efeito no fim do parágrafo ("A
    noite tem dono.", "O que muda é o lugar de quem lê."). Por fidelidade, a tradução leva tudo isso junto.
    O lugar de cortar é a revisão do português. Da adaptação portuguesa da Wikipédia entram: "serve como",
    "desempenha um papel", "não apenas… mas também", "em vez de", "além disso" abrindo frase, "em resumo",
    a regra de três, "ostenta", "vibrante", "rico" e "profundo".

**Precisam de código** (fatias futuras, com ensaio antes):

14. **Ressalva conferida por script:** o "quase", o "pelo menos", o "até", o "segundo" e o "me parece" do
    português têm de chegar à tradução e ao humanizado. Hoje só a leitura confere.
15. **Narração e voz sintética**, quando chegar esse passo:
    - tirar os ids das citações do texto falado;
    - escrever número e data como se falam;
    - montar uma lista de pronúncia dos nomes (Isnard, Bizango, Artibonite, Samedi, Laguerre, Tonton
      Macoute);
    - não usar parênteses.

## 5. O que fica de fora

- **A rigidez do stop-slop:** nenhum advérbio, "dois é melhor que três", "você" sempre. Corta nuance e
  ressalva; o próprio exemplo dele tira um "most", o que muda o fato.
- **Nota de 1 a 10 dada pelo próprio Claude:** ver o item 12.
- **Passar em detector de IA:** não é a meta, e a Wikipédia desaconselha.
- **Duas traduções independentes reconciliadas** (ISPOR): dobra os tokens (D-027). O papel fica com a
  retrotradução e o Decisor.
- **Ouvintes nativos de verdade** (o teste da ISPOR): custa. Fica para quando houver voluntários.

## 6. Proposta

1. **Atualizar as skills** com os itens 1 a 13:
   - `/humanizar`: lista com números, quando não mexer, passada de sentido, retrotradução como ouvinte,
     regras para o ouvido, caminhos nos comandos, tempo medido;
   - `/traduzir`: os 4 critérios, falsos cognatos, versão da fonte, caminhos;
   - `/revisar`: a lista em português.
2. **Refazer a humanização do tema 1 pela skill nova:**
   - corrigir os 10 pontos da tabela;
   - gravar o `traducao.md` e o `humanizacao.md`;
   - rodar de novo as conferências, a retrotradução e a tela.

   Só então o Decisor lê a tela. Assim, o aceite da 033 testa as skills que vão ser usadas nos temas 2 a 4.
3. **Itens 14 e 15:** entram no MAPA como candidatos, com ensaio antes.

## Feito (2026-11-13, aprovado pelo Decisor)

**Skills.**
- A lista numerada de vícios ficou em `docs/prompts/vicios-de-ia.md`, comum à `/escrever`, à `/revisar` e à
  `/humanizar`.
- A `/humanizar` ganhou: quando não mexer, a passada de sentido, as regras para o ouvido, a retrotradução
  como ouvinte de teste, os caminhos nos comandos e o tempo medido.
- A `/traduzir` ganhou: os 4 critérios, os falsos cognatos (`falsos-cognatos.md`), a data da fonte e os
  caminhos.
- A `/revisar` ganhou o item "g. Vícios de IA".
- O `roteiro-regras.md` ganhou a regra dos caminhos.

**Tema 1, pela skill revisada.**
- As 10 correções da tabela, e mais uma achada pela lista nova: V12 "quietly", em 2.3.
- A primeira retrotradução (608 s) acertou as correções. Pela regra do ouvinte de teste, apontou mais duas
  ambiguidades do inglês: "the one court" lido como "a única corte" (5.7) e "This is where" lido como
  lugar (3.1). As duas foram corrigidas.
- A segunda retrotradução levou 461 s. As conferências deram 0 alertas, e a tela, 62 parágrafos e 0
  marcados.
- Ficaram 5 erros só do modelo local, anotados em `humanizacao.md`.
- Foram gravados o `traducao.md` e o `humanizacao.md`.
- As três escolhas (2.2, 4.9, 5.3) ficam com o Decisor.

**Tema 1 em francês (2026-11-13), pelas skills revisadas.**
- Decisões do Decisor:
  - o verso do cap. 1 vai traduzido (`decisoes.md`, item 4);
  - o glossário francês tem 20 termos; dois foram escolha dele: vodu → vodou e terreiro → péristyle.
- Tradução: glossário e invariantes com 0 alertas na primeira rodada; 17 raras e 1 expressão.
- Humanizado: 0 alertas; legibilidade com 5 raras (2 delas falso alarme) e 0 expressões.
- A primeira retrotradução (486 s) ficou bem mais perto do português que a do inglês. Ela apontou 4
  leituras que o francês permitia: "Retenez" lido como "Detenha", "coups de fouet" como "chicotadas", "lui
  est venu" como "veio à mente" e "robes" como vestido de mulher. As quatro foram corrigidas.
- A segunda retrotradução levou 464 s. A tela deu 62 parágrafos e 2 marcados, os dois por erro do modelo
  local: manteve "Baron Samedi" como nome e traduziu "Jean Baptiste".

**Achados novos no francês:**
- `traducao.md` e `humanizacao.md` não levavam a língua no nome, e o francês sobrescreveria o inglês. Agora
  são `traducao-<língua>.md` e `humanizacao-<língua>.md`.
- A legibilidade não separa a elisão francesa: nome depois de "l'" ou "qu'" ("l'Artibonite",
  "qu'Isnard") vira palavra rara.
- Em janela estreita, a tela tem rótulo para o texto em inglês e não tem para o francês.
- As duas últimas são candidatas a uma correção pequena, com teste.

## Reavaliação da qualidade (2026-11-13, a pedido do Decisor)

**Método.** O Claude avalia mal o próprio texto (item 12), então houve dois avaliadores:

- **Um juiz independente e gratuito:** o Nemotron 3 Ultra (550B), pelo 9Router, só no endereço local, com o
  Ernie 5.5 de reserva. Recebeu um pedido por capítulo e língua, com o português ao lado da tradução, as
  citações mascaradas e o prompt do método MQM. As categorias foram exatidão (acréscimo, omissão, sentido,
  trecho sem traduzir), fluência (gramática, literal, registro), termos e ouvinte (ambíguo). A gravidade foi
  menor, maior ou crítica. Nenhum trecho do livro saiu do computador.
- **O arquiteto:** fez a triagem de cada achado, aceitando ou recusando com o motivo, e uma passada própria.

**Achados do juiz:** 14, sendo 7 no inglês e 7 no francês. Foram aceitos 8 e recusados 6. Ele acerta pouco
mais da metade, como os estudos com modelo de juiz já mostravam.

- **Aceitos no inglês:**
  - 4.8, maior: a metáfora do narrador invertida, "are the same man in different clothes" → "sometimes
    dress the same man";
  - 4.6, menor: perdeu a suspeita do "não virou" → "may have become";
  - 3.3, menor: "them" ambíguo → "these things";
  - 5.6, menor: "sentence" também quer dizer frase → "a sentence, a punishment".
- **Aceitos no francês:**
  - 1.5, maior: "Un secrétaire, une machette et une bougie" soa como uma lista de três → "avec";
  - 2.14, menor: a frase dividida separava o aviso de adoecer;
  - 4.9, menor: "d'autres arrivent" ambíguo → "la suite arrive";
  - 5.3, menor: o decalque "sous le sort de" → "à qui un magicien a jeté un sort".
- **Recusados:**
  - 1.10 (en): o "ela" do português é a noite, não a mulher;
  - 3.4 (en): "a mulher de outro" é de outro homem;
  - 4.5 (en): "isn't sure" foi simplificação de propósito, sem perder o sentido;
  - 3.1 (fr): o "aqui" é o momento da história;
  - 5.7 (fr), dado como crítico: a tradução está certa, o cinema julgou justamente o tribunal que exige prova;
  - 6.5 (fr): "péristyle" é escolha do Decisor, e a cena é no Haiti.
- **Da passada do arquiteto:** o 2.14 também no inglês; no francês, 3.3 ("dépôt d'argent") e 5.2 ("groupe
  de discussion").

**Nota MQM antes destas correções.** Peso 1 para erro menor, 5 para maior, 25 para crítico.

| Língua | Palavras | Pontos | Nota |
|---|---|---|---|
| Inglês | 1.851 | 9 (1 maior, 4 menores) | 99,5 de 100 |
| Francês | 1.970 | 10 (1 maior, 5 menores) | 99,5 de 100 |

Nenhum erro crítico nas duas. Depois das correções, não fica erro conhecido. As conferências seguem com 0
alertas.

**Proposta:** o juiz independente pode virar um passo fixo da `/humanizar`. Seria um comando da CLI, numa
fatia com ensaio antes; hoje ele é um script de rascunho.

## Fontes

- humanizer: https://github.com/blader/humanizer
- stop-slop: https://github.com/hardikpandya/stop-slop
- unslop: https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md
- slopkit: https://github.com/ehmo/slopkit
- Comparativo anti-slop: https://flaviocopes.com/anti-slop/
- Wikipedia (en): https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Wikipédia (pt): https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:Sinais_de_texto_gerado_por_intelig%C3%AAncia_artificial
- Wikipédia (fr): https://fr.wikipedia.org/wiki/Aide:Identifier_l%27usage_d%27une_IA_g%C3%A9n%C3%A9rative
- Tiques em francês: https://www.blogdumoderateur.com/chatgpt-mots-utilises-chatbot/
- translation-agent: https://github.com/andrewyng/translation-agent
- translation (marketing-skills): https://github.com/kostja94/marketing-skills
- ISPOR (Wild et al., 2005): https://www.ispor.org/heor-resources/good-practices/article/principles-of-good-practice-for-the-translation-and-cultural-adaptation-process-for-patient-reported-outcomes-%28pro%29-measures
- MT Summit 2025 (anotação de erros por modelo): https://aclanthology.org/2025.mtsummit-1.15.pdf
- Lost in Translation: https://arxiv.org/abs/2604.12911
- VOA Learning English: https://learningenglish.voanews.com/a/sentence-length-are-short-sentences-childish-/6636852.html
- Media Helping Media: https://mediahelpingmedia.org/basics/tips-for-writing-radio-news-scripts/
- Simple English Wikipedia: https://simple.wikipedia.org/wiki/Wikipedia:How_to_write_Simple_English_pages
- Azure SSML: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation
- Google SSML: https://docs.cloud.google.com/text-to-speech/docs/ssml
