"""Confere a tabela do AP (src/ap/transicoes.py) contra a GLC e contra a definição da linguagem.

Uso (na raiz do repositório):
    python docs/modelagem/verificar_ap.py

Verificações:
  1. Força bruta: toda cadeia de Σ* com até FORCA_BRUTA símbolos -> AP aceita  <=>  definição.
  2. GLC = AP: o conjunto de cadeias geradas pela GLC com até N_GLC símbolos é igual ao conjunto
     aceito pelo AP com até N_GLC símbolos (o AP é explorado por busca em largura sobre as
     configurações; como ele é determinístico, isso enumera exatamente as cadeias aceitas).
  3. Determinismo: nenhum par (estado, topo) tem transição ε e de leitura ao mesmo tempo.
  4. Invariante da pilha: em toda configuração alcançada, a pilha tem a forma (X|Y)* Z.
  5. Número de passos: AP para em no máximo |w| + (nº de símbolos de fechamento) <= 2|w| passos.
"""
import itertools
import random
import sys
from collections import deque
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

from src.ap import transicoes as T  # noqa: E402
from src.ap.automato_pilha import reconhecer  # noqa: E402

FORCA_BRUTA = 7      # 9^7 ≈ 4,8 milhões de cadeias
N_GLC = 16
ALEATORIAS = 20000


# ---------- definição direta da linguagem (sem autômato) ----------
def bem_aninhado(x: str) -> bool:
    pilha = []
    par = {"]": "[", "}": "{"}
    for s in x:
        if s in "[{":
            pilha.append(s)
        elif s in "]}":
            if not pilha or pilha.pop() != par[s]:
                return False
        else:
            return False
    return not pilha


def lote_ok(y: str) -> bool:
    i = 0
    for letra in "PECD":
        j = i
        while j < len(y) and y[j] == letra:
            j += 1
        if j == i:
            return False
        i = j
    return i == len(y)


def definicao(w: str) -> bool:
    if w.count("#") != 1:
        return False
    x, y = w.split("#")
    return len(x) > 0 and bem_aninhado(x) and lote_ok(y)


# ---------- GLC: S -> B#L ; B -> A | AB ; A -> [] | [B] | {} | {B} ; L -> Ps Es Cs Ds ----------
GLC = {
    "S": [["B", "#", "L"]],
    "B": [["A"], ["A", "B"]],
    "A": [["[", "]"], ["[", "B", "]"], ["{", "}"], ["{", "B", "}"]],
    "L": [["Ps", "Es", "Cs", "Ds"]],
    "Ps": [["P"], ["P", "Ps"]],
    "Es": [["E"], ["E", "Es"]],
    "Cs": [["C"], ["C", "Cs"]],
    "Ds": [["D"], ["D", "Ds"]],
}
TERMINAIS = set("[]{}#PECD")


def gerar_glc(n_max: int) -> set[str]:
    """Todas as cadeias com até n_max símbolos geradas por derivações mais à esquerda.
    Toda variável gera ≥ 1 terminal, então formas sentenciais com mais de n_max símbolos são podadas."""
    geradas, vistos = set(), set()
    fila = deque([("S",)])
    while fila:
        forma = fila.popleft()
        i = next((k for k, s in enumerate(forma) if s not in TERMINAIS), None)
        if i is None:
            geradas.add("".join(forma))
            continue
        for corpo in GLC[forma[i]]:
            nova = forma[:i] + tuple(corpo) + forma[i + 1:]
            if len(nova) <= n_max and nova not in vistos:
                vistos.add(nova)
                fila.append(nova)
    return geradas


def aceitas_ap(n_max: int) -> set[str]:
    """Busca em largura nas configurações (estado, pilha, cadeia lida). Fecha ε antes de ler."""
    aceitas = set()
    fila = deque([(T.ESTADO_INICIAL, T.SIMBOLO_INICIAL_PILHA, "")])
    while fila:
        q, pilha, lido = fila.popleft()
        while (q, T.EPS, pilha[0]) in T.TRANSICOES:           # fecho ε (determinístico)
            q, emp = T.TRANSICOES[(q, T.EPS, pilha[0])]
            pilha = emp + pilha[1:]
        assert set(pilha[:-1]) <= {"X", "Y"} and pilha[-1] == "Z", pilha   # invariante
        if q in T.ESTADOS_FINAIS:
            aceitas.add(lido)
        if len(lido) == n_max:
            continue
        for s in sorted(T.ALFABETO):
            if (q, s, pilha[0]) in T.TRANSICOES:
                novo, emp = T.TRANSICOES[(q, s, pilha[0])]
                fila.append((novo, emp + pilha[1:], lido + s))
    return aceitas


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    # 3. determinismo
    for (q, a, z) in T.TRANSICOES:
        if a == T.EPS:
            assert not any((q, s, z) in T.TRANSICOES for s in T.ALFABETO), (q, z)
    print(f"determinismo: ok ({len(T.TRANSICOES)} transições, {len(T.ESTADOS)} estados)")

    # 2. GLC = AP
    g, a = gerar_glc(N_GLC), aceitas_ap(N_GLC)
    assert g == a, (sorted(g - a)[:5], sorted(a - g)[:5])
    assert all(definicao(w) for w in g)
    print(f"GLC = AP para |w| <= {N_GLC}: ok ({len(g)} cadeias); invariante da pilha: ok")

    # 1. força bruta contra a definição + 5. passos
    simb = sorted(T.ALFABETO)
    total = aceitas = 0
    for n in range(FORCA_BRUTA + 1):
        for t in itertools.product(simb, repeat=n):
            w = "".join(t)
            r = reconhecer(w)
            assert r.aceita == definicao(w), w
            passos = len(r.rastro) - 2
            assert passos <= 2 * len(w), (w, passos)
            total += 1
            aceitas += r.aceita
    print(f"força bruta |w| <= {FORCA_BRUTA}: ok ({total} cadeias, {aceitas} aceitas)")

    # cadeias longas aleatórias, com viés para quase-aceitas
    rnd = random.Random(2026)
    pool = sorted(g, key=len)[-2000:]
    for _ in range(ALEATORIAS):
        w = list(rnd.choice(pool)) * rnd.randint(1, 2)
        for _ in range(rnd.randint(0, 2)):
            op, i = rnd.random(), rnd.randrange(len(w))
            if op < 0.4:
                w[i] = rnd.choice(simb)
            elif op < 0.7:
                del w[i]
            else:
                w.insert(i, rnd.choice(simb))
        w = "".join(w)
        assert reconhecer(w).aceita == definicao(w), w
    print(f"{ALEATORIAS} cadeias aleatórias (até ~34 símbolos): ok")


if __name__ == "__main__":
    main()
