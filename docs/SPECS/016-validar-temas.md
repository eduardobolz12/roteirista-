# SPEC 016 — Validador da sugestão de temas

**Estado:** exemplos aprovados pelo Decisor em 2026-11-11; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que a sugestão de temas chegue até mim já conferida (ids que existem, enigma,
números e rachadura apontados no livro, cada assunto com uma casa), para que eu só escolha, sem caçar
erro (D-017, D-018).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro validar-temas <slug> <arquivo>`.

## Fora de escopo
- Julgar se o tema é bom: isso é do Claude e do Decisor.
- Conferir as contagens da coluna "Itens no livro".

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Arquivo:** Markdown no formato de `docs/maquetes/M-003-sugestao-temas.md`, com as seções (linhas
  que começam por `## `) `Resumo`, `Assuntos compartilhados e a casa de cada um`,
  `Detalhe de cada candidato` e `Sua decisão`.
- **Id no texto:** id de parágrafo do livro (`CC.PPP`, `CC.nPP`), de fonte (`W01.002`) ou intervalo do
  mesmo capítulo ou fonte (`15.073-15.091`, com hífen ou travessão `–`). Todo id do arquivo tem de
  existir; num intervalo, todos os ids dele.
- **Temas:** as linhas da tabela do `Resumo` que começam por `| <número> |`. Cada tema tem um
  `### <número> — <título>` em `Detalhe de cada candidato`, com três itens que começam por
  `- **Enigma`, `- **Números` e `- **Rachadura`, cada um com pelo menos um id.
- **Mais de um capítulo:** os ids de livro desses três itens de um tema caem em pelo menos 2 capítulos
  do livro (ids de fonte não contam).
- **Casas:** na tabela de `Assuntos compartilhados...`, as linhas abaixo do cabeçalho; as colunas
  depois de `Ids principais` são os temas, em ordem. Cada linha tem exatamente uma célula `casa`
  (sem diferenciar maiúsculas, com ou sem `**`).
- **Saída:** um problema por linha, nesta ordem: as seções que faltam (`falta a seção: <nome>`), na
  ordem acima; depois os problemas de uma linha do arquivo, pelo número da linha
  (`<linha>: id inexistente: <id>`, `<linha>: assunto sem casa`, `<linha>: assunto com mais de uma casa`);
  depois os de tema, pelo número do tema (`tema <n>: falta o detalhe`,
  `tema <n>: falta <o enigma | os números | a rachadura> com id`, `tema <n>: material num só capítulo do livro`).
  Por fim `<P> problemas`, código `1`. Sem problema: só `ok: <T> temas, <A> assuntos`, código `0`.
  Arquivo que não existe: stderr `arquivo inexistente: <arquivo>`, código `2`.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`: `01.001` a `01.003`, `02.001` e `02.002`) e três arquivos em
`fixtures/`:

- `temas-ok.md`: tema 1 `O nome no túmulo` (enigma `[01.001]`, números `[02.001]`, rachadura `[01.002]`)
  e tema 2 `A cova aberta` (enigma `[02.002]`, números `[02.001]`, rachadura `[01.003]`); assuntos
  `O túmulo` (`01.001`; casa no 1) e `A certidão` (`02.001`; casa no 2).
- `temas-erros.md`: o mesmo, com quatro defeitos: a rachadura do tema 1 aponta `[01.009]` (linha 25) e
  a dele passa a ser só do capítulo 01 (enigma `[01.001]`, números `[01.003]`); o tema 2 sem rachadura (e com números `[01.002]`, para continuar em dois
  capítulos);
  o assunto `O túmulo` sem casa (linha 16) e `A certidão` com duas (linha 17).
- `temas-incompleto.md`: sem a seção `Assuntos compartilhados...`, e com um tema 3 no resumo sem
  detalhe.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro e `temas-ok.md` | `livro validar-temas teste temas-ok.md` | código `0`; stdout exatamente `ok: 2 temas, 2 assuntos\n` |
| CA-2 | o livro e `temas-erros.md` | `livro validar-temas teste temas-erros.md` | código `1`; stdout exatamente `16: assunto sem casa\n17: assunto com mais de uma casa\n25: id inexistente: 01.009\ntema 1: material num só capítulo do livro\ntema 2: falta a rachadura com id\n5 problemas\n` |
| CA-3 | o livro e `temas-incompleto.md` | `livro validar-temas teste temas-incompleto.md` e `livro validar-temas teste nada.md` | o primeiro sai com código `1` e stdout exatamente `falta a seção: Assuntos compartilhados e a casa de cada um\ntema 3: falta o detalhe\n2 problemas\n`; o segundo com código `2` e `arquivo inexistente: nada.md` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/016-validar-temas --junitxml=relatorios/016-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, um módulo novo para os validadores

## Arquivo-exemplo
O subcomando `montar` (ids e intervalos).

## Roteiro manual (3 passos)
1. Rode `livro validar-temas serpent docs/maquetes/M-003-sugestao-temas.md`: a maquete usa ids do
   piloto, então aparecem vários `id inexistente` (por exemplo `03.038`).
2. Monte uma sugestão com dois temas do Serpent atual (o arquiteto tem um modelo: Bizango e Narcisse)
   e rode: `ok: 2 temas, 2 assuntos`.
3. Apague a rachadura de um tema e rode de novo: `tema <n>: falta a rachadura com id`.

## Decisões pendentes
nenhuma
