# SPEC 015 — Visão compacta e contagem por tema

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que o Claude veja o livro inteiro em poucas linhas e saiba quanto material há para um
tema, para que a sugestão de temas custe poucos tokens e nunca exija ler o livro (D-017, E-004).

## Fronteira testada
CLI `livro`: `livro visao <slug>` e `livro contar-tema <slug> <termo>...`.

## Fora de escopo
- Agrupar assuntos sozinho: quem escolhe os termos de um tema é o Claude.
- Busca por sentido (fatia 013, na reserva).

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Nome:** numa afirmação, uma sequência de palavras seguidas que começam por maiúscula, com pelo menos
  duas letras cada uma. Se a sequência abre a frase (início da afirmação, ou depois de `.`, `!`, `?`,
  `:`, `;`, aspas de abertura ou parêntese), a primeira palavra dela sai; o resto, se houver, é o nome.
- **`visao`:** para cada capítulo com fichas, em ordem, três linhas:
  - `<CC> <título> — <N> fichas; numero <n>, contradicao <c>`;
  - `   nomes: ` seguido dos até 10 nomes que aparecem 2 vezes ou mais nas afirmações do capítulo, no
    formato `<nome> (<vezes>)`, separados por `, `, do mais frequente ao menos frequente, e no empate na
    ordem em que aparecem primeiro; sem nenhum, `—`;
  - `   termos: ` seguido das até 8 âncoras diferentes das fichas de tipo `termo`, da mais frequente à
    menos frequente, e no empate na ordem em que aparecem primeiro; sem nenhuma, `—`.
- **`contar-tema`:** uma ficha conta se a âncora ou a afirmação tem uma palavra que começa por algum dos
  termos, sem diferenciar maiúsculas; um termo de várias palavras conta como sequência. Saída em três
  linhas: `<F> fichas, <P> parágrafos, <K> capítulos`; `capítulos: ` com `<CC> (<fichas>)`, separados
  por `, `, do capítulo com mais fichas ao com menos, e no empate na ordem do livro; e
  `numero <n>, contradicao <c>`. Nada encontrado: só a primeira linha, com zeros, e código `1`.

## Tabela de CA

Fixture: `tests/acceptance/015-visao-e-temas/fixtures/ingles.pdf`, gerada por `_gerar_pdf.py` na mesma
pasta: dois capítulos em inglês, "Chapter One" e "Chapter Two", com três parágrafos cada. O livro é
convertido com `--lingua en` e indexado com as respostas de `fixtures/respostas/`.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro indexado | `livro visao en` | stdout exatamente `01 Chapter One — 4 fichas; numero 1, contradicao 1\n   nomes: Saint Marc (2), Max Beauvoir (2)\n   termos: powder\n02 Chapter Two — 4 fichas; numero 0, contradicao 0\n   nomes: Bizango (3), Saint Marc (2)\n   termos: Bizango\n` |
| CA-2 | o mesmo livro | `livro contar-tema en bizango` e `livro contar-tema en "saint marc" powder` | stdout exatamente `3 fichas, 2 parágrafos, 1 capítulos\ncapítulos: 02 (3)\nnumero 0, contradicao 0\n` e `5 fichas, 4 parágrafos, 2 capítulos\ncapítulos: 01 (3), 02 (2)\nnumero 1, contradicao 0\n`; código `0` nos dois |
| CA-3 | o mesmo livro | `livro contar-tema en zumbi` | stdout exatamente `0 fichas, 0 parágrafos, 0 capítulos\n`; código `1` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/015-visao-e-temas --junitxml=relatorios/015-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, `src/roteirista/banco.py`

## Arquivo-exemplo
O subcomando `itens`.

## Roteiro manual (3 passos)
1. Rode `livro visao serpent`: cerca de 6 mil caracteres, um bloco por capítulo.
2. Rode `livro contar-tema serpent bizango shanpwel "secret societ"` e compare com a linha do Bizango no
   E-004 (102 fichas por expressão regular; a regra da spec pode dar um pouco diferente).
3. Rode `livro contar-tema serpent zumbi`: nada, porque o índice está em inglês.

## Decisões pendentes
nenhuma
