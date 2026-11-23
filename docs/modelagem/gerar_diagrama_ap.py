"""Gera o diagrama do AP (Graphviz) a partir da tabela em src/ap/transicoes.py.

Uso (na raiz do repositório):
    python docs/modelagem/gerar_diagrama_ap.py
    dot -Tsvg docs/modelagem/ap_diagrama.dot -o docs/modelagem/ap_diagrama.svg
    dot -Tpng -Gdpi=150 docs/modelagem/ap_diagrama.dot -o docs/modelagem/ap_diagrama.png

Rótulos: "a, Z / γ" = lê a com Z no topo, troca Z por γ (γ = ε desempilha).
Várias linhas no mesmo rótulo = uma transição para cada linha, entre os mesmos estados.
"""
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from src.ap import transicoes as T  # noqa: E402

ORDEM = "[{]}#PECD"

grupos: dict[tuple[str, str], list[tuple[str, str, str]]] = defaultdict(list)
for (q, lido, topo), (novo, empilha) in T.TRANSICOES.items():
    grupos[(q, novo)].append((lido, topo, empilha))


def chave(t: tuple[str, str, str]) -> tuple[int, str]:
    lido, topo, _ = t
    return (ORDEM.index(lido) if lido else -1, topo)


linhas = [
    "digraph AP {",
    '  rankdir=LR; nodesep=0.5; ranksep=0.7;',
    '  node [shape=circle, fontname="Helvetica", fontsize=12, width=0.6, fixedsize=true];',
    '  edge [fontname="Helvetica", fontsize=10];',
    '  inicio [shape=point, width=0.08];',
    *(f"  {q} [shape=doublecircle];" for q in sorted(T.ESTADOS_FINAIS)),
    f"  inicio -> {T.ESTADO_INICIAL};",
]
for (q, novo), ts in sorted(grupos.items(), key=lambda kv: (int(kv[0][0][1:]), int(kv[0][1][1:]))):
    rot = "\\n".join(f"{lido or 'ε'}, {topo} / {emp or 'ε'}" for lido, topo, emp in sorted(ts, key=chave))
    linhas.append(f'  {q} -> {novo} [label="{rot}"];')
linhas += [
    '  nota [shape=note, fixedsize=false, fontsize=10, label="a, Z / γ: lê a com Z no topo e troca Z por γ\\n'
    '(topo é o 1º símbolo de γ; γ = ε desempilha).\\n'
    'Pilha: Z = fundo, X = [ aberto, Y = { aberto.\\n'
    'Par ausente = sem transição = rejeita.\\n'
    'Aceita: entrada consumida em q8."];',
    "}",
]

saida = Path(__file__).with_name("ap_diagrama.dot")
saida.write_text("\n".join(linhas) + "\n", encoding="utf-8")
print(f"gerado: {saida.relative_to(RAIZ)}")
