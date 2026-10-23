# SPEC 006 — Conferir e buscar

**Estado:** testes vermelhos escritos a pedido do Decisor; **exemplos ainda não aprovados — não levar ao gate antes da aprovação**

## Intenção
Como Decisor, quero saber se uma frase existe literalmente no livro e onde aparece um termo, para
que toda citação do roteiro seja conferida contra o texto e nenhuma paráfrase passe por citação.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`:

- `livro conferir <slug> "<frase>"`
- `livro buscar <slug> "<termo>"`

## Fora de escopo
- Busca por sentido (fatia 013).
- Expressões regulares, curingas, busca aproximada.
- Conferir frase que atravessa dois parágrafos.

## Formatos
Valem os formatos das SPECs anteriores. Acrescentam-se:

- **Onde procurar:** parágrafos do corpo, notas (`CC.nPP`) e bibliografia (`bib.PPP`).
- **Conferir:** a frase existe quando aparece **literalmente**, diferenciando maiúsculas e acentos,
  depois de normalizar frase e texto em NFC e reduzir espaços repetidos a um. As marcas de chamada
  `[nPP]` do texto são ignoradas: `corpo. O` confere com `corpo.[n01] O`.
- **Saída de conferir:** existe → stdout `EXISTE <ids>`, ids separados por espaço, na ordem do
  livro; código `0`. Não existe → stdout `NÃO EXISTE`; código `1`.
- **Buscar:** o termo é procurado sem diferenciar maiúsculas (acentos continuam diferenciando),
  como trecho de palavra. Saída: um id por linha, sem repetir, na ordem do livro: capítulos em
  ordem; dentro do capítulo, parágrafos e depois notas; a bibliografia por último. Nenhum resultado
  → stdout vazio, código `1`.

## Tabela de CA

Fixture: `tests/acceptance/006-conferir-buscar/fixtures/notas.pdf`, cópia do PDF da SPEC 003
(`01.001` = `O médico assinou a certidão sem examinar o corpo.[n01]`; `01.002` = `A família
guardou uma cópia na igreja.`; `01.n01` = `A certidão foi encontrada em 1981 nos arquivos do
hospital.`; `02.001` = `O caso chegou aos jornais da capital.`; `bib.001` e `bib.002`).

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `notas.pdf` convertido com `--slug teste` | `livro conferir teste "sem examinar o corpo."` e `livro conferir teste "guardou uma   cópia"` (três espaços) | stdout `EXISTE 01.001\n` e `EXISTE 01.002\n`; código `0` nos dois |
| CA-2 | o mesmo livro | `livro conferir teste "sem examinar o cadáver"` e `livro conferir teste "O MÉDICO assinou"` | stdout `NÃO EXISTE\n` nos dois; código `1` nos dois |
| CA-3 | o mesmo livro | `livro buscar teste "CERTIDÃO"`, `livro buscar teste "serpent"` e `livro buscar teste "zumbi"` | stdout exatamente `01.001\n01.n01\n`, `bib.001\n` e vazio; códigos `0`, `0` e `1` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs anteriores.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/006-conferir-buscar --junitxml=relatorios/006-junit.xml
```

As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py`, `src/roteirista/banco.py`

## Arquivo-exemplo
`src/roteirista/banco.py`: a leitura de parágrafo por id usada por `trecho`.

## Roteiro manual (3 passos)
1. Copie do roteiro do piloto (tema 01) uma citação original em inglês e rode `livro conferir
   serpent "<citação>"`: deve dar `EXISTE`.
2. Troque uma palavra da citação e confira de novo: `NÃO EXISTE`.
3. Rode `livro buscar serpent "Narcisse"` e veja em quantos capítulos ele aparece.

## Decisões pendentes
nenhuma
