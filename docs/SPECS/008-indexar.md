# SPEC 008 — Indexar um capítulo

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que o modelo local leia um capítulo e grave um índice do que ele contém, sem que
nenhum id errado entre, para que o Claude trabalhe sobre o índice e nunca precise ler o livro.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS` e `ROTEIRISTA_OLLAMA`:

- `livro indexar <slug> <CC>`
- `livro itens <slug> <CC>`

Nos testes, `ROTEIRISTA_OLLAMA` aponta para um servidor falso que imita a API do Ollama (D-013).

## Fora de escopo
- Capítulo em janelas (SPEC 009).
- Conferência de âncoras (SPEC 010).
- Lacunas e repescagem (SPEC 011).
- Indexar o livro inteiro num comando (fatia 028).

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Servidor:** `ROTEIRISTA_OLLAMA` tem a URL base; sem ela, `http://localhost:11434`.
- **Pedido:** `POST <url>/api/generate` com JSON: `model` `qwen3:14b`, `stream` `false`, `think`
  `false` e `options` `temperature` `0`, `num_ctx` `16384`, `num_predict` `3000`, `repeat_penalty`
  `1.1`. O campo `response` da resposta traz o texto.
- **Prompt:** o conteúdo de `docs/prompts/indexar.txt`, sem alteração, seguido dos parágrafos do
  capítulo, cada um como `[<id>] <texto>`, separados por uma linha em branco. O arquivo é do arquiteto
  e tem de ser levado para dentro do pacote com os mesmos bytes.
- **Linha do modelo:** `id | tipo | ancora | afirmacao`. O id pode vir entre colchetes. Linhas em
  branco são ignoradas. Os espaços em volta de cada campo são tirados.
- **Tipos:** `doutrina`, `cena`, `caso`, `numero`, `contradicao`, `termo`, `informante`, `marginal`.
- **Rejeição:** a linha é rejeitada, nesta ordem de verificação, por `formato` (não tem os 4 campos),
  `id inexistente`, `id fora do capítulo` ou `tipo inválido`.
- **Saída de `indexar`:** uma linha `rejeitado (<motivo>): <linha do modelo>` por rejeição, na ordem
  da resposta. A última linha é `<N> itens gravados, <C> corrigidos, <M> rejeitados` (`<C>` é sempre
  `0` nesta fatia). Código `0`, mesmo com rejeições.
- **Regravar:** `indexar` substitui todos os itens daquele capítulo.
- **`itens`:** imprime um item por linha, `<id> | <tipo> | <ancora> | <afirmacao>`, na ordem do livro;
  no mesmo parágrafo, na ordem em que foram gravados. Capítulo sem itens: stdout vazio, código `0`.
- **Erros:** capítulo que não existe → stderr `capítulo inexistente: <CC>`, código `2`. Servidor fora
  do ar ou resposta com erro → stderr `modelo inacessível: <url>`, código `3`, e os itens que já
  existiam ficam como estavam.

## Tabela de CA

Fixture: `tests/acceptance/008-indexar/fixtures/dois-capitulos.pdf`, cópia do PDF da SPEC 001. As
respostas do servidor falso são os arquivos de `fixtures/respostas/`, escolhidos pelo primeiro id do
trecho.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `dois-capitulos.pdf` convertido; o modelo devolve 3 itens válidos, um com id entre colchetes, com uma linha em branco no meio | `livro indexar teste 01` e `livro itens teste 01` | código `0`; stdout de `indexar` exatamente `3 itens gravados, 0 corrigidos, 0 rejeitados\n`; `itens` dá as 3 linhas, com os ids sem colchetes; o servidor recebeu um pedido, com o modelo, as opções e o prompt definidos em **Formatos** |
| CA-2 | o mesmo livro; o modelo devolve para o capítulo 02 um item válido, um de id `02.009`, um de id `01.001`, um de tipo `afirmacao` e uma linha sem separadores | `livro indexar teste 02` e `livro itens teste 02` | código `0`; stdout com as 4 linhas `rejeitado (...)`, nesta ordem: `id inexistente`, `id fora do capítulo`, `tipo inválido`, `formato`; a última linha é `1 itens gravados, 0 corrigidos, 4 rejeitados`; `itens` dá só o item válido |
| CA-3 | o capítulo 01 indexado | `livro indexar teste 01` com outra resposta; depois com o servidor fora do ar; depois `livro indexar teste 09` | a segunda indexação substitui os itens; a terceira sai com código `3`, stderr com `modelo inacessível:`, e `itens` não muda; a última sai com código `2` e stderr com `capítulo inexistente: 09` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores. O servidor falso é levantado pelo `conftest.py` da fatia.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/008-indexar --junitxml=relatorios/008-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, `src/roteirista/banco.py`, um módulo novo para falar com o modelo, e o
  prompt dentro do pacote

## Arquivo-exemplo
`src/roteirista/cli.py`: o subcomando `montar` e o seu tratamento de erro.

## Roteiro manual (3 passos)
1. Com o Ollama aberto, rode `livro indexar serpent 06`. Espere uns 5 minutos, porque nesta fatia o
   capítulo vai inteiro.
2. Rode `livro itens serpent 06` e leia dez linhas: a frase em português bate com o parágrafo?
3. Feche o Ollama e rode de novo: `modelo inacessível`, e os itens continuam lá.

## Decisões pendentes
nenhuma
