# E-007 — Skills que já existem para este trabalho

Feito em 2026-11-12 pelo arquiteto, a pedido do Decisor, antes de escrever as skills do lote 6. Pergunta:
já existem skills do Claude que transformam livro em roteiro de vídeo, e o que vale aproveitar de cada
uma? Os arquivos foram lidos no original (SKILL.md e referências baixados do GitHub), não pelas descrições
dos catálogos.

## O que foi lido

| Skill | Origem | O que faz |
|---|---|---|
| As 12 skills do piloto (`temas`, `arquitetar`, `escrever` com 6 guias, `revisar`, agente `revisor`) | `roteiros-youtube/.claude/` | o fluxo inteiro do piloto; os guias geraram o capítulo do E-004, aprovado |
| claude-youtube (script, hook, guia de retenção) | AgriciDaniel/claude-youtube | roteiro de YouTube por retenção |
| youtube-script-writer | mohitagw15856/pm-claude-skills | roteiro com gancho, capítulos e recompensa |
| youtube-hooks-scripts | jscraik/Agent-Skills | gancho e roteiro técnico com afirmações provadas |
| narrative-structure, narrator, fact-checker | revfactory/harness-100 (documentário) | estrutura de documentário, narração e checagem |
| citation-audit | jewzaam/claude-skill-cited-research | auditoria de citação contra a fonte |
| humanizer | blader/humanizer | 26 padrões de texto com cara de IA (Wikipedia "Signs of AI writing") |
| stop-slop | hardikpandya/stop-slop | cortes de vício de IA, com nota de 1 a 10 |
| document-to-narration (guia de adaptação falada) | jwynia/agent-skills | texto escrito para ser ouvido |
| skill-creator | anthropics/skills | como escrever skill |

Nenhuma skill de terceiros faz o trabalho inteiro (livro de antropologia → vídeo fiel, com citação
conferida). As de YouTube são de marketing; as de documentário não conferem citação; as de checagem não
escrevem. O piloto é o mais próximo e é a base.

## O que entra nas skills do lote 6

**Do piloto (base):** as seis funções e os guias de voz dos capítulos; a dívida do cap. 1 paga no cap. 2;
a segunda volta do cap. 3 na mesma ordem do cap. 2; uma só pergunta sem resposta (fim do cap. 3); convite
só no 4; despedida antes da âncora no 6; orçamento 16/27/19/14/14/10 %; a lista de checagem do revisor
(clareza, coerência, repetição, sustentação, curva, tempo) com gravidade grave/média/leve; "a família"
não vira "as irmãs"; leitura marcada como leitura; lacuna declarada, nunca preenchida.

**Mudanças do sistema novo sobre o piloto:** citação no original com id (D-028), conferida por
`livro contar --briefing`; briefing aprovado por capítulo (D-010) no lugar dos pacotes da arquitetura;
revisão do sentido por modelo gratuito (`livro revisar`, D-023) no lugar do subagente revisor; pesquisa
por Europe PMC e Wikipédia (D-027); 150 palavras por minuto.

**De terceiros, o que serve a um vídeo fiel:**

- Gancho que promete só o que o roteiro paga, e final que responde ao gancho (jscraik); prova que falta
  vira lacuna, não frase (jscraik, fact-checker).
- Laço aberto: a pergunta do cap. 1 segura o vídeo até o fim (claude-youtube, "suspension bridge").
- Volta à tese a cada 2–3 minutos no vídeo educativo longo (claude-youtube, "anchor pattern"): no nosso
  formato, cada capítulo retoma o fio, não a aula.
- Do específico ao abstrato e de volta ao específico; o pico de emoção no meio (narrative-structure),
  que confirma o cap. 3 como pico.
- Narração: uma informação por frase, contexto que a imagem não dá, não pensar pelo espectador
  (narrator, narrative-structure).
- Checagem: a fonte tem de **sustentar** a afirmação, não só tratar do assunto; o "parcial" é onde mora a
  distorção; reconsiderar cada aprovação antes de fechar (citation-audit).
- Para o ouvido: sem parênteses e sem abreviação; número escrito como se fala; frases de 15 a 25
  palavras em média; ler em voz alta (document-to-narration).
- Vícios de IA a caçar no texto (humanizer, stop-slop), adaptados ao português: "não X, mas Y" que só
  infla; frase de efeito que fecha parágrafo sem fato novo; aforismo; tríade forçada; mesma abertura de
  frase em sequência; travessão em toda parte; significado inflado ("marcou para sempre"); linguagem de
  folheto sobre outra cultura (exotizar); autoridade emprestada; três frases seguidas do mesmo tamanho.
- Como escrever skill (skill-creator): SKILL.md curto, guias em arquivos lidos só quando precisa;
  explicar o porquê em vez de empilhar "SEMPRE" e "NUNCA".

**O que fica de fora:** CTA, títulos e miniaturas de clique, efeitos sonoros, cortes de câmera e
"interrupções de padrão" a cada poucos segundos (marketing, sem relação com fidelidade); voz em segunda
pessoa com "você" constante (o piloto usa primeira pessoa); 250 palavras por minuto (revfactory; aqui
vale a D-028, 150); scripts próprios nas skills (o que é código fica com a CLI, D-019).

**Para o lote 7:** o humanizer inteiro (os 26 padrões e o modo de trabalhar: marcar, reescrever,
conferir se algum fato, nome, número ou citação mudou) e a retrotradução para conferir (D-012).
