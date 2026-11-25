"""Casos oficiais: expectativas derivadas das regras formais, não do simulador."""

BASE = "[{}[{}]]{[]}"
LOTE = "PPEEECCDDD"

# (id, entrada, aceita, regra verificada)
AP = [
    ("AP01", BASE + "#" + LOTE, True, "Aninhamento misto e blocos completos"),
    ("AP02", "["*7 + "]"*7 + "#PECD", True, "Sete níveis de colchetes"),
    ("AP03", "{"*7 + "}"*7 + "#PECD", True, "Sete níveis de chaves"),
    ("AP04", "[]{}"*4 + "#PECD", True, "Blocos consecutivos"),
    ("AP05", "{[{}]}"*3 + "#PECD", True, "Tipos alternados e blocos consecutivos"),
    ("AP06", "[]#PPPPPEEEEECCCCCD", True, "Quantidades distintas são permitidas pelo AP"),
    ("AP07", BASE + "#PPEEECCCDD", True, "Dependência cruzada não é responsabilidade do AP"),
    ("AP08", "[{}]#PPPEEECCCDDDDD", True, "Bloco D mais longo"),
    ("AP09", "[{}[{]}]{[]}#" + LOTE, False, "Fechamento de tipo incorreto"),
    ("AP10", "[" + BASE + "#" + LOTE, False, "Abertura sem fechamento antes de #"),
    ("AP11", BASE + "]#" + LOTE, False, "Fechamento excedente"),
    ("AP12", BASE + LOTE, False, "Separador ausente"),
    ("AP13", BASE + "##" + LOTE, False, "Separador duplicado"),
    ("AP14", BASE + "#PPCCCCDDDD", False, "Bloco E ausente"),
    ("AP15", BASE + "#PPCCEEEDDD", False, "Blocos fora de ordem"),
    ("AP16", BASE + "#" + LOTE + "P", False, "Símbolo após o bloco D"),
    ("AP17", "[]#PECD", True, "Comprimento mínimo: 7 símbolos"),
    ("AP18", "", False, "Entrada vazia"),
]

def lote(n, m, c, d):
    return "P"*n + "E"*m + "C"*c + "D"*d

ALL = [
    (f"ALL{i:02}", lote(n,m,n,m), True, f"P=C={n}; E=D={m}")
    for i, (n,m) in enumerate([(1,8),(2,7),(3,6),(4,5),(5,4),(6,3),(7,2),(8,1)], 1)
] + [
    ("ALL09", lote(5,5,4,5), False, "P excedente: P > C"),
    ("ALL10", lote(4,5,5,5), False, "C excedente: P < C"),
    ("ALL11", lote(5,5,5,4), False, "E excedente: E > D"),
    ("ALL12", lote(5,4,5,5), False, "D excedente: E < D"),
    ("ALL13", lote(0,6,6,6), False, "Bloco P ausente"),
    ("ALL14", lote(6,0,6,6), False, "Bloco E ausente"),
    ("ALL15", lote(6,6,0,6), False, "Bloco C ausente"),
    ("ALL16", lote(6,6,6,0), False, "Bloco D ausente"),
    ("ALL17", "PECD", True, "Comprimento mínimo: 4 símbolos"),
    ("ALL18", "", False, "Entrada vazia"),
    ("ALL19", "P"*5 + "C"*5 + "E"*5 + "D"*5, False, "Quantidades iguais, ordem incorreta"),
]

# (id, entrada, AP esperado, ALL esperado, regra)
INTEGRACAO = [
    ("INT01", BASE + "#" + LOTE, True, True, "Estrutura e dependências válidas"),
    ("INT02", "[{}[{]}]{[]}#" + LOTE, False, None, "AP rejeita; ALL não pode executar"),
    ("INT03", BASE + "#PPEEECCCDD", True, False, "Estrutura válida, P != C e E != D"),
]
INVALIDA = BASE + "#PPEEExCCDDD"
