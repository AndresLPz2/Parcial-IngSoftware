@echo off
setlocal
chcp 65001 >nul
title Resultados de pruebas del parcial EnvíaYa
cd /d "%~dp0.."
set "PYTHON=%TEMP%\envios-evidencias-venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    echo No se encuentra el entorno temporal de pruebas.
    echo Instala pytest y pytest-cov siguiendo las instrucciones del README.md.
    pause
    exit /b 1
)

echo ============================================================
echo EVIDENCIA 1 DE 5 - AUDITORÍA DEL CÓDIGO HEREDADO
echo Se esperan nueve fallos reproducibles. Toma la captura.
echo ============================================================
"%PYTHON%" -m pytest --runxfail -q --tb=no test_legado_v1.py
set "SALIDA=%ERRORLEVEL%"
echo Codigo de salida observado: %SALIDA% ^(se espera 1 por los defectos^)
pause

echo ============================================================
echo EVIDENCIA 2 DE 5 - DEFECTO DE REDONDEO EN EL LEGADO
echo PLEG-07 debe fallar antes de la corrección. Toma la captura.
echo ============================================================
"%PYTHON%" -m pytest --runxfail -q --tb=no -k PLEG_07 test_legado_v1.py
set "SALIDA=%ERRORLEVEL%"
echo Codigo de salida observado: %SALIDA% ^(se espera 1^)
pause

echo ============================================================
echo EVIDENCIA 3 DE 5 - PRUEBA DEL REDONDEO CORREGIDO
echo Se comprueba el empate de 10.350 hacia 10.400. Toma la captura.
echo ============================================================
"%PYTHON%" -c "from envios import calc; valor=calc(4,'rural','normal',1); assert valor==10400, f'Esperado 10400, obtenido {valor}'; print(f'Prueba aprobada: esperado=10400, obtenido={valor}')"
set "SALIDA=%ERRORLEVEL%"
echo Codigo de salida observado: %SALIDA% ^(se espera 0^)
pause

echo ============================================================
echo EVIDENCIA 4 DE 5 - REGRESION Y COBERTURA
echo Deben aprobar 32 pruebas con 100 por ciento de cobertura.
echo ============================================================
"%PYTHON%" -m pytest -q --cov=envios --cov-branch --cov-report=term-missing test_envios.py
set "SALIDA=%ERRORLEVEL%"
echo Codigo de salida observado: %SALIDA% ^(se espera 0^)
pause

echo ============================================================
echo EVIDENCIA 5 DE 5 - RAMAS, VERSIONES E HISTORIAL DE GIT
echo ============================================================
echo --- Repositorio remoto ---
git remote -v
echo --- Ramas ---
git branch --list
echo --- Versiones ---
git tag --list
echo --- Historial reciente ---
git log -8 --oneline --decorate --graph
echo.
echo Toma la última captura; la demostración terminó.
pause
endlocal
