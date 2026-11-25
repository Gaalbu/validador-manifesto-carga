import re
import pytest
from src.ap import automato_pilha as ap
from src.all import automato_linear as all_mod
from src.main import validar, main
from tests.casos_frente4 import AP, ALL, INTEGRACAO, INVALIDA, lote

@pytest.mark.parametrize("id,entrada,esperado,regra", AP, ids=[c[0] for c in AP])
def test_ap(id, entrada, esperado, regra):
    assert ap.reconhecer(entrada).aceita == esperado, regra

@pytest.mark.parametrize("id,entrada,esperado,regra", ALL, ids=[c[0] for c in ALL])
def test_all(id, entrada, esperado, regra):
    r = all_mod.reconhecer(entrada)
    assert r.aceita == esperado, regra
    # A cada configuração, a fita mantém n+2 células e as bordas fixas.
    for linha in r.rastro:
        m = re.search(r"cab=(\d+)\s*\|\s*([<>PECDpecd\[\]]+)", linha)
        if m:
            cab, fita = int(m[1]), m[2].replace("[", "").replace("]", "")
            assert len(fita) == len(entrada) + 2
            assert fita[0] == "<" and fita[-1] == ">"
            assert 0 <= cab < len(fita)

@pytest.mark.parametrize("id,entrada,ap_ok,all_ok,regra", INTEGRACAO, ids=[c[0] for c in INTEGRACAO])
def test_integracao(id, entrada, ap_ok, all_ok, regra, monkeypatch, capsys):
    if not ap_ok:
        def nao_executar(*args):
            pytest.fail("ALL executado após rejeição do AP")
        monkeypatch.setattr(all_mod, "reconhecer", nao_executar)
    r = validar(entrada)
    assert r["ap"].aceita == ap_ok
    assert (r["all"].aceita if r["all"] is not None else None) == all_ok
    assert r["aceita"] == (ap_ok and all_ok is True)
    assert main([entrada, "--trace"]) == (0 if ap_ok and all_ok else 1)
    out = capsys.readouterr().out
    assert "pos=" in out and "pilha=" in out
    if ap_ok:
        assert "cab=" in out
    else:
        assert "ALL: não executado" in out and "cab=" not in out


def test_simbolo_invalido(capsys):
    assert main([INVALIDA]) == 2
    err = capsys.readouterr().err
    assert f"símbolo 'x' na posição {INVALIDA.index('x')}" in err
    assert "não pertence ao alfabeto de entrada" in err

@pytest.mark.parametrize("casos,alfabeto", [(AP, set("[]{}#PECD")), (ALL, set("PECD"))])
def test_cobertura(casos, alfabeto):
    assert len({c[1] for c in casos}) == len(casos)
    assert all(set(c[1]) <= alfabeto for c in casos)
    for esperado in (True, False):
        assert sum(len(c[1]) >= 18 and c[2] == esperado for c in casos) >= 8
    assert any(c[1] == "" for c in casos)

@pytest.mark.parametrize("n", [18,36,72,144])
def test_crescimento_all(n):
    k = n//4
    m = n//2-k
    r = all_mod.reconhecer(lote(k,m,k,m))
    assert r.aceita
    assert r.passos <= 2*(n+1)*(n+3)
