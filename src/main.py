"""Fluxo integrado: AP primeiro; se aceitar, ALL no trecho após '#'.

Uso:
    python -m src.main "<cadeia>" [--trace]          fluxo completo
    python -m src.main "<cadeia>" --so ap [--trace]  só o AP
    python -m src.main "<cadeia>" --so all [--trace] só o ALL (alfabeto P E C D)
"""
import argparse
import sys

from src.erros import SimboloForaDoAlfabeto
from src.ap import automato_pilha as ap
from src.all import automato_linear as lba


def validar(cadeia: str) -> dict:
    """Retorna o resultado das duas etapas. O ALL só roda se o AP aceitar."""
    r_ap = ap.reconhecer(cadeia)
    if not r_ap.aceita:
        return {"ap": r_ap, "all": None, "aceita": False}
    lote = cadeia.split("#", 1)[1]
    r_all = lba.reconhecer(lote)
    return {"ap": r_ap, "all": r_all, "aceita": r_all.aceita}


def _imprimir(titulo: str, r, trace: bool) -> None:
    print(f"== {titulo}: {'ACEITA' if r.aceita else 'REJEITA'} — {r.motivo}")
    if trace:
        print("\n".join(r.rastro))
        print()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validador de manifesto de carga (AP + ALL)")
    p.add_argument("cadeia", help='ex.: "[{}[{}]]{[]}#PPEEECCDDD" (use "" para a cadeia vazia)')
    p.add_argument("--trace", action="store_true", help="mostra o rastreamento passo a passo")
    p.add_argument("--so", choices=["ap", "all"], help="executa só um dos reconhecedores")
    a = p.parse_args(argv)

    print(f"Entrada: {a.cadeia!r} ({len(a.cadeia)} símbolos)")
    try:
        if a.so == "ap":
            r = ap.reconhecer(a.cadeia)
            _imprimir("AP", r, a.trace)
            return 0 if r.aceita else 1
        if a.so == "all":
            r = lba.reconhecer(a.cadeia)
            _imprimir("ALL", r, a.trace)
            return 0 if r.aceita else 1

        res = validar(a.cadeia)
        _imprimir("AP", res["ap"], a.trace)
        if res["all"] is None:
            print("== ALL: não executado (o AP rejeitou)")
        else:
            lote = a.cadeia.split("#", 1)[1]
            print(f"   trecho enviado ao ALL: {lote!r}")
            _imprimir("ALL", res["all"], a.trace)
        print(f"DECISÃO FINAL: {'ACEITA' if res['aceita'] else 'REJEITA'}")
        return 0 if res["aceita"] else 1
    except SimboloForaDoAlfabeto as e:
        print(e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
