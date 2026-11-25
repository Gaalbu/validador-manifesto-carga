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

No Windows, `exemplos\demo_windows.bat` (dois cliques) roda os três cenários de integração, o erro de alfabeto e um rastreamento de cada autômato.

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
- **Ferramenta:** Claude (Anthropic) — Frente 5.
- **Tarefas apoiadas:** consolidação do relatório técnico a partir dos textos das frentes (`docs/relatorio/relatorio.pdf`), slides da apresentação (`docs/slides/`), troca dos rótulos de movimento do rastreamento do ALL para `R`/`L`/`S` e atualização do `TAREFAS.md`.
- **Verificação da equipe:** suíte completa reexecutada no clone oficial em 25/11/2026 (`python -m pytest -v` → 55 aprovados) e os três cenários de integração e o erro de alfabeto conferidos pela CLI. <!-- cada integrante: acrescentar aqui o que revisou pessoalmente -->

## Equipe

Turma CC6NA — Linguagens Formais e Autômatos — Prof. Daniel Leal Souza.

| Integrante | Frente | Contribuição | Parte na apresentação |
|---|---|---|---|
| Alberto Eduardo Acosta | 1 | GLC, prova de não regularidade, derivação, especificação e justificativa do AP, diagrama e `verificar_ap.py` | GLC ↔ AP, derivação e rastreamento do AP |
| Davi Maciel Corrêa | 2 | linguagem sensível ao contexto, prova de não ser LLC, gramática monotônica, especificação do ALL, limite da fita e diagrama | abertura (problema) e ALL com rastreamento |
| Gabriel Albuquerque Alencar | 3 | estrutura do repositório, simuladores dirigidos por tabela, fluxo integrado, CLI e argumento de terminação | implementação e demonstração ao vivo |
| José Joaquim Valdez | 4 | casos oficiais, testes automatizados, tabela de resultados, README e análise da limitação | testes e limitação observada |
| Jorge Lobato Gonçalves | 5 | relatório técnico consolidado, slides da apresentação, organização da demonstração e checklist de entrega | — |

Relatório: [`docs/relatorio/relatorio.pdf`](docs/relatorio/relatorio.pdf) · Slides: [`docs/slides/apresentacao.pdf`](docs/slides/apresentacao.pdf) ([`.pptx`](docs/slides/apresentacao.pptx)).
