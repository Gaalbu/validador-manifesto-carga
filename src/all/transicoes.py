"""Tabela de transições do autômato linearmente limitado (ALL).

Linguagem: L = { P^n E^m C^n D^m | n, m >= 1 }
(nº de pedidos = nº de confirmações E nº de envios = nº de devoluções — dependência cruzada).

Fita: <  w_1 ... w_n  >   (n células graváveis + 2 marcadores fixos).
Marcação: P->p, E->e, C->c, D->d. Nenhum outro símbolo é escrito.

Estratégia:
  q1..q5   conferem o formato P+E+C+D+ numa passada (e voltam pelo q6)
  q7..q9   casam cada P com um C (marca os dois e volta ao início)
  q10..q11 conferem que não sobrou C sem par
  q12..q14 casam cada E com um D
  q15      confere que não sobrou D sem par e aceita no marcador direito
Qualquer combinação (estado, símbolo) ausente da tabela leva a q_rej.
"""

ALFABETO = frozenset("PECD")
BORDA_ESQ, BORDA_DIR = "<", ">"
ALFABETO_FITA = frozenset("PECDpecd<>")
ESTADO_INICIAL = "q0"
ACEITA, REJEITA = "q_acc", "q_rej"
L, R, S = -1, +1, 0

ESTADOS = {
    "q0": "início sobre o marcador esquerdo",
    "q1": "formato: espera o primeiro P",
    "q2": "formato: bloco de P",
    "q3": "formato: bloco de E",
    "q4": "formato: bloco de C",
    "q5": "formato: bloco de D",
    "q6": "volta ao marcador esquerdo",
    "q7": "procura o próximo P não marcado",
    "q8": "procura o C correspondente",
    "q9": "volta ao início (par P/C marcado)",
    "q10": "confere que não sobrou C",
    "q11": "volta ao início",
    "q12": "procura o próximo E não marcado",
    "q13": "procura o D correspondente",
    "q14": "volta ao início (par E/D marcado)",
    "q15": "confere que não sobrou D",
    ACEITA: "aceita",
    REJEITA: "rejeita",
}


def _voltar(estado: str, proximo: str) -> dict:
    """Move à esquerda sobre qualquer símbolo até o marcador esquerdo; lá vai para `proximo`."""
    t = {(estado, s): (estado, s, L) for s in "PECDpecd"}
    t[(estado, BORDA_ESQ)] = (proximo, BORDA_ESQ, R)
    return t


# (estado, símbolo lido) -> (novo estado, símbolo escrito, movimento)
TRANSICOES: dict[tuple[str, str], tuple[str, str, int]] = {
    ("q0", "<"): ("q1", "<", R),
    # formato P+E+C+D+
    ("q1", "P"): ("q2", "P", R),
    ("q2", "P"): ("q2", "P", R),
    ("q2", "E"): ("q3", "E", R),
    ("q3", "E"): ("q3", "E", R),
    ("q3", "C"): ("q4", "C", R),
    ("q4", "C"): ("q4", "C", R),
    ("q4", "D"): ("q5", "D", R),
    ("q5", "D"): ("q5", "D", R),
    ("q5", ">"): ("q6", ">", L),
    **_voltar("q6", "q7"),
    # casa P com C
    ("q7", "p"): ("q7", "p", R),
    ("q7", "P"): ("q8", "p", R),
    ("q7", "E"): ("q10", "E", R),
    ("q8", "P"): ("q8", "P", R),
    ("q8", "E"): ("q8", "E", R),
    ("q8", "c"): ("q8", "c", R),
    ("q8", "C"): ("q9", "c", L),
    **_voltar("q9", "q7"),
    # nenhum C pode sobrar
    ("q10", "E"): ("q10", "E", R),
    ("q10", "c"): ("q10", "c", R),
    ("q10", "D"): ("q11", "D", L),
    **_voltar("q11", "q12"),
    # casa E com D
    ("q12", "p"): ("q12", "p", R),
    ("q12", "e"): ("q12", "e", R),
    ("q12", "E"): ("q13", "e", R),
    ("q12", "c"): ("q15", "c", R),
    ("q13", "E"): ("q13", "E", R),
    ("q13", "c"): ("q13", "c", R),
    ("q13", "d"): ("q13", "d", R),
    ("q13", "D"): ("q14", "d", L),
    **_voltar("q14", "q12"),
    # nenhum D pode sobrar
    ("q15", "c"): ("q15", "c", R),
    ("q15", "d"): ("q15", "d", R),
    ("q15", ">"): (ACEITA, ">", S),
}
