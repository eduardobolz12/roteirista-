# SPEC 027 — Tela lado a lado

**Estado:** exemplos aprovados pelo Decisor em 2026-11-12; testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero ver, parágrafo por parágrafo, o texto que vai para a narração ao lado da
retrotradução, com o português aprovado à mão e os parágrafos com alerta marcados, dizendo se o alerta é
da tradução ou da retrotradução, para aprovar capítulo a capítulo lendo em português, sem rede e sem
tokens (D-012, maquete M-002).

## Fronteira testada
CLI `livro`, com `ROTEIRISTA_LIVROS`: `livro lado-a-lado <slug> <português> <tradução> <retrotradução>`.

## Fora de escopo
- Gravar a decisão do Decisor: ele decide na conversa; a caixa de decisão da tela é só o lembrete.
- Rodar a retrotradução: é a SPEC 026.

## Formatos
Valem os formatos das SPECs anteriores, com as correções da SPEC 045. Acrescentam-se:

- **Arquivos:** a língua de cada um vem do nome (SPEC 024). O português e a retrotradução têm de ser `pt`
  e a tradução `en` ou `fr`; sem língua no nome, `língua desconhecida: <nome do arquivo>`; com outra
  língua, `língua errada: <nome do arquivo>`; código `2` nos dois. Arquivo que não existe: como na SPEC 016.
- **Alertas de cada parágrafo** (o parágrafo `<n>.<p>` da tradução), nesta ordem:
  1. os de `livro invariantes <slug> <português> <tradução>`, como `Tradução: <alerta>`;
  2. os de `livro glossario <slug> <língua> --conferir <português> <tradução>`, como `Tradução: <alerta>`;
  3. os de `livro invariantes <slug> <tradução> <retrotradução>`, como `Retrotradução: <alerta>`;
  4. cada termo do glossário com alguma forma da tradução no parágrafo traduzido e nenhuma forma do termo
     no retraduzido (palavra inteira, sem diferenciar maiúsculas, fora das citações), em ordem alfabética
     do termo: `Retrotradução: <primeira forma da tradução> não voltou como <primeira forma do termo>`;
  5. `[ambíguo]` no parágrafo retraduzido: `Retrotradução: frase marcada como ambígua`.

  As linhas `cap. <n>: …` das conferências viram avisos do capítulo: `Tradução: cap. <n>: …` (1 e 2) ou
  `Retrotradução: cap. <n>: …` (3). Num capítulo com aviso de retrotradução, os alertas 3 a 5 não são
  calculados.
- **Saída:** o arquivo `lado-a-lado-<nome da tradução sem .md>.html`, na pasta da tradução, trocado se já
  existir, com o estilo da maquete M-002 dentro dele, sem `<script>`, sem `<link>` e sem endereço `http`.
  Todo texto do roteiro e dos alertas vai com `&`, `<`, `>` e `"` trocados por `&amp;`, `&lt;`, `&gt;` e
  `&quot;`. A página tem:
  - `<title>Lado a lado — <nome da tradução></title>` e
    `<div class="meta"><Inglês|Francês> · <C> capítulos · <P> parágrafos · <M> marcados</div>`;
  - cada aviso de capítulo como `<div class="aviso"><aviso></div>`;
  - para cada capítulo, `<h2 id="cap-<n>">Capítulo <n></h2>`, os parágrafos e
    `<div class="decisao"><b>Sua decisão sobre o capítulo <n></b><br>☐ Aprovado · ☐ Aprovado com sugestões
    (escreva na conversa, em português, citando o §) · ☐ Refazer</div>`;
  - cada parágrafo numa linha só, sem espaço entre as partes, como `<div class="par" id="p-<n>-<p>">`
    (com alerta, `class="par suspeito"`), com
    `<span class="num"><n>.<p></span>`, `<p class="<língua>"><texto traduzido></p>`,
    `<p class="pt"><texto retraduzido></p>` (vazio se faltar), cada alerta como
    `<span class="nota">⚠ <alerta></span>` ou, sem alerta, `<span class="ok">✓ sem alerta</span>`, e
    `<details><summary>Português aprovado</summary><p><texto do português></p></details>`.
- **stdout:** os avisos de capítulo e os alertas, `<n>.<p>: <alerta>`, na ordem da página; por fim
  `<P> parágrafos, <M> marcados: <nome do arquivo>`. Código `0`: alerta é para o Decisor ler, não erro.

## Tabela de CA

Fixture: o PDF da SPEC 001 (livro `teste`), glossário `en` com `facão → machete` e
`sociedade|sociedades → society|societies`, e em `fixtures/`:

- `roteiro-pt.md`, dois capítulos: 1.1 com "1962", "dois médicos" e "Narcisse"; 1.2 com "facão" e a
  citação `"leu o próprio nome gravado no cimento" [01.001]`; 2.1 com "sociedade";
- `roteiro-en.md` e `retro-pt-roteiro-en.md`: a tradução fiel e a retrotradução fiel;
- `roteiro-en-humanizado.md`: "three doctors" no lugar de "two doctors" em 1.1;
  `retro-pt-roteiro-en-humanizado.md`: "três médicos" e "Narciso" em 1.1, "machado" em 1.2 e
  `[ambíguo]` em 2.1;
- `retro-pt-curto.md`: a retrotradução fiel sem o capítulo 2;
- `notas.md`.

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | o livro e o glossário | `livro lado-a-lado teste roteiro-pt.md roteiro-en.md retro-pt-roteiro-en.md` | código `0`; stdout exatamente `3 parágrafos, 0 marcados: lado-a-lado-roteiro-en.html\n`; o HTML contém `<title>Lado a lado — roteiro-en.md</title>`, `<div class="meta">Inglês · 2 capítulos · 3 parágrafos · 0 marcados</div>`, `<div class="par" id="p-1-2"><span class="num">1.2</span><p class="en">The secretary raises the machete and reads the date: &quot;leu o próprio nome gravado no cimento&quot; [01.001].</p>`, `<span class="ok">✓ sem alerta</span>`, `<details><summary>Português aprovado</summary><p>A sociedade julga a alma, não o corpo.</p></details>` e `<b>Sua decisão sobre o capítulo 2</b>`, e não contém `http`, `<script` nem `<link` |
| CA-2 | o livro e o glossário | `livro lado-a-lado teste roteiro-pt.md roteiro-en-humanizado.md retro-pt-roteiro-en-humanizado.md` | código `0`; stdout exatamente `1.1: Tradução: números: 2, 1962 → 3, 1962\n1.1: Retrotradução: nome sumiu: Narcisse\n1.1: Retrotradução: nome novo: Narciso\n1.2: Retrotradução: machete não voltou como facão\n2.1: Retrotradução: frase marcada como ambígua\n3 parágrafos, 3 marcados: lado-a-lado-roteiro-en-humanizado.html\n`; o HTML contém `<div class="par suspeito" id="p-1-1">`, `<span class="nota">⚠ Retrotradução: nome novo: Narciso</span>` e `<div class="meta">Inglês · 2 capítulos · 3 parágrafos · 3 marcados</div>` |
| CA-3 | o livro e o glossário | `livro lado-a-lado teste roteiro-pt.md roteiro-en.md retro-pt-curto.md` e `livro lado-a-lado teste roteiro-pt.md notas.md retro-pt-roteiro-en.md` | o primeiro com código `0`, stdout exatamente `Retrotradução: cap. 2: 1 parágrafos antes, 0 depois\n3 parágrafos, 0 marcados: lado-a-lado-roteiro-en.html\n` e o HTML com `<div class="aviso">Retrotradução: cap. 2: 1 parágrafos antes, 0 depois</div>` e `<p class="pt"></p>`; o segundo com código `2` e `língua desconhecida: notas.md` no stderr |

## Risco declarado
nenhum

## Como rodar os testes
```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/027-tela-lado-a-lado --junitxml=relatorios/027-junit.xml
```
As suítes anteriores têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/cli.py` e um módulo novo da tela, que usa o módulo das conferências da tradução; o
  estilo da maquete `docs/maquetes/M-002-lado-a-lado.html`, copiado para dentro do pacote.

## Arquivo-exemplo
A maquete M-002 e as conferências das SPECs 023, 024 e 045.

## Roteiro manual (3 passos)
1. `livro lado-a-lado serpent` com o `roteiro-pt.md`, o `roteiro-en-humanizado.md` e a retrotradução dele,
   do tema 1: abre no navegador sem rede, 62 parágrafos em 6 capítulos.
2. Os parágrafos marcados batem com os alertas do stdout, e cada nota diz se é da tradução ou da
   retrotradução.
3. Numa cópia do humanizado, troque "seven cracks" por "six cracks": 1.2 aparece marcado com
   `Tradução: números: 7 → 6`, e a retrotradução de 1.2 mostra o "seis".

## Decisões pendentes
nenhuma
