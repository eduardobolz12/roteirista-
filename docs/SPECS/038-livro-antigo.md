# SPEC 038 — Livro convertido por uma versão anterior

**Estado:** exemplos aprovados pelo Decisor em 2026-11-10; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que um livro convertido antes de uma fatia nova continue funcionando com os
comandos novos, sem perder nada, para não ter de reconverter e reindexar o livro (cerca de 2 horas de
modelo) a cada lote.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS` e `ROTEIRISTA_OLLAMA`: `trecho`, `ficha`, `indexar`, `itens`,
`lacunas` e `repescar`, sobre um livro gravado no formato do bloco A.

## Fora de escopo
- Converter de novo o texto: os parágrafos de um livro antigo ficam como estão.
- Livro com um formato que nenhuma versão do `livro` gravou.

## Formatos
Valem os formatos das SPECs anteriores. Acrescenta-se:

- **Livro antigo:** qualquer comando que abre um livro deixa nele o que as fatias posteriores à
  conversão precisam, sem apagar nem mudar nada do que já está gravado. O livro antigo se comporta
  como um livro convertido agora, sem itens e sem marcas.

## Tabela de CA

Fixture: `tests/acceptance/038-livro-antigo/fixtures/antigo/livro.sqlite`, gerada por
`_gerar_banco.py` na mesma pasta: o livro do PDF da SPEC 001 (`dois-capitulos.pdf`), gravado no
formato do commit `af7a1d3` (fim do bloco A), sem as tabelas do lote 1. O teste copia esse arquivo
para `ROTEIRISTA_LIVROS/teste/livro.sqlite`.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro antigo `teste` | `livro itens teste 01`, `livro indexar teste 01` e `livro itens teste 01` | o primeiro `itens` sai com código `0` e stdout vazio; `indexar` sai com código `0` e `3 itens gravados, 0 corrigidos, 0 rejeitados\n`; o segundo `itens` dá as 3 linhas |
| CA-2 | o livro antigo `teste` | `livro lacunas teste 01` e `livro repescar teste 01` | `lacunas` dá `01.001\n01.002\n01.003\n`; `repescar` sai com código `0` e a última linha `3 itens gravados, 0 sem conteúdo, 0 rejeitados` |
| CA-3 | o livro antigo `teste` | `livro indexar teste 01`; depois `livro trecho teste 01.001`, `livro trecho teste 02.002` e `livro ficha teste` | os trechos e a ficha são exatamente os do livro antigo: `O homem parou diante do túmulo e leu o próprio nome gravado no cimento.\n`, `Ninguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.\n` e `língua: não informada\ncapítulos: 2\nparágrafos: 5\n` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/038-livro-antigo --junitxml=relatorios/038-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/banco.py`

## Arquivo-exemplo
`src/roteirista/banco.py`: `criar`.

## Roteiro manual (3 passos)
1. Sem reconverter, rode `livro itens serpent 06` no Serpent do aceite do lote 1: os itens continuam lá.
2. Copie `livros\serpent\livro.sqlite` para um lugar seguro, por precaução, e rode
   `livro lacunas serpent 05`: sai a lista, sem erro.
3. Rode `livro trecho serpent 06.001`: o texto é o mesmo de antes.

## Decisões pendentes
nenhuma
