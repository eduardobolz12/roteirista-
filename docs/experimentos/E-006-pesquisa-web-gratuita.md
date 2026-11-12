# E-006 — Pesquisa web gratuita

**Data:** 2026-11-11 · **Decisão relacionada:** D-008, D-023 · **Fatias que mede:** 017, 018

## Pergunta
As perguntas de web do piloto saem certas por um caminho gratuito (busca + páginas baixadas + modelo
gratuito que responde citando), sem o Claude ler as páginas?

## Montagem
- **Perguntas** (`perguntas.json`): as três do paralelo da anestesia da maquete M-001 (NAP5 geral e com
  bloqueador; sofrimento com paralisia; Sebel 2004) e a que faltava ao capítulo 1 do E-004 (ano e
  recepção do livro).
- **Caminho** (`pesquisar.py`): a busca devolve até 3 fontes; o texto delas vai ao modelo gratuito
  (9Router → OpenRouter `:free`), que responde em linhas `fato | "citação literal" | URL`; o script
  confere se a citação está, letra por letra (sem diferenciar maiúsculas e espaços), na fonte daquela URL.

## O que não funcionou
- **Buscadores comuns bloqueiam acesso automático.** O DuckDuckGo respondeu na primeira consulta e
  depois passou a devolver uma página de verificação (código 202, sem resultados). Contornar esse tipo
  de bloqueio não é caminho para o projeto.
- **O OpenCode Free** estava fora do ar; Gemma e Inkling, indisponíveis (ver E-005).

## O que funcionou
Fontes com acesso aberto e oficial, sem chave:
- **Europe PMC** (artigos científicos: título, autores, ano, resumo);
- **Wikipédia** (API de busca e de texto).

| Pergunta | Esperado | Resposta | Citação confere | Fonte |
|---|---|---|---|---|
| P1 NAP5 | ~1:19.600; ~1:8.200 com bloqueador | **as duas, certas** | sim, sim | Pandit et al. 2014 (MED/25204697) |
| P2 paralisia | sofrimento e dano mais prováveis com paralisia | **certa** na 2ª busca | sim | Cook et al. 2014 (MED/25204696) |
| P3 Sebel | 0,13% | **certa** | sim | Sebel et al. 2004 (MED/15333419) |
| P4 o livro | 1985; best-seller; críticas | **certa**: 1985, best-seller, imprecisões científicas, pouca ou nenhuma tetrodotoxina nas amostras, acusação de fraude | sim (4 de 4) | Wikipédia |

Observações:
- **8 de 8 citações conferem.** Nenhum fato inventado.
- **P2 dependeu das palavras da busca.** A primeira ("psychological consequences") não trouxe o artigo
  de Cook; a segunda ("patient experiences Cook") trouxe. Quem escreve a busca importa.
- **P2 rodou no Nemotron**: o ERNIE atingiu o limite de uso do provedor no meio do teste. A lista de
  reserva de modelos (E-005) foi necessária de verdade.
- **P4 não trouxe a editora nem o filme**: a fonte tinha, a resposta não incluiu. Pergunta mais
  estreita resolve.
- Custo: 3 a 7 mil tokens de entrada por pergunta no modelo gratuito; 3 a 20 segundos. Para o Claude,
  só as linhas conferidas (algumas centenas de tokens), contra cerca de 230 mil tokens de web no piloto.

## Conclusão
1. **O caminho gratuito responde às perguntas do piloto, com citação conferida.** A conferência por
   script é o que torna o resultado confiável, como a conferência de âncora no índice.
2. **A fonte de busca precisa ser uma API aberta, não um buscador.** Europe PMC para dados científicos,
   Wikipédia para contexto e recepção. Cobre bem livro e ciência; não cobre imprensa (o relato
   "Sandra" da M-001 viria de um jornal).
3. Para imprensa e páginas gerais, opções a decidir: a busca do próprio OpenRouter (`:online`, paga,
   centavos por busca), uma chave gratuita de um buscador com API (Brave Search, por exemplo, com limite
   mensal), ou o Claude só nessas lacunas (D-008).

## Para as SPECs 017 e 018
- 017: a fonte é gravada com URL, título, autor e ano; o texto vem da API (resumo ou artigo), quebrado
  em parágrafos com id.
- 018: `pesquisar-web` usa Europe PMC e Wikipédia; aceita a busca escrita pelo Claude; modelos em ordem,
  com reserva; só grava fato cuja citação confere; bloqueio ou limite viram erro claro.
