# SPEC 040 — Nova tentativa quando o modelo falha

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que uma falha passageira do Ollama não jogue fora um capítulo inteiro, porque no
E-003 o Ollama respondeu erro uma vez e, num livro de duas horas, recomeçar o capítulo custa caro.

## Fronteira testada
CLI `livro`: `livro indexar` e `livro repescar`.

## Substitui
Esta spec não altera as SPECs anteriores; onde divergem, vale esta (D-024):

- SPECs 008 e 009, **Erros**: o `modelo inacessível` só vem depois da terceira tentativa do mesmo pedido.

## Fora de escopo
- Retomar um capítulo do ponto onde parou.
- Distinguir tipos de falha: servidor fora do ar, erro de resposta e tempo esgotado contam igual.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Tentativas:** um pedido que falha é repetido, igual, até completar 3 tentativas, com 2 segundos
  entre elas. Cada pedido de janela tem as suas 3 tentativas.
- **Aviso:** cada repetição escreve no stderr `modelo falhou, nova tentativa (<n> de 2)`.
- **Desistência:** se as 3 tentativas falharem, vale o `modelo inacessível` das SPECs 008 e 009, com o
  capítulo como estava.

## Tabela de CA

Fixture: `tests/acceptance/040-nova-tentativa/fixtures/dois-capitulos.pdf`, cópia do PDF da SPEC 001. O
servidor falso pode responder erro em pedidos escolhidos pelo teste.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro convertido; o primeiro pedido falha | `livro indexar teste 01` | código `0`; stdout `3 itens gravados, 0 corrigidos, 0 rejeitados\n`; stderr com `modelo falhou, nova tentativa (1 de 2)`; 2 pedidos, com o mesmo prompt |
| CA-2 | o capítulo já indexado; os três pedidos seguintes falham | `livro indexar teste 01` e `livro itens teste 01` | código `3`, stderr com `nova tentativa (1 de 2)`, `nova tentativa (2 de 2)` e `modelo inacessível:`; 3 pedidos; `itens` igual ao de antes |
| CA-3 | o livro convertido; o segundo pedido falha uma vez | `livro indexar teste 01 --janela 40` e `livro repescar teste 01`, com o primeiro pedido da repescagem falhando uma vez | `indexar` sai com código `0` depois de 3 pedidos (janela 1, janela 2 com erro, janela 2 de novo); `repescar` sai com código `0` depois de 2 pedidos |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/040-nova-tentativa --junitxml=relatorios/040-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- O módulo que fala com o modelo

## Arquivo-exemplo
A chamada ao Ollama da SPEC 008.

## Roteiro manual (3 passos)
1. Comece `livro indexar serpent 14` e, no meio, feche o Ollama pela bandeja.
2. Veja as linhas `nova tentativa` no terminal e, depois de uns segundos, o `modelo inacessível`.
3. Abra o Ollama, rode de novo e confira com `livro itens serpent 14` que o capítulo ficou completo.

## Decisões pendentes
nenhuma
