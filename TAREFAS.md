# Divisão do trabalho por frentes — AV2 LFA (AP + ALL)

> Entrega: **25/11 (CC6NA) ou 27/11 (CC6MA)**, antes do início da aula. Apresentação no mesmo dia.
> Trocar `Membro 1..5` pelos nomes reais.

## ⚠️ Antes de tudo
O enunciado diz: **"Equipes de 1 a 4 integrantes. Equipes com mais de 4 integrantes não serão permitidas."**
Com 5 pessoas, falar com o professor **já** (ou dividir em 4 + 1). A frente 5 cuida disso no dia 1.

## Problema proposto (a confirmar com a equipe)
**Validador de manifesto de carga** — entrada `ESTRUTURA#LOTE`.

- **AP (GLC):** antes do `#`, uma estrutura de containers aninhados com dois tipos de delimitador,
  `[ ]` (palete) e `{ }` (caixa), bem aninhados e não vazia; depois do `#`, um lote no formato
  `P+ E+ C+ D+` (pedido, envio, confirmação, devolução). Dyck com 2 tipos não é regular (lema do bombeamento regular).
- **ALL (sensível ao contexto):** no trecho após `#`, verifica a **dependência cruzada**
  `P^n E^m C^n D^m` (nº de pedidos = nº de confirmações **e** nº de envios = nº de devoluções).
  `{aⁿbᵐcⁿdᵐ}` não é livre de contexto (lema do bombeamento para LLC — Sipser, Hopcroft/Ullman).
  É diferente do exemplo do professor (três blocos iguais).

Exemplos (≥ 18 caracteres):
- `[{}[{}]]{[]}#PPEEECCDDD` → AP aceita, ALL aceita
- `[{}[{]}]{[]}#PPEEECCDDD` → AP rejeita (aninhamento errado), ALL não roda
- `[{}[{}]]{[]}#PPEEECCCDD` → AP aceita, ALL rejeita (P≠C e E≠D)

Requisito: **AP e ALL com no mínimo 8 estados cada.**

---

> **Atualização:** as tabelas de transição do AP (`src/ap/transicoes.py`, 9 estados) e do ALL
> (`src/all/transicoes.py`, 16 estados + aceita/rejeita) já estão implementadas e verificadas.
> As Frentes 1 e 2 agora **documentam e justificam** essas tabelas (e propõem mudanças, se acharem
> melhor; a Frente 3 ajusta o código).

## Frente 1 — GLC + Autômato de Pilha (modelagem formal)
**Responsável:** Membro 1 · **Pasta:** `docs/modelagem/ap.md`
- [ ] Alfabeto, regra de formação e GLC (V, Σ, P, S)
- [ ] Argumento de que a linguagem **não é regular** (bombeamento)
- [ ] Derivação completa de uma cadeia aceita (≥ 18 caracteres) — será mostrada na apresentação
- [ ] AP: estados (≥ 8), Σ, Γ, configuração inicial, tabela de transições, critério de aceitação (estado final ou pilha vazia, consumindo toda a entrada)
- [ ] Justificativa: por que o AP reconhece exatamente L(GLC)
- [ ] Diagrama do AP (indicar origem: feito pela equipe / ferramenta)
- [ ] Transcrever/revisar a tabela de `src/ap/transicoes.py` em formato de relatório

## Frente 2 — Linguagem sensível ao contexto + ALL (modelagem formal)
**Responsável:** Membro 2 · **Pasta:** `docs/modelagem/all.md`
- [ ] Alfabeto e regra de aceitação
- [ ] Prova/referência de que a linguagem **não é livre de contexto** (bombeamento para LLC) e de que é sensível ao contexto
- [ ] ALL: estados (≥ 8), alfabeto de entrada e da fita, marcadores de borda `<` `>`, config. inicial, transições (lê/escreve/move), aceitação e rejeição
- [ ] Mostrar que usa só **n células + 2 marcadores** (sem fita extra)
- [ ] Diagrama do ALL
- [ ] Transcrever/revisar a tabela de `src/all/transicoes.py` em formato de relatório

## Frente 3 — Implementação dos simuladores ✅
**Responsável:** Gabriel · **Pastas:** `src/`, `docs/implementacao.md`
- [x] Simulador do AP dirigido pela tabela de transições (não "if" ad hoc): rastreamento com estado, posição de leitura e pilha
- [x] Simulador do ALL: rastreamento com estado, fita e posição do cabeçote; cabeçote não passa das bordas
- [x] Fluxo integrado: AP → (se aceitar) ALL sobre o trecho após `#`
- [x] Erro claro para símbolo fora do alfabeto
- [x] Texto curto: **por que o programa termina** para toda entrada; se houver não determinismo, como explora alternativas e quando rejeita
- [x] CLI simples (`python -m src.main "<cadeia>" --trace`)

## Frente 4 — Testes + README/reprodutibilidade
**Responsável:** Membro 4 · **Pastas:** `tests/`, `exemplos/`, `README.md`
- [ ] AP: ≥ 8 aceitas + ≥ 8 rejeitadas, distintas, com caso-limite (vazia / mínima)
- [ ] ALL: ≥ 8 aceitas + ≥ 8 rejeitadas, distintas, com caso-limite
- [ ] Integração: 3 cenários (aceita/aceita · AP rejeita · AP aceita e ALL rejeita)
- [ ] Teste com símbolo fora do alfabeto (registrar a mensagem)
- [ ] Tabela de resultados: entrada | esperado | obtido | regra verificada (`docs/relatorio/testes.md`)
- [ ] README: instalar, executar, rodar testes; seção de **uso de IA** (ferramenta, tarefas, o que foi verificado)
- [ ] Levantar **uma limitação observada nos testes** (cobrada na apresentação)

## Frente 5 — Slides, entrega e "o que mais falta" (menor parte)
**Responsável:** Membro 5 · **Pastas:** `docs/slides/`, `docs/relatorio/`
- [ ] **Dia 1:** resolver a questão dos 5 integrantes com o professor
- [ ] **Dia 1:** abrir a **rubrica completa** no Classroom (o PDF diz que ela está lá) e listar aqui qualquer exigência que não esteja neste arquivo
- [ ] Ver comentários da turma/particulares e confirmar data da turma (CC6NA 25/11 ou CC6MA 27/11)
- [ ] Montar o relatório (juntar textos das frentes): problema, fontes, modelos, derivação, justificativas, testes, análise, **contribuição de cada um**, origem de código/diagramas
- [ ] Slides (≤ 15 min): problema → GLC/AP + derivação → ALL → demo dos 3 cenários → limitação; **uma parte técnica por integrante**
- [ ] Checklist de entrega: relatório PDF, slides PDF/PPTX, link do GitHub, nomes completos; os demais marcam entrega com o mesmo link; repo acessível ao professor

---

## Para todos (arguição = 1,20 pt individual)
Cada um precisa saber, sem ler: relação GLC ↔ AP, por que a regra do ALL é sensível ao contexto,
o limite da fita (n + 2), e **prever a decisão para uma cadeia nova** seguindo as transições.
Ensaio geral no dia 24.

## Cronograma
| Dia | Marco |
|---|---|
| 21 (sáb) | Problema fechado · questão dos 5 resolvida · rubrica lida |
| 22 (dom) | Tabelas de transição do AP e do ALL prontas |
| 23 (seg) | Simuladores rodando com rastreamento · testes escritos |
| 24 (ter) | Relatório + slides prontos · ensaio com arguição simulada |
| 25 (qua) | Postar antes da aula (se CC6NA) |
