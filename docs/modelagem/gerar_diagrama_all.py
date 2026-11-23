"""Gera o diagrama do ALL (Graphviz) a partir da tabela em src/all/transicoes.py.

Uso (na raiz do repositório):
    python docs/modelagem/gerar_diagrama_all.py
    dot -Tsvg docs/modelagem/all_diagrama.dot -o docs/modelagem/all_diagrama.svg
    dot -Tpng -Gdpi=150 docs/modelagem/all_diagrama.dot -o docs/modelagem/all_diagrama.png

Rótulos: "x / R" = lê x, reescreve x, move à direita; "x→y / L" = lê x, escreve y, move à esquerda.
Vários símbolos separados por vírgula = uma aresta para cada símbolo, com a mesma ação.
"""
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from src.all import transicoes as T  # noqa: E402

MOV = {T.L: "L", T.R: "R", T.S: "S"}
ORDEM = "<PECDpecd>"

grupos: dict[tuple[str, str], dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
for (q, lido), (novo, escrito, mov) in T.TRANSICOES.items():
    acao = f"{lido}→{escrito}" if escrito != lido else lido
    grupos[(q, novo)][MOV[mov]].append(acao)

linhas = [
    "digraph ALL {",
    '  rankdir=LR; nodesep=0.35; ranksep=0.55;',
    '  node [shape=circle, fontname="Helvetica", fontsize=12, width=0.6, fixedsize=true];',
    '  edge [fontname="Helvetica", fontsize=10];',
    '  inicio [shape=point, width=0.08];',
    f'  {T.ACEITA} [shape=doublecircle, label="q_acc", width=0.75];',
    f'  {T.REJEITA} [shape=circle, style=dashed, label="q_rej", width=0.75];',
    '  inicio -> q0;',
]
for (q, novo), por_mov in sorted(grupos.items(), key=lambda kv: (int(kv[0][0][1:]), kv[0][1])):
    partes = []
    for mov, acoes in sorted(por_mov.items()):
        acoes.sort(key=lambda a: ORDEM.index(a[0]))
        partes.append(f"{','.join(acoes)} / {mov}")
    linhas.append(f'  {q} -> {novo} [label="{chr(10).join(partes)}"];'.replace(chr(10), "\\n"))
linhas += [
    '  nota [shape=note, fixedsize=false, fontsize=10, label="Qualquer par (estado, símbolo)\\n'
    'sem aresta vai para q_rej.\\nR = direita, L = esquerda, S = parado.\\n'
    'x→y: lê x, escreve y; x sozinho: reescreve x."];',
    f'  nota -> {T.REJEITA} [style=dotted, arrowhead=none];',
    "}",
]

saida = Path(__file__).with_name("all_diagrama.dot")
saida.write_text("\n".join(linhas) + "\n", encoding="utf-8")
print(f"gerado: {saida.relative_to(RAIZ)}")
