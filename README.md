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
| `src/`, `docs/implementacao.md` | simuladores, tabelas de transição, CLI, terminação | 3 |
| `tests/`, `exemplos/` | testes e cadeias de exemplo | 4 |
| `docs/relatorio/`, `docs/slides/` | relatório e apresentação | 5 |

## Instalar
Requer Python 3.10+.
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Executar
```bash
python -m src.main "[{}[{}]]{[]}#PPEEECCDDD"            # fluxo completo
python -m src.main "[{}[{}]]{[]}#PPEEECCDDD" --trace    # com rastreamento dos dois autômatos
python -m src.main "[{}[{]}]{[]}#PPEEECCDDD" --so ap    # só o AP
python -m src.main "PPPPEEEEECCCCDDDDD" --so all --trace # só o ALL
```
Código de saída: `0` aceita, `1` rejeita, `2` símbolo fora do alfabeto.

Cenários de integração (em `exemplos/integracao.txt`):

| Entrada | AP | ALL |
|---|---|---|
| `[{}[{}]]{[]}#PPEEECCDDD` | aceita | aceita |
| `[{}[{]}]{[]}#PPEEECCDDD` | rejeita | não executa |
| `[{}[{}]]{[]}#PPEEECCCDD` | aceita | rejeita |

## Testes
```bash
python -m pytest -v
```

## Uso de inteligência artificial
- **Ferramenta:** Claude (Anthropic).
- **Tarefas apoiadas:** estrutura do repositório e divisão por frentes; primeira versão dos simuladores,
  das tabelas de transição e de `tests/test_implementacao.py`.
- **O que a equipe verificou:** <!-- Frente 4: preencher (ex.: conferência manual das tabelas, rastreamentos, testes) -->

## Equipe
<!-- nomes completos e contribuição de cada integrante -->
