# E-009 — Ensaio: humanização, retrotradução local e tela lado a lado

Feito em 2026-11-12 pelo arquiteto, antes de escrever as SPECs 026 e 027 e de entregar as skills da 033,
para rodar a cadeia do D-011 e do D-012 num roteiro real (D-021). Os arquivos ficam em
`livros/serpent/temas/1/`, fora do git: `roteiro-en-humanizado.md`, `retro-pt-roteiro-en.md`,
`retro-pt-roteiro-en-humanizado.md` e `lado-a-lado-roteiro-en-humanizado.html`.

## Passos

1. **Humanização** do inglês do tema 1 (o do E-008) pela skill `/humanizar` em rascunho: as citações
   trocadas por marcas antes da edição e devolvidas por script, para saírem iguais por construção.
2. **Retrotradução** pelo `qwen3:14b` local, um pedido por parágrafo, com o glossário invertido no prompt
   (só os termos do parágrafo) e as citações protegidas por marcas `⟦k⟧`: primeiro com o prompt do E-001
   (sem contexto), no inglês do E-008; depois com o prompt novo (o capítulo inteiro como contexto e a regra
   de não traduzir nomes e títulos), no humanizado.
3. **Tela lado a lado** no molde da maquete M-002, gerada por um protótipo com as conferências das SPECs
   023, 024 e 045.
4. Cada parágrafo da retrotradução lido contra o português aprovado.

## Resultado

| Etapa | Resultado |
|---|---|
| Humanização | 0 alertas nas invariantes (inglês → humanizado e português → humanizado) e no glossário; legibilidade de 6 raras e 2 expressões para 1 rara ("conch", que o texto explica com "shell") e 0 expressões; 15 parágrafos mexidos |
| Retrotradução 1 (prompt do E-001) | 496 s para 62 parágrafos (113 s de carga do modelo); 0 citações perdidas; 17 alertas nas invariantes; na leitura, 10 parágrafos com erro que engana, em 4 capítulos |
| Retrotradução 2 (prompt novo, no humanizado) | 409 s; 0 citações perdidas; 0 alertas nas invariantes e no glossário; na leitura, 2 parágrafos com erro que engana, em capítulos diferentes |
| Tela | 62 parágrafos, 0 marcados, 47 KB, sem rede |

**Os erros da primeira retrotradução:** nomes e títulos traduzidos ("Narcisse" → "Narciso", "Saint Marc"
→ "São Marcos", "Night of the Living Dead" → "a Noite dos Mortos-Vivos"); "machete" → "machado";
"the secretary… his" → "a secretária… ela"; "harming your own family" → "matar"; "the peasantry" → "a
camponesa"; "a sensational account" → "uma conta"; "It's a sentence" → "É uma frase"; "army corporal" →
"soldado comum". Pelo gatilho do D-012 (mais de um falso alarme por capítulo), a retrotradução assim não
servia.

**O que resolveu:** o capítulo como contexto (gênero, "sentence" no tribunal, "account" no livro), a
regra dos nomes e títulos, a humanização (palavra simples o modelo erra menos: "peasants", "servant") e
dois termos a mais no glossário, `facão → machete` e `búzio → conch`. Sobraram "blindfolded" → "cegado"
(2.9) e "corporal" → "soldado comum" (4.7), um por capítulo: dentro do D-012.

## O que o ensaio ensinou

1. **A retrotradução precisa de contexto.** Parágrafo solto, o 14B erra gênero e o sentido das palavras de
   dois sentidos; com o capítulo no prompt, acerta. O tempo quase não muda (uns 7 s por parágrafo).
2. **Nome e título não se traduzem, e a regra tem de estar no prompt.** Sem ela, a tela mostraria
   "Narciso", e o Decisor pensaria que o inglês trocou o nome.
3. **A tela não substitui a leitura.** As conferências não pegam "cegado" nem "soldado comum"; o português
   aprovado, recolhido sob cada parágrafo, deixa o Decisor comparar quando estranhar.
4. **A humanização e a retrotradução se ajudam:** a palavra que a legibilidade aponta como rara é a que o
   modelo local mais erra na volta.
5. **O glossário serve aos dois lados:** um termo que se repete e que o modelo erra na volta (facão,
   búzio) entra no glossário, e a `/traduzir` passa a usá-lo também.
