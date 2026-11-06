# SPEC 036 — Medida da linha em PDF comercial

**Estado:** exemplos aprovados pelo Decisor em 2026-11-06; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que as regras de parágrafo da SPEC 035 funcionem num PDF comercial de verdade,
e não só num PDF simples, para que o parágrafo do livro saia inteiro, sem a primeira linha cortada.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro novo` e `livro trecho`.

## Substitui
Nada. Esta spec fixa como valem as medidas da SPEC 035.

## Fora de escopo
- Mudar as regras da SPEC 035: elas continuam as mesmas.
- PDF com páginas giradas ou com colunas.
- Junção de linhas (SPEC 037).

## Formatos
Valem os formatos das SPECs anteriores. Acrescenta-se:

- **Medidas na página impressa:** margens, início e fim de linha e o tamanho `T` da SPEC 035 são
  medidos como a linha aparece impressa na página, qualquer que seja o jeito de o PDF desenhar o
  texto: com escala na página, com fonte embutida, letra por letra, com a justificação nos espaços
  entre palavras.

## Tabela de CA

Fixture: `tests/acceptance/036-medida-da-linha/fixtures/recuo-escala.pdf`, gerada por `_gerar_pdf.py`
na mesma pasta. Tem o mesmo texto e a mesma organização do PDF da SPEC 035, com o desenho de um PDF
comercial: fonte embutida, cada letra posicionada num bloco de texto por linha, justificação nos
espaços e a página inteira reduzida por uma escala de 0,72.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `recuo-escala.pdf`; pasta vazia | `livro novo recuo-escala.pdf --slug teste`, `livro trecho teste 01.002`, `01.003`, `01.004` e `01.005` | última linha do `novo` é `3 capítulos, 17 parágrafos`; `01.002` é exatamente `A irmã do morto contou a história na manhã seguinte, à porta da igreja, sem pressa, enquanto os vizinhos fingiam não ouvir nada do que ela dizia. Ninguém na aldeia duvidou daquela versão. Os mais velhos lembravam o enterro e o nome gravado na cruz de madeira do cemitério.\n`; `01.003` termina em `por causa da neve e\n`; `01.004` é exatamente `Na primavera, o bispo mandou buscar o livro e nunca o devolveu.\n`; `01.005` sai com código `2` |
| CA-2 | o mesmo livro | `livro trecho teste 02.001` a `02.006` | exatamente, nesta ordem: `O legista escreveu ao bispo e descreveu o que tinha visto no corpo, dizendo apenas isto:\n`, `O paciente estava pálido e consciente, com o pulso pequeno e intermitente, e a respiração foi ficando difícil até cessar.\n`, `Depois disso, o bispo não respondeu a nenhuma carta do legista e o caso foi esquecido.\n`, `"Professor."\n`, `"Sim?"\n` e `"O senhor leu a carta do legista antes de mandar buscar o livro?"\n` |
| CA-3 | o mesmo livro | `livro trecho teste 03.001`, `03.004`, `03.007` e `03.008` | `03.001` é exatamente `ASSON Chocalho sagrado feito de cabaça e usado pelo sacerdote nos ritos.\n`; `03.004` é `CANZO O rito do fogo.\n`; `03.007` é `MAMBO A sacerdotisa do vodu, que conduz a cerimônia e guarda o asson.\n`; `03.008` sai com código `2` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/036-medida-da-linha --junitxml=relatorios/036-junit.xml
```

As suítes 001 a 007, 034 e 035 têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/pdf.py`

## Arquivo-exemplo
`src/roteirista/pdf.py`: `_linhas_da_pagina`.

## Roteiro manual (3 passos)
1. Apague `livros\serpent`, reconverta o Serpent com `--lingua en` e leia a linha de resumo: perto de
   1.485 parágrafos (a conta do arquiteto antes da construção).
2. Rode `livro trecho serpent 04.001`: o parágrafo inteiro, não só a linha "MY FIRST MEETING…".
3. Rode `livro trecho serpent 10.083`: é o parágrafo `08.083` do piloto ("It didn't take me long…").

## Decisões pendentes
nenhuma
