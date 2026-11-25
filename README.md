# Validador de manifesto de carga — AP + ALL

Trabalho prático AV2 de Linguagens Formais e Autômatos (Prof. Daniel Leal Souza).

Validação em duas etapas:
1. **Autômato de pilha (AP)** verifica a estrutura definida por uma GLC: delimitadores `[]` e `{}` bem aninhados, seguidos de `#` e quatro blocos não vazios na ordem P, E, C, D.
2. **Autômato linearmente limitado (ALL)** verifica a dependência sensível ao contexto: P e C têm a mesma quantidade; E e D têm a mesma quantidade.

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

Requer Python 3.10+ e Git. Execute na raiz do repositório:

```bash
git clone https://github.com/Gaalbu/validador-manifesto-carga.git
cd validador-manifesto-carga
python -m venv .venv
```

Ative o ambiente virtual conforme o terminal:

- Windows (PowerShell): `.venv\Scripts\Activate.ps1`
- Windows (CMD): `.venv\Scripts\activate.bat`
- Linux/macOS: `source .venv/bin/activate`

```bash
python -m pip install -r requirements.txt
```

## Executar
```bash
python -m src.main "[{}[{}]]{[]}#PPEEECCDDD"
python -m src.main "[{}[{}]]{[]}#PPEEECCDDD" --trace
python -m src.main "[{}[{]}]{[]}#PPEEECCDDD" --so ap --trace
python -m src.main "PPPPEEEEECCCCDDDDD" --so all --trace
```

Código de saída: `0` aceita, `1` rejeita, `2` símbolo fora do alfabeto.

Cenários de integração (em `exemplos/integracao.txt`):

| Entrada | AP | ALL |
|---|---|---|
| `[{}[{}]]{[]}#PPEEECCDDD` | aceita | aceita |
| `[{}[{]}]{[]}#PPEEECCDDD` | rejeita | não executa |
| `[{}[{}]]{[]}#PPEEECCCDD` | aceita | rejeita |

Exemplo de erro de alfabeto:

```bash
python -m src.main "[{}[{}]]{[]}#PPEEExCCDDD"
```

## Testes

Suíte oficial da Frente 4:

```bash
python -m pytest tests/test_frente4.py -v
```

Todas as suítes (incluindo os testes exaustivos preexistentes da implementação; podem demorar mais):

```bash
python -m pytest -v
```

Regenerar a tabela de resultados e o arquivo de exemplos:

```bash
python -m tests.gerar_relatorio_frente4
```

- [`tests/casos_frente4.py`](tests/casos_frente4.py): entradas e decisões esperadas.
- [`tests/test_frente4.py`](tests/test_frente4.py): testes automatizados.
- [`docs/relatorio/testes.md`](docs/relatorio/testes.md): resultados e limitação.
- [`exemplos/casos_frente4.tsv`](exemplos/casos_frente4.tsv): entradas, decisões e motivos em formato tabular.

## Uso de inteligência artificial
- **Ferramenta:** Claude (Anthropic).
- **Tarefas apoiadas:** estrutura do repositório e divisão por frentes; primeira versão dos simuladores, das tabelas de transição e de `tests/test_implementacao.py`.
- **Ferramenta:** ChatGPT (OpenAI).
- **Tarefas apoiadas:** elaboração dos casos oficiais, testes automatizados, geração das tabelas de resultados, análise do crescimento de passos e revisão das instruções de execução.
- **Verificação realizada com apoio da IA:** execução dos testes oficiais numa cópia local do código consultado no GitHub, conferência de decisões esperadas e obtidas, limites da fita, fluxo de integração e mensagem de erro.
- **Verificação da equipe:** antes da entrega, reexecutar os testes no clone oficial, conferir o relatório e os rastreamentos e registrar aqui o que foi efetivamente revisado pelos integrantes.

## Equipe
<!-- nomes completos e contribuição de cada integrante -->
