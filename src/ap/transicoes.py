"""Tabela de transições do autômato de pilha (AP).

Linguagem: L = { x # y | x é uma sequência não vazia de blocos bem aninhados com [ ] e { },
                         y pertence a P+ E+ C+ D+ }

GLC correspondente:
    S  -> B # L
    B  -> A | A B
    A  -> [ ] | [ B ] | { } | { B }
    L  -> Ps Es Cs Ds
    Ps -> P | P Ps      (idem para Es, Cs, Ds)

Pilha: Z = fundo, X = "[" aberto, Y = "{" aberto. Topo é o primeiro símbolo da string.
Aceitação por estado final (q8), com a entrada consumida por inteiro.
O AP é determinístico: q2 só tem transições vazias (ε), uma para cada topo possível.
"""

ALFABETO = frozenset("[]{}#PECD")
ALFABETO_PILHA = frozenset("ZXY")
ESTADO_INICIAL = "q0"
SIMBOLO_INICIAL_PILHA = "Z"
ESTADOS_FINAIS = frozenset({"q8"})
EPS = ""

ESTADOS = {
    "q0": "início: espera o primeiro bloco",
    "q1": "dentro de um bloco",
    "q2": "acabou de fechar um bloco: verifica o nível (ε)",
    "q3": "nível externo: abre outro bloco ou lê #",
    "q4": "leu #: espera P",
    "q5": "bloco de P",
    "q6": "bloco de E",
    "q7": "bloco de C",
    "q8": "bloco de D (final)",
}

# (estado, símbolo lido ou EPS, topo) -> (novo estado, string empilhada no lugar do topo)
TRANSICOES: dict[tuple[str, str, str], tuple[str, str]] = {
    ("q0", "[", "Z"): ("q1", "XZ"),
    ("q0", "{", "Z"): ("q1", "YZ"),

    ("q1", "[", "X"): ("q1", "XX"),
    ("q1", "[", "Y"): ("q1", "XY"),
    ("q1", "{", "X"): ("q1", "YX"),
    ("q1", "{", "Y"): ("q1", "YY"),
    ("q1", "]", "X"): ("q2", ""),
    ("q1", "}", "Y"): ("q2", ""),

    ("q2", EPS, "Z"): ("q3", "Z"),
    ("q2", EPS, "X"): ("q1", "X"),
    ("q2", EPS, "Y"): ("q1", "Y"),

    ("q3", "[", "Z"): ("q1", "XZ"),
    ("q3", "{", "Z"): ("q1", "YZ"),
    ("q3", "#", "Z"): ("q4", "Z"),

    ("q4", "P", "Z"): ("q5", "Z"),
    ("q5", "P", "Z"): ("q5", "Z"),
    ("q5", "E", "Z"): ("q6", "Z"),
    ("q6", "E", "Z"): ("q6", "Z"),
    ("q6", "C", "Z"): ("q7", "Z"),
    ("q7", "C", "Z"): ("q7", "Z"),
    ("q7", "D", "Z"): ("q8", "Z"),
    ("q8", "D", "Z"): ("q8", "Z"),
}
