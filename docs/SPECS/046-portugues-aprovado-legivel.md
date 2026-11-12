# SPEC 046 — Português aprovado legível na tela

**Estado:** exemplo aprovado pelo Decisor em 2026-11-12, no aceite da 027; testes vermelhos entregues para o
gate

## Intenção
Como Decisor, quero abrir o português aprovado de um parágrafo na tela lado a lado e lê-lo embaixo do texto
traduzido e da retrotradução, na largura das duas colunas, como a nota de alerta, para conferir o sentido sem
esforço. Correção da SPEC 027, aceita com correção em 2026-11-12: no roteiro manual, aberto, o português
aprovado caía na coluna estreita do número, uma palavra por linha, porque o estilo da maquete M-002 não tinha
regra para ele.

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro lado-a-lado <slug> <português> <tradução> <retrotradução>`
(SPEC 027).

## Fora de escopo
- Qualquer outra mudança na página: textos, alertas, ordem e o resto do estilo seguem a SPEC 027.

## Formatos
Vale a SPEC 027, com uma mudança: o estilo da página ganha estas duas linhas, a segunda depois da primeira.

```css
details { grid-column: 2 / 4; }
@media (max-width: 700px) { details { grid-column: 1; } }
```

A primeira põe o português aprovado embaixo das duas colunas de texto, como a nota de alerta. A segunda vale
para a tela estreita, em que a página tem uma coluna só, e põe o português aprovado na largura toda.

As **linhas do estilo** são o texto entre `<style>` e `</style>`, quebrado em linhas e sem os espaços das
pontas.

## Tabela de CA

Fixture: a da SPEC 027. O PDF da SPEC 001 (livro `teste`), o glossário `en` com `facão → machete` e
`sociedade|sociedades → society|societies`, e em `fixtures/` `roteiro-pt.md`, `roteiro-en.md`,
`retro-pt-roteiro-en.md`, `roteiro-en-humanizado.md` e `retro-pt-roteiro-en-humanizado.md`.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro e o glossário | `livro lado-a-lado teste roteiro-pt.md roteiro-en.md retro-pt-roteiro-en.md` | código `0`; nas linhas do estilo, `details { grid-column: 2 / 4; }` |
| CA-2 | o livro e o glossário | `livro lado-a-lado teste roteiro-pt.md roteiro-en-humanizado.md retro-pt-roteiro-en-humanizado.md` | código `0`; nas linhas do estilo, a do CA-1; o HTML contém `⚠ Retrotradução: nome novo: Narciso</span><details><summary>Português aprovado</summary>` |
| CA-3 | o livro e o glossário | `livro lado-a-lado teste roteiro-pt.md roteiro-en.md retro-pt-roteiro-en.md` | código `0`; nas linhas do estilo, a do CA-1 e, depois dela, `@media (max-width: 700px) { details { grid-column: 1; } }` |

## Risco declarado
nenhum

## Como rodar os testes
```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/046-portugues-aprovado-legivel --junitxml=relatorios/046-junit.xml
```
As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/estilos/lado-a-lado.css`.

## Arquivo-exemplo
A tela da SPEC 027 e o protótipo do ensaio E-009, que já tinha as duas regras.

## Roteiro manual (3 passos)
1. `livro lado-a-lado serpent` com o `roteiro-pt.md`, o `roteiro-en-humanizado.md` e a retrotradução dele, do
   tema 1: no navegador, sem rede, abra o "Português aprovado" de 1.1. O texto fica embaixo do inglês e da
   retrotradução, na largura das duas colunas.
2. Estreite a janela para menos de 700 px: o português aprovado ocupa a largura toda.
3. O resto da página não muda: 62 parágrafos em 6 capítulos, com os mesmos marcados do stdout.

## Decisões pendentes
nenhuma
