---
name: revisar
description: Revisa o roteiro em português de um tema inteiro (os 6 capítulos) depois da escrita — clareza, coerência, repetição, sustentação, curva e tempo —, grava livros/<slug>/temas/<n>/revisao.md com cada problema e a gravidade, aplica as correções graves e médias e confere de novo com `livro contar` e `livro revisar`.
disable-model-invocation: true
argument-hint: <slug> <número do tema>
---

# Revisar

Argumentos (`$ARGUMENTS`): o slug e o número do tema. Pasta: `livros/<slug>/temas/<n>/`.
Saída: `revisao.md`, os capítulos corrigidos e `roteiro-pt.md` refeito.

Antes de tudo, leia `docs/prompts/roteiro-regras.md`. Valem as regras de lá.

## Por que esta revisão

Cada capítulo já foi conferido sozinho na escrita: citações pelo `livro contar`, sentido pelo `livro
revisar`. O que só aparece no roteiro inteiro escapa dessas conferências: uma pessoa usada antes de ser
apresentada, a mesma imagem em dois capítulos, uma pergunta retórica fora do cap. 3, a segunda volta fora
de ordem, um capítulo desproporcional. Esta skill lê o roteiro como o espectador vai ouvir, do começo ao
fim. O português tem no máximo duas passadas desta revisão.

## Pré-condições

- Existem `cap-1.md` a `cap-6.md` e `briefing-1.md` a `briefing-6.md`.
- Se `revisao.md` já marca "segunda passada aplicada", pare e diga.
- Leia `decisoes.md`, se existir: correção que mexe no que ele protege não se aplica; vai para o Decisor.

## Passos

1. **Sincronia e contas.** Refaça `roteiro-pt.md` a partir dos capítulos (cada um depois de uma linha
   `## <k>`, sem mudar uma palavra). Rode `livro contar <slug> cap-<k>.md --briefing briefing-<k>.md`
   para os seis (todos com `0 problemas`) e `livro contar <slug> roteiro-pt.md` para o total.

2. **Leitura inteira.** Leia `roteiro-pt.md` de uma vez, e de `plano.md` a escada e a tabela do ciclo.
   Não releia o livro: para conferir uma frase suspeita, use `livro trecho` no id que a sustenta (está na
   conferência do capítulo).

3. **O que verificar**, anotando cada problema com o capítulo e a frase exata:
   - **a. Clareza:** onde um espectador que nunca ouviu falar do assunto travaria? Pessoa, termo ou
     lugar usados antes de apresentados; salto que pressupõe o que o roteiro não disse.
   - **b. Coerência:** pronome com referente ambíguo; fato que contradiz outro capítulo (data, número,
     nome, quem fez o quê); a segunda volta do cap. 3 nas mesmas etapas e na mesma ordem do cap. 2
     (liste as duas e compare).
   - **c. Repetição:** a mesma construção, imagem ou movimento em capítulos diferentes, inclusive as
     marcas de leitura ("me parece", "eu leio"): conte quantas vezes cada uma aparece. A mesma ideia com
     outras palavras, sobretudo entre o espelho do 5 e a inversão do 6. A âncora só no 1 e no 6.
   - **d. Sustentação:** leitura dita como fato; atribuição trocada; título ou profissão sem fonte.
     Confira no `livro trecho` a frase que parecer dizer mais do que a fonte.
   - **e. Curva e regras dos guias:** nada nos caps. 4 a 6 sobe acima do soco do 3; os caps. 1 e 2 não
     terminam em pergunta nem em convite; uma só pergunta sem resposta no vídeo, a do fim do 3
     (pergunta retórica em outro capítulo conta); convite só no 4; no 6, inversão → divisão → despedida →
     âncora, e nada depois; cada distorção do 5 diz o que pegou e o que descartou.
   - **f. Tempo:** a fatia de cada capítulo no total contra a prevista (16/27/19/14/14/10%); cerca de
     30% acima ou abaixo é sinal leve, dito como proporção, nunca como corte.

4. **Gravidade.** **grave:** fato errado, atribuição errada, leitura dita como fato, ou algo que o
   espectador não entende. **média:** quebra de regra dos guias ou da curva, ambiguidade, repetição que
   se nota. **leve:** o resto. Na dúvida entre duas, a mais alta. Gosto pessoal sem uma dessas
   categorias não entra.

5. **Gravar `revisao.md`** no formato abaixo.

6. **Corrigir.** Aplique as correções graves e médias nos capítulos (as leves, só se forem de uma
   palavra), sem tocar no que `decisoes.md` protege. Para cada capítulo alterado: `livro contar --briefing`
   de novo (0 problemas) e `livro revisar` com os ids do briefing; apontamento novo é julgado como na
   escrita. Refaça `roteiro-pt.md`. Marque no topo de `revisao.md` "primeira passada aplicada" (ou
   "segunda").

## Formato de `revisao.md`

```markdown
# Revisão — Tema <n> <título>

**Estado:** primeira passada aplicada, <data>
**Contas:** <palavras> palavras, <min> min; <C> citações, 0 problemas. Fatias: cap. 1 <x>% (previsto 16%) ...

| # | Cap. | Gravidade | Problema | Frase | Correção | Feito |
|---|---|---|---|---|---|---|
| 1 | 3 | grave | atribuição | "<frase exata>" | <a correção> | sim |

**Contagens:** "me parece" <n>, "eu leio" <n>, ...
**Escalado ao Decisor:** <o que toca decisoes.md, ou "nada">
```

## Resumo na conversa

- A contagem por gravidade e quantas foram corrigidas.
- Os itens graves, um por linha.
- O que foi escalado ao Decisor.
- Próximo passo: o Decisor lê `roteiro-pt.md`; depois, a tradução (lote 7).
