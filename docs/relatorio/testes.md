# Testes e análise dos resultados — Frente 4

## Metodologia

Os resultados esperados foram definidos pelas linguagens formais, independentemente dos simuladores. Cada módulo tem pelo menos oito entradas aceitas e oito rejeitadas, distintas, com 18 ou mais símbolos e pertencentes ao seu alfabeto. Os casos-limite adicionais (entrada vazia e menor cadeia aceita) são intencionalmente menores que 18 símbolos.

Execução: `python -m pytest tests/test_frente4.py -v`. Para regenerar este relatório e os dados: `python -m tests.gerar_relatorio_frente4`.

As decisões abaixo são obtidas pela execução dos reconhecedores; a tabela não é preenchida com previsões. A execução inicial foi feita em uma cópia local reconstruída do código Python da branch `main` consultado no GitHub, sem alterar a lógica. Reexecute no clone oficial antes da entrega.

## AP — testes isolados

| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |
|---|---|---:|---|---|---|
| AP01 | `[{}[{}]]{[]}#PPEEECCDDD` | 23 | Aceita | Aceita | Aninhamento misto e blocos completos |
| AP02 | `[[[[[[[]]]]]]]#PECD` | 19 | Aceita | Aceita | Sete níveis de colchetes |
| AP03 | `{{{{{{{}}}}}}}#PECD` | 19 | Aceita | Aceita | Sete níveis de chaves |
| AP04 | `[]{}[]{}[]{}[]{}#PECD` | 21 | Aceita | Aceita | Blocos consecutivos |
| AP05 | `{[{}]}{[{}]}{[{}]}#PECD` | 23 | Aceita | Aceita | Tipos alternados e blocos consecutivos |
| AP06 | `[]#PPPPPEEEEECCCCCD` | 19 | Aceita | Aceita | Quantidades distintas são permitidas pelo AP |
| AP07 | `[{}[{}]]{[]}#PPEEECCCDD` | 23 | Aceita | Aceita | Dependência cruzada não é responsabilidade do AP |
| AP08 | `[{}]#PPPEEECCCDDDDD` | 19 | Aceita | Aceita | Bloco D mais longo |
| AP09 | `[{}[{]}]{[]}#PPEEECCDDD` | 23 | Rejeita | Rejeita | Fechamento de tipo incorreto |
| AP10 | `[[{}[{}]]{[]}#PPEEECCDDD` | 24 | Rejeita | Rejeita | Abertura sem fechamento antes de # |
| AP11 | `[{}[{}]]{[]}]#PPEEECCDDD` | 24 | Rejeita | Rejeita | Fechamento excedente |
| AP12 | `[{}[{}]]{[]}PPEEECCDDD` | 22 | Rejeita | Rejeita | Separador ausente |
| AP13 | `[{}[{}]]{[]}##PPEEECCDDD` | 24 | Rejeita | Rejeita | Separador duplicado |
| AP14 | `[{}[{}]]{[]}#PPCCCCDDDD` | 23 | Rejeita | Rejeita | Bloco E ausente |
| AP15 | `[{}[{}]]{[]}#PPCCEEEDDD` | 23 | Rejeita | Rejeita | Blocos fora de ordem |
| AP16 | `[{}[{}]]{[]}#PPEEECCDDDP` | 24 | Rejeita | Rejeita | Símbolo após o bloco D |
| AP17 | `[]#PECD` | 7 | Aceita | Aceita | Comprimento mínimo: 7 símbolos |
| AP18 | ε (vazia) | 0 | Rejeita | Rejeita | Entrada vazia |

## ALL — testes isolados

| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |
|---|---|---:|---|---|---|
| ALL01 | `PEEEEEEEECDDDDDDDD` | 18 | Aceita | Aceita | P=C=1; E=D=8 |
| ALL02 | `PPEEEEEEECCDDDDDDD` | 18 | Aceita | Aceita | P=C=2; E=D=7 |
| ALL03 | `PPPEEEEEECCCDDDDDD` | 18 | Aceita | Aceita | P=C=3; E=D=6 |
| ALL04 | `PPPPEEEEECCCCDDDDD` | 18 | Aceita | Aceita | P=C=4; E=D=5 |
| ALL05 | `PPPPPEEEECCCCCDDDD` | 18 | Aceita | Aceita | P=C=5; E=D=4 |
| ALL06 | `PPPPPPEEECCCCCCDDD` | 18 | Aceita | Aceita | P=C=6; E=D=3 |
| ALL07 | `PPPPPPPEECCCCCCCDD` | 18 | Aceita | Aceita | P=C=7; E=D=2 |
| ALL08 | `PPPPPPPPECCCCCCCCD` | 18 | Aceita | Aceita | P=C=8; E=D=1 |
| ALL09 | `PPPPPEEEEECCCCDDDDD` | 19 | Rejeita | Rejeita | P excedente: P > C |
| ALL10 | `PPPPEEEEECCCCCDDDDD` | 19 | Rejeita | Rejeita | C excedente: P < C |
| ALL11 | `PPPPPEEEEECCCCCDDDD` | 19 | Rejeita | Rejeita | E excedente: E > D |
| ALL12 | `PPPPPEEEECCCCCDDDDD` | 19 | Rejeita | Rejeita | D excedente: E < D |
| ALL13 | `EEEEEECCCCCCDDDDDD` | 18 | Rejeita | Rejeita | Bloco P ausente |
| ALL14 | `PPPPPPCCCCCCDDDDDD` | 18 | Rejeita | Rejeita | Bloco E ausente |
| ALL15 | `PPPPPPEEEEEEDDDDDD` | 18 | Rejeita | Rejeita | Bloco C ausente |
| ALL16 | `PPPPPPEEEEEECCCCCC` | 18 | Rejeita | Rejeita | Bloco D ausente |
| ALL17 | `PECD` | 4 | Aceita | Aceita | Comprimento mínimo: 4 símbolos |
| ALL18 | ε (vazia) | 0 | Rejeita | Rejeita | Entrada vazia |
| ALL19 | `PPPPPCCCCCEEEEEDDDDD` | 20 | Rejeita | Rejeita | Quantidades iguais, ordem incorreta |

## Integração

| ID | Entrada | Tam. | Esperado (AP / ALL) | Obtido (AP / ALL) | Regra verificada |
|---|---|---:|---|---|---|
| INT01 | `[{}[{}]]{[]}#PPEEECCDDD` | 23 | Aceita / Aceita | Aceita / Aceita | Estrutura e dependências válidas |
| INT02 | `[{}[{]}]{[]}#PPEEECCDDD` | 23 | Rejeita / Não executado | Rejeita / Não executado | AP rejeita; ALL não pode executar |
| INT03 | `[{}[{}]]{[]}#PPEEECCCDD` | 23 | Aceita / Rejeita | Aceita / Rejeita | Estrutura válida, P != C e E != D |

## Símbolo fora do alfabeto

Entrada: `[{}[{}]]{[]}#PPEEExCCDDD` (24 símbolos).

Esperado: código de saída 2 e mensagem identificando o símbolo `x` e sua posição (índice começando em zero).

Obtido: código de saída 2.

```text
Erro: símbolo 'x' na posição 18 não pertence ao alfabeto de entrada { # C D E P [ ] { } }
```

## Análise e limitação observada

41 de 41 casos de decisão coincidiram com o esperado (18 do AP, 19 do ALL, 3 de integração e 1 erro). A suíte automatizada acrescenta verificações de cobertura e crescimento, além de conferir a fita e o rastreamento durante os testes.

O AP aceita estruturas bem formadas mesmo quando as quantidades não correspondem; a responsabilidade de comparar P/C e E/D é do ALL. Na integração, uma rejeição do AP impede a chamada ao ALL, e uma rejeição do ALL torna o manifesto inválido mesmo com a estrutura correta.

### Crescimento do número de transições do ALL

Foram executados lotes válidos, mantendo P=C e E=D e aproximadamente a mesma quantidade de cada símbolo. A contagem é retornada pelo próprio simulador.

| Símbolos do lote | Passos do ALL | Configurações registradas |
|---:|---:|---:|
| 18 | 338 | 339 |
| 36 | 1158 | 1159 |
| 72 | 4254 | 4255 |
| 144 | 16278 | 16279 |

**Limitação:** o ALL precisa realizar sucessivas varreduras para marcar e casar símbolos. Nas entradas válidas testadas, o número de passos cresce aproximadamente de forma quadrática. Além disso, o simulador guarda uma representação da fita em cada passo, inclusive quando a opção `--trace` não é solicitada; o histórico de diagnóstico pode consumir O(n³) espaço no pior caso. Isso não altera o limite da memória de trabalho do modelo formal, que permanece em n células graváveis e dois marcadores fixos. Uma melhoria seria tornar o registro opcional ou emitir cada configuração sem acumular o histórico.

Os testes oferecem evidências de funcionamento nos casos escolhidos; não constituem uma prova de corretude para todas as cadeias.
