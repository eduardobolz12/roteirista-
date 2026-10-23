# MAPA de fatias

Premissa: `DESIGN.md`. Cada fatia tem 2–3 CAs e cabe numa sessão. Toda fatia que lê dados depende
de uma que os escreve. "Livro de teste" = fixture pequena dentro da pasta da fatia, nunca o Serpent
(direitos autorais). Modelo local nos testes = servidor falso (D-013).

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

## Bloco B — Leitura pelo modelo local (escreve o índice)

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 008 | indexar um capítulo, com validação de ids | 001 | `livro indexar <slug> <cap>` grava os itens que o modelo devolve; id inexistente ou fora do capítulo é rejeitado e listado; tipo fora da lista é rejeitado |
| 009 | capítulo longo em janelas | 008 | capítulo maior que o contexto é lido em janelas; nenhum parágrafo fica fora de todas as janelas; itens não se duplicam na emenda |
| 010 | conferência de âncoras | 008, 006 | número ou nome de um item que não está no parágrafo apontado é procurado nos vizinhos (até 3) e o id é corrigido; não achado, o item é rejeitado |
| 011 | cobertura e repescagem | 008 | `livro lacunas` lista os parágrafos sem item; a repescagem cobre só esses, com item ou `sem-conteudo` |
| 012 | resumo por capítulo | 008, 010 | `livro resumir` grava temas, cenas, números e contradições do capítulo, cada linha com ids válidos |
| 013 | embeddings e busca por sentido | 001 | `livro vetorizar` grava um vetor por parágrafo no banco; `livro perguntar "<pergunta>"` devolve ids ordenados, nunca texto reescrito |
| 014 | candidatos a contradição | 001 | `livro hesitacoes` lista os parágrafos com palavras-marca da língua do livro ("perhaps", "wrong", "conjecture"...); o julgamento do Claude é gravado só para ids da lista |

## Bloco C — Temas (lê o índice)

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 015 | visão compacta e contagem por assunto | 008, 012 | `livro visao` dá o índice compacto do livro; `livro assuntos` agrupa e conta itens por tipo e capítulo |
| 016 | validador da sugestão de temas | 015 | `livro validar-temas` confere um arquivo no formato M-003: ids existem, todo candidato tem enigma, números e rachadura com ids, casas sem assunto órfão |

## Bloco D — Pesquisa web (escreve as fontes externas)

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 017 | página web vira fonte com ids | 001 | `livro fonte-web <url>` baixa, quebra em parágrafos com id e grava autor, título, data e URL; a origem `[W ...]` sai do script |
| 018 | busca web gratuita | 017 | `livro pesquisar-web "<pergunta>"` busca, baixa os primeiros resultados e grava cada um como fonte; bloqueio do buscador vira erro claro, não silêncio |
| 019 | PDFs externos | 002, 017 | PDF em `externas/` vira fonte `[E ...]` com ids, pelo mesmo caminho do livro |

## Bloco E — Briefing e conferência do roteiro (lê índice, temas e fontes)

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 020 | validador do briefing | 016, 017 | `livro validar-briefing` confere o formato M-001: seções presentes, ids existem, toda linha tem origem, citação prevista transcrita por script |
| 021 | casa dos assuntos | 020 | passagem marcada "desenvolver" que é casa de outro vídeo gera aviso, sem bloquear; "mencionar" nunca avisa |
| 022 | contar e conferir citações do capítulo | 006 | `livro contar` dá palavras e minutos só do texto narrado; toda citação do capítulo é conferida no literal |

## Bloco F — Tradução, humanização e aprovação

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 023 | glossário | 001 | `livro glossario` grava termo → tradução por livro e língua; o mesmo termo com duas traduções no roteiro gera alerta |
| 024 | invariantes entre versões | 022 | `livro invariantes <antes> <depois>` aponta parágrafo em que mudou citação, marca de origem, número ou nome |
| 025 | legibilidade en/fr | — | `livro legibilidade` dá, por parágrafo, tamanho de frase, palavras fora da lista de vocabulário e expressões idiomáticas marcadas |
| 026 | retrotradução local | 023 | `livro retraduzir` grava a versão em português, parágrafo por parágrafo, com os termos do glossário respeitados |
| 027 | tela lado a lado | 026, 024 | `livro lado-a-lado` gera o HTML da M-002 sem rede e sem tokens; parágrafo com alerta aparece marcado |

## Bloco G — Orquestração (skills do Claude Code)

As skills são prompts: o resultado delas não é sim/não e não passa por teste automático de conteúdo.
Cada uma vira fatia **depois** do núcleo que ela usa, com aceite pelo validador do arquivo que ela
produz + roteiro manual. As skills são escritas pelo arquiteto (D-019).

| NNN | nome | depende de | como se sabe que ficou pronta |
|-----|------|-----------|-------------------------------|
| 028 | /novo-livro e /indexar | 005, 009, 011, 012, 013, 014 | um livro de teste sai convertido, indexado e com resumos, sem o Claude ler o livro |
| 029 | /temas | 016 | o arquivo de sugestão passa no `validar-temas` |
| 030 | /pesquisar e /completar | 018, 019 | o dossiê só tem origens `[L]`, `[W]`, `[E]` que existem |
| 031 | /briefing | 020, 021, 029, 030 | os 6 briefings passam no `validar-briefing` |
| 032 | /escrever e /revisar | 022, 031 | cada capítulo passa no `contar` e na conferência de citações |
| 033 | /traduzir e /humanizar | 023, 024, 025, 027 | o capítulo humanizado passa nas invariantes e gera a tela lado a lado |
