# SPEC 044 — Colunas faltando no briefing

**Estado:** exemplos aprovados pelo Decisor em 2026-11-12; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que uma linha de tabela do briefing com coluna faltando seja apontada, e não pulada
em silêncio, para que nenhum id deixe de ser conferido só porque a linha veio incompleta (correção do
aceite da SPEC 020, em 2026-11-12).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro validar-briefing <slug> <arquivo>`.

## Fora de escopo
- Linha com colunas a mais e cabeçalho com nomes diferentes: o que vale é a posição da célula.
- Linha de momento cuja primeira célula não é um número.
- As tabelas da sugestão de temas (SPEC 016).

## Formatos
Valem os formatos da SPEC 020, com esta mudança:

- **Colunas de cada tabela:** as do formato da SPEC 020, em ordem:
  `O que será abordado`: `#`, `Momento`, `O que entra`, `De onde vem`;
  `Cenas e passagens do livro`: `Id`, `O que é`, `Momento`, `Trato`;
  `Citações literais previstas`: `Id`, `Trecho (original)`, `Uso`;
  `Dados da web`: `Id`, `Dado`, `Uso`.
- **Linha com colunas faltando:** a linha de dados com menos células que as colunas da sua tabela dá o
  problema `<linha>: faltam colunas: <nomes das que faltam, em ordem, separados por ", ">`. As células
  que a linha tem são conferidas como na SPEC 020; o que depende de uma coluna que falta não é
  conferido (sem `Trato`, não há `trato inválido`; sem `De onde vem`, o momento existe, mas não tem regra
  de origem; sem o trecho, a citação não é conferida).
- A passagem com colunas faltando conta para a origem dos momentos que ela tem e para o total de
  passagens.
- **Ordem na saída:** `faltam colunas` é o último problema da sua linha.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`) e quatro briefings em `fixtures/`, todos com os momentos
`1` (`Livro`) e `2` (`Narrador`):

- `briefing-ok.md`: passagens `01.001` (linha 21) e `02.001` (linha 22) completas; a citação `01.001`
  `"leu o próprio nome gravado no cimento"` (linha 28).
- `briefing-sem-trato.md`: como na maquete M-001, a tabela de passagens não tem a coluna `Trato`, nem no
  cabeçalho; passagens `01.001` (linha 21) e `01.009`, que não existe (linha 22).
- `briefing-linhas-curtas.md`: o momento 2 sem `De onde vem` (linha 15); a passagem `02.001` só com id e
  descrição (linha 22); a citação `"leu o nome próprio gravado no cimento"`, que não confere, sem `Uso`
  (linha 28).
- `briefing-so-id.md`: a passagem da linha 22 é só `| 01.009 |`.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro e `briefing-sem-trato.md` | `livro validar-briefing teste briefing-sem-trato.md` | código `1`; stdout exatamente `21: faltam colunas: Trato\n22: id inexistente: 01.009\n22: faltam colunas: Trato\n3 problemas\n` |
| CA-2 | o livro e `briefing-linhas-curtas.md` | `livro validar-briefing teste briefing-linhas-curtas.md` | código `1`; stdout exatamente `15: faltam colunas: De onde vem\n22: faltam colunas: Momento, Trato\n28: citação não confere em 01.001: leu o nome próprio gravado no cimento\n28: faltam colunas: Uso\n4 problemas\n` |
| CA-3 | o livro, `briefing-so-id.md` e `briefing-ok.md` | `livro validar-briefing teste briefing-so-id.md` e `livro validar-briefing teste briefing-ok.md` | o primeiro sai com código `1` e stdout exatamente `22: id inexistente: 01.009\n22: faltam colunas: O que é, Momento, Trato\n2 problemas\n`; o segundo com código `0` e stdout exatamente `ok: 2 momentos, 2 passagens, 1 citações, 0 dados da web\n` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/044-colunas-faltando --junitxml=relatorios/044-junit.xml
```

As suítes anteriores têm de continuar verdes, inclusive 020, 021 e 022.

## Arquivos que serão tocados (previsão)
- `src/roteirista/validadores.py`

## Arquivo-exemplo
O validador da SPEC 020.

## Roteiro manual (3 passos)
1. Rode `livro validar-briefing serpent docs/maquetes/M-001-briefing-cap3.md`: as 9 passagens da maquete
   dão `faltam colunas: Trato`, e os ids do piloto que não existem no Serpent atual saem como
   `id inexistente` (entre eles `03.038`).
2. Rode com o briefing real do capítulo 1 do Bizango: continua `ok: 3 momentos, 6 passagens, 2 citações, 1 dados da web`.
3. Apague a coluna `Trato` das passagens do briefing real e rode de novo: `faltam colunas: Trato` nas
   linhas 22 a 25.

## Decisões pendentes
nenhuma
