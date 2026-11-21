"""Simulador do autômato linearmente limitado, dirigido pela tabela em `transicoes.py`."""
from dataclasses import dataclass, field

from src.erros import SimboloForaDoAlfabeto
from src.all import transicoes as T

_MOV = {T.L: "E", T.R: "D", T.S: "-"}


@dataclass
class Resultado:
    aceita: bool
    motivo: str
    passos: int = 0
    rastro: list[str] = field(default_factory=list)


def _fita_com_cabecote(fita: list[str], cab: int) -> str:
    return "".join(f"[{s}]" if i == cab else s for i, s in enumerate(fita))


def reconhecer(cadeia: str) -> Resultado:
    for i, s in enumerate(cadeia):
        if s not in T.ALFABETO:
            raise SimboloForaDoAlfabeto(s, i, T.ALFABETO)

    # n células graváveis + 2 marcadores fixos; nada além disso é alocado
    fita = [T.BORDA_ESQ, *cadeia, T.BORDA_DIR]
    estado, cab, n = T.ESTADO_INICIAL, 0, 0
    rastro = [f"{0:>4} | {estado:<5} | cab={cab:<3} | {_fita_com_cabecote(fita, cab)}"]

    while estado not in (T.ACEITA, T.REJEITA):
        lido = fita[cab]
        chave = (estado, lido)
        if chave not in T.TRANSICOES:
            rastro.append(f"     sem transição para ({estado}, '{lido}') -> {T.REJEITA}")
            return Resultado(False, f"sem transição para ({estado}, '{lido}'): {T.ESTADOS[estado]}", n, rastro)
        novo, escrito, mov = T.TRANSICOES[chave]
        if lido in (T.BORDA_ESQ, T.BORDA_DIR) and escrito != lido:
            raise AssertionError("a tabela tenta sobrescrever um marcador de borda")
        fita[cab] = escrito
        cab += mov
        if not 0 <= cab < len(fita):
            raise AssertionError("o cabeçote saiu dos marcadores de borda")
        estado = novo
        n += 1
        rastro.append(
            f"{n:>4} | {estado:<5} | cab={cab:<3} | {_fita_com_cabecote(fita, cab)}"
            f"   (leu {lido}, escreveu {escrito}, {_MOV[mov]})"
        )

    if estado == T.ACEITA:
        return Resultado(True, "todos os P casaram com C e todos os E com D", n, rastro)
    return Resultado(False, "rejeitada", n, rastro)
