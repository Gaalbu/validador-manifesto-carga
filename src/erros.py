class SimboloForaDoAlfabeto(ValueError):
    def __init__(self, simbolo: str, posicao: int, alfabeto) -> None:
        self.simbolo, self.posicao = simbolo, posicao
        permitidos = " ".join(sorted(alfabeto))
        super().__init__(
            f"Erro: símbolo '{simbolo}' na posição {posicao} não pertence ao alfabeto de entrada {{ {permitidos} }}"
        )
