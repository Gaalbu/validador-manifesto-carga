"""Frente 3 — verificação da implementação.

Compara os simuladores com uma definição direta (de referência) das linguagens em TODAS as
cadeias curtas do alfabeto e em cadeias aleatórias longas. Os testes oficiais do enunciado
(8 aceitas + 8 rejeitadas por módulo, integração, tabela) ficam com a Frente 4.
"""
import itertools
import random
import re

import pytest

from src.ap import automato_pilha as ap
from src.all import automato_linear as lba
from src.erros import SimboloForaDoAlfabeto
from src.main import validar


def ref_ap(w: str) -> bool:
    if w.count("#") != 1:
        return False
    x, y = w.split("#")
    if not x or not re.fullmatch(r"P+E+C+D+", y):
        return False
    pilha = []
    for s in x:
        if s not in "[]{}":
            return False
        if s in "[{":
            pilha.append(s)
        elif not pilha or pilha.pop() != {"]": "[", "}": "{"}[s]:
            return False
    return not pilha


def ref_all(w: str) -> bool:
    m = re.fullmatch(r"(P+)(E+)(C+)(D+)", w)
    return bool(m) and len(m[1]) == len(m[3]) and len(m[2]) == len(m[4])


def test_ap_todas_as_cadeias_curtas():
    for k in range(0, 8):
        for t in itertools.product("[]{}#PECD", repeat=k):
            w = "".join(t)
            assert ap.reconhecer(w).aceita == ref_ap(w), w


def test_all_todas_as_cadeias_curtas():
    for k in range(0, 10):
        for t in itertools.product("PECD", repeat=k):
            w = "".join(t)
            assert lba.reconhecer(w).aceita == ref_all(w), w


def _aleatoria_ap(rng):
    def bloco(d):
        a, f = rng.choice([("[", "]"), ("{", "}")])
        dentro = "".join(bloco(d + 1) for _ in range(rng.randint(0, 2))) if d < 4 else ""
        return a + dentro + f
    x = "".join(bloco(0) for _ in range(rng.randint(1, 3)))
    y = "".join(c * rng.randint(1, 5) for c in "PECD")
    w = x + "#" + y
    if rng.random() < 0.5:  # perturba
        i = rng.randrange(len(w))
        w = w[:i] + rng.choice("[]{}#PECD") + w[i + 1:]
    return w


def test_aleatorias():
    rng = random.Random(2026)
    for _ in range(3000):
        w = _aleatoria_ap(rng)
        assert ap.reconhecer(w).aceita == ref_ap(w), w
        n, m = rng.randint(1, 8), rng.randint(1, 8)
        v = "P" * n + "E" * m + "C" * (n + rng.choice([0, 0, 1, -1])) + "D" * (m + rng.choice([0, 0, 1, -1]))
        assert lba.reconhecer(v).aceita == ref_all(v), v


@pytest.mark.parametrize("entrada, ap_ok, all_ok", [
    ("[{}[{}]]{[]}#PPEEECCDDD", True, True),
    ("[{}[{]}]{[]}#PPEEECCDDD", False, None),
    ("[{}[{}]]{[]}#PPEEECCCDD", True, False),
])
def test_tres_cenarios_de_integracao(entrada, ap_ok, all_ok):
    r = validar(entrada)
    assert r["ap"].aceita == ap_ok
    assert (r["all"].aceita if r["all"] else None) == all_ok


def test_simbolo_fora_do_alfabeto():
    with pytest.raises(SimboloForaDoAlfabeto, match="'x' na posição 3"):
        validar("[{}x]#PECD")
    with pytest.raises(SimboloForaDoAlfabeto):
        lba.reconhecer("PE#CD")


def test_all_usa_so_n_mais_2_celulas_e_termina_em_tempo_quadratico():
    w = "P" * 30 + "E" * 25 + "C" * 30 + "D" * 25
    r = lba.reconhecer(w)
    assert r.aceita
    assert r.passos <= 2 * (len(w) + 2) ** 2
