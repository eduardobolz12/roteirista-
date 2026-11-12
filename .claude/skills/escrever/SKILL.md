---
name: escrever
description: Escreve UM capítulo (1 a 6) do roteiro em português, a partir só do briefing aprovado, do plano, do guia do capítulo, do texto literal dos ids do briefing e dos capítulos anteriores. Grava livros/<slug>/temas/<n>/cap-<k>.md e a conferência, e confere com `livro contar --briefing` e `livro revisar`.
disable-model-invocation: true
argument-hint: <slug> <número do tema> <capítulo, 1 a 6>
---

# Escrever

Argumentos (`$ARGUMENTS`): o slug, o número do tema e o capítulo `k` (1 a 6). Pasta:
`livros/<slug>/temas/<n>/`. Um capítulo por chamada; os capítulos são escritos em ordem.

Antes de tudo, leia `docs/prompts/roteiro-regras.md`. Valem as regras de lá.

O briefing manda no conteúdo; o guia manda na voz. O capítulo é escrito com o que o briefing designa e
nada mais: o que faltar é lacuna, dita na conferência, não preenchida.

## Pré-condições

Pare e diga o que falta se:

- `briefing-<k>.md` não estiver aprovado pelo Decisor (um `[x]` em "Aprovado como está" ou "Aprovado com
  mudanças"; no segundo caso, as mudanças escritas valem sobre o briefing);
- o briefing não passar em `livro validar-briefing <slug> <briefing> --temas livros/<slug>/temas.md`;
- faltar algum capítulo anterior (`cap-1.md` a `cap-<k-1>.md`).

## Entrada

Leia só isto:

1. `briefing-<k>.md` inteiro e, de `plano.md`, o fio, a pergunta, a escada, a âncora e a tabela do ciclo.
2. O guia `.claude/skills/escrever/capitulo-<k>.md`, inteiro.
3. O texto literal dos ids do briefing: `livro montar <slug> <ids das passagens e das citações>`, e
   `livro trecho <slug> <id>` para cada dado da web. Passagem `mencionar` vira no máximo uma ou duas
   frases.
4. Os capítulos anteriores, só o texto narrado (`cap-1.md` a `cap-<k-1>.md`; nunca as conferências).
5. `decisoes.md`, se existir: o que ele protege não se reabre.

Não leia outros capítulos do livro, o índice nem outras fontes. O que o briefing não dá é lacuna.

## Escrita

- **Momentos do briefing, na ordem dele**, com as funções que o guia descreve. A duração é referência de
  proporção, não teto: o capítulo cresce o que o material pedir.
- **Citação (D-028):** só as da tabela "Citações literais previstas" ou de um dado da web do briefing,
  no original, entre aspas retas, seguidas do id: `"I won't talk" [15.083]`. Copie do texto do
  `montar`; nunca de memória. A frase em português em volta da citação deixa o sentido claro para quem
  ouve, sem traduzi-la palavra por palavra. Fora das citações, nada entre aspas, nem título de obra:
  aspas sem id viram aviso no `livro contar`.
- **Marca de id fora de citação:** não ponha. O id da afirmação fica na conferência, não no texto.
- **Para o ouvido:** frases de uma informação; sem parênteses, sem abreviação, sem nota; quantidades por
  extenso ("sete estalos", "quatro líderes"), anos em algarismos; termo nativo só com o sentido amarrado
  a uma cena, no máximo um ou dois por capítulo.
- **Leitura é leitura:** o que a fonte não diz e você conclui leva "me parece", "eu leio isso como".
  Quem fez e quem disse, como a fonte diz.
- **Cap. 1, o verso.** Se o Decisor deu um verso, use-o. Senão, escolha um e mais duas alternativas, de
  obra publicada antes de 1929, cada uma conferida numa página pública (Wikisource, Project Gutenberg) com
  WebFetch, no máximo três páginas por verso: poeta, obra, ano, língua e texto original. Nunca componha
  nem monte verso de memória. Sem verso conferido, a primeira linha do capítulo é
  `[VERSO: a escolher pelo usuário]`.

## Vícios a caçar antes de entregar

Releia o capítulo procurando, além do que o guia proíbe:

- "não X, mas Y" que só serve para inflar (o guia já limita a um por capítulo);
- parágrafo que fecha com frase de efeito sem fato novo; aforismo; frase que parece feita para ser
  citada;
- três itens só porque três soa completo; três frases seguidas do mesmo tamanho; a mesma abertura de
  frase em sequência;
- travessão como conector em toda parte;
- significado inflado ("marcou para sempre", "mudaria tudo") e linguagem de folheto sobre outra cultura
  ("misterioso", "exótico", "fascinante");
- coisa fazendo ação de gente ("a noite decide", "o silêncio julga") quando havia uma pessoa para ser o
  sujeito.

Uma frase curta e forte é bem-vinda quando carrega um fato. O problema é a fórmula, não o efeito.

## Saída

- `cap-<k>.md`: só o texto narrado, parágrafos separados por linha em branco. Sem título e sem
  comentário. A marca do verso, se houver, numa linha só.
- `cap-<k>-conferencia.md`: `# Conferência — cap. <k>`, a data e os itens do "Bloco de conferência" do
  guia, na ordem dele.
- Depois do cap. 6, `roteiro-pt.md`: os seis capítulos juntos, sem mudar uma palavra, cada um depois de
  uma linha `## <k>`.

## Verificação

1. `livro contar <slug> livros/<slug>/temas/<n>/cap-<k>.md --briefing livros/<slug>/temas/<n>/briefing-<k>.md`
   tem de dar `0 problemas`. Citação que não confere: copie de novo do `montar`; se ainda falhar, ela
   sai do texto. A contagem de palavras vai para a conferência; desproporção grande em relação ao
   briefing (cerca de 30% para mais ou para menos) é sinalizada, nunca cortada.
2. `livro revisar <slug> livros/<slug>/temas/<n>/cap-<k>.md <ids das passagens e dos dados>`: um modelo
   gratuito procura frase que diz mais do que o material sustenta. Para cada apontamento, leia o
   parágrafo do id e decida: corrigir a frase, ou manter, dizendo por quê na conferência. O apontamento
   não manda; o texto do livro manda.
3. Releia contra o guia: o que o capítulo não pode ter (explicação antecipada, número guardado,
   pergunta ou convite fora de lugar, frase depois da âncora no cap. 6) e os vícios acima.

## Resumo na conversa

- O texto narrado do capítulo, como está em `cap-<k>.md`.
- Três linhas: palavras (contagem e previsto); alertas (o que o `contar` e o `revisar` apontaram e o
  que foi feito); lacunas.
- No cap. 1, o verso escolhido e as alternativas, com poeta e obra, para o Decisor aprovar ou trocar.
- Próximo passo: `/escrever <slug> <n> <k+1>`; depois do 6, `/revisar <slug> <n>`.
