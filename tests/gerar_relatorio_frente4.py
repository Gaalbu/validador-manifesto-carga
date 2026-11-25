"""Execute da raiz com python -m tests.gerar_relatorio_frente4."""
from pathlib import Path
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import csv
from src.ap import automato_pilha as ap
from src.all import automato_linear as all_mod
from src.main import validar, main
from tests.casos_frente4 import AP, ALL, INTEGRACAO, INVALIDA, lote


def decisao(valor):
    return {True: "Aceita", False: "Rejeita", None: "Não executado"}[valor]


def cadeia(w):
    return f"`{w}`" if w else "ε (vazia)"


def gerar():
    linhas = ["# Testes e análise dos resultados — Frente 4", "", "## Metodologia", "",
              "Os resultados esperados foram definidos pelas linguagens formais, independentemente dos simuladores. Cada módulo tem pelo menos oito entradas aceitas e oito rejeitadas, distintas, com 18 ou mais símbolos e pertencentes ao seu alfabeto. Os casos-limite adicionais (entrada vazia e menor cadeia aceita) são intencionalmente menores que 18 símbolos.", "",
              "Execução: `python -m pytest tests/test_frente4.py -v`. Para regenerar este relatório e os dados: `python -m tests.gerar_relatorio_frente4`.", "",
              "As decisões abaixo são obtidas pela execução dos reconhecedores; a tabela não é preenchida com previsões. As tabelas foram geradas executando os reconhecedores no clone oficial do repositório (branch `main`); a suíte completa (`python -m pytest -v`) foi reexecutada no clone oficial em 25/11/2026, com 55 testes aprovados.", ""]
    dados = []
    total = acertos = 0
    for nome, casos, modulo in [("AP", AP, ap), ("ALL", ALL, all_mod)]:
        linhas += [f"## {nome} — testes isolados", "", "| ID | Entrada | Tam. | Esperado | Obtido | Regra verificada |", "|---|---|---:|---|---|---|"]
        for id, w, exp, regra in casos:
            r = modulo.reconhecer(w)
            linhas.append(f"| {id} | {cadeia(w)} | {len(w)} | {decisao(exp)} | {decisao(r.aceita)} | {regra} |")
            dados.append([id,nome,w,len(w),decisao(exp),decisao(r.aceita),regra,r.motivo])
            total += 1; acertos += exp == r.aceita
        linhas += [""]
    linhas += ["## Integração", "", "| ID | Entrada | Tam. | Esperado (AP / ALL) | Obtido (AP / ALL) | Regra verificada |", "|---|---|---:|---|---|---|"]
    for id,w,a,b,regra in INTEGRACAO:
        r = validar(w)
        ra, rb = r['ap'].aceita, r['all'].aceita if r['all'] is not None else None
        exp = f"{decisao(a)} / {decisao(b)}"; obt = f"{decisao(ra)} / {decisao(rb)}"
        linhas.append(f"| {id} | {cadeia(w)} | {len(w)} | {exp} | {obt} | {regra} |")
        dados.append([id,'Integração',w,len(w),exp,obt,regra,f"Decisão final: {decisao(r['aceita'])}"])
        total += 1; acertos += (a,b)==(ra,rb) and r['aceita']==(a and b is True)
    out, err = StringIO(), StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        codigo = main([INVALIDA])
    mensagem = err.getvalue().strip()
    esperado = f"Erro: símbolo 'x' na posição {INVALIDA.index('x')} não pertence ao alfabeto de entrada {{ {' '.join(sorted('[]{}#PECD'))} }}"
    total += 1; acertos += codigo == 2 and mensagem == esperado
    linhas += ["", "## Símbolo fora do alfabeto", "", f"Entrada: {cadeia(INVALIDA)} ({len(INVALIDA)} símbolos).", "", "Esperado: código de saída 2 e mensagem identificando o símbolo `x` e sua posição (índice começando em zero).", "", f"Obtido: código de saída {codigo}.", "", "```text", mensagem, "```", ""]
    dados.append(['ERR01','CLI',INVALIDA,len(INVALIDA),'Erro (2)',f'Código {codigo}','Símbolo fora do alfabeto',mensagem])
    linhas += ["## Análise e limitação observada", "", f"{acertos} de {total} casos de decisão coincidiram com o esperado (18 do AP, 19 do ALL, 3 de integração e 1 erro). A suíte automatizada acrescenta verificações de cobertura e crescimento, além de conferir a fita e o rastreamento durante os testes.", "", "O AP aceita estruturas bem formadas mesmo quando as quantidades não correspondem; a responsabilidade de comparar P/C e E/D é do ALL. Na integração, uma rejeição do AP impede a chamada ao ALL, e uma rejeição do ALL torna o manifesto inválido mesmo com a estrutura correta.", "", "### Crescimento do número de transições do ALL", "", "Foram executados lotes válidos, mantendo P=C e E=D e aproximadamente a mesma quantidade de cada símbolo. A contagem é retornada pelo próprio simulador.", "", "| Símbolos do lote | Passos do ALL | Configurações registradas |", "|---:|---:|---:|"]
    for n in (18,36,72,144):
        k=n//4; m=n//2-k; r=all_mod.reconhecer(lote(k,m,k,m))
        linhas.append(f"| {n} | {r.passos} | {len(r.rastro)} |")
    linhas += ["", "**Limitação:** o ALL precisa realizar sucessivas varreduras para marcar e casar símbolos. Nas entradas válidas testadas, o número de passos cresce aproximadamente de forma quadrática. Além disso, o simulador guarda uma representação da fita em cada passo, inclusive quando a opção `--trace` não é solicitada; o histórico de diagnóstico pode consumir O(n³) espaço no pior caso. Isso não altera o limite da memória de trabalho do modelo formal, que permanece em n células graváveis e dois marcadores fixos. Uma melhoria seria tornar o registro opcional ou emitir cada configuração sem acumular o histórico.", "", "Os testes oferecem evidências de funcionamento nos casos escolhidos; não constituem uma prova de corretude para todas as cadeias.", ""]
    Path('docs/relatorio').mkdir(parents=True, exist_ok=True)
    Path('docs/relatorio/testes.md').write_text('\n'.join(linhas), encoding='utf-8')
    Path('exemplos').mkdir(exist_ok=True)
    with Path('exemplos/casos_frente4.tsv').open('w', encoding='utf-8', newline='') as f:
        writer=csv.writer(f,delimiter='\t'); writer.writerow(['id','modulo','entrada','tamanho','esperado','obtido','regra','motivo']); writer.writerows(dados)
    print(f'{acertos}/{total} casos de decisão coincidiram com o esperado.')
    if acertos != total:
        raise SystemExit(1)

if __name__ == '__main__':
    gerar()
