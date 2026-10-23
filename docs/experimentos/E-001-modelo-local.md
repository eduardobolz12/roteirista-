# E-001 — Modelo local na RTX 2060

Objetivo: medir, antes de decidir, se um modelo local consegue fazer o trabalho de leitura do livro
(apontar ids, resumir capítulo) e a retrotradução para português, nesta máquina (RTX 2060, 24 GB
de RAM livres, HD).

Gabarito: o índice que o Sonnet fez no piloto para o mesmo capítulo
(`indice/04-3-the-calabar-hypothesis.txt`, 35 itens, 3 contradições, 4 números).

Tempo estimado: 1 hora, quase toda esperando download.

## Caminhos usados

```powershell
$PILOTO = "C:\Users\alder\OneDrive\Documentos\VScode\projetos\roteiros\roteiros-youtube\livros\serpent-and-the-rainbow"
$EXP = "C:\dev\projetos\roteirista\docs\experimentos\E-001"
```

Rode essas duas linhas no começo de cada janela do PowerShell.

## Passo 0 — VRAM da placa

```powershell
nvidia-smi --query-gpu=name,memory.total --format=csv
```

Anote o resultado (medido: 12 GB, RTX 2060 12 GB).

## Passo 1 — Instalar o Ollama

1. Baixe e instale de https://ollama.com/download (Windows).
2. Variáveis de ambiente do usuário (Configurações → Sistema → Sobre → Configurações avançadas →
   Variáveis de ambiente → Novo, em "Variáveis de usuário"):
   - `OLLAMA_CONTEXT_LENGTH` = `16384` (um capítulo inteiro cabe)
   - `OLLAMA_KEEP_ALIVE` = `30m` (o modelo fica carregado; recarregar do HD custa caro)
3. Feche o Ollama pelo ícone da bandeja e abra de novo, para valer.

## Passo 2 — Baixar os modelos

```powershell
ollama pull qwen3:8b
ollama pull qwen3:14b
```

(~5 GB e ~9 GB. Com 12 GB de VRAM o 14B cabe inteiro na placa; comparamos qualidade e velocidade.)

## Passo 3 — Tempo de carga do HD

```powershell
Measure-Command { ollama run qwen3:8b "Responda só: ok /no_think" } | Select-Object TotalSeconds
Measure-Command { ollama run qwen3:8b "Responda só: ok /no_think" } | Select-Object TotalSeconds
```

A primeira medida é a carga fria (do HD). A segunda é com o modelo já carregado.

## Passo 4 — Testes

Antes dos testes, nesta mesma janela (sem isso, o PowerShell troca os acentos por `?`):

```powershell
$OutputEncoding = [Console]::OutputEncoding = [Text.UTF8Encoding]::new()
New-Item -ItemType Directory -Force $EXP | Out-Null
```

### Teste A — Apontar passagens (o trabalho do leitor)

```powershell
$cap = Get-Content "$PILOTO\texto\04-3-the-calabar-hypothesis.md" -Raw -Encoding UTF8
$p = Get-Content "$EXP\..\E-001-prompt-A.txt" -Raw -Encoding UTF8
($p + "`n`n" + $cap) | ollama run qwen3:8b --verbose *> "$EXP\saida-A-qwen3.txt"
```

### Teste B — Resumo técnico do capítulo em português

```powershell
$p = Get-Content "$EXP\..\E-001-prompt-B.txt" -Raw -Encoding UTF8
($p + "`n`n" + $cap) | ollama run qwen3:8b --verbose *> "$EXP\saida-B-qwen3.txt"
```

### Teste C — Retrotradução para português

```powershell
$en = Get-Content "$PILOTO\temas\01-narcisse\roteiro\roteiro-en.md" -Raw -Encoding UTF8
$p = Get-Content "$EXP\..\E-001-prompt-C.txt" -Raw -Encoding UTF8
($p + "`n`n" + $en.Substring(0, [Math]::Min(4000, $en.Length))) | ollama run qwen3:8b --verbose *> "$EXP\saida-C-qwen3.txt"
```

### Teste A com o 14B

```powershell
$p = Get-Content "$EXP\..\E-001-prompt-A.txt" -Raw -Encoding UTF8
($p + "`n`n" + $cap) | ollama run qwen3:14b --verbose *> "$EXP\saida-A-qwen3-14b.txt"
```

## Passo 5 — Entrega

Escreva no fim deste arquivo, na seção "Anotações do Decisor":

- a VRAM (passo 0) e os dois tempos do passo 3;
- se algum comando deu erro (copie a mensagem);
- sua opinião em uma linha sobre o Teste B (o resumo faz sentido?) e o Teste C (o português fiel
  ao inglês?).

Depois me avise. Eu comparo `saida-A-*.txt` com o gabarito do Sonnet e preencho a tabela.

## Resultados (preenchido pelo arquiteto)

Rodado em 2026-10-23 pelo arquiteto, com autorização do Decisor. Máquina: RTX 2060 **12 GB**,
Ollama 0.40.9, contexto 16384, temperatura 0, `think: false`. Capítulo: 04 (Calabar), 38
parágrafos, ~5.400 tokens. Saídas em `E-001/`.

### Velocidade

| Medida | qwen3:8b | qwen3:14b |
|---|---|---|
| Carga fria do HD | ~111 s (com subida do servidor) | 148 s |
| Carga com modelo já na memória | ~5 s | ~7 s |
| Leitura (tokens/s) | ~1.300 | ~300–650 |
| Escrita (tokens/s) | ~45 | ~11 |
| Teste A (capítulo inteiro) | 40 s | 268 s (com carga) |
| VRAM usada | 7,5 GB, 100% GPU | 11,3 GB (no limite) |

### Teste A — índice completo numa passada (gabarito: Sonnet do piloto)

| Medida | qwen3:8b | qwen3:14b | Sonnet |
|---|---|---|---|
| Itens | 38 | 31 | 35 |
| Formato válido | 38/38 | 0/31 (ids entre colchetes) | 100% |
| Ids inexistentes | 0 | 0 | 0 |
| Cobertura de parágrafos | 38/38 (um item por parágrafo, mecânico) | 30/38 | — |
| Números (de 4) | 0 (o único `numero` é lixo: 04.016) | 0 | 4 |
| Contradições (de 3) | 1 (04.038) | 1 (04.038) | 3 |
| "doutrina" | 20 de 38 | 11 de 31 | 17 de 35 |

Qualidade das afirmações (8B): viola a regra "o que o texto afirma" ("O autor descreve…") e tem
erro de fato (04.025: "origem africana"; o texto diz Ásia).

### Teste A2 — uma pergunta por passada

| Pergunta | qwen3:8b | qwen3:14b |
|---|---|---|
| Números | 2 certos (021, 023); 1779 e 10 pés com **id errado** (025, 032); 4 linhas lixo; faltou 400 mil | 3 certos (021, 023, 033) + 1 válido fora do gabarito (015); 1779 e 400 mil com **id errado** (025 em vez de 028); 1 inventado ("16 sementes") |
| Contradições | "nenhum" | "nenhum" |

Primeira tentativa do 8B entrou em **loop de repetição** (>10 min); resolvido com
`num_predict` e `repeat_penalty`.

### Teste B — resumo técnico em português

- 8B: estrutura ok; números razoáveis (028, 033 certos); "incertezas" inventadas (04.023, 04.038 com
  sentido trocado).
- 14B: temas e cenas bons, com intervalos de ids corretos; seção de números é lixo (título,
  páginas) e **inventou o id 04.000**; acertou a contradição de 04.037.

### Teste C — retrotradução en → pt (comparada com o `roteiro-pt.md` original)

- 8B: entendível, mas com erros que pareceriam erro da tradução: "tirou uma foto" (got = recebeu),
  "peixes-palitos" (baiacu), "pepita do zumbi" (pepino), "caixa de madeira" (caixão).
- 14B: claramente melhor ("obteve uma foto", "pepino do zumbi", "droga", "por dentro"); erro em
  "peixe-palha" (baiacu).

### Conclusões do arquiteto

1. **Velocidade não é problema.** 8B lê um capítulo em segundos; 14B em poucos minutos. Livro
   inteiro: minutos (8B) a ~1 h (14B).
2. **Ids:** os dois modelos apontam para parágrafos que existem, mas **erram o parágrafo** (vizinho,
   até 3 de distância) e às vezes inventam (04.000). Validador por script é obrigatório; e todo
   apontamento com âncora verificável (número, nome, termo) pode ser conferido no literal pelo
   script — o "1779" não está em 04.025, está em 04.028.
3. **Extração simples** (números, cenas, temas): utilizável com o 14B + conferência por script.
4. **Interpretação** (contradição, hesitação do autor): **os dois falham** — "nenhum" num capítulo
   que diz "conjecture" e "wrong" explicitamente. Modelo local não substitui o Sonnet nisso.
5. **Retrotradução:** 14B serve para o Decisor ler; 8B introduz ruído. Glossário no prompt deve
   corrigir termos (baiacu, pepino do zumbi).

## Anotações do Decisor

