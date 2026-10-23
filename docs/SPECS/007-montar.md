# SPEC 007 — Montar

**Estado:** testes vermelhos escritos a pedido do Decisor; **exemplos ainda não aprovados — não levar ao gate antes da aprovação**

## Intenção
Como Decisor, quero juntar num documento o texto literal de vários parágrafos escolhidos, na ordem
em que os pedi, para entregar ao escritor só o material designado, sem ninguém transcrever à mão.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro montar <slug> <id ou intervalo>...`

## Fora de escopo
- Ler a lista de ids de um arquivo.
- Intervalo que atravessa capítulos (`01.003-02.001`).
- Intervalo de notas ou de bibliografia (ids avulsos de nota e bibliografia são aceitos).
- Gravar em arquivo (a saída é o stdout; quem chama redireciona).

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Argumentos:** cada um é um id (`01.002`, `01.n01`, `bib.001`) ou um intervalo de parágrafos do
  mesmo capítulo (`01.001-01.003`, inclusivo).
- **Ordem:** a dos argumentos; dentro de um intervalo, a do livro. Id repetido aparece de novo.
- **Saída:** um bloco por parágrafo, `## <id>`, linha em branco, o texto literal; blocos separados
  por uma linha em branco; a saída termina com uma única LF.
- **Erro:** se qualquer id ou intervalo não existe, ou o intervalo atravessa capítulos, nada vai
  para o stdout; stderr `id inexistente: <id>` (o primeiro que falhou) ou
  `intervalo inválido: <intervalo>`; código `2`.

## Tabela de CA

Fixture: `tests/acceptance/007-montar/fixtures/dois-capitulos.pdf`, cópia do PDF da SPEC 001.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `dois-capitulos.pdf` convertido com `--slug teste` | `livro montar teste 02.002 01.001` | código `0`; stdout exatamente `## 02.002\n\nNinguém soube dizer à família, naquela manhã de maio, quem tinha aberto a cova durante a noite.\n\n## 01.001\n\nO homem parou diante do túmulo e leu o próprio nome gravado no cimento.\n` |
| CA-2 | o mesmo livro | `livro montar teste 01.002-01.003` | código `0`; stdout exatamente `## 01.002\n\nA irmã reconheceu o apelido de infância antes de reconhecer o rosto.\n\n## 01.003\n\nNaquela tarde, ninguém na aldeia quis falar sobre o enterro.\n` |
| CA-3 | o mesmo livro | `livro montar teste 01.001 02.009` e `livro montar teste 01.003-02.001` | os dois: stdout vazio e código `2`; stderr com `id inexistente: 02.009` e com `intervalo inválido: 01.003-02.001` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/007-montar --junitxml=relatorios/007-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, `src/roteirista/banco.py`

## Arquivo-exemplo
`src/roteirista/cli.py`: o subcomando `trecho` e o seu tratamento de id inexistente.

## Roteiro manual (3 passos)
1. Pegue no piloto o `cap-3-material.txt` do tema 01 e monte os mesmos ids com `livro montar
   serpent ... > material.md`.
2. Compare com o `cap-3-material.md` do piloto: mesmo texto, na mesma ordem.
3. Abra o `material.md` no VS Code e confira que os acentos e as aspas saíram certos.

## Decisões pendentes
nenhuma
