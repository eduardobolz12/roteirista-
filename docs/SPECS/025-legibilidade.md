# SPEC 025 — Legibilidade

**Estado:** exemplos aprovados pelo Decisor em 2026-11-12; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero saber, por parágrafo, onde o texto em inglês ou francês fica difícil para quem não é
nativo (frase longa, palavra rara, expressão idiomática), para que a humanização saiba o que simplificar
sem mudar o que o texto diz (D-011, D-029).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro legibilidade <slug> <roteiro> [--limiar <z>]`.

## Fora de escopo
- Trocar palavras: é da humanização.
- Travar o fluxo: a legibilidade é medida, não erro.

## Formatos
Valem os formatos das SPECs anteriores, o **roteiro** da SPEC 023 e a **língua do arquivo**, os **nomes** e
as **frases** da SPEC 024. Acrescentam-se:

- **Palavras:** as do texto fora das citações e das marcas de id, sem o `'s` final.
- **Frase longa:** frase com mais de 25 palavras.
- **Palavra rara:** frequência Zipf da palavra, em minúsculas, na língua do arquivo, pela biblioteca
  gratuita `wordfreq` (versão 3.1.1, sem rede), abaixo do limiar (padrão `3.0`; `--limiar` troca). Não
  contam: os nomes, como na SPEC 024 (inclusive o do começo da frase); as palavras das traduções do
  glossário do livro nessa língua. Cada palavra uma vez por parágrafo.
- **Expressões:** as linhas de `<ROTEIRISTA_EXPRESSOES>/<língua>.txt` (padrão `docs/expressoes`), menos as
  vazias e as que começam por `#`, procuradas como palavras inteiras, sem diferenciar maiúsculas, fora das
  citações. Sem o arquivo, nenhuma expressão.
- **Saída:** para cada parágrafo, nesta ordem, `<n>.<p>: frase de <k> palavras` (uma por frase longa),
  `<n>.<p>: raras: <a>, <b>` (em minúsculas, em ordem alfabética) e `<n>.<p>: expressão: <e>` (uma por
  expressão, na ordem da lista); por fim
  `<P> parágrafos, <F> frases longas, <R> palavras raras, <E> expressões`. Código `0`. Língua desconhecida
  e arquivo que não existe: como na SPEC 024.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`), `roteiro-en.md` da SPEC 023, e em `fixtures/`:

- `roteiro-en-dificil.md`: um capítulo com dois parágrafos: "Isnard" no começo das frases e como nome no
  fim; "bokor"; "henchman"; "the hard way"; uma frase de 33 palavras com "peasantry";
- `expressoes/en.txt`: um comentário, "the hard way" e "spill the beans";
- `notas.md`: um arquivo sem língua no nome.

`ROTEIRISTA_EXPRESSOES` aponta para `fixtures/expressoes` nos três CAs.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro | `livro legibilidade teste roteiro-en.md` | código `0`; stdout exatamente `6 parágrafos, 0 frases longas, 0 palavras raras, 0 expressões\n` |
| CA-2 | o livro com `bokor → bokor` no glossário `en` | `livro legibilidade teste roteiro-en-dificil.md` | código `0`; stdout exatamente `1.1: raras: henchman\n1.1: expressão: the hard way\n1.2: frase de 33 palavras\n1.2: raras: peasantry\n2 parágrafos, 1 frases longas, 2 palavras raras, 1 expressões\n` |
| CA-3 | o livro com `túmulo\|túmulos → tomb\|tombs` | `livro legibilidade teste roteiro-en.md --limiar 4.0` e `livro legibilidade teste notas.md` | o primeiro com código `0` e stdout exatamente `1.2: raras: eighteen\n2.1: raras: judged\n6 parágrafos, 0 frases longas, 2 palavras raras, 0 expressões\n`; o segundo com código `2` e `língua desconhecida: notas.md` no stderr |

## Risco declarado
A frequência vem da `wordfreq` 3.1.1; outra versão pode mudar a fronteira de uma palavra. A versão fica
fixa no `pyproject.toml`.

## Como rodar os testes
```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/025-legibilidade --junitxml=relatorios/025-junit.xml
```
As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, o módulo das conferências da tradução e `pyproject.toml` (`wordfreq==3.1.1`).

## Arquivo-exemplo
As invariantes (SPEC 024): nomes e frases.

## Roteiro manual (3 passos)
1. `livro legibilidade serpent livros/serpent/temas/1/roteiro-en.md`, com o glossário do E-008: 6 raras
   (conch, unjustly, accuser, peasantry, hesitates, henchman) e 2 expressões (the hard way, up close); a
   frase longa da primeira tradução (2.14) já foi dividida na varredura.
2. Numa cópia, troque "peasantry" por "peasants" e junte de novo as duas frases de 2.14: some o alerta de
   "peasantry" e volta o de `frase de 27 palavras`.
3. Rode com `--limiar 3.5`: aparecem mais raras (machete, sorcerer...), nenhuma delas nome de pessoa.

## Decisões pendentes
nenhuma
