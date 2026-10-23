# DESIGN — roteirista

## Contexto
Livros de antropologia da religião viram roteiros de vídeo para o YouTube (4 por livro, um por
tema escolhido pelo Decisor, 6 capítulos cada), narrados em inglês ou francês para público que não é nativo dessas
línguas. Um único operador, o Decisor, que revisa só em português. Máquina: Windows, RTX 2060
12 GB, 24 GB de RAM livres, HD (não SSD). Restrições: o limite de tokens do Claude (o Claude nunca
lê o livro inteiro), direitos autorais (o livro não vai para o git) e nenhuma citação fora do
literal. Volume: 1 livro por mês, 4 vídeos por livro. O piloto `roteiros-youtube` é só referência.
Evidência do modelo local: `docs/experimentos/E-001-modelo-local.md`.

## Decisões

### D-001 — Núcleo determinístico + orquestração por agentes
- Decidido: monólito modular em Python com uma CLI (o núcleo); as skills e os agentes do Claude Code falam com ele só pela CLI. Uma parte só vira serviço separado com evidência.
- Alternativa rejeitada: pipeline que chama a API do Claude sozinho, porque perde as aprovações interativas do Decisor e cobra API à parte.
- Gatilho de revisão: precisar rodar a cadeia sem o Claude Code ou sem o Decisor presente.

### D-002 — O parágrafo com id é o contrato central
- Decidido: o livro convertido é uma lista de parágrafos com id `CC.PPP` (notas `CC.nPP`); toda origem do livro aponta para ids.
- Alternativa rejeitada: os pedaços (chunks) de uma ferramenta de RAG, porque o recorte não é nosso e o id se perde.
- Gatilho de revisão: um livro com mais de 99 capítulos ou mais de 999 parágrafos num capítulo.

### D-003 — O modelo aponta, o script transcreve e confere
- Decidido: a citação literal só sai do script, a partir do id. Toda saída de modelo com id é validada (o id existe e estava entre os candidatos), e toda âncora verificável (número, nome, termo) é conferida no literal pelo script, que corrige o id para o vizinho (até 3 de distância) ou rejeita.
- Alternativa rejeitada: aceitar o texto ou o id do modelo como estão, porque o E-001 mostrou ids no parágrafo vizinho e um id inventado.
- Gatilho de revisão: a correção automática por vizinho errar mais do que acerta, nas métricas.

### D-004 — O livro é lido por um modelo local
- Decidido: qwen3:14b no Ollama, um modelo só. O trabalho roda em fases (todo o embedding, depois toda a leitura), com o modelo mantido carregado, limite de tamanho na resposta e capítulos longos divididos em janelas.
- Alternativa rejeitada: o Sonnet lendo o livro (custo de tokens) e o qwen3:8b (pior no E-001, com erros na retrotradução).
- Gatilho de revisão: um modelo local novo que caiba em 12 GB e vença o 14B no protocolo do E-001, ou uma troca de hardware.

### D-005 — A interpretação fica com o Claude, sobre uma lista curta
- Decidido: o script seleciona os parágrafos candidatos a contradição ou hesitação do autor por palavras-marca, na língua do livro; o Claude (Sonnet) julga só essa lista.
- Alternativa rejeitada: o modelo local, que respondeu "nenhuma" no E-001 com "conjecture" e "wrong" explícitos no texto; e o Sonnet lendo tudo, pelo custo.
- Gatilho de revisão: contradições achadas depois, fora da lista, em mais de um tema; ou um modelo local que passe nesse teste.

### D-006 — Índice simplificado
- Decidido: cada item tem ids, tipo (doutrina, cena, caso, numero, contradicao, termo, informante, marginal) e uma afirmação curta. As categorias saem. A cobertura (parágrafos sem item) é conferida por script.
- Alternativa rejeitada: a grade de 8 tipos × 8 categorias do piloto, que é a parte mais exigente para o modelo e é coberta pela busca por sentido.
- Gatilho de revisão: o `/temas` ficar sem base para agrupar assuntos.

### D-007 — Busca e armazenamento locais, num arquivo por livro
- Decidido: o índice e os embeddings (bge-m3 no Ollama, a validar na sua fatia) ficam num único arquivo SQLite por livro, gravado em lotes. A busca devolve ids, nunca texto reescrito.
- Alternativa rejeitada: o open-notebook no centro (Docker e SurrealDB pesados no HD, recorte fora do nosso controle). Fica como ferramenta opcional de exploração do Decisor.
- Gatilho de revisão: precisar conversar com o livro mais do que a CLI atende, ou migrar para SSD.

### D-008 — Pesquisa web gratuita, com o Claude só nas lacunas críticas
- Decidido: um script busca num buscador gratuito, baixa as páginas e as quebra em parágrafos com id; o modelo local aponta; a origem `[W]` sai do script. O Claude entra só no `/completar`, com os trechos já recortados. PDFs do Decisor entram em `externas/` pelo mesmo caminho do livro.
- Alternativa rejeitada: o pesquisador web no Claude para toda a pesquisa, pelo custo de tokens.
- Gatilho de revisão: o buscador gratuito bloquear com frequência, ou lacunas críticas vindas da pesquisa local em mais de um tema.

### D-009 — Seis capítulos fixos
- Decidido: todo roteiro tem os 6 capítulos com as funções fixas. O teor de cada um vive no seu guia (prompt), que pode mudar sem mudar a arquitetura.
- Alternativa rejeitada: número de capítulos como parâmetro, porque ninguém pediu.
- Gatilho de revisão: o Decisor criar outro formato de vídeo.

### D-010 — Briefing aprovado antes da escrita
- Decidido: cada capítulo tem um briefing no formato de `docs/maquetes/M-001-briefing-cap3.md`, conferido por script (ids existem, toda linha tem origem, seções presentes). Com os 6 aprovados, escrita, revisão e tradução rodam sem parar até a humanização. Escrever sem briefing aprovado é bloqueado.
- Alternativa rejeitada: o pacote da arquitetura indo direto para a escrita, como no piloto.
- Gatilho de revisão: o Decisor aprovar briefings sem mudanças em 10 temas seguidos.

### D-011 — Cadeia escritor → tradutor → humanizador
- Decidido: o Claude escreve em português, traduz e humaniza numa língua por vez (en ou fr; a skill pergunta qual). Duas passadas: parágrafo por parágrafo, depois integridade do roteiro inteiro. Bonito nunca vence fiel. Um script confere invariantes (citações byte a byte, marcas de origem, números, nomes) e mede legibilidade. Glossário fixo por livro e língua.
- Alternativa rejeitada: tradução e humanização numa passada só, que mistura fidelidade e acessibilidade e impede verificar cada uma.
- Gatilho de revisão: o revisor de fidelidade apontar o mesmo tipo de desvio do humanizador em mais de um tema.

### D-012 — Aprovação do humanizado em português, sem tokens
- Decidido: a cada capítulo humanizado, o qwen3:14b retraduz para português com o glossário, e um script gera a tela lado a lado (`docs/maquetes/M-002-lado-a-lado.html`) com os alertas. O Decisor aprova capítulo a capítulo e as sugestões voltam para o Claude.
- Alternativa rejeitada: o Claude retraduzir (gasta tokens) ou o 8B (erros que parecem da tradução, no E-001).
- Gatilho de revisão: a retrotradução gerar falso alarme em mais de um parágrafo por capítulo, ou o Decisor passar a ler en/fr.

### D-013 — Testes do núcleo sem o modelo real
- Decidido: nos testes de aceite, a CLI fala com um servidor falso que imita a API do Ollama e devolve respostas fixas de `fixtures/`. A qualidade do modelo real é medida à parte, em `docs/experimentos/`.
- Alternativa rejeitada: chamar o modelo real nos testes, que não dão o mesmo resultado duas vezes.
- Gatilho de revisão: um defeito que só aparece com o modelo real escapar dos testes.

### D-014 — Reconstrução do zero, guiada por testes
- Decidido: o núcleo é construído fatia por fatia pelo workflow. O código do piloto pode ser lido como referência, mas não é copiado. O Serpent é reconvertido; o tema 01 do piloto fica lá.
- Alternativa rejeitada: copiar o `livro.py` do piloto (2.271 linhas sem teste de aceite), que não dá régua ao DSH.
- Gatilho de revisão: na revisão das 10 fatias, os dados de `docs/metricas.csv` mostrarem que reconstruir com testes custa mais do que entrega.

### D-015 — Stack e ambiente
- Decidido: Python 3.12 com `uv`, pytest com `--junitxml`, Windows, ambiente em `.venv/`. `fonte/` e `texto/` de cada livro ficam fora do git, por direitos autorais.
- Alternativa rejeitada: outra linguagem, porque o ecossistema de PDF/EPUB e de Ollama em Python é o mais maduro e o piloto prova que funciona.
- Gatilho de revisão: uma dependência essencial sem suporte em Python 3.12 no Windows.

### D-016 — As decisões de conteúdo do Decisor são protegidas
- Decidido: as decisões do Decisor sobre cada tema (fio, cortes, verso, texto fixado) vão para `decisoes.md` do tema. Nenhum agente altera esse arquivo nem o que ele protege; conflito é escalado.
- Alternativa rejeitada: as decisões vivendo só na conversa, que se perde entre sessões.
- Gatilho de revisão: o Decisor decidir delegar a um agente alguma decisão de conteúdo (por exemplo, a escolha do verso).

### D-017 — Sugestão de temas aprovada pelo Decisor
- Decidido: o Claude propõe temas sozinho, sem sugestão do Decisor, a partir da visão compacta do índice (nunca do livro), no formato de `docs/maquetes/M-003-sugestao-temas.md`, com viabilidade por capítulo e assuntos compartilhados; o Decisor escolhe até 4 e a ordem. Guia de 3 a 8 candidatos; só entra tema com material no livro para enigma, números e rachadura, em mais de um capítulo. Livro fraco rende lista curta, até 1, e nunca é completado com tema fraco.
- Alternativa rejeitada: sugestão e viabilidade em passos separados (piloto), que pede duas aprovações sem o quadro completo.
- Gatilho de revisão: um tema aprovado travar na viabilidade depois da escolha.

### D-018 — Cada assunto compartilhado tem uma casa
- Decidido: informação repetida entre os vídeos é normal; construção repetida, não. Cada assunto compartilhado tem um vídeo-casa que o desenvolve, e nos outros ele é menção. O briefing marca cada passagem como desenvolver ou mencionar; o script avisa quando um "desenvolver" pertence à casa de outro vídeo, sem bloquear.
- Alternativa rejeitada: proibir a repetição de cenas entre os vídeos, porque o problema não é a cena, é o tema repetido.
- Gatilho de revisão: o Decisor ignorar o aviso de casa na maioria dos briefings.

### D-019 — O arquiteto escreve as skills
- Decidido: as skills (prompts de orquestração do Claude Code) são escritas pelo arquiteto como parte da spec da fatia. O aceite é o validador do arquivo que a skill produz, construído pelo Kimi com teste, mais o roteiro manual do Decisor. É a única exceção à regra "arquiteto não escreve produção" e não vale para código.
- Alternativa rejeitada: o Kimi escrever as skills, porque seria um modelo instruindo o Claude sem o contexto do debate; e o Decisor escrever, pelo trabalho.
- Gatilho de revisão: uma skill produzir arquivo que passa no validador mas falha no roteiro manual em mais de uma fatia.
