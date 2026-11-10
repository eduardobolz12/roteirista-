# E-002 — Indexação real do Serpent

Rodado em 2026-11-06 pelo arquiteto, antes das SPECs 008 a 011, como manda a D-021. Modelo
`qwen3:14b`, Ollama local, temperatura 0, `think: false`, `num_ctx` 16384, `num_predict` 3000,
`repeat_penalty` 1.1. Parágrafos lidos do banco gerado pelo núcleo no commit `36a514c`. Saídas em
`E-002/`.

## Pergunta

1. Ler em janelas rende mais do que ler o capítulo inteiro?
2. O modelo consegue copiar uma âncora literal, para o script conferir o id sem interpretar português?
3. A repescagem fecha as lacunas?

## Resultados

Capítulo 06 (Calabar, 38 parágrafos, 5,8 mil tokens) e capítulo 14 (Tell My Horse, 59 parágrafos, 17
mil tokens, o maior).

| Rodada | Linhas | Âncora no id | Corrigível no vizinho | Não achada | Parágrafos cobertos | Tempo |
|---|---|---|---|---|---|---|
| 06, inteiro, prompt 1 | 38 | 30 | 3 | 5 | 30/38 | 251 s |
| 06, janela 2000, prompt 1 | 85 | 65 | 3 | 17 | 34/38 | 308 s |
| 14, janela 2000, prompt 1 | 242 | 206 | 11 | 24 | 59/59 | 693 s |
| **06, janela 2000, prompt 2** | **62** | **53** | **5** | **4** | **33/38** | **181 s** |

Em nenhuma rodada houve id inventado. Uma única linha teve tipo inválido (`afirmacao`, no capítulo 14).

O prompt 1 pedia a âncora "copiada exatamente". O modelo traduzia (`400.000 escravos`, `10 pés`). O
prompt 2, hoje em `docs/prompts/indexar.txt`, proíbe a tradução com um exemplo e limita a 3 linhas por
parágrafo.

Correções por vizinho com o prompt 2, lidas uma a uma pelo arquiteto: as 5 parecem certas, entre elas
`four hundred thousand slaves`, de `06.027` para `06.028`, o mesmo erro de id visto no E-001.

**Repescagem**, capítulo 06, prompt em `docs/prompts/repescar.txt`: 5 lacunas, 31 s, 4 fechadas. A
quinta é o ornamento `•`, de um caractere. Daí a regra de que parágrafo sem letra nem número não é
lacuna.

## Conclusões

1. **Janela de 2000 tokens** como padrão.
2. **Âncora literal no item.** Ela transforma a conferência da D-003 em comparação de texto, e vale para
   todo tipo de item, não só para números.
3. **Item sem âncora é rejeitado.** Com o prompt 2 isso custou 6% dos itens do capítulo 06.
4. **Repescagem** fecha o que sobra.

## Limites

- O prompt 2 só foi medido no capítulo 06. O capítulo 14 foi medido com o prompt 1.
- Um item com âncora certa pode ter afirmação errada: o script não confere o sentido.
- Em itens de tipo `numero`, o modelo ainda erra às vezes: `South Station` e `deathlike stupor` saíram
  como número, com âncora válida. O tipo não é conferido.
- Os números do gabarito do E-001 não foram recontados um a um.
- Tempo do livro inteiro estimado por regra de três, não medido: entre 1h20 e 1h40.
