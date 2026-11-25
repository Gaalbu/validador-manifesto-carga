"""Monta docs/relatorio/relatorio.md a partir dos textos das frentes e gera o PDF.

Execute da raiz do repositório:
    python docs/relatorio/montar_relatorio.py          # só o .md
    python docs/relatorio/montar_relatorio.py --pdf    # .md + .pdf (requer pandoc e xelatex)

As seções de modelagem, implementação e testes são copiadas de:
    docs/modelagem/ap.md, docs/modelagem/all.md, docs/implementacao.md, docs/relatorio/testes.md
Edite esses arquivos (não o relatorio.md) e rode o script de novo.
"""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
REL = RAIZ / "docs" / "relatorio"
GH = "https://github.com/Gaalbu/validador-manifesto-carga"
GH_BLOB = GH + "/blob/main/"

# Nomes completos da equipe (usados na capa e na seção de contribuição).
EQUIPE = [
    # (nome, frente, contribuição, parte na apresentação)
    ("Alberto", "1",
     "GLC, prova de que a linguagem do AP não é regular, derivação, especificação e justificativa "
     "do AP (L(M) = L(G)), diagrama e script de conferência `verificar_ap.py`",
     "GLC ↔ AP, derivação e rastreamento do AP"),
    ("Davi Maciel Corrêa", "2 e 5",
     "linguagem sensível ao contexto, prova de que não é livre de contexto, gramática monotônica, "
     "especificação do ALL, limite da fita e diagrama; montagem do relatório, slides e checklist "
     "de entrega (assumiu a Frente 5)",
     "abertura (problema) e ALL com rastreamento"),
    ("Gabriel Albuquerque Alencar", "3",
     "estrutura do repositório, simuladores do AP e do ALL dirigidos por tabela, fluxo integrado, "
     "CLI, tratamento de símbolo fora do alfabeto e argumento de terminação",
     "implementação e demonstração ao vivo"),
    ("José Valdez", "4",
     "casos oficiais de teste, testes automatizados, tabela de resultados, README "
     "(instalação, execução e testes) e análise da limitação observada",
     "testes e limitação observada"),
    ("Jorge Lobato", "5 (inicial)",
     "responsável inicial pela Frente 5; não pôde concluí-la, e a frente foi assumida por Davi",
     "—"),
]


def ler(rel: str) -> str:
    return (RAIZ / rel).read_text(encoding="utf-8")


def secoes(texto: str) -> dict:
    """Divide um .md pelos títulos '## ' e devolve {número ou título: corpo com o título}."""
    partes = re.split(r"(?m)^(?=## )", texto)
    out = {}
    for p in partes[1:]:
        titulo = p.splitlines()[0][3:].strip()
        m = re.match(r"(\d+)\.", titulo)
        out[m.group(1) if m else titulo] = p
    return out


def ajustar(texto: str, origem: str, nivel_extra: int = 0) -> str:
    """Rebaixa títulos, tira a numeração manual, remove imagens/réguas e corrige links relativos."""
    base = (RAIZ / origem).parent

    def titulo(m):
        hashes, resto = m.group(1), m.group(2)
        resto = re.sub(r"^\d+(\.\d+)*\.?\s+", "", resto)
        return "#" * (len(hashes) + nivel_extra) + " " + resto

    texto = re.sub(r"(?m)^(#{2,6}) (.*)$", titulo, texto)
    texto = re.sub(r"(?m)^!\[.*\]\(.*\)\s*$\n?", "", texto)
    texto = re.sub(r"(?m)^---\s*$\n?", "", texto)

    def link(m):
        rotulo, alvo = m.group(1), m.group(2)
        if alvo.startswith(("http", "#", "mailto:")):
            return m.group(0)
        caminho = (base / alvo.split("#")[0]).resolve().relative_to(RAIZ).as_posix()
        return f"[{rotulo}]({GH_BLOB}{caminho})"

    texto = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", link, texto)
    texto = texto.replace("∎", "■")
    # larguras relativas das tabelas de testes (pandoc usa a quantidade de traços)
    texto = texto.replace("|---|---|---:|---|---|---|",
                          "|-----|----------------------|----:|-------|-------|----------------|")
    return texto.strip() + "\n"


def pegar(sec: dict, chaves, origem, nivel_extra=0) -> str:
    return "\n".join(ajustar(sec[k], origem, nivel_extra) for k in chaves)


def montar() -> str:
    ap = secoes(ler("docs/modelagem/ap.md"))
    lba = secoes(ler("docs/modelagem/all.md"))
    imp = secoes(ler("docs/implementacao.md"))
    tst = secoes(ler("docs/relatorio/testes.md"))

    autores = "\n".join(f"  - {n}" for n, *_ in EQUIPE)
    capa = f"""---
title: "Validador de manifesto de carga: autômato de pilha + autômato linearmente limitado"
subtitle: "Relatório técnico — Atividade Prática AV2 de Linguagens Formais e Autômatos"
author:
{autores}
date: "CESUPA — Ciência da Computação — Turma CC6NA — Prof. Daniel Leal Souza — 25/11/2026"
toc: true
toc-depth: 2
numbersections: true
---

**Repositório:** <{GH}>

"""

    problema = f"""# Problema

Um centro de distribuição recebe **manifestos de carga** como cadeias no formato `ESTRUTURA#LOTE`.

- A **estrutura** descreve como os volumes estão acondicionados: um **palete** `[ ]` pode conter
  caixas e outros paletes, e uma **caixa** `{{ }}` pode conter paletes e outras caixas, mas os volumes
  não podem se cruzar (`[{{]}}` é inválido). A estrutura não pode ser vazia.
- O **lote** registra os eventos do manifesto em quatro blocos não vazios, nessa ordem:
  **P**edidos, **E**nvios, **C**onfirmações e **D**evoluções.

O manifesto é validado em duas etapas:

1. **Autômato de pilha (AP)** — verifica a estrutura definida por uma GLC: estrutura bem aninhada e
   não vazia, um único `#` e o lote no formato `P+E+C+D+`.
2. **Autômato linearmente limitado (ALL)** — executado só se o AP aceitar, sobre o trecho após o `#`:
   verifica a **dependência cruzada** "todo pedido tem confirmação e todo envio tem devolução", isto
   é, nº de `P` = nº de `C` **e** nº de `E` = nº de `D`.

| Manifesto (23 símbolos) | AP | ALL | Por quê |
|------------------------------|---------|-------------|------------------------------|
| `[{{}}[{{}}]]{{[]}}#PPEEECCDDD` | aceita | aceita | estrutura válida; 2 P = 2 C e 3 E = 3 D |
| `[{{}}[{{]}}]{{[]}}#PPEEECCDDD` | rejeita | não executa | `]` fecha com uma caixa `{{` aberta no topo |
| `[{{}}[{{}}]]{{[]}}#PPEEECCCDD` | aceita | rejeita | estrutura válida, mas 2 P ≠ 3 C e 3 E ≠ 2 D |

O problema difere do exemplo da lauda em dois pontos: a estrutura usa **dois tipos** de delimitador
(e não só parênteses), e a regra sensível ao contexto é uma dependência **cruzada** entre pares de
blocos (P↔C e E↔D, intercalados), e não "três blocos com a mesma quantidade". Os dois autômatos foram
modelados pela equipe para este problema: o AP tem **9 estados** e o ALL tem **16 estados de trabalho
+ aceitação + rejeição (18)**.

| Etapa | Linguagem | Classe na hierarquia de Chomsky |
|---|---|---|
| AP | L_AP = {{ x#y : x ∈ {{[,],{{,}}}}⁺ bem aninhada, y ∈ P⁺E⁺C⁺D⁺ }} | livre de contexto (determinística), **não regular** |
| ALL | L_ALL = {{ PⁿEᵐCⁿDᵐ : n, m ≥ 1 }} | sensível ao contexto, **não livre de contexto** |

# Fontes consultadas

- SIPSER, M. *Introdução à Teoria da Computação*. 2. ed. São Paulo: Cengage Learning, 2007.
  Seções 1.4 (linguagens não regulares e lema do bombeamento), 2.1–2.2 (GLC e autômatos com pilha),
  2.3 (linguagens não livres do contexto) e 5.1 (autômatos linearmente limitados).
- HOPCROFT, J. E.; MOTWANI, R.; ULLMAN, J. D. *Introdução à Teoria de Autômatos, Linguagens e
  Computação*. 2. ed. Rio de Janeiro: Campus/Elsevier, 2002. Seção 4.1 (bombeamento para linguagens
  regulares), capítulos 5 e 6 (GLC, ambiguidade, autômatos de pilha, aceitação por estado final ×
  pilha vazia, APD) e seção 7.2 (bombeamento para LLC; exemplo {{0ⁱ1ʲ2ⁱ3ʲ}}).
- MENEZES, P. B. *Linguagens Formais e Autômatos*. 6. ed. Porto Alegre: Bookman, 2011. Capítulos
  sobre linguagens livres do contexto, autômato com pilha, linguagens sensíveis ao contexto e
  autômato com fita limitada.
- KURODA, S.-Y. Classes of languages and linear-bounded automata. *Information and Control*, v. 7,
  n. 2, p. 207–223, 1964.
- Documentação do Python 3 (<https://docs.python.org/3/>), do pytest (<https://docs.pytest.org/>) e
  do Graphviz (<https://graphviz.org/documentation/>), usados na implementação, nos testes e nos
  diagramas.

"""

    sec_ap = "# Linguagem livre de contexto e autômato de pilha\n\n" + pegar(
        ap, [str(i) for i in range(1, 10)], "docs/modelagem/ap.md")
    sec_ap += """
## Diagrama do AP

![Diagrama de estados do AP, gerado da tabela `src/ap/transicoes.py`. Rótulo `a, t / γ`: lê *a* (ou ε) com *t* no topo e troca *t* por γ. Pares ausentes não têm transição (rejeita).](figuras/ap_tb.png){ height=23.5cm }
"""

    sec_all = "# Linguagem sensível ao contexto e autômato linearmente limitado\n\n" + pegar(
        lba, [str(i) for i in range(1, 9)], "docs/modelagem/all.md")
    sec_all += """
## Diagrama do ALL

![Diagrama de estados do ALL, gerado da tabela `src/all/transicoes.py`. As arestas para `q_rej` foram omitidas: todo par (estado, símbolo) sem aresta vai para lá.](figuras/all_tb.png){ height=23cm }
"""

    sec_imp = "# Implementação\n\n" + pegar(
        imp, ["Linguagem e interface", "Por que o programa termina para toda entrada",
              "Verificação da implementação"], "docs/implementacao.md")
    sec_imp += f"""
## Como instalar, executar e repetir os testes

Os comandos completos estão no `README.md` do repositório (<{GH}>). Resumo:

```bash
git clone {GH}.git
cd validador-manifesto-carga
python -m venv .venv            # ative o ambiente (ver README)
python -m pip install -r requirements.txt
python -m src.main "[{{}}[{{}}]]{{[]}}#PPEEECCDDD" --trace   # fluxo completo com rastreamento
python -m pytest -v                                       # todos os testes
```

Código de saída da CLI: `0` aceita, `1` rejeita, `2` símbolo fora do alfabeto.
"""

    testes_secs = [k for k in tst if k != "Análise e limitação observada"]
    sec_testes = "# Testes\n\n" + pegar(tst, testes_secs, "docs/relatorio/testes.md")
    sec_analise = "# Análise dos resultados e limitação observada\n\n" + ajustar(
        tst["Análise e limitação observada"], "docs/relatorio/testes.md").split("\n", 1)[1]
    sec_analise += """
Além dos 41 casos oficiais, a suíte `tests/test_implementacao.py` compara os simuladores com uma
definição direta das linguagens em **todas** as cadeias de até 7 símbolos (AP) e até 9 símbolos (ALL)
e em 3000 cadeias aleatórias longas, e as Frentes 1 e 2 conferiram por força bruta a GLC contra o AP
(até 16 símbolos) e o limite de passos do ALL (todas as cadeias até 12 símbolos). A suíte completa
foi reexecutada no clone oficial do repositório em 25/11/2026: **55 testes aprovados**.

Em número de passos, o AP é linear (no máximo 2|w|) e o ALL é quadrático (no máximo
2(n+1)(n+3)), o que confirma na prática a diferença entre usar uma pilha (cada símbolo é visto uma
vez) e usar a própria fita como memória (cada par casado exige uma ida e volta).
"""

    linhas = ["| Integrante | Frente | Contribuição | Parte na apresentação |", "|---|---|---|---|"]
    linhas += [f"| {n} | {f} | {c} | {a} |" for n, f, c, a in EQUIPE]
    sec_contrib = "# Contribuição de cada integrante\n\n" + "\n".join(linhas) + """

Cada integrante apresenta uma parte técnica, e todos se prepararam para a arguição individual:
relação GLC ↔ AP, justificativa da regra do ALL e do limite da fita (n + 2 células) e previsão da
decisão para uma cadeia nova (roteiros nas seções de rastreamento do AP e de condições de aceitação
do ALL).
"""

    sec_origem = """# Origem do código, dos diagramas e dos exemplos; uso de IA

- **Código-fonte** (`src/`): escrito pela equipe; os simuladores leem as tabelas de transição em
  `src/ap/transicoes.py` e `src/all/transicoes.py`, sem regras da linguagem escritas à mão.
- **Diagramas**: gerados pelos scripts `docs/modelagem/gerar_diagrama_ap.py` e
  `gerar_diagrama_all.py`, que leem as mesmas tabelas usadas pelos simuladores e escrevem arquivos
  `.dot` renderizados com o Graphviz (neste relatório, com orientação vertical:
  `dot -Grankdir=TB`). Por isso, diagrama e código não podem divergir.
- **Exemplos e casos de teste**: `exemplos/integracao.txt`, `exemplos/casos_frente4.tsv` e
  `tests/casos_frente4.py`, elaborados pela equipe a partir das definições formais das linguagens.
- **Derivação, contagens e rastreamentos** reproduzidos neste relatório foram gerados ou conferidos
  executando o código do repositório.

**Uso de inteligência artificial** (também registrado no `README.md`):

| Ferramenta | Tarefas apoiadas |
|---|---|
| Claude (Anthropic) | estrutura do repositório e divisão por frentes; primeira versão dos simuladores, das tabelas de transição e de `tests/test_implementacao.py`; consolidação deste relatório e dos slides (Frente 5) |
| ChatGPT (OpenAI) | elaboração dos casos oficiais, testes automatizados, tabelas de resultados, análise do crescimento de passos e revisão das instruções de execução |

As provas, tabelas e decisões foram conferidas pela equipe executando o código e os scripts de
verificação (seção de testes). Os testes mostram o funcionamento nos casos escolhidos e nas
verificações exaustivas por comprimento; a corretude para todas as cadeias é sustentada pelas
justificativas formais das seções de modelagem.
"""

    corpo = "\n".join([problema, sec_ap, sec_all, sec_imp, sec_testes, sec_analise,
                       sec_contrib, sec_origem])
    aviso = ("<!-- Arquivo gerado por docs/relatorio/montar_relatorio.py — edite as fontes "
             "(docs/modelagem, docs/implementacao.md, docs/relatorio/testes.md) e rode o script. -->\n\n")
    return capa + aviso + corpo


CABECALHO_TEX = r"""
\usepackage{fvextra}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,breakanywhere,commandchars=\\\{\},fontsize=\footnotesize}
\RecustomVerbatimEnvironment{verbatim}{Verbatim}{breaklines,breakanywhere,fontsize=\footnotesize}
\usepackage{etoolbox}
\AtBeginEnvironment{longtable}{\small}
\setlength{\emergencystretch}{3em}
\AtBeginDocument{\renewcommand{\contentsname}{Sumário}\renewcommand{\figurename}{Figura}\renewcommand{\tablename}{Tabela}}
"""


def gerar_pdf(md: Path) -> None:
    tex = REL / "_cabecalho.tex"
    tex.write_text(CABECALHO_TEX, encoding="utf-8")
    try:
        subprocess.run([
            "pandoc", md.name, "-o", "relatorio.pdf",
            "--pdf-engine=xelatex", "-H", tex.name,
            "-V", "geometry:margin=2.2cm", "-V", "fontsize=11pt", "-V", "papersize=a4",
            "-V", "mainfont=DejaVu Serif", "-V", "sansfont=DejaVu Sans",
            "-V", "monofont=DejaVu Sans Mono", "-V", "mathfont=DejaVu Math TeX Gyre",
            "-V", "colorlinks=true", "-V", "linkcolor=blue", "-V", "urlcolor=blue",
            "-V", "toccolor=black",
        ], cwd=REL, check=True)
    finally:
        tex.unlink(missing_ok=True)


if __name__ == "__main__":
    md = REL / "relatorio.md"
    md.write_text(montar(), encoding="utf-8")
    print(f"escrito {md.relative_to(RAIZ)}")
    if "--pdf" in sys.argv:
        gerar_pdf(md)
        print("escrito docs/relatorio/relatorio.pdf")
