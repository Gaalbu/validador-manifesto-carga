# Frente 5 — Relatório técnico

- [`relatorio.pdf`](relatorio.pdf) — versão para o Classroom.
- [`relatorio.md`](relatorio.md) — gerado por [`montar_relatorio.py`](montar_relatorio.py) a partir de
  `docs/modelagem/ap.md`, `docs/modelagem/all.md`, `docs/implementacao.md` e `testes.md`.
  Para mudar o conteúdo dessas seções, edite as fontes e rode de novo:

```bash
python docs/relatorio/montar_relatorio.py          # só o .md
python docs/relatorio/montar_relatorio.py --pdf    # .md + .pdf (requer pandoc e xelatex)
```

Seções: problema · fontes consultadas · especificação dos modelos · derivação · justificativas ·
implementação e terminação · testes · análise dos resultados e limitação · contribuição de cada
integrante · origem de código, diagramas e exemplos · uso de IA.
Os diagramas verticais em `figuras/` são os mesmos `.dot` de `docs/modelagem/` renderizados com
`dot -Grankdir=TB`.

## Checklist de entrega (Classroom, turma CC6NA, 25/11)

- [ ] Um integrante anexa: `docs/relatorio/relatorio.pdf`, `docs/slides/apresentacao.pdf` (ou `.pptx`),
      o link https://github.com/Gaalbu/validador-manifesto-carga e os **nomes completos** da equipe.
- [ ] Os demais registram a entrega com o mesmo link e informam quem enviou os arquivos.
- [ ] Repositório público (acesso do professor durante a correção).
- [x] Nomes completos conferidos no README, no relatório e nos slides: Alberto Eduardo Acosta, Davi Maciel Corrêa,
      Gabriel Albuquerque Alencar, José Joaquim Valdez e Jorge Lobato Gonçalves.
