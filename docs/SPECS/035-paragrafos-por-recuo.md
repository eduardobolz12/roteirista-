# SPEC 035 — Parágrafos por recuo

**Estado:** exemplos e limitação aprovados pelo Decisor em 2026-11-06; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que os parágrafos de um livro comercial saiam como o autor os escreveu, mesmo
quando nada os separa além do recuo da primeira linha, para que um id aponte para um parágrafo e não
para páginas inteiras de texto.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro novo` e `livro trecho`.

## Substitui
Esta spec não altera as SPECs anteriores; onde divergem, vale esta (D-020):

- SPEC 001, **Parágrafo**: o recuo horizontal também separa parágrafos.
- SPEC 002, **Virada de página**: num capítulo com recuo, quem decide é o recuo, não a pontuação.

## Fora de escopo
- Juntar os versos de um poema: cada verso sai como um parágrafo (limitação aceita, ver abaixo).
- Citação em bloco que atravessa a página.
- EPUB, onde o parágrafo já vem marcado.

## Formatos
Valem os formatos das SPECs anteriores. Valem por capítulo e olham só as linhas na fonte do corpo.
`T` é o tamanho da fonte do corpo.

- **Margens:** a margem esquerda é a posição mais à esquerda das linhas; a direita é a posição de
  fim de linha mais frequente.
- **Linha recuada:** começa mais de `0,6 T` à direita da margem esquerda.
- **Linha cheia:** termina a menos de `0,6 T` da margem direita.
- **Linha curta:** termina a mais de `2,5 T` da margem direita.
- **Capítulo com recuo:** tem 3 linhas recuadas ou mais. Os demais seguem as regras anteriores.
- **Capítulo de glossário:** capítulo com 5 ou mais linhas recuadas logo depois de uma linha sem
  recuo, em que mais de 80% delas vêm depois de uma linha cheia. Nele, toda linha sem recuo abre um
  parágrafo e toda linha recuada continua o anterior.
- **Nos demais capítulos com recuo:**
  - salto vertical maior que `1,6` vez a entrelinha abre parágrafo, como antes;
  - linha recuada abre parágrafo, exceto na **citação em bloco**: a linha anterior é recuada, sem
    ser cheia nem curta, e a linha atual não é cheia. Aí ela continua a citação;
  - linha sem recuo abre parágrafo quando a anterior é recuada e não é cheia (fim de citação ou de
    fala curta), ou quando a anterior é curta e termina em `.`, `!`, `?`, `…` ou `:`, seguidos ou
    não de aspas de fechamento;
  - qualquer outra linha continua o parágrafo, **também na virada de página**.
- As partes se unem com um espaço, aplicando a regra da hifenização (SPEC 002).

## Tabela de CA

Fixture: `tests/acceptance/035-paragrafos-por-recuo/fixtures/recuo.pdf`, gerada por `_gerar_pdf.py`
na mesma pasta. PDF A5 de 5 páginas com 3 marcadores, entrelinha constante, sem espaço entre
parágrafos. O texto exato está no gerador.

- **Capítulo Um** (páginas 1 a 3): prosa com recuo. A página 1 termina em `…daquela versão.` e a 2
  continua na margem. A página 2 termina em `…por causa da neve e` e a 3 começa com recuo.
- **Capítulo Dois** (página 4): prosa, citação em bloco com recuo dos dois lados e diálogo curto.
- **Glossário** (página 5): entrada na margem, continuação recuada, com uma entrada de uma linha só.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `recuo.pdf`; pasta vazia | `livro novo recuo.pdf --slug teste`, `livro trecho teste 01.002`, `01.003`, `01.004` e `01.005` | última linha do `novo` é `3 capítulos, 17 parágrafos`; `01.002` é exatamente `A irmã do morto contou a história na manhã seguinte, à porta da igreja, sem pressa, enquanto os vizinhos fingiam não ouvir nada do que ela dizia. Ninguém na aldeia duvidou daquela versão. Os mais velhos lembravam o enterro e o nome gravado na cruz de madeira do cemitério.\n`; `01.003` termina em `por causa da neve e\n`; `01.004` é exatamente `Na primavera, o bispo mandou buscar o livro e nunca o devolveu.\n`; `01.005` sai com código `2` |
| CA-2 | o mesmo livro | `livro trecho teste 02.001` a `02.006` | exatamente, nesta ordem: `O legista escreveu ao bispo e descreveu o que tinha visto no corpo, dizendo apenas isto:\n`, `O paciente estava pálido e consciente, com o pulso pequeno e intermitente, e a respiração foi ficando difícil até cessar.\n`, `Depois disso, o bispo não respondeu a nenhuma carta do legista e o caso foi esquecido.\n`, `"Professor."\n`, `"Sim?"\n` e `"O senhor leu a carta do legista antes de mandar buscar o livro?"\n` |
| CA-3 | o mesmo livro | `livro trecho teste 03.001`, `03.004`, `03.007` e `03.008` | `03.001` é exatamente `ASSON Chocalho sagrado feito de cabaça e usado pelo sacerdote nos ritos.\n`; `03.004` é `CANZO O rito do fogo.\n`; `03.007` é `MAMBO A sacerdotisa do vodu, que conduz a cerimônia e guarda o asson.\n`; `03.008` sai com código `2` |

## Limitação aceita
Cada verso de um poema sai como um parágrafo. No Serpent isso afeta 5 capítulos (2, 4, 9, 12 e 13
do livro). O texto continua literal e conferível; só há mais ids.

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/035-paragrafos-por-recuo --junitxml=relatorios/035-junit.xml
```

As suítes 001 a 007 e 034 têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/pdf.py`

## Arquivo-exemplo
`src/roteirista/pdf.py`: `_paragrafos`. Referência de comportamento: a detecção de recuo do
`converter` em `ferramentas/livro.py` do piloto.

## Roteiro manual (3 passos)
1. Apague `livros\serpent`, reconverta o Serpent com `--lingua en` e rode
   `livro trecho serpent 10.083`: é o parágrafo `08.083` do piloto ("It didn't take me long…").
2. Rode `livro medir serpent`: nenhum capítulo passa de 20 mil tokens.
3. No PDF, escolha uma citação em bloco (página 106 do arquivo) e confira com `buscar` e `trecho`
   que ela saiu como um parágrafo só.

## Decisões pendentes
nenhuma
