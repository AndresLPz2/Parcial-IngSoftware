# Parcial 3 - EnvíaYa

El informe está en `Informe_Parcial3.md`; la implementación está en `envios.py`; las pruebas de regresión están en `test_envios.py`; las reproducciones de defectos del legado están en `test_legado_v1.py`.

La salida de historial solicitada por el enunciado está en `git-log.txt`.

Parámetros usados para el código 0182310057 según la regla de las seis últimas cifras del PDF: A–F=3,1,0,0,5,7. Cambio asignado: cliente empresarial. `envios_legado_v1.py` conserva literalmente el código legado etiquetado como v1.0.0; sus identificadores en inglés se mantienen para coincidir con el original.

## Ejecutar

```powershell
python -m pip install pytest pytest-cov
python -m pytest --runxfail -q --tb=no test_legado_v1.py
python -m pytest -q --cov=envios --cov-branch --cov-report=term-missing test_envios.py
```

Última ejecución: auditoría del legado, 9 fallos reproducibles; regresión, 32 pruebas aprobadas; 62 sentencias, 18 ramas y cobertura del 100%. Las evidencias están en `evidencias/README.md`; `mostrar_resultados.cmd` presenta cinco verificaciones en una consola visible y se pausa para tomar capturas.

Etiquetas locales: v1.0.0 (legado), v2.0.0 (correcciones y retirada incompatible de `flag`), v2.1.0 (refactorización y cliente empresarial), v2.1.1 (evidencias y métricas actualizadas) y v2.1.2 (secuencia para capturas directas). Se conservan las ramas requeridas por el enunciado: `fix/DEF-01` a `fix/DEF-08`, `test/suite`, `refactor/estrategia` y `feat/cliente-empresarial`.
