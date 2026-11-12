# SPEC 026 — Retrotradução local

**Estado:** exemplos aprovados pelo Decisor em 2026-11-12; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero o roteiro traduzido ou humanizado de volta em português, parágrafo por parágrafo,
feito pelo modelo local com o glossário do livro, para aprovar o texto em inglês ou francês lendo em
português, sem gastar tokens (D-012).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS` e `ROTEIRISTA_OLLAMA`: `livro retraduzir <slug> <roteiro>`.

## Fora de escopo
- Julgar a retrotradução e mostrar os alertas: é a tela lado a lado (SPEC 027).
- Retraduzir de outra língua que não `en` ou `fr`.

## Formatos
Valem os formatos das SPECs anteriores, o **roteiro** da SPEC 023, a **língua do arquivo** da SPEC 024 e
as **citações** da SPEC 022. Acrescentam-se:

- **Língua:** a do nome do roteiro, `en` ou `fr`. Roteiro `pt`: stderr `o roteiro já está em português:
  <nome do arquivo>`, código `2`. Sem língua no nome: `língua desconhecida: <nome do arquivo>`, código `2`.
  Arquivo que não existe: como na SPEC 016.
- **Pedido:** um por parágrafo, na ordem do roteiro, ao Ollama como o do índice (SPEC 008): modelo
  `qwen3:14b`, `"think": false`, temperatura 0. O prompt é `docs/prompts/retraduzir.txt` com:
  - `{lingua}`: `inglês` ou `francês`;
  - `{capitulo}`: os parágrafos do capítulo, separados por uma linha em branco, com cada citação trocada
    por `⟦c⟧`;
  - `{texto}`: o parágrafo, com a k-ésima citação trocada por `⟦k⟧`;
  - `{glossario}`: se a tradução de algum termo do glossário do livro nessa língua aparece no parágrafo
    (alguma forma, palavra inteira, sem diferenciar maiúsculas, fora das citações), a linha
    `- Use estas traduções:` e, para cada termo assim, em ordem alfabética da tradução sem diferenciar
    maiúsculas, a linha `  <formas da tradução, separadas por ", "> → <formas do termo, separadas por ", ">`;
    cada linha termina em quebra de linha. Sem termo, vazio.
- **Resposta:** sem o trecho `<think>…</think>`, com os espaços e quebras de linha seguidos trocados por um
  espaço e as pontas aparadas; cada `⟦k⟧` vira a k-ésima citação do parágrafo. Se as marcas da resposta não
  forem exatamente `⟦1⟧` a `⟦K⟧`, uma vez cada (K = citações do parágrafo): stdout `<n>.<p>: citação perdida
  na retrotradução`, e o parágrafo é gravado assim mesmo.
- **Saída:** o arquivo `retro-pt-<nome do roteiro>`, na pasta do roteiro, trocado se já existir: a linha
  `# Retrotradução de <nome do roteiro> (qwen3:14b)`, uma linha em branco e, para cada capítulo, `## <n>`,
  uma linha em branco e cada parágrafo seguido de uma linha em branco. No stdout, depois dos avisos,
  `<P> parágrafos retraduzidos em <nome da saída>`; código `0`.
- **Modelo fora do ar:** depois das tentativas da SPEC 008, stderr `modelo inacessível: <url>`, código `3`,
  e nenhum arquivo gravado.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`) e, em `fixtures/`:

- `roteiro-en.md`, dois capítulos: no 1, um parágrafo com "machete" e a citação
  `"leu o próprio nome gravado no cimento" [01.001]`, e um com "1962" e "two doctors"; no 2, um parágrafo
  com "society";
- `outro-en.md`: um parágrafo com a mesma citação;
- `respostas.json`: para cada parágrafo enviado (o `{texto}`), a resposta do Ollama falso; a de
  `outro-en.md` vem sem a marca `⟦1⟧`;
- `roteiro-pt.md` e `notas.md`.

Glossário `en` do livro nos três CAs: `facão → machete` e `sociedade|sociedades → society|societies`.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro e o glossário | `livro retraduzir teste roteiro-en.md` | código `0`; stdout exatamente `3 parágrafos retraduzidos em retro-pt-roteiro-en.md\n`; `retro-pt-roteiro-en.md` exatamente `# Retrotradução de roteiro-en.md (qwen3:14b)\n\n## 1\n\nO secretário ergue o facão e lê a data: "leu o próprio nome gravado no cimento" [01.001].\n\nEm 1962, dois médicos assinaram a certidão.\n\n## 2\n\nA sociedade julga a alma, não o corpo.\n\n`; 3 pedidos com o modelo `qwen3:14b`; o primeiro prompt contém `  machete → facão\n- Escreva só a tradução do PARÁGRAFO.`, `CAPÍTULO:\n\nThe secretary raises the machete and reads the date: ⟦c⟧.\n\nIn 1962, two doctors signed the certificate.\n\nPARÁGRAFO:\n\nThe secretary raises the machete and reads the date: ⟦1⟧.`; o segundo não contém `Use estas traduções`; o terceiro contém `  society, societies → sociedade, sociedades\n` |
| CA-2 | o livro e o glossário | `livro retraduzir teste outro-en.md` | código `0`; stdout exatamente `1.1: citação perdida na retrotradução\n1 parágrafos retraduzidos em retro-pt-outro-en.md\n`; `retro-pt-outro-en.md` exatamente `# Retrotradução de outro-en.md (qwen3:14b)\n\n## 1\n\nEle lê a data.\n\n` |
| CA-3 | o livro, com o Ollama fora do ar | `livro retraduzir teste roteiro-en.md`, `livro retraduzir teste roteiro-pt.md` e `livro retraduzir teste notas.md` | o primeiro com código `3`, `modelo inacessível:` no stderr e sem `retro-pt-roteiro-en.md`; o segundo com código `2` e `o roteiro já está em português: roteiro-pt.md` no stderr; o terceiro com código `2` e `língua desconhecida: notas.md` no stderr |

## Risco declarado
O modelo local erra: no ensaio E-009, sem o contexto do capítulo e sem a regra dos nomes, traduziu
"Narcisse" e "Saint Marc", trocou "sentence" por "frase" e "harming" por "matar". A tela (SPEC 027) marca
o que as conferências pegam; o resto, o Decisor lê sabendo que a retrotradução é do modelo local.

## Como rodar os testes
```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/026-retrotraducao-local --junitxml=relatorios/026-junit.xml
```
As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, o módulo das conferências da tradução (leitura do roteiro e citações), o módulo
  do modelo local (pedido ao Ollama) e `src/roteirista/prompts/retraduzir.txt`, cópia de
  `docs/prompts/retraduzir.txt`.

## Arquivo-exemplo
O subcomando `indexar` (pedido ao Ollama, tentativas e modelo fora do ar) e a SPEC 023 (glossário).

## Roteiro manual (3 passos)
1. `livro retraduzir serpent livros/serpent/temas/1/roteiro-en-humanizado.md` (uns 8 minutos): 62
   parágrafos, nenhuma citação perdida.
2. `livro invariantes serpent livros/serpent/temas/1/roteiro-en-humanizado.md livros/serpent/temas/1/retro-pt-roteiro-en-humanizado.md`:
   nenhum nome traduzido ("Narcisse", "Saint Marc" e os títulos dos filmes voltam como estão).
3. Leia a retrotradução de 3.4, 5.6 e 1.7: "prejudicar a própria família", "é uma sentença" e "o
   secretário… ele", não "matar", "frase" nem "a secretária".

## Decisões pendentes
nenhuma
