# E-008 — Ensaio: a tradução do tema 1 e as conferências por regra

Feito em 2026-11-12 pelo arquiteto, antes de escrever as SPECs 023, 024 e 025, para rodar as regras
num roteiro real (D-021). O texto traduzido fica em `livros/serpent/temas/1/roteiro-en.md`, fora do git.

## Passos

1. **Tradução.** O roteiro em português do tema 1 (aprovado pelo Decisor) foi traduzido para o inglês
   pelas regras da skill `traduzir` do piloto: um parágrafo para cada parágrafo, números, nomes e
   atribuições exatos, marcas de leitura mantidas, frases de até 25 palavras, "I'm Alderick, and…", o verso
   de Dickinson no original (decisão do Decisor) e as 10 citações copiadas iguais.
2. **Glossário de 17 termos** (sociedade, imperador, terreiro, caixão, zumbi, tribunal, vodu, carrasco,
   bokor, julgamento, Barão, Brasil, Estado, presidente, haitiano, Estados Unidos, zumbificação).
3. **Protótipo descartável** das três conferências, rodado no português contra o inglês e em cinco
   arquivos pequenos de exemplo.

## Resultado

| Conferência | Primeira rodada | Depois das regras |
|---|---|---|
| Glossário | 17 termos, 0 alertas | igual |
| Invariantes | 5 falsos alarmes: "I've" e "Romero's" como nomes; "both" sem valer 2 (três vezes) | 2 novos falsos alarmes ("Para", "O" depois de citação que termina em ponto); com a citação fechando a frase, 62 parágrafos, 0 alertas |
| Legibilidade | nomes no começo de frase ("Isnard", "Seabrook") contados como raros | 1 frase de 27 palavras (a tradução esticou uma frase de 22); 6 raras: conch, unjustly, accuser, peasantry, hesitates, henchman; 2 expressões: the hard way, up close |

## Varredura individual (pedido do Decisor)

Cada parágrafo da tradução lido contra o português, cada apontamento da legibilidade julgado e cada número
e nome extraído conferido:

- **Extração:** 18 números e 71 nomes conferidos, todos certos; 4 nomes não eram conferidos por aparecerem
  só no começo da frase ("Isnard" três vezes, "Davis" uma). A regra nova (o nome do começo da frase que
  aparece como nome no arquivo e nunca em minúscula) fecha esse ponto cego sem falso alarme: tirar
  "Isnard" de 2.6 dá exatamente `2.6: nome sumiu: Isnard`.
- **O que as regras não pegam (6 achados na leitura):** uma atribuição errada (o livro "acusado de fraude",
  quando a acusação foi a Davis; estava também no português aprovado e foi corrigida em `cap-1.md`); um
  sentido torto ("wear the same man"); uma frase pouco natural ("The trial is of the soul"); uma frase
  ambígua; um tempo verbal; uma palavra de dois sentidos para quem não é nativo ("bands"). Sentido,
  naturalidade e ambiguidade ficam com a revisão do sentido (SPEC 042), a humanização e a retrotradução
  (SPEC 026); as regras do D-029 não substituem a leitura.
- **Legibilidade, um por um:** dos 8 apontamentos, 6 têm troca simples e fiel (unjustly → unfairly;
  accuser → the person who accused; up close → well; peasantry → peasants; hesitates → isn't sure;
  henchman → servant) e 2 ficam como escolha (conch, que o texto já acompanha de "shell"; the hard way,
  expressão comum). Nenhum apontamento falso.
- **Glossário, termo a termo:** 16 dos 17 termos certos; "Estados Unidos → American" era um arranjo para
  uma frase, não um termo fixo. O certo é `Estados Unidos|americano|americana → United States|American`.

## O que o ensaio ensinou

1. **As regras dão régua sem modelo.** Citações, números e nomes conferidos por script não deram falso
   alarme no roteiro real, depois de quatro regras pequenas (I e contrações; `'s`; "both" = 2; citação que
   fecha a frase).
2. **A legibilidade aponta trabalho de verdade para a humanização:** as seis palavras raras e as duas
   expressões têm troca simples para um público não nativo, e a frase longa nasceu na tradução.
3. **O glossário precisa das formas** (singular e plural) e dos nomes que mudam entre línguas
   (Barão → Baron, Brasil → Brazil); sem ele, as invariantes acusam o nome traduzido como "sumiu" e
   "novo".
