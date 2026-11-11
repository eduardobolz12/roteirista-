# SPEC 043 — Indexar o livro inteiro

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero indexar o livro inteiro com um comando só, que eu possa interromper e retomar,
porque o Serpent leva mais de duas horas e hoje isso depende de um laço feito à mão.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS` e `ROTEIRISTA_OLLAMA`: `livro indexar-livro <slug> [--janela
<tokens>] [--refazer]` e `livro indexar <slug> <CC>`.

## Fora de escopo
- Rodar capítulos em paralelo.
- Estimar o tempo que falta.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Ordem:** os capítulos em ordem. Para cada um, `indexar` e depois `repescar`, como nas SPECs 008 a
  011 e 039 a 040, com a mesma `--janela`.
- **Linha por capítulo:** `<CC> | <última linha de indexar> | <última linha de repescar> | lacunas <n>`,
  em que `<n>` é o número de lacunas depois da repescagem.
- **Capítulo sem parágrafos:** `<CC> | sem parágrafos`, sem pedido ao modelo.
- **Capítulo pronto:** fica marcado quando a sua repescagem termina. Na próxima chamada, sai
  `<CC> | já indexado`, sem pedido ao modelo. `--refazer` ignora as marcas. `livro indexar` de um
  capítulo apaga a marca dele.
- **Fim:** a última linha é `<K> capítulos indexados, <J> já estavam`.
- **Falha:** se um capítulo terminar em `modelo inacessível` (SPEC 040), o comando para ali: stderr
  `modelo inacessível: <url>`, código `3`. Os capítulos anteriores ficam prontos, e o da falha fica como
  estava antes.

## Tabela de CA

Fixture: `tests/acceptance/043-indexar-livro/fixtures/dois-capitulos.pdf`, cópia do PDF da SPEC 001. As
respostas do servidor falso cobrem todos os parágrafos, então a repescagem não faz pedido.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro convertido | `livro indexar-livro teste` | código `0`; stdout exatamente `01 \| 3 itens gravados, 0 corrigidos, 0 rejeitados \| 0 itens gravados, 0 sem conteúdo, 0 rejeitados \| lacunas 0\n02 \| 2 itens gravados, 0 corrigidos, 0 rejeitados \| 0 itens gravados, 0 sem conteúdo, 0 rejeitados \| lacunas 0\n2 capítulos indexados, 0 já estavam\n`; 2 pedidos |
| CA-2 | o livro convertido; os pedidos do capítulo 02 falham | `livro indexar-livro teste`; depois, com o servidor normal, de novo | a primeira sai com código `3`, a linha do `01` no stdout e `modelo inacessível:` no stderr; a segunda sai com código `0`, começa por `01 \| já indexado\n`, indexa o `02` e termina em `1 capítulos indexados, 1 já estavam\n` |
| CA-3 | o livro indexado inteiro | `livro indexar-livro teste`; `livro indexar teste 01` e `livro indexar-livro teste`; `livro indexar-livro teste --refazer` | a primeira termina em `0 capítulos indexados, 2 já estavam` sem pedido; a segunda reindexa só o `01` e termina em `1 capítulos indexados, 1 já estavam`; a terceira termina em `2 capítulos indexados, 0 já estavam` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/043-indexar-livro --junitxml=relatorios/043-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, `src/roteirista/banco.py`, o módulo que fala com o modelo

## Arquivo-exemplo
Os subcomandos `indexar` e `repescar`.

## Roteiro manual (3 passos)
1. Num livro novo, rode `livro indexar-livro <slug>` e acompanhe as linhas.
2. No meio, feche o Ollama: o comando para com `modelo inacessível`.
3. Abra o Ollama e rode de novo: os capítulos prontos saem como `já indexado`, e ele continua dali.

## Decisões pendentes
nenhuma
