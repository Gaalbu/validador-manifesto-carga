"""Frente 3 — fluxo integrado: AP primeiro; se aceitar, ALL no trecho após '#'."""
import argparse


def main() -> None:
    p = argparse.ArgumentParser(description="Validador AP + ALL")
    p.add_argument("cadeia")
    p.add_argument("--trace", action="store_true")
    args = p.parse_args()
    raise NotImplementedError("Frente 3: validar alfabeto, rodar AP e depois ALL")


if __name__ == "__main__":
    main()
