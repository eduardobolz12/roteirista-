# SPEC 022 — Contar e conferir o capítulo

**Estado:** exemplos aprovados pelo Decisor em 2026-11-11; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero saber quanto tempo de narração um capítulo escrito dá e ter cada citação dele
conferida no livro, para que nenhuma frase atribuída ao autor ou a uma fonte chegue até mim inventada
ou trocada (D-003, D-028).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro contar <slug> <capitulo> [--briefing <arquivo>]`.

## Fora de escopo
- Conferir o sentido do texto: é a SPEC 042 (`livro revisar`).
- Conferir números e nomes fora das citações.

## Formatos
Valem os formatos das SPECs anteriores, o **id no texto** da SPEC 016 e a **regra de citação** da
SPEC 020 (D-028). Acrescentam-se:

- **Texto narrado:** as linhas do arquivo, menos as vazias, as que começam por `#` e as que são só uma
  marca entre colchetes (`[VERSO: a escolher pelo usuário]`); das que sobram, saem as marcas de id
  (`[01.001]`, `[15.082-15.085]`). **Palavras:** os pedaços do texto narrado separados por espaço que
  têm pelo menos uma letra ou algarismo. **Minutos:** palavras ÷ 150, com uma casa decimal e vírgula.
- **Citação:** texto entre aspas (`"..."`, `“...”` ou `«...»`) seguido, depois de espaços, de uma marca
  de id. Cada citação: o id existe (senão `<linha>: id inexistente: <id>`); confere pela regra de
  citação (senão `<linha>: citação não confere em <id>: <texto>`); com `--briefing`, o id está, como
  escrito, na tabela `Citações literais previstas` ou na tabela `Dados da web` do briefing (senão
  `<linha>: citação fora do briefing: <id>`). Cada citação dá no máximo um problema, o primeiro desta
  ordem.
- **Aviso:** texto entre aspas sem marca de id depois: `<linha>: aviso: aspas sem id: <texto>`. Não
  conta como problema.
- **Saída:** os problemas e avisos pela linha e, na mesma linha, na ordem em que aparecem; por fim
  `<P> palavras, <M> min; <C> citações, <R> problemas`. Código `1` se houver problema; senão `0`.
  Arquivo que não existe: como na SPEC 016.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`) e, em `fixtures/`:

- `capitulo.md`: uma marca `[VERSO: ...]`, um título `# Capítulo 1` e quatro parágrafos com cinco
  citações: `"leu o próprio nome gravado no cimento" [01.001]` (linha 5);
  `"reconheceu o apelido... antes de reconhecer o rosto" [01.002]` e
  `"quis falar do enterro" [01.003]` (linha 7, o livro diz "falar sobre o enterro");
  `"a certidão às três horas da tarde" [02.001]` e a palavra `"tarde"` entre aspas sem id (linha 9);
  `"Ninguém soube dizer à família" [02.009]` (linha 11, id que não existe). 51 palavras narradas.
- `capitulo-ok.md`: duas citações certas, uma delas com aspas curvas; 18 palavras narradas.
- `briefing.md`: um briefing cuja única citação prevista é `01.001`.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro e `capitulo.md` | `livro contar teste capitulo.md` | código `1`; stdout exatamente `7: citação não confere em 01.003: quis falar do enterro\n9: aviso: aspas sem id: tarde\n11: id inexistente: 02.009\n51 palavras, 0,3 min; 5 citações, 2 problemas\n` |
| CA-2 | o livro, `capitulo.md` e `briefing.md` | `livro contar teste capitulo.md --briefing briefing.md` | código `1`; stdout exatamente `7: citação fora do briefing: 01.002\n7: citação não confere em 01.003: quis falar do enterro\n9: citação fora do briefing: 02.001\n9: aviso: aspas sem id: tarde\n11: id inexistente: 02.009\n51 palavras, 0,3 min; 5 citações, 4 problemas\n` |
| CA-3 | o livro e `capitulo-ok.md` | `livro contar teste capitulo-ok.md` e `livro contar teste nada.md` | o primeiro sai com código `0` e stdout exatamente `18 palavras, 0,1 min; 2 citações, 0 problemas\n`; o segundo com código `2` e `arquivo inexistente: nada.md` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/022-contar-capitulo --junitxml=relatorios/022-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, o módulo dos validadores

## Arquivo-exemplo
O validador da SPEC 020 (regra de citação).

## Roteiro manual (3 passos)
1. Rode `livro contar serpent` com o capítulo 1 real do Bizango que o arquiteto montou, com o canto
   citado no original: 3 citações, 0 problemas, e um aviso para `"mãe da sociedade"`.
2. Rode com `docs/experimentos/E-004/cap-1.md`, o ensaio aprovado: a citação traduzida, sem id, sai como
   aviso; perto de 220 palavras e 1,5 min.
3. Troque uma palavra do canto citado e rode de novo: `citação não confere`.

## Decisões pendentes
nenhuma
