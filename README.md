# Validador de manifesto de carga — AP + ALL

Trabalho prático AV2 de Linguagens Formais e Autômatos (Prof. Daniel Leal Souza).

Validação em duas etapas:
1. **Autômato de pilha (AP)** verifica a estrutura definida por uma GLC.
2. **Autômato linearmente limitado (ALL)** verifica uma dependência sensível ao contexto.

Divisão do trabalho: [`TAREFAS.md`](TAREFAS.md).

## Estrutura
| Pasta | Conteúdo | Frente |
|---|---|---|
| `docs/modelagem/ap.md` | GLC, derivação, especificação do AP | 1 |
| `docs/modelagem/all.md` | linguagem sensível ao contexto, especificação do ALL | 2 |
| `src/` | simuladores e CLI | 3 |
| `tests/`, `exemplos/` | testes e cadeias de exemplo | 4 |
| `docs/relatorio/`, `docs/slides/` | relatório e apresentação | 5 |

## Instalar
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Executar
```bash
python -m src.main "[{}[{}]]{[]}#PPEEECCDDD" --trace
```

## Testes
```bash
python -m pytest -v
```

## Uso de inteligência artificial
<!-- Frente 4: ferramenta usada, tarefas apoiadas e o que a equipe verificou -->

## Equipe
<!-- nomes completos e contribuição de cada integrante -->
