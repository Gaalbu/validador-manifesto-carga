"""Simulador do autômato de pilha, dirigido pela tabela em `transicoes.py`."""
from dataclasses import dataclass, field

from src.erros import SimboloForaDoAlfabeto
from src.ap import transicoes as T


@dataclass
class Resultado:
    aceita: bool
    motivo: str
    rastro: list[str] = field(default_factory=list)


def _passo(n: int, estado: str, pos: int, cadeia: str, pilha: str, acao: str) -> str:
    restante = cadeia[pos:] or "ε"
    return f"{n:>4} | {estado:<3} | pos={pos:<3} | resta={restante:<28} | pilha={pilha:<12} | {acao}"


def reconhecer(cadeia: str) -> Resultado:
    for i, s in enumerate(cadeia):
        if s not in T.ALFABETO:
            raise SimboloForaDoAlfabeto(s, i, T.ALFABETO)

    estado, pos, pilha = T.ESTADO_INICIAL, 0, T.SIMBOLO_INICIAL_PILHA
    rastro = [_passo(0, estado, pos, cadeia, pilha, "configuração inicial")]
    n = 0
    while True:
        topo = pilha[0] if pilha else None
        if topo is None:
            return Resultado(False, f"pilha vazia em {estado}", rastro)

        # 1) transição vazia (só existe em q2, que não tem transições de leitura)
        if (estado, T.EPS, topo) in T.TRANSICOES:
            novo, empilha = T.TRANSICOES[(estado, T.EPS, topo)]
            lido = "ε"
        elif pos < len(cadeia) and (estado, cadeia[pos], topo) in T.TRANSICOES:
            novo, empilha = T.TRANSICOES[(estado, cadeia[pos], topo)]
            lido = cadeia[pos]
            pos += 1
        elif pos == len(cadeia):
            if estado in T.ESTADOS_FINAIS:
                rastro.append(f"     entrada consumida em {estado} (final) -> ACEITA")
                return Resultado(True, "entrada consumida em estado final", rastro)
            rastro.append(f"     entrada consumida em {estado} (não final) -> REJEITA")
            return Resultado(False, f"entrada terminou em {estado} ({T.ESTADOS[estado]})", rastro)
        else:
            s = cadeia[pos]
            rastro.append(f"     sem transição para ({estado}, '{s}', {topo}) -> REJEITA")
            return Resultado(False, f"sem transição para ({estado}, '{s}', {topo}) na posição {pos}", rastro)

        pilha = empilha + pilha[1:]
        n += 1
        estado = novo
        rastro.append(_passo(n, estado, pos, cadeia, pilha, f"leu {lido}, topo {topo} -> empilha {empilha or 'ε'}"))
