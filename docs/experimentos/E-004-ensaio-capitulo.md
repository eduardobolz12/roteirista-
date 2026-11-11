# E-004 — Ensaio: um capítulo de vídeo a partir do índice

Feito em 2026-11-10 pelo arquiteto, depois do aceite do lote 2, para responder se o que já existe gera
um texto fiel e quanto custa. Livro: Serpent, indexado inteiro em inglês (1.993 fichas). Tema escolhido
pelo Decisor entre 8 sugestões: Bizango. Capítulo: 1, O enigma, com o guia `capitulo-1.md` e a skill
`escrever` do piloto. Texto em `E-004/cap-1.md`. O material literal não entra no git (direitos autorais).

## Passos

1. **Temas sem ler o livro.** Uma visão compacta do índice (assuntos mais citados por capítulo, cerca de
   1.500 tokens) e a contagem de fichas por palavras-chave deram 8 temas com a porcentagem de material.
   A contagem por palavra subestima temas de capítulo inteiro (morte aparente: 13% medido, cerca de 45%
   pelo conteúdo).
2. **A cena pelo índice.** Fichas de tipo `cena`, `caso` e `informante` dos capítulos 15 a 17 levaram à
   cerimônia de 15.073 a 15.091.
3. **O texto literal** dos parágrafos escolhidos, com `livro montar`.
4. **Escrita** em português, seguindo os tempos do guia.
5. **Conferência:** 8 citações, todas `EXISTE` com `livro conferir`.

## Resultado

- Aprovado pelo Decisor: "está excelente".
- 221 palavras. O capítulo 1 do piloto tinha 150.
- Lacunas: o verso (precisa ser conferido na web) e o ano e a recepção do livro (pesquisa web).
- Custo estimado num fluxo dedicado: cerca de 11 mil tokens (regras 4 mil, visão do índice e temas 2 mil,
  fichas 2 mil, texto literal 1,5 mil, escrita 1,5 mil). A estimativa anterior era de 15 a 20 mil.

## O que o ensaio ensinou

1. **O índice serve para achar o material.** A cena saiu só das fichas, e o literal confirmou.
2. **Conferir citação não basta.** O primeiro rascunho tinha as 8 citações certas e 4 infidelidades: a
   ordem dos acontecimentos trocada, um contraste inventado ("não o chamam de túmulo"), um detalhe que
   o livro não diz (Davis segurando uma vela) e uma generalização ("um povo" em vez de uma sociedade).
   O arquiteto só as achou relendo contra o material. Falta uma etapa de revisão do sentido, que pode
   usar os modelos gratuitos da D-023.
3. **O capítulo 1 depende da pesquisa web**: a fonte pede o ano e a recepção da obra.
