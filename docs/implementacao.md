# Frente 3 — Implementação

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

## AP — resumo (detalhar na Frente 1)
- 9 estados `q0..q8`, Σ = `[ ] { } # P E C D`, Γ = `Z X Y`, início `(q0, Z)`.
- Abre `[` → empilha `X`; abre `{` → empilha `Y`; fecha → desempilha o par correspondente.
- `q2` só tem transições vazias: olha o topo para saber se voltou ao nível externo (`Z` → `q3`)
  ou se ainda está dentro de um bloco (`X`/`Y` → `q1`).
- Depois do `#`, `q4..q8` conferem `P+E+C+D+` com a pilha parada em `Z`.
- **Aceitação por estado final** (`q8`) com a entrada inteira consumida.

## ALL — resumo (detalhar na Frente 2)
- 16 estados de trabalho `q0..q15` + `q_acc` e `q_rej`. Σ = `P E C D`, Γ = `P E C D p e c d < >`.
- Fita = `<` + as n células da entrada + `>`. Nenhuma célula extra.
- `q1..q5` conferem o formato; `q7..q9` marcam um P e um C por volta; `q10..q11` conferem que não
  sobrou C; `q12..q14` marcam um E e um D por volta; `q15` confere que não sobrou D e aceita em `>`.
- Nos marcadores, a tabela só move para dentro (ou para em `>`) e reescreve o próprio marcador;
  o simulador também verifica isso a cada passo.

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
