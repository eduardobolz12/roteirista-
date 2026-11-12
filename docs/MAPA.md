# MAPA de fatias

Premissa: `DESIGN.md`. Cada fatia tem 2–3 CAs e cabe numa sessão. Toda fatia que lê dados depende
de uma que os escreve. "Livro de teste" = fixture pequena dentro da pasta da fatia, nunca o Serpent
(direitos autorais). Modelo local nos testes = servidor falso (D-013).

Reorganizado em 2026-11-10 depois do ensaio E-004 (D-025): o que falta vai em lotes, pelo caminho mais
curto até um vídeo completo. Os números das fatias não mudam; as novas recebem números livres.

# Feito

## Bloco A — O livro (escreve o texto; tudo depende dele)

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 001 | walking skeleton: PDF → banco → trecho | — | `livro novo` num PDF de 2 capítulos cria o banco SQLite do livro; `livro trecho <slug> 02.001` imprime o parágrafo literal; id inexistente sai com erro |
| 002 | PDF real: hifenização, cabeçalho, rodapé | 001 | palavra quebrada no fim da linha volta inteira; número de página e título corrido não viram parágrafo |
| 003 | notas e bibliografia separadas | 002 | nota vira id `CC.nPP` fora do corpo; chamada `[n12]` no texto não é id; bibliografia fica fora dos parágrafos |
| 004 | EPUB | 001 | `livro novo` num EPUB de 2 capítulos gera os mesmos ids que o PDF equivalente |
| 005 | ficha do livro e medida | 001 | `livro medir` dá palavras e tokens por capítulo; `livro novo` grava a língua informada na ficha e mostra 3 parágrafos para conferência |
| 006 | conferir e buscar | 001 | `livro conferir` diz EXISTE/NÃO EXISTE para uma frase literal; `livro buscar` devolve todos os ids de um termo, sem diferenciar maiúsculas |
| 007 | montar | 001 | `livro montar` gera um documento com o texto literal de uma lista de ids e intervalos, na ordem pedida |
| 034 | estrutura do livro: partes, páginas de serviço, abertura de capítulo | 006, 005 | capítulo é marcador sem filhos; copyright, sumário e índice saem; capa sem texto mantém o número; nenhum texto aparece em dois capítulos |
| 035 | parágrafos por recuo | 034 | recuo horizontal separa parágrafos e decide a virada de página; citação em bloco é um parágrafo; glossário sai por entrada |
| 036 | medida da linha em PDF comercial | 035 | as regras da 035 valem num PDF com escala, fonte embutida e texto letra por letra; o parágrafo do Serpent sai inteiro |
| 037 | junção de linhas | 002, 036 | travessão une sem espaço; hífen fica antes de maiúscula e em composto cujas partes o livro conhece |
| 038 | livro antigo | 011 | livro gravado por uma versão anterior aceita os comandos novos sem perder nada |

## Bloco B — Leitura pelo modelo local (escreve o índice)

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 008 | indexar um capítulo, com validação de ids | 001 | `livro indexar <slug> <cap>` grava os itens que o modelo devolve; id inexistente ou fora do capítulo é rejeitado e listado; tipo fora da lista é rejeitado |
| 009 | capítulo longo em janelas | 008 | capítulo maior que o contexto é lido em janelas; nenhum parágrafo fica fora de todas as janelas; itens não se duplicam na emenda |
| 010 | conferência de âncoras | 008, 006 | número ou nome de um item que não está no parágrafo apontado é procurado nos vizinhos (até 3) e o id é corrigido; não achado, o item é rejeitado |
| 011 | cobertura e repescagem | 008 | `livro lacunas` lista os parágrafos sem item; a repescagem cobre só esses, com item ou `sem-conteudo` |
| 039 | fichas na língua do livro | 011 | livro com língua usa os prompts na língua do livro; âncora como palavra inteira; mesma frase vira uma ficha |
| 040 | nova tentativa | 009 | pedido que falha é repetido até 3 vezes antes do `modelo inacessível` |

## Bloco C — Base do índice para os temas (lote 3, aceito em 2026-11-11)

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 041 | âncora pelas palavras | 039 | a âncora confere quando as palavras dela aparecem no parágrafo, na mesma ordem e próximas, ignorando a pontuação; `make somebody lot money` confere com "make somebody a lot of money" |
| 043 | indexar o livro inteiro | 040 | `livro indexar-livro <slug>` indexa e repesca todos os capítulos em ordem, grava o andamento e retoma de onde parou |
| 015 | visão compacta e contagem por tema | 039 | `livro visao` dá, por capítulo, fichas, nomes repetidos e termos; `livro contar-tema` conta fichas, parágrafos e capítulos de um tema |
| 014 | hesitações do autor | 005 | `livro hesitacoes` lista os parágrafos com palavras-marca fortes da língua do livro (`--todas` inclui as fracas); `livro julgar` grava o julgamento do Claude só para ids da lista |


## Bloco D — Revisão e pesquisa gratuitas (lote 4, aceito em 2026-11-11)

Medições feitas: E-005 (revisão, 4 de 4 infidelidades achadas) e E-006 (pesquisa por Europe PMC e
Wikipédia, 4 de 4 perguntas certas). Tudo gratuito (D-027). Ordem de construção: 017, 042, 018.

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 017 | fonte web com ids | 001 | `livro fonte <slug> <url>` grava um artigo do Europe PMC ou uma página da Wikipédia como fonte `W01`, com parágrafos `W01.001`; `livro trecho` lê esses ids |
| 042 | revisão do sentido por modelo gratuito | 041, 017 | `livro revisar <slug> <texto> <ids>` manda texto e material a um modelo gratuito, com modelos de reserva; só sai apontamento cuja frase está no texto e cujo id está no material; o texto não muda |
| 018 | pesquisa gratuita | 017, 042 | `livro pesquisar <slug> "<pergunta>" --busca "<termos>" [--wiki]` grava as fontes achadas e só mostra o fato cuja citação está no parágrafo apontado; busca fora do ar vira erro claro |

## Bloco E — Validadores do briefing e do capítulo (lote 5, aceito em 2026-11-12)

Regras testadas antes num protótipo descartável, nos arquivos de teste (14 de 14 saídas) e em arquivos
reais do Serpent (temas Bizango e Narcisse, briefing e capítulo 1 do Bizango). Ordem: 016, 020, 021, 022.
A 020 foi aceita com correção: linha de tabela com coluna faltando era ignorada (fatia 044).

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 016 | validador da sugestão de temas | 015 | `livro validar-temas` confere o formato M-003: seções, ids que existem, enigma, números e rachadura com id em mais de um capítulo, uma casa por assunto |
| 020 | validador do briefing | 016, 017 | `livro validar-briefing` confere o formato M-001: campos, seções, ids, momentos, trato, origem de cada momento e citações pela regra da D-028 |
| 021 | casa dos assuntos | 020 | com `--temas`, passagem `desenvolver` que é casa de outro tema gera aviso, sem mudar o código; `mencionar` nunca avisa |
| 022 | contar e conferir o capítulo | 020 | `livro contar` dá palavras e minutos (150 por minuto) do texto narrado e confere cada citação no original pelas palavras (D-028) |

| 044 | colunas faltando no briefing | 020 | linha de tabela do briefing com menos colunas que as do formato gera `<linha>: faltam colunas: <nomes>`, e as colunas que ela tem continuam conferidas (correção da 020, aceita em 2026-11-12) |


# A seguir

## Lote 6 — Skills: do tema ao capítulo escrito

As skills são prompts: o resultado delas não é sim/não e não passa por teste automático de conteúdo.
Cada uma vira fatia **depois** do núcleo que ela usa, com aceite pelo validador do arquivo que ela
produz + roteiro manual. As skills são escritas pelo arquiteto (D-019).

Antes de escrever, o arquiteto leu as skills que já existem para este trabalho (E-007): o piloto é a
base; das de terceiros entraram regras de gancho, checagem de fonte, escrita para o ouvido e vícios de IA.
Skills escritas e testadas de ponta a ponta no tema 1 do Serpent em 2026-11-12; aguardam o roteiro manual
e o aceite do Decisor.

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 029 | /temas | 016 | o arquivo de sugestão passa no `validar-temas` |
| 030 | /pesquisar | 018 | todo achado da `pesquisa.md` tem id W que existe; a 019 (PDFs externos) fica na reserva, e a lacuna que só ela resolveria vira "link do Decisor" ou "sem fonte" |
| 031 | /briefing | 020, 021, 044, 029, 030 | os 6 briefings passam no `validar-briefing --temas` |
| 032 | /escrever e /revisar | 022, 042, 031 | cada capítulo passa no `contar --briefing` com 0 problemas e cada apontamento do `revisar` está decidido |

## Lote 7 — Tradução, humanização e aprovação

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 023 | glossário | 001 | `livro glossario` grava termo → tradução por livro e língua; o mesmo termo com duas traduções no roteiro gera alerta |
| 024 | invariantes entre versões | 022 | `livro invariantes <antes> <depois>` aponta parágrafo em que mudou citação, marca de origem, número ou nome |
| 025 | legibilidade en/fr | — | `livro legibilidade` dá, por parágrafo, tamanho de frase, palavras fora da lista de vocabulário e expressões idiomáticas marcadas |
| 026 | retrotradução local | 023 | `livro retraduzir` grava a versão em português, parágrafo por parágrafo, com os termos do glossário respeitados |
| 027 | tela lado a lado | 026, 024 | `livro lado-a-lado` gera o HTML da M-002 sem rede e sem tokens; parágrafo com alerta aparece marcado |
| 033 | /traduzir e /humanizar | 023, 024, 025, 027 | o capítulo humanizado passa nas invariantes e gera a tela lado a lado |

# Reserva

Fatias do plano original que o ensaio E-004 não pediu. Entram num lote quando fizerem falta.

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 012 | resumo por capítulo | 008, 010 | `livro resumir` grava temas, cenas, números e contradições do capítulo, cada linha com ids válidos |
| 013 | embeddings e busca por sentido | 001 | `livro vetorizar` grava um vetor por parágrafo no banco; `livro perguntar "<pergunta>"` devolve ids ordenados, nunca texto reescrito |
| 019 | PDFs externos | 002, 017 | PDF em `externas/` vira fonte `[E ...]` com ids, pelo mesmo caminho do livro |
| 028 | /novo-livro e /indexar | 005, 009, 011, 012, 013, 014 | um livro de teste sai convertido, indexado e com resumos, sem o Claude ler o livro |
