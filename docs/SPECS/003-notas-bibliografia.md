# SPEC 003 — Notas de rodapé e bibliografia separadas do corpo

**Estado:** exemplos aprovados pelo Decisor em 2026-10-23 (chamada de nota como `[nPP]`); testes vermelhos entregues para o gate

## Intenção
Como Decisor, quero que as notas de rodapé e a bibliografia do livro fiquem fora dos parágrafos do
corpo, mas acessíveis pelo próprio id, para que uma citação do corpo nunca carregue o texto de uma
nota e uma nota possa ser citada sozinha.

## Fronteira testada
CLI `livro`, como nas SPECs 001 e 002: `livro novo <pdf> --slug <slug>` e
`livro trecho <slug> <id>`, com `ROTEIRISTA_LIVROS`.

## Fora de escopo
- Notas no fim do capítulo ou do livro (endnotes, capítulo "Notes"): só notas de rodapé, no pé da
  página.
- Nota que continua na página seguinte.
- Dois números de nota iguais no mesmo capítulo.
- Separar autor, título e ano dentro de uma entrada de bibliografia.
- Notas e bibliografia de EPUB (004).

## Formatos
Valem os formatos das SPECs 001 e 002. Acrescentam-se:

- **Nota de rodapé:** bloco no pé da página, abaixo da última linha do corpo, em fonte menor que a
  do corpo (o tamanho mais frequente do livro), cuja primeira linha começa pelo número da nota. A
  nota não é parágrafo do corpo e não conta no resumo.
- **Id da nota:** `CC.nPP`: capítulo da página onde a nota está, `n`, e o número impresso da nota
  com 2 dígitos (`01.n01`). `trecho` devolve o texto da nota **sem** o número inicial.
- **Chamada de nota:** o número em sobrescrito no corpo vira `[nPP]`, colado ao caractere anterior,
  sem espaço (`corpo.[n01]`). `[nPP]` é marca de texto, não id.
- **Bibliografia:** o capítulo cujo marcador, sem diferenciar maiúsculas, é um destes:
  `Bibliography`, `Annotated Bibliography`, `References`, `Works Cited`, `Bibliografia`,
  `Referências`, `Bibliographie`. Ela não recebe número de capítulo e não conta no resumo. Cada
  parágrafo dela é uma entrada, com id `bib.PPP` (`bib.001`).
- **Resumo de `novo`:** inalterado: `<N> capítulos, <M> parágrafos`, contando só o corpo.

## Tabela de CA

Fixture: `tests/acceptance/003-notas-bibliografia/fixtures/notas.pdf`, PDF A5 de 3 páginas, com 3
marcadores. Corpo em 11 pt; nota em 8 pt.

- Página 1, marcador **"Capítulo Um"**:
  - 1º parágrafo: `O médico assinou a certidão sem examinar o corpo.` seguido de `1` em sobrescrito;
  - 2º parágrafo: `A família guardou uma cópia na igreja.`;
  - no pé, a nota: `1 A certidão foi encontrada em 1981 nos arquivos do hospital.`
- Página 2, marcador **"Capítulo Dois"**: `O caso chegou aos jornais da capital.`
- Página 3, marcador **"Bibliografia"**: `Davis, Wade. The Serpent and the Rainbow. 1985.` · `Métraux, Alfred. Le Vaudou haïtien. 1958.`

| ID | Dado | Quando | Então |
|------|------|--------|-------|
| CA-1 | `notas.pdf` convertido com `--slug teste` | `livro trecho teste 01.n01` | código `0`; stdout exatamente `A certidão foi encontrada em 1981 nos arquivos do hospital.\n` |
| CA-2 | `notas.pdf` convertido com `--slug teste` | `livro trecho teste 01.001` e `livro trecho teste 01.002` | stdout exatamente `O médico assinou a certidão sem examinar o corpo.[n01]\n` e `A família guardou uma cópia na igreja.\n` |
| CA-3 | `notas.pdf`; `ROTEIRISTA_LIVROS` numa pasta vazia | `livro novo notas.pdf --slug teste`, depois `livro trecho teste bib.001`, `bib.002` e `03.001` | última linha do `novo` é `2 capítulos, 3 parágrafos`; `bib.001` e `bib.002` dão exatamente `Davis, Wade. The Serpent and the Rainbow. 1985.\n` e `Métraux, Alfred. Le Vaudou haïtien. 1958.\n`; `03.001` sai com código `2` e `id inexistente: 03.001` |

## Risco declarado
nenhum

## Como rodar os testes
Como nas SPECs 001 e 002.

```powershell
uv run --with pytest==8.3.4 pytest tests/acceptance/003-notas-bibliografia --junitxml=relatorios/003-junit.xml
```

As suítes da 001 e da 002 têm de continuar verdes.

## Arquivos que serão tocados (previsão)
- `src/roteirista/pdf.py`, `src/roteirista/banco.py`, `src/roteirista/cli.py`

## Arquivo-exemplo
`src/roteirista/pdf.py` (fatia 002: linhas com página, posição e tamanho de fonte). Referência de
comportamento: o passo "notas de rodapé" do `converter` em `ferramentas/livro.py` do piloto.

## Roteiro manual (3 passos)
1. Reconverta o Serpent: o resumo não conta a bibliografia anotada como capítulo.
2. Rode `livro trecho serpent bib.001`: sai a primeira entrada da bibliografia anotada.
3. Num livro com notas de rodapé (qualquer PDF seu), confira com `trecho` um parágrafo que tenha
   chamada: aparece `[nPP]`, e o `CC.nPP` correspondente devolve o texto da nota.

## Decisões pendentes
nenhuma
