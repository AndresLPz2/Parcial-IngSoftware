# Evidencias de ejecución de pruebas

Las imágenes actuales son resúmenes gráficos en español de los resultados reales de pytest; no son fotografías de la ventana del terminal. El archivo `mostrar_resultados.cmd` presenta cinco evidencias en una consola visible y se detiene entre cada una para que se pueda tomar una captura directa: defectos del legado, prueba roja del redondeo heredado, prueba verde del redondeo corregido, regresión con cobertura y ramas/versiones/historial de Git.

## Código heredado

![Pruebas que fallan en el código heredado](captura_pruebas_legado.png)

La auditoría muestra nueve fallos reproducibles en la versión heredada. El código de salida 1 es el resultado esperado en esta comprobación, porque las pruebas exponen los defectos.

## Código corregido

![Pruebas de regresión aprobadas](captura_regresion_corregida.png)

La regresión termina con código de salida 0: 32 pruebas aprobadas, 62 sentencias y 18 ramas cubiertas, con 100 % de cobertura.

## Reproducción

Para tomar capturas directas, abrir `mostrar_resultados.cmd` y fotografiar la consola en cada pausa. El archivo usa el entorno temporal preparado en este equipo. Para reproducirlo en otro equipo, instalar Python, `pytest` y `pytest-cov`, y ajustar la ruta del intérprete en el archivo si hace falta. `generar_capturas.py` vuelve a crear los resúmenes gráficos; requiere `Pillow`.

## Capturas directas recibidas

![Auditoría fallida del código heredado](Captura%20de%20pantalla%202026-11-11%20212959.png)

![Fallo de redondeo heredado y corrección aprobada](Captura%20de%20pantalla%202026-11-11%20213009.png)

![Regresión corregida y cobertura](Captura%20de%20pantalla%202026-11-11%20213015.png)

La quinta captura recibida muestra que Git no se encontró en la consola y se excluye como evidencia aprobada. Se ajustó el guion para mostrar el historial y las versiones desde los registros guardados del proyecto; se debe volver a ejecutar el último paso para capturarlo correctamente.
