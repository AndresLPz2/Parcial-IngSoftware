# Parcial 3 - EnvíaYa

El informe está en `Informe_Parcial3.md`; implementación en `envios.py`; regresión en `test_envios.py`; reproducción de defectos heredados en `test_legacy_v1.py`.

Parámetros usados para el código 0182310057 según la regla de seis cifras del PDF: A–F=3,1,0,0,5,7. Cambio asignado: cliente empresarial. `envios_legacy_v1.py` es la copia ejecutable exacta etiquetada como v1.0.0.

## Ejecutar

```powershell
python -m pip install pytest pytest-cov
python -m pytest -q test_legacy_v1.py
python -m pytest -q --cov=envios --cov-branch --cov-report=term-missing test_envios.py
```

Última ejecución: auditoría legacy, 9 xfailed como reproducción de los defectos; regresión, 32 passed; 64 sentencias, 18 ramas y 100% de cobertura.

Etiquetas locales: v1.0.0 (legado), v2.0.0 (correcciones y retirada incompatible de flag), v2.1.0 (refactor y cliente empresarial). Las ramas `fix/DEF-01` a `fix/DEF-08`, `test/suite`, `refactor/estrategia` y `feat/cliente-empresarial` conservan el flujo realizado.
