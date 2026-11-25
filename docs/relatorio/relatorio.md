---
title: "Validador de manifesto de carga: autômato de pilha + autômato linearmente limitado"
subtitle: "Relatório técnico — Atividade Prática AV2 de Linguagens Formais e Autômatos"
author:
  - Alberto
  - Davi Maciel Corrêa
  - Gabriel Albuquerque Alencar
  - José Valdez
  - Jorge Lobato
date: "CESUPA — Ciência da Computação — Turma CC6NA — Prof. Daniel Leal Souza — 25/11/2026"
toc: true
toc-depth: 2
numbersections: true
---

**Repositório:** <https://github.com/Gaalbu/validador-manifesto-carga>

<!-- Arquivo gerado por docs/relatorio/montar_relatorio.py — edite as fontes (docs/modelagem, docs/implementacao.md, docs/relatorio/testes.md) e rode o script. -->

# Problema

Um centro de distribuição recebe **manifestos de carga** como cadeias no formato `ESTRUTURA#LOTE`.

- A **estrutura** descreve como os volumes estão acondicionados: um **palete** `[ ]` pode conter
  caixas e outros paletes, e uma **caixa** `{ }` pode conter paletes e outras caixas, mas os volumes
  não podem se cruzar (`[{]}` é inválido). A estrutura não pode ser vazia.
- O **lote** registra os eventos do manifesto em quatro blocos não vazios, nessa ordem:
  **P**edidos, **E**nvios, **C**onfirmações e **D**evoluções.

O manifesto é validado em duas etapas:

1. **Autômato de pilha (AP)** — verifica a estrutura definida por uma GLC: estrutura bem aninhada e
   não vazia, um único `#` e o lote no formato `P+E+C+D+`.
2. **Autômato linearmente limitado (ALL)** — executado só se o AP aceitar, sobre o trecho após o `#`:
   verifica a **dependência cruzada** "todo pedido tem confirmação e todo envio tem devolução", isto
   é, nº de `P` = nº de `C` **e** nº de `E` = nº de `D`.

| Manifesto (23 símbolos) | AP | ALL | Por quê |
|------------------------------|---------|-------------|------------------------------|
| `[{}[{}]]{[]}#PPEEECCDDD` | aceita | aceita | estrutura válida; 2 P = 2 C e 3 E = 3 D |
| `[{}[{]}]{[]}#PPEEECCDDD` | rejeita | não executa | `]` fecha com uma caixa `{` aberta no topo |
| `[{}[{}]]{[]}#PPEEECCCDD` | aceita | rejeita | estrutura válida, mas 2 P ≠ 3 C e 3 E ≠ 2 D |

O problema difere do exemplo da lauda em dois pontos: a estrutura usa **dois tipos** de delimitador
(e não só parênteses), e a regra sensível ao contexto é uma dependência **cruzada** entre pares de
blocos (P↔C e E↔D, intercalados), e não "três blocos com a mesma quantidade". Os dois autômatos foram
modelados pela equipe para este problema: o AP tem **9 estados** e o ALL tem **16 estados de trabalho
+ aceitação + rejeição (18)**.

| Etapa | Linguagem | Classe na hierarquia de Chomsky |
|---|---|---|
| AP | L_AP = { x#y : x ∈ {[,],{,}}⁺ bem aninhada, y ∈ P⁺E⁺C⁺D⁺ } | livre de contexto (determinística), **não regular** |
| ALL | L_ALL = { PⁿEᵐCⁿDᵐ : n, m ≥ 1 } | sensível ao contexto, **não livre de contexto** |

# Fontes consultadas

- SIPSER, M. *Introdução à Teoria da Computação*. 2. ed. São Paulo: Cengage Learning, 2007.
  Seções 1.4 (linguagens não regulares e lema do bombeamento), 2.1–2.2 (GLC e autômatos com pilha),
  2.3 (linguagens não livres do contexto) e 5.1 (autômatos linearmente limitados).
- HOPCROFT, J. E.; MOTWANI, R.; ULLMAN, J. D. *Introdução à Teoria de Autômatos, Linguagens e
  Computação*. 2. ed. Rio de Janeiro: Campus/Elsevier, 2002. Seção 4.1 (bombeamento para linguagens
  regulares), capítulos 5 e 6 (GLC, ambiguidade, autômatos de pilha, aceitação por estado final ×
  pilha vazia, APD) e seção 7.2 (bombeamento para LLC; exemplo {0ⁱ1ʲ2ⁱ3ʲ}).
- MENEZES, P. B. *Linguagens Formais e Autômatos*. 6. ed. Porto Alegre: Bookman, 2011. Capítulos
  sobre linguagens livres do contexto, autômato com pilha, linguagens sensíveis ao contexto e
  autômato com fita limitada.
- KURODA, S.-Y. Classes of languages and linear-bounded automata. *Information and Control*, v. 7,
  n. 2, p. 207–223, 1964.
- Documentação do Python 3 (<https://docs.python.org/3/>), do pytest (<https://docs.pytest.org/>) e
  do Graphviz (<https://graphviz.org/documentation/>), usados na implementação, nos testes e nos
  diagramas.


# Linguagem livre de contexto e autômato de pilha

## Alfabeto e regra de formação

O AP recebe o **manifesto inteiro**, no formato `ESTRUTURA#LOTE`.

| Símbolo | Significado | Parte |
|---|---|---|
| `[` `]` | abre / fecha um **palete** | estrutura |
| `{` `}` | abre / fecha uma **caixa** | estrutura |
| `#` | separador entre estrutura e lote | — |
| `P` `E` `C` `D` | pedido, envio, confirmação, devolução | lote |

**Alfabeto de entrada:** Σ = { `[`, `]`, `{`, `}`, `#`, `P`, `E`, `C`, `D` } (9 símbolos)

**Linguagem reconhecida:**

$$L_{AP} = \{\, x\,\#\,y \;\mid\; x \in \Sigma_{e}^{+} \text{ é bem aninhada},\ y \in P^{+}E^{+}C^{+}D^{+} \,\}$$

com Σₑ = { `[`, `]`, `{`, `}` }.

**Regra de formação.** Uma cadeia *w* pertence a L_AP se, e somente se:

1. *w* tem exatamente um `#`;
2. a estrutura *x* (antes do `#`) **não é vazia** e é **bem aninhada**: todo `[` fecha com `]`, todo
   `{` fecha com `}`, e o último aberto é o primeiro a ser fechado (um palete pode conter caixas e
   vice-versa, mas não podem se cruzar: `[{]}` é inválido);
3. o lote *y* (depois do `#`) tem quatro blocos não vazios, nessa ordem: `P+ E+ C+ D+`.

As **quantidades** de P, E, C e D **não** são conferidas pelo AP: isso é trabalho do ALL (Frente 2).

| Cadeia | \|w\| | Decisão do AP |
|---|---|---|
| `[]#PECD` | 7 | aceita (menor cadeia aceita: caso-limite) |
| `[{}[{}]]{[]}#PPEEECCDDD` | 23 | aceita (cadeia da derivação, seção 4) |
| `[{}[{}]]{[]}#PPEEECCCDD` | 23 | aceita (P≠C e E≠D: quem rejeita é o ALL) |
| ε (vazia) | 0 | rejeita: termina em `q0` (caso-limite) |
| `#PECD` | 5 | rejeita: estrutura vazia, sem transição `(q0, #, Z)` |
| `[{}[{]}]{[]}#PPEEECCDDD` | 23 | rejeita: `]` com `{` aberto no topo, sem transição `(q1, ], Y)` |
| `[[]#PECD` | 8 | rejeita: `#` com `[` ainda aberto, sem transição `(q1, #, X)` |
| `[]][#PECD` | 9 | rejeita: `]` no nível externo, sem transição `(q3, ], Z)` |
| `[]#PEDC` | 7 | rejeita: D antes de C, sem transição `(q6, D, Z)` |
| `[]#PEC` | 6 | rejeita: lote sem D, termina em `q7` (não final) |

## Por que L_AP **não é regular**

**Lema do bombeamento para linguagens regulares** (Sipser, seção 1.4; Hopcroft, Motwani e Ullman,
seção 4.1): se *L* é regular, existe *p* ≥ 1 tal que toda *s* ∈ *L* com |*s*| ≥ *p* pode ser escrita
como *s* = *xyz*, com |*y*| ≥ 1, |*xy*| ≤ *p* e *xyⁱz* ∈ *L* para todo *i* ≥ 0.

**Prova (por contradição).** Suponha L_AP regular e seja *p* o comprimento de bombeamento. Escolha

$$s = [^{\,p}\; ]^{\,p}\, \#PECD \in L_{AP}, \qquad |s| = 2p + 5 \ge p.$$

Como |*xy*| ≤ *p*, *x* e *y* estão dentro dos *p* primeiros símbolos, que são todos `[`. Logo
*y* = `[`ᵏ com *k* ≥ 1. Bombeando para baixo (*i* = 0):

$$xy^0z = [^{\,p-k}\; ]^{\,p}\, \#PECD$$

A estrutura tem *p* − *k* aberturas e *p* fechamentos, então não é bem aninhada e a cadeia ∉ L_AP.
(Com *i* = 2 também falha: sobram *k* paletes abertos.) Contradição: **L_AP não é regular.**

**Intuição.** Um autômato finito tem memória limitada, mas para aceitar `[ⁿ]ⁿ` precisa lembrar *n*,
que pode ser qualquer número. Além disso, com **dois tipos** de delimitador não basta um contador: é
preciso lembrar a **ordem** dos abertos (`[{` exige `}]`, não `]}`). Uma pilha faz exatamente isso.

## GLC: G = (V, Σ, P, S)

- **Variáveis:** V = { S, B, A, L, Ps, Es, Cs, Ds }
- **Terminais:** Σ = { `[`, `]`, `{`, `}`, `#`, `P`, `E`, `C`, `D` }
- **Símbolo inicial:** S
- **Produções P:**

```
S  → B # L                       manifesto = estrutura # lote
B  → A | A B                     estrutura = 1 ou mais blocos lado a lado
A  → [ ] | [ B ] | { } | { B }   bloco = palete ou caixa, vazio ou com conteúdo
L  → Ps Es Cs Ds                 lote = P+ E+ C+ D+
Ps → P | P Ps
Es → E | E Es
Cs → C | C Cs
Ds → D | D Ds
```

(Na notação BNF compacta: `B → A+`, `A → [B?] | {B?}`.)

**Significado de cada variável.**

| Variável | Gera | Exemplo |
|---|---|---|
| A | **um** bloco: um palete ou uma caixa, com o que estiver dentro | `[{}[{}]]` |
| B | um ou mais blocos lado a lado (estrutura não vazia e bem aninhada) | `[{}[{}]]{[]}` |
| L | o lote `P+E+C+D+` | `PPEEECCDDD` |
| Ps, Es, Cs, Ds | um bloco não vazio de P, E, C, D | `PP` |

**A gramática não é ambígua.** Toda estrutura bem aninhada não vazia se decompõe de um só jeito em
blocos externos (cada um fecha quando a profundidade volta a 0), e cada bloco tem um único par de
delimitadores externo. O lote também tem uma única divisão em P+, E+, C+, D+. Por isso cada cadeia
tem uma única árvore de derivação — o que combina com o AP ser **determinístico** (seção 5).

## Derivação de uma cadeia aceita (23 símbolos)

Cadeia: `[{}[{}]]{[]}#PPEEECCDDD` — estrutura com 2 blocos externos: o palete `[{}[{}]]` (que contém
uma caixa vazia e um palete com uma caixa) e a caixa `{[]}` (que contém um palete vazio); lote com 2 P,
3 E, 2 C, 3 D.

**Derivação mais à esquerda** (em cada passo, a regra é aplicada à variável mais à esquerda):

| # | Regra | Forma sentencial |
|---|---|---|
| 0 | — | S |
| 1 | S → B#L | B # L |
| 2 | B → AB | A B # L |
| 3 | A → [B] | [ B ] B # L |
| 4 | B → AB | [ A B ] B # L |
| 5 | A → {} | [ { } B ] B # L |
| 6 | B → A | [ { } A ] B # L |
| 7 | A → [B] | [ { } [ B ] ] B # L |
| 8 | B → A | [ { } [ A ] ] B # L |
| 9 | A → {} | [ { } [ { } ] ] B # L |
| 10 | B → A | [ { } [ { } ] ] A # L |
| 11 | A → {B} | [ { } [ { } ] ] { B } # L |
| 12 | B → A | [ { } [ { } ] ] { A } # L |
| 13 | A → [] | [ { } [ { } ] ] { [ ] } # L |
| 14 | L → Ps Es Cs Ds | [{}[{}]]{[]} # Ps Es Cs Ds |
| 15 | Ps → P Ps | [{}[{}]]{[]} # P Ps Es Cs Ds |
| 16 | Ps → P | [{}[{}]]{[]} # P P Es Cs Ds |
| 17 | Es → E Es | [{}[{}]]{[]} # P P E Es Cs Ds |
| 18 | Es → E Es | [{}[{}]]{[]} # P P E E Es Cs Ds |
| 19 | Es → E | [{}[{}]]{[]} # P P E E E Cs Ds |
| 20 | Cs → C Cs | [{}[{}]]{[]} # P P E E E C Cs Ds |
| 21 | Cs → C | [{}[{}]]{[]} # P P E E E C C Ds |
| 22 | Ds → D Ds | [{}[{}]]{[]} # P P E E E C C D Ds |
| 23 | Ds → D Ds | [{}[{}]]{[]} # P P E E E C C D D Ds |
| 24 | Ds → D | `[{}[{}]]{[]}#PPEEECCDDD` |

São 24 passos de derivação. Cada passo foi conferido por script (regra existe em G e é aplicada na
variável mais à esquerda).

**Árvore de derivação** da estrutura (o lote L é uma "escada" à direita:
Ps → P Ps → P P, Es → E Es → E E Es → E E E, e assim por diante):

```
                    S
          __________|__________
         B          #          L ⇒* PPEEECCDDD
    _____|______
   A            B
 __|____        |
[  B    ]       A
  _|__        __|__
 A    B      {  B  }
 |    |         |
{ }   A         A
    __|__       |
   [  B  ]     [ ]
      |
      A
      |
     { }
```

## Especificação do AP

M = (Q, Σ, Γ, δ, q₀, Z, F)

### Estados (9)

| Estado | Papel | Pilha nesse estado |
|---|---|---|
| `q0` | início: espera o primeiro bloco (a estrutura não pode ser vazia) | `Z` |
| `q1` | dentro de um bloco: empilha aberturas, desempilha fechamentos | ≥ 1 aberto sobre `Z` |
| `q2` | acabou de fechar um bloco: consulta o topo **sem ler** (só transições ε) | qualquer |
| `q3` | nível externo: já houve ≥ 1 bloco; abre outro bloco ou lê `#` | `Z` |
| `q4` | leu `#`: espera o primeiro `P` | `Z` |
| `q5` | bloco de `P` | `Z` |
| `q6` | bloco de `E` | `Z` |
| `q7` | bloco de `C` | `Z` |
| `q8` | bloco de `D` — **único estado final** | `Z` |

Por que `q0` e `q3` são estados diferentes, se os dois têm só `Z` na pilha? Porque `q3` aceita `#` e
`q0` não: é assim que o AP exige a estrutura **não vazia** (`#PECD` é rejeitada).

### Alfabetos, configuração inicial e estados finais

- **Σ** (entrada) = { `[`, `]`, `{`, `}`, `#`, `P`, `E`, `C`, `D` }
- **Γ** (pilha) = { `Z`, `X`, `Y` }: `Z` = fundo da pilha; `X` = um `[` aberto; `Y` = um `{` aberto
- **Estado inicial:** `q0`; **símbolo inicial da pilha:** `Z`
- **Configuração inicial:** (`q0`, *w*, `Z`) — estado, entrada ainda não lida, pilha (topo à esquerda)
- **Estados finais:** F = { `q8` }

### Tabela de transições

Notação: δ(q, a, t) = (q', γ) significa "no estado q, lendo a (ou ε, sem ler), com t no topo: vai
para q' e troca t por γ". O topo é o primeiro símbolo de γ; γ = ε desempilha. Toda combinação que
não está na tabela **não tem transição**: o AP trava e **rejeita**.

| # | Estado | Lê | Topo | → Estado | Empilha (no lugar do topo) | Significado |
|---|---|---|---|---|---|---|
| 1 | q0 | `[` | Z | q1 | XZ | abre o 1º palete |
| 2 | q0 | `{` | Z | q1 | YZ | abre a 1ª caixa |
| 3 | q1 | `[` | X | q1 | XX | palete dentro de palete |
| 4 | q1 | `[` | Y | q1 | XY | palete dentro de caixa |
| 5 | q1 | `{` | X | q1 | YX | caixa dentro de palete |
| 6 | q1 | `{` | Y | q1 | YY | caixa dentro de caixa |
| 7 | q1 | `]` | X | q2 | ε | fecha palete (topo tem de ser `[`) |
| 8 | q1 | `}` | Y | q2 | ε | fecha caixa (topo tem de ser `{`) |
| 9 | q2 | ε | Z | q3 | Z | fechou um bloco externo: volta ao nível externo |
| 10 | q2 | ε | X | q1 | X | ainda dentro de um palete |
| 11 | q2 | ε | Y | q1 | Y | ainda dentro de uma caixa |
| 12 | q3 | `[` | Z | q1 | XZ | abre outro palete externo |
| 13 | q3 | `{` | Z | q1 | YZ | abre outra caixa externa |
| 14 | q3 | `#` | Z | q4 | Z | fim da estrutura |
| 15 | q4 | `P` | Z | q5 | Z | 1º pedido |
| 16 | q5 | `P` | Z | q5 | Z | mais pedidos |
| 17 | q5 | `E` | Z | q6 | Z | 1º envio |
| 18 | q6 | `E` | Z | q6 | Z | mais envios |
| 19 | q6 | `C` | Z | q7 | Z | 1ª confirmação |
| 20 | q7 | `C` | Z | q7 | Z | mais confirmações |
| 21 | q7 | `D` | Z | q8 | Z | 1ª devolução |
| 22 | q8 | `D` | Z | q8 | Z | mais devoluções |

São 22 transições. Na parte do lote (`q4`…`q8`) a pilha fica parada em `Z`: essa parte é regular e
funciona como um autômato finito.

**O AP é determinístico (APD).** Em cada configuração existe no máximo uma transição aplicável: as
transições ε existem só em `q2`, e `q2` não tem nenhuma transição de leitura; nos outros estados, cada
par (símbolo lido, topo) aparece no máximo uma vez. Não há escolhas a explorar, e o simulador segue um
único caminho.

### Critério de aceitação

**Aceitação por estado final:** *w* é aceita se, e somente se, o AP **consome a entrada inteira** e
termina em `q8`. Rejeita se:

- trava antes do fim (não há transição para (estado, símbolo, topo)) — ex.: fechamento trocado, `#`
  com bloco aberto, lote fora de ordem, segundo `#`; ou
- consome tudo, mas para fora de `q8` — ex.: entrada vazia (`q0`), lote incompleto (`q4`…`q7`).

Ao aceitar, a pilha contém só `Z`. Por isso também seria possível aceitar **por pilha vazia**,
acrescentando a transição δ(q8, ε, Z) = (q8, ε) a ser usada só no fim da entrada; preferimos estado
final porque o simulador fica mais simples (o AP continua determinístico).

## Relação GLC ↔ AP (o que o AP faz com cada regra)

| Regra da GLC | Transições do AP | Ideia |
|---|---|---|
| A → `[` B `]` / A → `[` `]` | 1, 3, 4, 12 (empilha X ao ler `[`) e 7 (desempilha X ao ler `]`) | o `]` que fecha A é o que encontra **o mesmo X** no topo |
| A → `{` B `}` / A → `{` `}` | 2, 5, 6, 13 (empilha Y) e 8 (desempilha Y) | idem para caixas |
| B → A B (B dentro de um bloco) | 10, 11 (volta a `q1` se ainda há abertos) | depois de fechar um bloco interno, pode vir outro |
| B → A B (nível externo) e S → B # L | 9 (`q2`→`q3`), 12, 13, 14 | no nível externo: mais um bloco ou `#` |
| B → A (exige ≥ 1 bloco) | `q0` não lê `#` | estrutura vazia é rejeitada |
| L → Ps Es Cs Ds, Ps → P \| P Ps, … | 15–22 | um estado por bloco do lote |

A pilha guarda **a sequência de produções A ainda não terminadas**: cada X/Y na pilha é um palete/caixa
cujo símbolo de fechamento ainda não foi lido. A recursão da gramática (A → `[` B `]` dentro de outro A)
vira empilhar sobre o que já está lá.

## Justificativa: L(M) = L(G)

**Passo 1 — o que B gera.** B gera exatamente as cadeias não vazias bem aninhadas sobre Σₑ.
(⊆) Por indução na derivação: `[]`, `{}` são bem aninhadas; envolver uma bem aninhada com `[ ]` ou
`{ }`, ou concatenar duas, mantém a propriedade. (⊇) Por indução no comprimento: uma cadeia bem
aninhada não vazia *x* começa com uma abertura; seja *a* o símbolo que a fecha. Então *x* = *a u ā v*,
com *u* e *v* bem aninhadas (talvez vazias). *a u ā* é gerada por A (A → *a* *ā* se *u* = ε, ou
A → *a* B *ā* pela hipótese de indução), e *v* é vazia (use B → A) ou gerada por B (use B → A B).
Logo L(G) = { *x* `#` *y* | *x* bem aninhada não vazia, *y* ∈ P⁺E⁺C⁺D⁺ } = L_AP (seção 1).

**Passo 2 — invariante do AP na estrutura.** Seja *u* o prefixo da estrutura já lido e defina
h(`[`) = X, h(`{`) = Y. Por indução em |*u*|, depois de fazer a transição ε de `q2` (quando houver):

1. se *u* não é prefixo de nenhuma cadeia bem aninhada, o AP **já travou** (rejeitou);
2. senão, se *u* tem aberturas pendentes *a₁ … aₖ* (*k* ≥ 1, *aₖ* a mais recente), o AP está em `q1`
   com pilha h(*aₖ*) … h(*a₁*) Z;
3. senão (*u* é bem aninhada), o AP está em `q0` se *u* = ε e em `q3` se *u* ≠ ε, com pilha `Z`.

O passo indutivo é a leitura da tabela: uma abertura empilha o X/Y correspondente (transições 1–6,
12, 13); um fechamento só tem transição se o topo for o do mesmo tipo (7, 8) — que é exatamente a
abertura pendente mais recente; depois disso, `q2` olha o topo e vai para `q1` (ainda há pendentes) ou
`q3` (topo `Z`, nível externo). Qualquer outro símbolo nesses estados não tem transição.

**Passo 3 — o `#` e o lote.** Só existe transição com `#` a partir de `q3`, ou seja (pelo passo 2),
exatamente quando a estrutura lida é bem aninhada e não vazia. A partir daí, `q4`…`q8` formam um
autômato finito determinístico para P⁺E⁺C⁺D⁺ (a pilha fica em `Z`), com `q8` final. Um segundo `#`
ou qualquer símbolo de estrutura depois do `#` não tem transição.

**Conclusão.** M termina em `q8` com a entrada consumida ⇔ *w* = *x* `#` *y* com *x* bem aninhada não
vazia e *y* ∈ P⁺E⁺C⁺D⁺ ⇔ *w* ∈ L(G). Portanto **L(M) = L(G) = L_AP**, e L_AP é livre de contexto (e,
mais que isso, livre de contexto **determinística**).

**Conferência por computador** ([`verificar_ap.py`](https://github.com/Gaalbu/validador-manifesto-carga/blob/main/docs/modelagem/verificar_ap.py)):
- o conjunto de cadeias geradas pela GLC e o conjunto aceito pelo AP são **iguais** para todos os
  comprimentos até 16 (23 670 cadeias);
- AP = definição da seção 1 em **todas** as 5 380 840 cadeias de Σ\* com até 7 símbolos e em 20 000
  cadeias aleatórias de até ~34 símbolos (variações de cadeias aceitas com trocas, inserções e remoções);
- o invariante do passo 2 (pilha sempre da forma (X|Y)\* Z) vale em todas as configurações alcançadas.

## Terminação e número de passos

Cada transição de leitura consome um símbolo. As transições ε só existem em `q2`, e `q2` sempre vai
para `q1` ou `q3`, que não têm transições ε; logo há no máximo **uma** transição ε por símbolo de
fechamento lido. Total de passos ≤ |*w*| + (nº de `]` e `}`) ≤ 2|*w*|, e o AP sempre para — aceitando
ou travando. Exemplo: a cadeia da seção 4 tem 23 símbolos e 6 fechamentos → 29 passos. O limite
2|*w*| foi verificado em todas as cadeias com até 7 símbolos.

## Rastreamento

```bash
python -m src.main "[{}[{}]]{[]}#PPEEECCDDD" --so ap --trace
```

```
   0 | q0  | pos=0   | resta=[{}[{}]]{[]}#PPEEECCDDD      | pilha=Z            | configuração inicial
   1 | q1  | pos=1   | resta={}[{}]]{[]}#PPEEECCDDD       | pilha=XZ           | leu [, topo Z -> empilha XZ
   2 | q1  | pos=2   | resta=}[{}]]{[]}#PPEEECCDDD        | pilha=YXZ          | leu {, topo X -> empilha YX
   3 | q2  | pos=3   | resta=[{}]]{[]}#PPEEECCDDD         | pilha=XZ           | leu }, topo Y -> empilha ε
   4 | q1  | pos=3   | resta=[{}]]{[]}#PPEEECCDDD         | pilha=XZ           | leu ε, topo X -> empilha X
   5 | q1  | pos=4   | resta={}]]{[]}#PPEEECCDDD          | pilha=XXZ          | leu [, topo X -> empilha XX
   6 | q1  | pos=5   | resta=}]]{[]}#PPEEECCDDD           | pilha=YXXZ         | leu {, topo X -> empilha YX
   7 | q2  | pos=6   | resta=]]{[]}#PPEEECCDDD            | pilha=XXZ          | leu }, topo Y -> empilha ε
   8 | q1  | pos=6   | resta=]]{[]}#PPEEECCDDD            | pilha=XXZ          | leu ε, topo X -> empilha X
   9 | q2  | pos=7   | resta=]{[]}#PPEEECCDDD             | pilha=XZ           | leu ], topo X -> empilha ε
  10 | q1  | pos=7   | resta=]{[]}#PPEEECCDDD             | pilha=XZ           | leu ε, topo X -> empilha X
  11 | q2  | pos=8   | resta={[]}#PPEEECCDDD              | pilha=Z            | leu ], topo X -> empilha ε
  12 | q3  | pos=8   | resta={[]}#PPEEECCDDD              | pilha=Z            | leu ε, topo Z -> empilha Z
  13 | q1  | pos=9   | resta=[]}#PPEEECCDDD               | pilha=YZ           | leu {, topo Z -> empilha YZ
  14 | q1  | pos=10  | resta=]}#PPEEECCDDD                | pilha=XYZ          | leu [, topo Y -> empilha XY
  15 | q2  | pos=11  | resta=}#PPEEECCDDD                 | pilha=YZ           | leu ], topo X -> empilha ε
  16 | q1  | pos=11  | resta=}#PPEEECCDDD                 | pilha=YZ           | leu ε, topo Y -> empilha Y
  17 | q2  | pos=12  | resta=#PPEEECCDDD                  | pilha=Z            | leu }, topo Y -> empilha ε
  18 | q3  | pos=12  | resta=#PPEEECCDDD                  | pilha=Z            | leu ε, topo Z -> empilha Z
  19 | q4  | pos=13  | resta=PPEEECCDDD                   | pilha=Z            | leu #, topo Z -> empilha Z
  20 | q5  | pos=14  | resta=PEEECCDDD                    | pilha=Z            | leu P, topo Z -> empilha Z
  21 | q5  | pos=15  | resta=EEECCDDD                     | pilha=Z            | leu P, topo Z -> empilha Z
  22 | q6  | pos=16  | resta=EECCDDD                      | pilha=Z            | leu E, topo Z -> empilha Z
  23 | q6  | pos=17  | resta=ECCDDD                       | pilha=Z            | leu E, topo Z -> empilha Z
  24 | q6  | pos=18  | resta=CCDDD                        | pilha=Z            | leu E, topo Z -> empilha Z
  25 | q7  | pos=19  | resta=CDDD                         | pilha=Z            | leu C, topo Z -> empilha Z
  26 | q7  | pos=20  | resta=DDD                          | pilha=Z            | leu C, topo Z -> empilha Z
  27 | q8  | pos=21  | resta=DD                           | pilha=Z            | leu D, topo Z -> empilha Z
  28 | q8  | pos=22  | resta=D                            | pilha=Z            | leu D, topo Z -> empilha Z
  29 | q8  | pos=23  | resta=ε                            | pilha=Z            | leu D, topo Z -> empilha Z
     entrada consumida em q8 (final) -> ACEITA
```

Rejeição por aninhamento cruzado (`[{}[{]}]{[]}#PPEEECCDDD`, final do rastro):

```
   5 | q1  | pos=4   | resta={]}]{[]}#PPEEECCDDD          | pilha=XXZ          | leu [, topo X -> empilha XX
   6 | q1  | pos=5   | resta=]}]{[]}#PPEEECCDDD           | pilha=YXXZ         | leu {, topo X -> empilha YX
     sem transição para (q1, ']', Y) -> REJEITA
```

O `]` chegou com um `{` (Y) no topo: a caixa aberta por último ainda não foi fechada.

**Como prever a decisão de uma cadeia nova (para a arguição).** Leia a estrutura mantendo a pilha de
abertos: cada `[`/`{` empilha X/Y; cada `]`/`}` precisa encontrar X/Y no topo, senão rejeita. O `#` só
passa com a pilha em `Z` e pelo menos um bloco lido. Depois, o lote tem de ser P…E…C…D…, cada bloco
com pelo menos um símbolo, e a cadeia tem de acabar num `D`.

## Diagrama do AP

![Diagrama de estados do AP, gerado da tabela `src/ap/transicoes.py`. Rótulo `a, t / γ`: lê *a* (ou ε) com *t* no topo e troca *t* por γ. Pares ausentes não têm transição (rejeita).](figuras/ap_tb.png){ height=23.5cm }

# Linguagem sensível ao contexto e autômato linearmente limitado

## Alfabeto e regra de aceitação

O ALL recebe o **trecho do manifesto após o `#`** (o lote). Cada símbolo é um evento:

| Símbolo | Evento |
|---|---|
| `P` | pedido |
| `E` | envio |
| `C` | confirmação (de um pedido) |
| `D` | devolução (de um envio) |

**Alfabeto de entrada:** Σ = { `P`, `E`, `C`, `D` }

**Linguagem reconhecida:**

$$L_{ALL} = \{\, P^n\, E^m\, C^n\, D^m \;\mid\; n \ge 1,\ m \ge 1 \,\}$$

**Regra de aceitação.** Uma cadeia *w* é aceita se, e somente se:

1. *w* tem o formato `P+ E+ C+ D+` (quatro blocos não vazios, nessa ordem);
2. nº de `P` = nº de `C` (todo pedido tem confirmação);
3. nº de `E` = nº de `D` (todo envio tem devolução).

As condições 2 e 3 formam uma **dependência cruzada**: o 1º bloco depende do 3º e o 2º depende do 4º,
e esses pares se intercalam (P … E … C … D). Isso não é o exemplo da lauda, que pede três blocos com
a mesma quantidade.

**Formato no fluxo integrado.** O AP já garante que o lote tem o formato `P+E+C+D+`. O ALL confere o
formato de novo porque também é testado **isoladamente** (testes de módulo com qualquer cadeia de Σ\*).
Assim, ele decide sozinho a linguagem L_ALL.

| Cadeia | \|w\| | n, m | Decisão |
|---|---|---|---|
| `PECD` | 4 | 1, 1 | aceita (menor cadeia aceita: caso-limite) |
| `PPPPEEEEECCCCDDDDD` | 18 | 4, 5 | aceita |
| `PPPPPEEEECCCCCDDDD` | 18 | 5, 4 | aceita |
| ε (vazia) | 0 | — | rejeita (caso-limite) |
| `PPPPPEEEECCCCDDDDD` | 18 | — | rejeita: 5 P × 4 C |
| `PPPPEEEEEECCCCDDDD` | 18 | — | rejeita: 6 E × 4 D |
| `PPPPEEEEDDDDCCCCCC` | 18 | — | rejeita: formato (D antes de C) |

## Classificação da linguagem

### L_ALL **não** é livre de contexto

**Lema do bombeamento para LLC** (Sipser, seção 2.3; Hopcroft, Motwani e Ullman, seção 7.2):
se *L* é livre de contexto, existe *p* ≥ 1 tal que toda *s* ∈ *L* com |*s*| ≥ *p* pode ser escrita
como *s* = *uvwxy*, com:

- (a) |*vwx*| ≤ *p*;
- (b) |*vx*| ≥ 1;
- (c) *u vⁱ w xⁱ y* ∈ *L* para todo *i* ≥ 0.

**Prova (por contradição).** Suponha que L_ALL seja LLC e seja *p* a constante do lema. Tome

$$s = P^p\,E^p\,C^p\,D^p \in L_{ALL}, \qquad |s| = 4p \ge p.$$

Seja *s* = *uvwxy* uma decomposição qualquer que satisfaça (a) e (b). Vamos usar *i* = 2:

- **Caso 1: *v* ou *x* contém dois símbolos diferentes.** Então, em *uv²wx²y*, aparece um símbolo
  depois de outro que deveria vir antes (por exemplo `…PEPE…`). A cadeia sai do formato
  `P+E+C+D+`, logo ∉ L_ALL.
- **Caso 2: *v* e *x* contêm, cada um, um só tipo de símbolo.** Os pares que precisam ter a mesma
  quantidade são (P, C) e (E, D). Entre o último `P` e o primeiro `C` há *p* símbolos `E`, então
  uma subcadeia que contenha `P` e `C` tem comprimento ≥ *p* + 2. Por (a), *vwx* não contém os dois.
  Pelo mesmo motivo (há *p* símbolos `C` entre eles), *vwx* não contém `E` e `D` ao mesmo tempo.
  Por (b), *vx* contém algum símbolo *a*, e o seu parceiro *a'* (P↔C, E↔D) não está em *vwx*.
  Em *uv²wx²y*, o formato continua `P+E+C+D+`, mas a quantidade de *a* passa a ser > *p* e a de
  *a'* continua *p*. Logo, *uv²wx²y* ∉ L_ALL.

Em todos os casos, (c) falha para *i* = 2. Isso contradiz o lema, então **L_ALL não é livre de
contexto**. ■

**Intuição (por que a pilha não basta).** Uma pilha casa dependências **aninhadas**: o último
aberto é o primeiro fechado, como em `[ { } ]`, e é isso que o AP do projeto faz. Aqui as dependências
são **cruzadas**. Para comparar os `P` com os `C`, a pilha precisaria ter os `P` no topo, mas os `E`
foram empilhados por cima e ainda precisam ser lembrados até os `D`. Ao desempilhar os `E` para
alcançar os `P`, a contagem dos `E` se perde.

Hopcroft, Motwani e Ullman (seção 7.2) aplicam o mesmo raciocínio à linguagem
{0ⁱ1ʲ2ⁱ3ʲ}, que tem a mesma estrutura (renomeando 0→P, 1→E, 2→C, 3→D).

### L_ALL **é** sensível ao contexto

São duas justificativas independentes.

**(i) Pelo autômato.** Pelo teorema de Kuroda (1964), uma linguagem sem ε é sensível ao contexto se,
e somente se, é reconhecida por um autômato linearmente limitado. A seção 3 apresenta um ALL que
**decide** L_ALL: ele para em toda entrada (seção 7) e usa só as *n* células da entrada mais os dois
marcadores (seção 6). Logo, L_ALL é sensível ao contexto.

**(ii) Por uma gramática.** Na definição de Menezes, uma gramática sensível ao contexto (monotônica)
tem toda produção α → β com |α| ≤ |β|. A gramática abaixo gera L_ALL:

G = ({ S, T, X, Y }, { P, E, C, D }, R, S), onde `X` "vira" `C` e `Y` "vira" `D`:

```
R1:  S  → P S X  |  P T X        gera Pⁿ … Xⁿ
R2:  T  → E T Y  |  E Y          gera Eᵐ Yᵐ   →  forma Pⁿ Eᵐ Yᵐ Xⁿ
R3:  Y X → X Y                    leva todos os X para antes dos Y
R4:  E X → E C                    um X só vira C se estiver logo após E ou C
     C X → C C
     C Y → C D                    um Y só vira D se estiver logo após C ou D
     D Y → D D
```

Todas as produções têm |α| ≤ |β|. **Correção (resumo):** R1 e R2 geram Pⁿ Eᵐ Yᵐ Xⁿ. R3 e R4
preservam a quantidade de X/C (= *n*) e de Y/D (= *m*). Um `C` terminal só é criado com `E` ou `C`
à esquerda, e um `D` só com `C` ou `D` à esquerda. Como terminais nunca são reescritos nem trocados de
lugar, a parte final de qualquer cadeia terminal é Cⁿ Dᵐ. A gramática foi conferida por força bruta:
ela gera exatamente as 15 cadeias de L_ALL com até 12 símbolos.

Exemplo de derivação de `PPECCD` (*n* = 2, *m* = 1):

```
S ⇒ P S X ⇒ P P T X X ⇒ P P E Y X X          (R1, R1, R2)
  ⇒ P P E X Y X ⇒ P P E X X Y                (R3, R3)
  ⇒ P P E C X Y ⇒ P P E C C Y ⇒ P P E C C D  (R4: EX→EC, CX→CC, CY→CD)
```

**Conclusão:** L_ALL ∈ LSC \ LLC. A linguagem do AP (Frente 1) fica em LLC \ Regulares. As duas
etapas do validador ocupam, portanto, níveis diferentes da hierarquia de Chomsky.

## Especificação do ALL

M = (Q, Σ, Γ, δ, q0, `<`, `>`, q_acc, q_rej)

### Estados (16 de trabalho + aceitação + rejeição = 18)

| Estado | Fase | Função |
|---|---|---|
| `q0` | início | cabeçote sobre o marcador esquerdo |
| `q1` | 1. formato | espera o primeiro `P` |
| `q2` | 1. formato | bloco de `P` |
| `q3` | 1. formato | bloco de `E` |
| `q4` | 1. formato | bloco de `C` |
| `q5` | 1. formato | bloco de `D` (até o `>`) |
| `q6` | 1. formato | volta ao marcador esquerdo |
| `q7` | 2. casa P–C | procura o próximo `P` não marcado |
| `q8` | 2. casa P–C | procura o `C` correspondente |
| `q9` | 2. casa P–C | volta ao início (par P/C marcado) |
| `q10` | 3. sobra de C | confere que não sobrou `C` sem par |
| `q11` | 3. sobra de C | volta ao início |
| `q12` | 4. casa E–D | procura o próximo `E` não marcado |
| `q13` | 4. casa E–D | procura o `D` correspondente |
| `q14` | 4. casa E–D | volta ao início (par E/D marcado) |
| `q15` | 5. sobra de D | confere que não sobrou `D` sem par |
| `q_acc` | — | aceitação (para) |
| `q_rej` | — | rejeição (para) |

### Alfabetos e marcadores

- **Entrada:** Σ = { `P`, `E`, `C`, `D` }
- **Fita:** Γ = { `P`, `E`, `C`, `D`, `p`, `e`, `c`, `d`, `<`, `>` }
  - minúscula = símbolo **já casado** (marcado);
  - `<` e `>` = marcadores de borda (∈ Γ \ Σ), fixos e nunca sobrescritos.
- **Movimentos:** `R` = direita, `L` = esquerda, `S` = permanece. As letras D/E não são usadas
  para movimento, para não confundir com os símbolos `D` e `E`.

### Configuração inicial

Fita `< w₁ w₂ … wₙ >`, estado `q0`, cabeçote na célula 0 (sobre `<`).
Para o lote do cenário de integração:

```
q0 | cab=0 | [<]PPEEECCDDD>
```

### Função de transição

δ : Q × Γ → Q × Γ × {L, R, S} é **parcial** e **determinística** (no máximo uma transição por par
(estado, símbolo)). Todo par ausente leva a `q_rej`. São **67 transições** no total.

Tabela compacta: uma linha com vários símbolos lidos representa uma transição para cada símbolo.
"(mesmo)" significa que o símbolo lido é reescrito sem mudança.

| Estado | Lê | Escreve | Move | Próximo | Papel |
|---|---|---|---|---|---|
| `q0` | `<` | `<` | R | `q1` | sai do marcador |
| `q1` | `P` | `P` | R | `q2` | 1º símbolo deve ser `P` |
| `q2` | `P` | `P` | R | `q2` | bloco P |
| `q2` | `E` | `E` | R | `q3` | início do bloco E |
| `q3` | `E` | `E` | R | `q3` | bloco E |
| `q3` | `C` | `C` | R | `q4` | início do bloco C |
| `q4` | `C` | `C` | R | `q4` | bloco C |
| `q4` | `D` | `D` | R | `q5` | início do bloco D |
| `q5` | `D` | `D` | R | `q5` | bloco D |
| `q5` | `>` | `>` | L | `q6` | formato OK |
| `q6` | `P E C D p e c d` | (mesmo) | L | `q6` | volta |
| `q6` | `<` | `<` | R | `q7` | começa a casar P–C |
| `q7` | `p` | `p` | R | `q7` | pula P já casados |
| `q7` | `P` | **`p`** | R | `q8` | marca um P |
| `q7` | `E` | `E` | R | `q10` | todos os P casados |
| `q8` | `P E c` | (mesmo) | R | `q8` | procura C livre |
| `q8` | `C` | **`c`** | L | `q9` | marca o C par |
| `q9` | `P E C D p e c d` | (mesmo) | L | `q9` | volta |
| `q9` | `<` | `<` | R | `q7` | próxima volta |
| `q10` | `E c` | (mesmo) | R | `q10` | não pode haver C livre |
| `q10` | `D` | `D` | L | `q11` | nenhum C sobrou |
| `q11` | `P E C D p e c d` | (mesmo) | L | `q11` | volta |
| `q11` | `<` | `<` | R | `q12` | começa a casar E–D |
| `q12` | `p e` | (mesmo) | R | `q12` | pula P e E já casados |
| `q12` | `E` | **`e`** | R | `q13` | marca um E |
| `q12` | `c` | `c` | R | `q15` | todos os E casados |
| `q13` | `E c d` | (mesmo) | R | `q13` | procura D livre |
| `q13` | `D` | **`d`** | L | `q14` | marca o D par |
| `q14` | `P E C D p e c d` | (mesmo) | L | `q14` | volta |
| `q14` | `<` | `<` | R | `q12` | próxima volta |
| `q15` | `c d` | (mesmo) | R | `q15` | não pode haver D livre |
| `q15` | `>` | `>` | S | **`q_acc`** | ACEITA |

### Tabela em forma de matriz

Cada célula mostra (próximo estado, escrito, movimento). `·` significa sem transição, ou seja,
vai para `q_rej`. Esta forma é a mais rápida para **prever a decisão** de uma cadeia nova na arguição.

| Estado | `<` | `P` | `E` | `C` | `D` | `p` | `e` | `c` | `d` | `>` |
|---|---|---|---|---|---|---|---|---|---|---|
| `q0` | q1, <, R | · | · | · | · | · | · | · | · | · |
| `q1` | · | q2, P, R | · | · | · | · | · | · | · | · |
| `q2` | · | q2, P, R | q3, E, R | · | · | · | · | · | · | · |
| `q3` | · | · | q3, E, R | q4, C, R | · | · | · | · | · | · |
| `q4` | · | · | · | q4, C, R | q5, D, R | · | · | · | · | · |
| `q5` | · | · | · | · | q5, D, R | · | · | · | · | q6, >, L |
| `q6` | q7, <, R | q6, P, L | q6, E, L | q6, C, L | q6, D, L | q6, p, L | q6, e, L | q6, c, L | q6, d, L | · |
| `q7` | · | q8, p, R | q10, E, R | · | · | q7, p, R | · | · | · | · |
| `q8` | · | q8, P, R | q8, E, R | q9, c, L | · | · | · | q8, c, R | · | · |
| `q9` | q7, <, R | q9, P, L | q9, E, L | q9, C, L | q9, D, L | q9, p, L | q9, e, L | q9, c, L | q9, d, L | · |
| `q10` | · | · | q10, E, R | · | q11, D, L | · | · | q10, c, R | · | · |
| `q11` | q12, <, R | q11, P, L | q11, E, L | q11, C, L | q11, D, L | q11, p, L | q11, e, L | q11, c, L | q11, d, L | · |
| `q12` | · | · | q13, e, R | · | · | q12, p, R | q12, e, R | q15, c, R | · | · |
| `q13` | · | · | q13, E, R | · | q14, d, L | · | · | q13, c, R | q13, d, R | · |
| `q14` | q12, <, R | q14, P, L | q14, E, L | q14, C, L | q14, D, L | q14, p, L | q14, e, L | q14, c, L | q14, d, L | · |
| `q15` | · | · | · | · | · | · | · | q15, c, R | q15, d, R | q_acc, >, S |

## Como o ALL decide (justificativa da modelagem)

A memória de trabalho é a **própria fita**: em vez de contadores, o ALL troca uma maiúscula por uma
minúscula para registrar "já casei este símbolo".

1. **Formato (q1–q6).** Uma passada para a direita confere `P+E+C+D+`, como um AFD embutido. Ao
   chegar em `>`, volta até `<`. Depois desta fase, as próximas sabem que os blocos estão na ordem.
2. **Casa P–C (q7–q9).** A cada volta, marca o `P` livre mais à esquerda (`P→p`) e o `C` livre mais à
   esquerda (`C→c`, pulando os `E` e os `c`) e volta ao `<`.
   **Invariante:** após *k* voltas, a fita é `< pᵏ Pⁿ⁻ᵏ Eᵐ cᵏ Cⁿ'⁻ᵏ Dᵐ' >`.
   - Se faltar `C` para um `P`, o cabeçote em `q8` chega a um `D` → rejeita (mais P que C).
3. **Sobra de C (q10–q11).** Quando `q7` encontra `E`, todos os `P` foram casados. O ALL anda até o
   primeiro `D` pulando `E` e `c`. Encontrar um `C` livre → rejeita (mais C que P).
4. **Casa E–D (q12–q14).** Mesmo esquema da fase 2 para o par (E, D).
   - Se faltar `D` para um `E`, `q13` chega a `>` → rejeita (mais E que D).
5. **Sobra de D (q15).** Quando `q12` encontra `c`, todos os `E` foram casados. O ALL anda até `>`
   pulando `c` e `d`. Encontrar um `D` livre → rejeita (mais D que E). Chegar a `>` → **aceita**.

Logo, o ALL aceita ⇔ formato correto ∧ #P = #C ∧ #E = #D ⇔ *w* ∈ L_ALL.

## Condições de aceitação e rejeição

- **Aceitação:** somente pela transição (`q15`, `>`) → `q_acc`. Isso exige que todos os quatro blocos
  tenham sido completamente casados.
- **Rejeição:** qualquer par (estado, símbolo) sem transição leva a `q_rej`. Cada causa de rejeição
  corresponde a um ponto específico da tabela:

| Onde para | Significado | Exemplo (18 símbolos) | Passos |
|---|---|---|---|
| `q1`…`q5` | formato errado | `PPPPEEEEDDDDCCCCCC` (para em `q3` lendo `D`) | 9 |
| `q5` lendo `P` | símbolo após o bloco D | `PPPPEEEECCCCDDDDDP` | 18 |
| `q8` lendo `D` | mais `P` que `C` | `PPPPPEEEECCCCDDDDD` | 144 |
| `q10` lendo `C` | mais `C` que `P` | `PPPPEEEEECCCCCDDDD` | 144 |
| `q13` lendo `>` | mais `E` que `D` | `PPPPEEEEEECCCCDDDD` | 319 |
| `q15` lendo `D` | mais `D` que `E` | `PPPPEEEECCCCDDDDDD` | 281 |
| `q1` lendo `>` | entrada vazia | ε | 1 |

**Roteiro para prever a decisão de uma cadeia nova:**

1. Ela tem o formato `P+E+C+D+`? Se não, rejeita na fase 1, no primeiro símbolo fora de ordem.
2. Compare #P com #C: se #P > #C, rejeita em (q8, D); se #P < #C, rejeita em (q10, C).
3. Compare #E com #D: se #E > #D, rejeita em (q13, >); se #E < #D, rejeita em (q15, D).
4. Caso contrário, aceita em (q15, >).

## Limite da fita: *n* células + 2 marcadores

- O simulador aloca `fita = [<] + w + [>]`, com exatamente *n* + 2 células e nenhuma outra estrutura
  de memória que cresça com a entrada. Estado, posição do cabeçote e contador de passos são finitos
  ou só servem para o rastreamento.
- **Células graváveis:** apenas 1…*n*. Nelas, a única escrita que muda o símbolo é
  maiúscula → minúscula (`P→p`, `C→c`, `E→e`, `D→d`).
- **Marcadores:** toda transição que lê `<` ou `>` reescreve o próprio marcador. Os movimentos são:

| Lê | Transições | Movimento |
|---|---|---|
| `<` | (q0,<), (q6,<), (q9,<), (q11,<), (q14,<) | sempre **R** (para dentro) |
| `>` | (q5,>) | **L** (para dentro) |
| `>` | (q15,>) | **S** (para em q_acc) |

  Não existe transição que mova para a esquerda sobre `<` nem para a direita sobre `>`. Por isso o
  cabeçote nunca sai do intervalo [0, *n*+1].
- O simulador também **verifica** isso a cada passo: lança erro se a tabela tentar sobrescrever um
  marcador ou mover o cabeçote para fora da fita. Nenhum teste dispara esse erro.
- Entrada vazia: fita `<>` (*n* = 0), `q0 → q1` e rejeição em (q1, `>`).

## Terminação e número de passos

- **Determinismo:** cada par (estado, símbolo) tem no máximo uma transição. Não há alternativas
  para explorar.
- **Potencial que só diminui:** nenhuma transição troca minúscula por maiúscula. Cada volta das
  fases 2 e 4 converte duas maiúsculas em minúsculas, então há no máximo *n*/2 voltas de marcação.
- **Cada passada é limitada:** as passadas de formato e de conferência (q1–q5, q10, q15) só andam
  para a direita até um marcador ou até rejeitar. As voltas (q6, q9, q11, q14) só andam para a
  esquerda até `<`. Cada passada tem no máximo *n* + 1 passos.
- **Limite:** são no máximo 1 + #P + 1 + #E + 1 ≤ *n* + 3 viagens de ida e volta, com ≤ 2(*n*+1)
  passos cada:

$$\text{passos} \le 2(n+1)(n+3) = O(n^2)$$

  Esse limite foi verificado exaustivamente para **todas** as cadeias de Σ\* com até 12 símbolos
  (22.369.621 cadeias).

Passos medidos:

| Entrada | n | Decisão | Passos |
|---|---|---|---|
| `PECD` | 4 | aceita | 38 |
| `PPEEECCDDD` | 10 | aceita | 130 |
| `PPEEECCCDD` | 10 | rejeita (mais C que P) | 56 |
| `PPPPEEEEECCCCDDDDD` | 18 | aceita | 338 |
| `PPPPPEEEECCCCCDDDD` | 18 | aceita | 340 |

## Rastreamento

Comando (cenário 1 de integração; o ALL recebe `PPEEECCDDD`):

```bash
python -m src.main "[{}[{}]]{[]}#PPEEECCDDD" --trace
# ou só o ALL:
python -m src.main "PPEEECCDDD" --so all --trace
```

Cada linha mostra passo | estado | posição do cabeçote | fita, com a célula sob o cabeçote
entre colchetes. Trechos do rastreamento real (130 passos):

```
   0 | q0    | cab=0   | [<]PPEEECCDDD>                                  configuração inicial
   1 | q1    | cab=1   | <[P]PEEECCDDD>   (leu <, escreveu <, R)
 ... fase 1: confere o formato até o '>' (passos 1–11) e volta (12–22)
  11 | q5    | cab=11  | <PPEEECCDDD[>]   (leu D, escreveu D, R)
  12 | q6    | cab=10  | <PPEEECCDD[D]>   (leu >, escreveu >, L)
  22 | q6    | cab=0   | [<]PPEEECCDDD>   (leu P, escreveu P, L)
 ... fase 2, 1ª volta: marca P e C
  23 | q7    | cab=1   | <[P]PEEECCDDD>   (leu <, escreveu <, R)
  24 | q8    | cab=2   | <p[P]EEECCDDD>   (leu P, escreveu p, R)      P → p
  28 | q8    | cab=6   | <pPEEE[C]CDDD>   (leu E, escreveu E, R)
  29 | q9    | cab=5   | <pPEE[E]cCDDD>   (leu C, escreveu c, L)      C → c
 ... 2ª volta: marca o 2º P e o 2º C
  42 | q9    | cab=6   | <ppEEE[c]cDDD>   (leu C, escreveu c, L)
 ... fase 3: q7 encontra E (acabaram os P); q10 confere que não há C livre
  51 | q7    | cab=3   | <pp[E]EEccDDD>   (leu p, escreveu p, R)
  52 | q10   | cab=4   | <ppE[E]EccDDD>   (leu E, escreveu E, R)
  57 | q11   | cab=7   | <ppEEEc[c]DDD>   (leu D, escreveu D, L)
 ... fase 4: três voltas casando E com D
  68 | q13   | cab=4   | <ppe[E]EccDDD>   (leu E, escreveu e, R)      E → e
  73 | q14   | cab=7   | <ppeEEc[c]dDD>   (leu D, escreveu d, L)      D → d
 109 | q14   | cab=9   | <ppeeeccd[d]d>   (leu D, escreveu d, L)
 ... fase 5: q12 encontra c (acabaram os E); q15 confere que não há D livre
 124 | q12   | cab=6   | <ppeee[c]cddd>   (leu e, escreveu e, R)
 125 | q15   | cab=7   | <ppeeec[c]ddd>   (leu c, escreveu c, R)
 129 | q15   | cab=11  | <ppeeeccddd[>]   (leu d, escreveu d, R)
 130 | q_acc | cab=11  | <ppeeeccddd[>]   (leu >, escreveu >, S)      ACEITA
```

> No rastreamento, a coluna de movimento usa `R` = direita, `L` = esquerda e `S` = parado
> (as letras D/E não são usadas para movimento, pois são símbolos da fita).

Cenário 3 de integração (`[{}[{}]]{[]}#PPEEECCCDD`, ALL recebe `PPEEECCCDD`): depois de casar os
dois `P` com dois `C`, `q10` encontra o terceiro `C` ainda maiúsculo:

```
  ...
  55 | q10   | cab=7   | <ppEEEc[c]CDD>   (leu c, escreveu c, R)
  56 | q10   | cab=8   | <ppEEEcc[C]DD>   (leu c, escreveu c, R)
       sem transição para (q10, 'C') -> q_rej                      REJEITA (mais C que P)
```

## Diagrama do ALL

![Diagrama de estados do ALL, gerado da tabela `src/all/transicoes.py`. As arestas para `q_rej` foram omitidas: todo par (estado, símbolo) sem aresta vai para lá.](figuras/all_tb.png){ height=23cm }

# Implementação

## Linguagem e interface
Python 3.10+, sem dependências em tempo de execução (só `pytest` para os testes), com interface de
linha de comando. A decisão sai **só da execução das transições**: os simuladores leem as tabelas
em `src/ap/transicoes.py` e `src/all/transicoes.py` e não têm nenhuma regra da linguagem escrita à mão.
Se a tabela não tem transição para a configuração atual, a cadeia é rejeitada.

| Arquivo | Papel |
|---|---|
| `src/ap/transicoes.py` | estados, alfabetos, pilha e tabela δ do AP |
| `src/ap/automato_pilha.py` | executa a tabela, gera o rastreamento (estado, posição, pilha) |
| `src/all/transicoes.py` | estados, alfabetos, fita e tabela δ do ALL |
| `src/all/automato_linear.py` | executa a tabela sobre `< w >`, gera o rastreamento (estado, fita, cabeçote) |
| `src/main.py` | fluxo integrado AP → ALL e CLI |
| `src/erros.py` | erro de símbolo fora do alfabeto |

## Por que o programa termina para toda entrada
**Símbolo fora do alfabeto:** é detectado antes de qualquer transição, e o programa sai com erro (código 2).

**AP:** é determinístico (no máximo uma transição para cada configuração). Toda transição que lê
avança a posição; a única transição vazia sai de `q2`, que não tem transições vazias para si mesmo
e vai para `q1` ou `q3`, que só têm transições de leitura. Logo há no máximo duas transições por
símbolo, ou seja, no máximo 2n passos.

**ALL:** também determinístico. Cada volta dos laços `q7→q8→q9→q7` e `q12→q13→q14→q12` troca uma
letra maiúscula por minúscula, e nenhuma transição faz o contrário. Há no máximo n marcações, e cada
volta percorre no máximo n + 2 células, pois o cabeçote não sai dos marcadores. As passadas de formato
(`q1..q6`) e de conferência (`q10`, `q11`, `q15`) andam numa só direção até um marcador. O total é
O(n²) passos, e toda configuração sem transição na tabela vai para `q_rej`.

**Não determinismo:** não há. Por isso o simulador não precisa explorar caminhos alternativos:
uma configuração sem transição rejeita na hora.

## Verificação da implementação
`tests/test_implementacao.py` compara os simuladores com uma definição direta das linguagens em
**todas** as cadeias de até 7 símbolos (AP) e até 9 (ALL), e em 3000 cadeias aleatórias longas.
Também cobre os 3 cenários de integração e o erro de alfabeto.
Os testes oficiais pedidos no enunciado (8 + 8 por módulo, tabela de resultados) ficam com a Frente 4.

## Como instalar, executar e repetir os testes

Os comandos completos estão no `README.md` do repositório (<https://github.com/Gaalbu/validador-manifesto-carga>). Resumo:

```bash
git clone https://github.com/Gaalbu/validador-manifesto-carga.git
cd validador-manifesto-carga
python -m venv .venv            # ative o ambiente (ver README)
python -m pip install -r requirements.txt
python -m src.main "[{}[{}]]{[]}#PPEEECCDDD" --trace   # fluxo completo com rastreamento
python -m pytest -v                                       # todos os testes
```

Código de saída da CLI: `0` aceita, `1` rejeita, `2` símbolo fora do alfabeto.

# Testes

## Metodologia

Os resultados esperados foram definidos pelas linguagens formais, independentemente dos simuladores. Cada módulo tem pelo menos oito entradas aceitas e oito rejeitadas, distintas, com 18 ou mais símbolos e pertencentes ao seu alfabeto. Os casos-limite adicionais (entrada vazia e menor cadeia aceita) são intencionalmente menores que 18 símbolos.

Execução: `python -m pytest tests/test_frente4.py -v`. Para regenerar este relatório e os dados: `python -m tests.gerar_relatorio_frente4`.

As decisões abaixo são obtidas pela execução dos reconhecedores; a tabela não é preenchida com previsões. As tabelas foram geradas executando os reconhecedores no clone oficial do repositório (branch `main`); a suíte completa (`python -m pytest -v`) foi reexecutada no clone oficial em 25/11/2026, com 55 testes aprovados.

## AP — testes isolados

| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |
|-----|----------------------|----:|-------|-------|----------------|
| AP01 | `[{}[{}]]{[]}#PPEEECCDDD` | 23 | Aceita | Aceita | Aninhamento misto e blocos completos |
| AP02 | `[[[[[[[]]]]]]]#PECD` | 19 | Aceita | Aceita | Sete níveis de colchetes |
| AP03 | `{{{{{{{}}}}}}}#PECD` | 19 | Aceita | Aceita | Sete níveis de chaves |
| AP04 | `[]{}[]{}[]{}[]{}#PECD` | 21 | Aceita | Aceita | Blocos consecutivos |
| AP05 | `{[{}]}{[{}]}{[{}]}#PECD` | 23 | Aceita | Aceita | Tipos alternados e blocos consecutivos |
| AP06 | `[]#PPPPPEEEEECCCCCD` | 19 | Aceita | Aceita | Quantidades distintas são permitidas pelo AP |
| AP07 | `[{}[{}]]{[]}#PPEEECCCDD` | 23 | Aceita | Aceita | Dependência cruzada não é responsabilidade do AP |
| AP08 | `[{}]#PPPEEECCCDDDDD` | 19 | Aceita | Aceita | Bloco D mais longo |
| AP09 | `[{}[{]}]{[]}#PPEEECCDDD` | 23 | Rejeita | Rejeita | Fechamento de tipo incorreto |
| AP10 | `[[{}[{}]]{[]}#PPEEECCDDD` | 24 | Rejeita | Rejeita | Abertura sem fechamento antes de # |
| AP11 | `[{}[{}]]{[]}]#PPEEECCDDD` | 24 | Rejeita | Rejeita | Fechamento excedente |
| AP12 | `[{}[{}]]{[]}PPEEECCDDD` | 22 | Rejeita | Rejeita | Separador ausente |
| AP13 | `[{}[{}]]{[]}##PPEEECCDDD` | 24 | Rejeita | Rejeita | Separador duplicado |
| AP14 | `[{}[{}]]{[]}#PPCCCCDDDD` | 23 | Rejeita | Rejeita | Bloco E ausente |
| AP15 | `[{}[{}]]{[]}#PPCCEEEDDD` | 23 | Rejeita | Rejeita | Blocos fora de ordem |
| AP16 | `[{}[{}]]{[]}#PPEEECCDDDP` | 24 | Rejeita | Rejeita | Símbolo após o bloco D |
| AP17 | `[]#PECD` | 7 | Aceita | Aceita | Comprimento mínimo: 7 símbolos |
| AP18 | ε (vazia) | 0 | Rejeita | Rejeita | Entrada vazia |

## ALL — testes isolados

| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |
|-----|----------------------|----:|-------|-------|----------------|
| ALL01 | `PEEEEEEEECDDDDDDDD` | 18 | Aceita | Aceita | P=C=1; E=D=8 |
| ALL02 | `PPEEEEEEECCDDDDDDD` | 18 | Aceita | Aceita | P=C=2; E=D=7 |
| ALL03 | `PPPEEEEEECCCDDDDDD` | 18 | Aceita | Aceita | P=C=3; E=D=6 |
| ALL04 | `PPPPEEEEECCCCDDDDD` | 18 | Aceita | Aceita | P=C=4; E=D=5 |
| ALL05 | `PPPPPEEEECCCCCDDDD` | 18 | Aceita | Aceita | P=C=5; E=D=4 |
| ALL06 | `PPPPPPEEECCCCCCDDD` | 18 | Aceita | Aceita | P=C=6; E=D=3 |
| ALL07 | `PPPPPPPEECCCCCCCDD` | 18 | Aceita | Aceita | P=C=7; E=D=2 |
| ALL08 | `PPPPPPPPECCCCCCCCD` | 18 | Aceita | Aceita | P=C=8; E=D=1 |
| ALL09 | `PPPPPEEEEECCCCDDDDD` | 19 | Rejeita | Rejeita | P excedente: P > C |
| ALL10 | `PPPPEEEEECCCCCDDDDD` | 19 | Rejeita | Rejeita | C excedente: P < C |
| ALL11 | `PPPPPEEEEECCCCCDDDD` | 19 | Rejeita | Rejeita | E excedente: E > D |
| ALL12 | `PPPPPEEEECCCCCDDDDD` | 19 | Rejeita | Rejeita | D excedente: E < D |
| ALL13 | `EEEEEECCCCCCDDDDDD` | 18 | Rejeita | Rejeita | Bloco P ausente |
| ALL14 | `PPPPPPCCCCCCDDDDDD` | 18 | Rejeita | Rejeita | Bloco E ausente |
| ALL15 | `PPPPPPEEEEEEDDDDDD` | 18 | Rejeita | Rejeita | Bloco C ausente |
| ALL16 | `PPPPPPEEEEEECCCCCC` | 18 | Rejeita | Rejeita | Bloco D ausente |
| ALL17 | `PECD` | 4 | Aceita | Aceita | Comprimento mínimo: 4 símbolos |
| ALL18 | ε (vazia) | 0 | Rejeita | Rejeita | Entrada vazia |
| ALL19 | `PPPPPCCCCCEEEEEDDDDD` | 20 | Rejeita | Rejeita | Quantidades iguais, ordem incorreta |

## Integração

| ID | Entrada | Tam. | Esperado (AP / ALL) | Obtido (AP / ALL) | Regra verificada |
|-----|----------------------|----:|-------|-------|----------------|
| INT01 | `[{}[{}]]{[]}#PPEEECCDDD` | 23 | Aceita / Aceita | Aceita / Aceita | Estrutura e dependências válidas |
| INT02 | `[{}[{]}]{[]}#PPEEECCDDD` | 23 | Rejeita / Não executado | Rejeita / Não executado | AP rejeita; ALL não pode executar |
| INT03 | `[{}[{}]]{[]}#PPEEECCCDD` | 23 | Aceita / Rejeita | Aceita / Rejeita | Estrutura válida, P != C e E != D |

## Símbolo fora do alfabeto

Entrada: `[{}[{}]]{[]}#PPEEExCCDDD` (24 símbolos).

Esperado: código de saída 2 e mensagem identificando o símbolo `x` e sua posição (índice começando em zero).

Obtido: código de saída 2.

```text
Erro: símbolo 'x' na posição 18 não pertence ao alfabeto de entrada { # C D E P [ ] { } }
```

# Análise dos resultados e limitação observada


41 de 41 casos de decisão coincidiram com o esperado (18 do AP, 19 do ALL, 3 de integração e 1 erro). A suíte automatizada acrescenta verificações de cobertura e crescimento, além de conferir a fita e o rastreamento durante os testes.

O AP aceita estruturas bem formadas mesmo quando as quantidades não correspondem; a responsabilidade de comparar P/C e E/D é do ALL. Na integração, uma rejeição do AP impede a chamada ao ALL, e uma rejeição do ALL torna o manifesto inválido mesmo com a estrutura correta.

### Crescimento do número de transições do ALL

Foram executados lotes válidos, mantendo P=C e E=D e aproximadamente a mesma quantidade de cada símbolo. A contagem é retornada pelo próprio simulador.

| Símbolos do lote | Passos do ALL | Configurações registradas |
|---:|---:|---:|
| 18 | 338 | 339 |
| 36 | 1158 | 1159 |
| 72 | 4254 | 4255 |
| 144 | 16278 | 16279 |

**Limitação:** o ALL precisa realizar sucessivas varreduras para marcar e casar símbolos. Nas entradas válidas testadas, o número de passos cresce aproximadamente de forma quadrática. Além disso, o simulador guarda uma representação da fita em cada passo, inclusive quando a opção `--trace` não é solicitada; o histórico de diagnóstico pode consumir O(n³) espaço no pior caso. Isso não altera o limite da memória de trabalho do modelo formal, que permanece em n células graváveis e dois marcadores fixos. Uma melhoria seria tornar o registro opcional ou emitir cada configuração sem acumular o histórico.

Os testes oferecem evidências de funcionamento nos casos escolhidos; não constituem uma prova de corretude para todas as cadeias.

Além dos 41 casos oficiais, a suíte `tests/test_implementacao.py` compara os simuladores com uma
definição direta das linguagens em **todas** as cadeias de até 7 símbolos (AP) e até 9 símbolos (ALL)
e em 3000 cadeias aleatórias longas, e as Frentes 1 e 2 conferiram por força bruta a GLC contra o AP
(até 16 símbolos) e o limite de passos do ALL (todas as cadeias até 12 símbolos). A suíte completa
foi reexecutada no clone oficial do repositório em 25/11/2026: **55 testes aprovados**.

Em número de passos, o AP é linear (no máximo 2|w|) e o ALL é quadrático (no máximo
2(n+1)(n+3)), o que confirma na prática a diferença entre usar uma pilha (cada símbolo é visto uma
vez) e usar a própria fita como memória (cada par casado exige uma ida e volta).

# Contribuição de cada integrante

| Integrante | Frente | Contribuição | Parte na apresentação |
|---|---|---|---|
| Alberto | 1 | GLC, prova de que a linguagem do AP não é regular, derivação, especificação e justificativa do AP (L(M) = L(G)), diagrama e script de conferência `verificar_ap.py` | GLC ↔ AP, derivação e rastreamento do AP |
| Davi Maciel Corrêa | 2 e 5 | linguagem sensível ao contexto, prova de que não é livre de contexto, gramática monotônica, especificação do ALL, limite da fita e diagrama; montagem do relatório, slides e checklist de entrega (assumiu a Frente 5) | abertura (problema) e ALL com rastreamento |
| Gabriel Albuquerque Alencar | 3 | estrutura do repositório, simuladores do AP e do ALL dirigidos por tabela, fluxo integrado, CLI, tratamento de símbolo fora do alfabeto e argumento de terminação | implementação e demonstração ao vivo |
| José Valdez | 4 | casos oficiais de teste, testes automatizados, tabela de resultados, README (instalação, execução e testes) e análise da limitação observada | testes e limitação observada |
| Jorge Lobato | 5 (inicial) | responsável inicial pela Frente 5; não pôde concluí-la, e a frente foi assumida por Davi | — |

Cada integrante apresenta uma parte técnica, e todos se prepararam para a arguição individual:
relação GLC ↔ AP, justificativa da regra do ALL e do limite da fita (n + 2 células) e previsão da
decisão para uma cadeia nova (roteiros nas seções de rastreamento do AP e de condições de aceitação
do ALL).

# Origem do código, dos diagramas e dos exemplos; uso de IA

- **Código-fonte** (`src/`): escrito pela equipe; os simuladores leem as tabelas de transição em
  `src/ap/transicoes.py` e `src/all/transicoes.py`, sem regras da linguagem escritas à mão.
- **Diagramas**: gerados pelos scripts `docs/modelagem/gerar_diagrama_ap.py` e
  `gerar_diagrama_all.py`, que leem as mesmas tabelas usadas pelos simuladores e escrevem arquivos
  `.dot` renderizados com o Graphviz (neste relatório, com orientação vertical:
  `dot -Grankdir=TB`). Por isso, diagrama e código não podem divergir.
- **Exemplos e casos de teste**: `exemplos/integracao.txt`, `exemplos/casos_frente4.tsv` e
  `tests/casos_frente4.py`, elaborados pela equipe a partir das definições formais das linguagens.
- **Derivação, contagens e rastreamentos** reproduzidos neste relatório foram gerados ou conferidos
  executando o código do repositório.

**Uso de inteligência artificial** (também registrado no `README.md`):

| Ferramenta | Tarefas apoiadas |
|---|---|
| Claude (Anthropic) | estrutura do repositório e divisão por frentes; primeira versão dos simuladores, das tabelas de transição e de `tests/test_implementacao.py`; consolidação deste relatório e dos slides (Frente 5) |
| ChatGPT (OpenAI) | elaboração dos casos oficiais, testes automatizados, tabelas de resultados, análise do crescimento de passos e revisão das instruções de execução |

As provas, tabelas e decisões foram conferidas pela equipe executando o código e os scripts de
verificação (seção de testes). Os testes mostram o funcionamento nos casos escolhidos e nas
verificações exaustivas por comprimento; a corretude para todas as cadeias é sustentada pelas
justificativas formais das seções de modelagem.
