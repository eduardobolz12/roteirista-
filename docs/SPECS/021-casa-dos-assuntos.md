# SPEC 021 — Casa dos assuntos

**Estado:** exemplos aprovados pelo Decisor em 2026-11-11; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero ser avisado quando um briefing desenvolve um assunto que é casa de outro vídeo,
para que os 4 vídeos do mesmo livro não repitam a mesma construção (D-018), sem que o aviso trave o
trabalho.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro validar-briefing <slug> <arquivo> --temas <arquivo-de-temas>`.

## Fora de escopo
- Bloquear: o aviso nunca muda o código de saída.
- Achar assunto repetido que não está na tabela de casas.

## Formatos
Valem os formatos das SPECs 016 e 020. Acrescentam-se:

- **Com `--temas`:** o arquivo de temas é conferido como na SPEC 016. Se tiver algum problema: stderr
  `o arquivo de temas tem problemas: rode livro validar-temas`, código `2`, e o briefing não é
  conferido. O campo `Tema` do briefing tem de ser um tema do arquivo; se não for, é um problema:
  `tema <n> não está no arquivo de temas`, logo depois dos campos e seções que faltam; nesse caso não
  há avisos de casa.
- **Aviso:** para cada passagem de `Cenas e passagens do livro` com trato `desenvolver` que tem algum
  id entre os `Ids principais` de um assunto cuja casa é outro tema:
  `aviso: <linha>: <id ou intervalo, como está no arquivo> é desenvolvido aqui, mas a casa de "<assunto>" é o tema <m>`.
  Passagem com `mencionar` nunca avisa. Os avisos saem depois dos problemas, pela linha, e antes da
  última linha (`ok: ...` ou `<P> problemas`); não contam como problema.
- Sem `--temas`, a conferência é a da SPEC 020, sem avisos.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`), `temas-ok.md` e `temas-erros.md` da SPEC 016 (assuntos
`O túmulo`, `01.001`, casa no tema 1, e `A certidão`, `02.001`, casa no tema 2), e três briefings sem
dados da web nem citações:

- `briefing-tema2.md`: tema 2; passagens `02.002` desenvolver (linha 21), `01.001` desenvolver (linha
  22), `02.001` desenvolver (linha 23) e `01.001-01.002` mencionar (linha 24);
- `briefing-tema1.md`: tema 1; passagens `01.001` desenvolver e `02.001` mencionar;
- `briefing-tema3.md`: tema 3, que não existe no arquivo de temas.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro, `temas-ok.md` e `briefing-tema2.md` | `livro validar-briefing teste briefing-tema2.md --temas temas-ok.md` | código `0`; stdout exatamente `aviso: 22: 01.001 é desenvolvido aqui, mas a casa de "O túmulo" é o tema 1\nok: 2 momentos, 4 passagens, 0 citações, 0 dados da web\n` |
| CA-2 | o mesmo, com `briefing-tema1.md` | `livro validar-briefing teste briefing-tema1.md --temas temas-ok.md` e, sem `--temas`, `livro validar-briefing teste briefing-tema2.md` | o primeiro dá exatamente `ok: 2 momentos, 2 passagens, 0 citações, 0 dados da web\n`; o segundo exatamente `ok: 2 momentos, 4 passagens, 0 citações, 0 dados da web\n`; código `0` nos dois |
| CA-3 | o livro, os dois arquivos de temas e `briefing-tema3.md` | `livro validar-briefing teste briefing-tema3.md --temas temas-ok.md` e `livro validar-briefing teste briefing-tema2.md --temas temas-erros.md` | o primeiro sai com código `1` e stdout exatamente `tema 3 não está no arquivo de temas\n1 problemas\n`; o segundo com código `2`, stdout vazio e `o arquivo de temas tem problemas: rode livro validar-temas` no stderr |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/021-casa-dos-assuntos --junitxml=relatorios/021-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, o módulo dos validadores

## Arquivo-exemplo
Os validadores das SPECs 016 e 020.

## Roteiro manual (3 passos)
1. Com a sugestão real de dois temas (Bizango e Narcisse) e o briefing real do capítulo 1 do Bizango,
   rode com `--temas`: sem aviso, porque a sessão 15.073-15.091 é casa do Bizango.
2. Troque o `Tema` do briefing para `2` e rode de novo: avisos nas passagens da sessão.
3. Troque essas passagens para `mencionar`: os avisos somem.

## Decisões pendentes
nenhuma
