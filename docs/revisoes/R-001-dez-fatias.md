# R-001 — Revisão das 10 fatias

Feita em 2026-11-06 pelo arquiteto, com 11 fatias (001 a 007 e 034 a 037), depois do aceite do bloco A.
Passou da 10ª porque a 036 e a 037 corrigiam a 035 e não fazia sentido parar no meio.

## Limite dos dados

O `docs/metricas.csv` não foi preenchido ao longo das fatias. Ele foi reconstruído pelas datas dos
commits. Por isso:

- os tempos são de commit, não de trabalho: não medem o tempo do Decisor;
- o custo em tokens e em colagens não foi medido;
- a 004, a 005 e a 007 foram para o Kimi em fila, e o tempo delas se soma;
- o gate da 006 foi commitado depois da entrega, então ela não tem tempo de construção.

## O que os dados mostram

| Medida | Valor |
|---|---|
| Fatias provadas | 11 de 37 |
| Testes de aceite | 33, todos verdes |
| Tempo entre o primeiro e o último commit de cada sessão | 7 h 09 em 3 sessões |
| Código do núcleo | 1.019 linhas (o `livro.py` do piloto tem 2.271, sem teste de aceite, e faz mais coisas) |
| Serpent contra o piloto | 1.394 de 1.433 parágrafos idênticos (97%) |
| Defeitos que passaram pelos testes e só apareceram no livro real | 4 |

## O que funcionou

- **O oráculo trancado.** Nenhum teste foi afrouxado para passar, e nenhum hash divergiu nas provas.
- **O aceite no livro real.** Foi ele que achou o que os testes não viam.
- **O Kimi seguiu a spec** e parou quando devia. Nenhum defeito do bloco A foi desobediência à spec.
- **Separar quem escreve de quem prova.** O relatório do Kimi nunca precisou ser aceito na palavra.

## O que falhou

**Testes verdes não diziam que o livro saía bom.** As 7 primeiras fatias foram provadas com fixtures
pequenas que escrevi sem compará-las com o livro real. O Serpent saiu com 12 capítulos e 210
parágrafos, e ninguém viu até o aceite, que ficou pendente por duas semanas.

Os quatro defeitos foram: capítulos dentro de partes, parágrafo por recuo, texto duplicado na
abertura de capítulo e medida errada do fim de linha, com a junção de linhas como parte da última
rodada. Todos vieram de specs e fixtures do arquiteto.

**A 035 repetiu o erro em menor escala.** Validei as regras com outro leitor de PDF, e não com o
código real. O resultado passou nos testes e falhou no livro.

**A métrica prometida não foi coletada.** A D-014 dependia do `metricas.csv`, que nenhum passo do
processo mandava preencher.

## Conclusões

1. **D-014 não dispara.** Reconstruir com testes custou 7 horas de sessão e entregou um núcleo menor,
   com 97% de igualdade ao piloto e correções que o piloto não tinha. O custo do retrabalho veio da
   fixture, não do método.
2. **O aceite tem de vir junto com a fatia**, não semanas depois. A D-021 já resolve isso: cada lote
   fecha com o Serpent.
3. **O arquiteto valida a regra no código real ou no modelo real antes da spec.** Também na D-021.
4. **O `metricas.csv` passa a ser atualizado pelo arquiteto ao fechar cada lote.**

## Para o Decisor decidir

Nada bloqueia o lote 1. Ficam em aberto as duas opções de automação que aguardavam esta revisão:

- **O DSH fazer o commit do próprio registro**, o que tira duas colagens por lote. Muda o
  `docs/agentes/DSH.md`.
- **Um script que rode gate, Kimi e prova em sequência.** Depende de como o Kimi e o DSH são
  executados, o que o arquiteto ainda não sabe.
