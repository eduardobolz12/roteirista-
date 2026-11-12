# SPEC 020 — Validador do briefing

**Estado:** exemplos aprovados pelo Decisor em 2026-11-11; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que o briefing de cada capítulo chegue até mim conferido (seções presentes, toda
passagem e todo dado com origem que existe, citações iguais ao livro), para que eu aprove o conteúdo
sem precisar conferir ids (D-010, D-028).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro validar-briefing <slug> <arquivo>`.

## Fora de escopo
- A casa dos assuntos entre vídeos: é a SPEC 021.
- Julgar se o momento é bom ou se a duração cabe.

## Formatos
Valem os formatos das SPECs anteriores e o **id no texto** da SPEC 016. Acrescentam-se:

- **Arquivo:** Markdown no formato de `docs/maquetes/M-001-briefing-cap3.md`, com:
  - os campos (linhas que começam por `**<nome>:**`) `Tema`, `Capítulo`, `Função do capítulo`,
    `Ao fim, o espectador entende` e `Duração estimada`;
  - as seções `O que será abordado`, `Cenas e passagens do livro`, `Citações literais previstas`,
    `Dados da web`, `O que fica de fora deste capítulo`, `Ressalvas` e `Sua decisão`.
- **Tabelas** (as linhas abaixo do cabeçalho, sem a linha `|---|`):
  - `O que será abordado`: `# | Momento | O que entra | De onde vem`; `De onde vem` é `Livro`, `Web`
    ou `Narrador`;
  - `Cenas e passagens do livro`: `Id | O que é | Momento | Trato`; `Momento` é um ou mais números de
    momento que existem (`1`, `1 e 2`, `1, 3`); `Trato` é `desenvolver` ou `mencionar`;
  - `Citações literais previstas`: `Id | Trecho (original) | Uso`; o trecho, sem as aspas das pontas,
    confere no texto do id pela regra de citação da D-028;
  - `Dados da web`: `Id | Dado | Uso`.
- **Regra de citação (D-028):** as palavras do trecho (sequências de letras e algarismos, em NFC, sem
  diferenciar maiúsculas) aparecem seguidas e na mesma ordem nas palavras do texto do id; num
  intervalo, nos textos dos ids juntos, em ordem. `...` ou `…` cortam o trecho em partes, e cada parte
  tem de aparecer depois da anterior.
- **Origem:** cada momento `Livro` tem pelo menos uma linha em `Cenas e passagens` que o cita; cada
  momento `Web` tem pelo menos uma linha em `Dados da web`.
- **Saída:** um problema por linha, nesta ordem: os campos que faltam (`falta o campo: <nome>`) e as
  seções que faltam (`falta a seção: <nome>`), na ordem acima; depois os problemas de uma linha do
  arquivo, pelo número da linha e, na mesma linha, na ordem das colunas
  (`<linha>: id inexistente: <id ou intervalo, como está no arquivo>`,
  `<linha>: momento inexistente: <n>`, `<linha>: trato inválido: <valor>`,
  `<linha>: origem inválida: <valor>`, `<linha>: citação não confere em <id>: <trecho>`); depois os de
  momento, pelo número (`momento <n>: origem Livro sem passagem`, `momento <n>: origem Web sem dado`).
  Por fim `<P> problemas`, código `1`. Sem problema: só
  `ok: <M> momentos, <C> passagens, <Q> citações, <D> dados da web`, código `0`. Arquivo que não
  existe: como na SPEC 016.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`), com a fonte `W01` gravada pelo `livro fonte` da SPEC 017
(o mesmo artigo de teste, num servidor falso), e três arquivos em `fixtures/`:

- `briefing-ok.md`: tema 1, capítulo 1; momentos 1 `Livro`, 2 `Narrador` e 3 `Web`; passagens `01.001`
  (momento 1, desenvolver) e `01.002-01.003` (momento 1, mencionar); a citação `01.001`
  `"leu o próprio nome gravado no cimento"`; o dado `W01.002`.
- `briefing-erros.md`: o mesmo, sem o campo `Função do capítulo`, com a passagem `01.001` no momento `4`
  (linha 21), a passagem `01.002-01.009` no momento 2 com trato `aprofundar` (linha 22), a citação
  `"leu o nome próprio gravado no cimento"` (linha 28) e sem dado da web.
- `briefing-incompleto.md`: sem as seções `Citações literais previstas` e `Ressalvas`, e com o dado
  `W05.001` (linha 29).

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro com a W01 e `briefing-ok.md` | `livro validar-briefing teste briefing-ok.md` | código `0`; stdout exatamente `ok: 3 momentos, 2 passagens, 1 citações, 1 dados da web\n` |
| CA-2 | o livro com a W01 e `briefing-erros.md` | `livro validar-briefing teste briefing-erros.md` | código `1`; stdout exatamente `falta o campo: Função do capítulo\n21: momento inexistente: 4\n22: id inexistente: 01.002-01.009\n22: trato inválido: aprofundar\n28: citação não confere em 01.001: leu o nome próprio gravado no cimento\nmomento 1: origem Livro sem passagem\nmomento 3: origem Web sem dado\n7 problemas\n` |
| CA-3 | o livro com a W01 e `briefing-incompleto.md` | `livro validar-briefing teste briefing-incompleto.md` | código `1`; stdout exatamente `falta a seção: Citações literais previstas\nfalta a seção: Ressalvas\n29: id inexistente: W05.001\n3 problemas\n` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/020-validar-briefing --junitxml=relatorios/020-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, o módulo dos validadores (SPEC 016)

## Arquivo-exemplo
O validador da SPEC 016.

## Roteiro manual (3 passos)
1. Rode `livro validar-briefing serpent` com o briefing real do capítulo 1 do Bizango que o arquiteto
   montou (cena 15.075 a 15.089, o canto 15.082-15.085 citado com outra pontuação, o dado W02.001):
   `ok`.
2. Rode com `docs/maquetes/M-001-briefing-cap3.md`: faltam os campos `Tema` e `Capítulo` e a coluna
   `Trato`, e os ids do piloto não existem.
3. Troque uma palavra da citação do canto e rode de novo: `citação não confere`.

## Decisões pendentes
nenhuma
