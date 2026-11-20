"""Frente 3 — simulador do ALL. Transições vêm da tabela da Frente 2 (docs/modelagem/all.md).

Fita = marcador esquerdo + n células + marcador direito. O cabeçote nunca sai dessas bordas.
Cada passo do rastreamento deve registrar: estado, fita e posição do cabeçote.
"""

def reconhecer(cadeia: str, rastrear: bool = False) -> tuple[bool, list[str]]:
    raise NotImplementedError("Frente 3: implementar a partir da tabela de transições do ALL")
