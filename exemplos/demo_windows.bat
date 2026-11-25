@echo off
REM Demonstracao ao vivo (slide 14): roda os 3 cenarios de integracao e o erro de alfabeto.
REM Uso: de dois cliques neste arquivo ou rode exemplos\demo_windows.bat na raiz do repositorio.
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0.."
set PY=python
where python >nul 2>nul || set PY=py
if exist .venv\Scripts\python.exe set PY=.venv\Scripts\python.exe
echo ================================================================
%PY% --version
echo Pasta: %CD%
echo ================================================================
echo.
echo [1] Cenario 1 - esperado: AP aceita, ALL aceita
%PY% -m src.main "[{}[{}]]{[]}#PPEEECCDDD"
echo     codigo de saida: %ERRORLEVEL%
echo.
echo [2] Cenario 2 - esperado: AP rejeita, ALL nao executa
%PY% -m src.main "[{}[{]}]{[]}#PPEEECCDDD"
echo     codigo de saida: %ERRORLEVEL%
echo.
echo [3] Cenario 3 - esperado: AP aceita, ALL rejeita
%PY% -m src.main "[{}[{}]]{[]}#PPEEECCCDD"
echo     codigo de saida: %ERRORLEVEL%
echo.
echo [4] Simbolo fora do alfabeto - esperado: erro, codigo 2
%PY% -m src.main "[{}[{}]]{[]}#PPEEExCCDDD"
echo     codigo de saida: %ERRORLEVEL%
echo.
echo [5] Rastreamento do AP no cenario 2
%PY% -m src.main "[{}[{]}]{[]}#PPEEECCDDD" --so ap --trace
echo.
echo [6] Rastreamento do ALL com a menor cadeia aceita (PECD)
%PY% -m src.main "PECD" --so all --trace
echo.
echo ================================================================
echo Para o rastreamento completo do cenario 1:
echo   %PY% -m src.main "[{}[{}]]{[]}#PPEEECCDDD" --trace
echo ================================================================
pause
