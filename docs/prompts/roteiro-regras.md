# Regras comuns das skills do roteiro

Valem para `/temas`, `/pesquisar`, `/briefing`, `/escrever`, `/revisar`, `/traduzir` e `/humanizar`. Cada regra diz de qual decisão
do `DESIGN.md` ela vem; se esta lista e o `DESIGN.md` divergirem, vale o `DESIGN.md`.

## Onde ficam os arquivos

Tudo de um livro fica em `livros/<slug>/`, fora do git (direitos autorais, D-015):

- `temas.md`: a sugestão de temas (`/temas`);
- `temas/<n>/`, uma pasta por tema escolhido, com `<n>` o número do tema em `temas.md`:
  `decisoes.md`, `pesquisa.md`, `plano.md`, `briefing-1.md` a `briefing-6.md`, `cap-1.md` a `cap-6.md`
  com as conferências, `roteiro-pt.md` e `revisao.md`; depois, por língua (`en` ou `fr`),
  `roteiro-<língua>.md` e `traducao.md` (`/traduzir`), `roteiro-<língua>-humanizado.md` e `humanizacao.md`
  (`/humanizar`), a retrotradução `retro-pt-roteiro-<língua>-humanizado.md` e a tela
  `lado-a-lado-roteiro-<língua>-humanizado.html`.

Cada skill lê dos arquivos o que precisa e pode rodar numa conversa nova.

## O livro nunca entra inteiro (D-004, D-005)

O Claude chega ao livro só pelo índice e por ids:

- para achar: `livro visao`, `livro contar-tema`, `livro hesitacoes`, `livro itens <slug> <cap>`,
  `livro buscar`;
- para ler: `livro trecho <slug> <id>` e `livro montar <slug> <ids...>`, só dos ids escolhidos.

Nunca leia `livro.sqlite` nem os arquivos de texto do livro. Se a saída de um comando for longa, filtre
antes de ler (`| grep -i -E "termo1|termo2"`, `| head`): cada linha lida custa token, e o Claude é o
único custo do projeto (D-027).

## Ids e origem (D-002, D-003)

- Livro: `CC.PPP` (`15.082`), nota `CC.nPP`, intervalo no mesmo capítulo `15.082-15.085`.
  Web: `W01.002`. Toda afirmação sobre o livro ou a fonte leva o id.
- Antes de usar um id num arquivo, confira que ele diz o que você vai dizer que ele diz: o índice é
  feito por um modelo local e pode estar torto. O texto que vale é o de `livro trecho`.
- **Sustentar, não só mencionar.** O parágrafo precisa afirmar o que a frase afirma. Ele tratar do
  mesmo assunto não basta; o "quase" é onde a distorção se esconde.
- **Atribuição literal.** Quem fez, quem disse, quem ficou com o quê: como a fonte diz. "A família" não
  vira "as irmãs"; profissão ou título só se a fonte der.

## Citação (D-028)

- No texto em português, a citação fica na língua original, entre aspas retas, seguida do id:
  `"What we see here, I won't talk" [15.082-15.083]`.
- Copiada da saída de `livro trecho` ou `livro montar`, nunca de memória. `...` marca um corte.
- Quem confere é o script (`livro validar-briefing`, `livro contar`). Citação que não confere sai do
  texto ou é copiada de novo; nunca se "ajusta" o original.

## Interpretação e lacuna (D-003, D-017)

- Leitura sua aparece como sua: "me parece", "eu leio isso como". Nunca atribua à fonte o que ela não
  diz.
- O que o material não dá é lacuna, dita como lacuna. Não se inventa para preencher, nem se completa uma
  lista com item fraco.

## Decisões do Decisor (D-016)

- As decisões do Decisor sobre um tema ficam em `temas/<n>/decisoes.md`. Leia o arquivo antes de
  propor qualquer coisa: o que ele protege não se reabre.
- Nenhuma skill altera esse arquivo por conta própria. Quando o Decisor decidir algo na conversa (fio,
  corte, verso, texto fixado), acrescente um item numerado: a decisão, o que ela protege, a data. Proposta
  sem resposta dele não entra.

## Na conversa

- Nunca transcreva trechos do livro na conversa: só ids e resumos curtos. O texto literal fica nos
  arquivos.
- No fim de cada skill: o resultado em poucas linhas, o que o Decisor decide e o próximo passo.
- Português sempre.
