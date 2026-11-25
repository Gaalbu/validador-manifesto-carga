# Frente 5 — Slides

- [`apresentacao.pptx`](apresentacao.pptx) (editável) e [`apresentacao.pdf`](apresentacao.pdf) (para o Classroom).
- 17 slides, ≈ 14 min + arguição. As notas do apresentador (no `.pptx`) trazem o que falar em cada slide e o tempo.

| Slides | Apresenta | Parte técnica |
|---|---|---|
| 1–4 | Davi | problema, as duas etapas e a hierarquia de Chomsky |
| 5–9 | Alberto | GLC, prova de não regularidade, AP, relação GLC ↔ AP, derivação e rastreamento do AP |
| 10–12 | Davi | linguagem sensível ao contexto, fases do ALL, rastreamento da fita e limite n + 2 |
| 13–14 | Gabriel | implementação dirigida por tabela, terminação e **demonstração ao vivo** |
| 15–16 | José | testes (41/41, 55 no pytest) e limitação observada |
| 17 | Davi | encerramento; roteiro para prever a decisão (fica na tela na arguição) |

## Demonstração ao vivo (slide 14)

Na raiz do repositório, com o ambiente ativado:

```bash
python -m src.main "[{}[{}]]{[]}#PPEEECCDDD" --trace   # AP aceita, ALL aceita
python -m src.main "[{}[{]}]{[]}#PPEEECCDDD" --trace   # AP rejeita, ALL não executa
python -m src.main "[{}[{}]]{[]}#PPEEECCCDD" --trace   # AP aceita, ALL rejeita
python -m src.main "[{}[{}]]{[]}#PPEEExCCDDD"          # erro de alfabeto, código 2
```

No PowerShell, as aspas duplas funcionam como acima. O rastreamento do cenário 1 é longo (ALL com 130 passos): role até as fases de marcação ou rode `--so all --trace` com `PPEEECCDDD`.
