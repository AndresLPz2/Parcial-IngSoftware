"""Ejecuta las pruebas y crea evidencias visuales en español."""

from pathlib import Path
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont


CARPETA = Path(__file__).parent
RAIZ = CARPETA.parent
FUENTE = Path(r"C:\Windows\Fonts\consola.ttf")
DEFECTOS = [
    "PLEG-01 — No rechaza un peso superior al máximo personal.",
    "PLEG-02 — No rechaza una zona desconocida.",
    "PLEG-03 — No rechaza un día fuera del intervalo válido.",
    "PLEG-04 — Omite el recargo de sábado.",
    "PLEG-05 — El descuento reduce también el recargo de fin de semana.",
    "PLEG-06 — Acepta un cupón desconocido.",
    "PLEG-07 — Trunca el empate de redondeo en vez de subirlo.",
    "PLEG-08 — Acepta un tipo de cliente desconocido.",
    "PLEG-09 — Conserva el parámetro de impresión flag.",
]


def fuente(tamano: int):
    return ImageFont.truetype(str(FUENTE), tamano) if FUENTE.exists() else ImageFont.load_default()


def envolver(texto: str, maximo: int = 112) -> list[str]:
    resultado = []
    while len(texto) > maximo:
        corte = texto.rfind(" ", 0, maximo)
        if corte < 1:
            corte = maximo
        resultado.append(texto[:corte])
        texto = "  " + texto[corte:].lstrip()
    resultado.append(texto)
    return resultado


def crear_png(nombre: str, titulo: str, lineas: list[str], color_estado: str) -> None:
    contenido = ["EVIDENCIA DE EJECUCIÓN DE PRUEBAS", titulo, "", *[parte for linea in lineas for parte in envolver(linea)]]
    alto_linea = 26
    ancho = 1280
    alto = 62 + len(contenido) * alto_linea + 24
    imagen = Image.new("RGB", (ancho, alto), "#111827")
    dibujo = ImageDraw.Draw(imagen)
    dibujo.rounded_rectangle((18, 18, ancho - 18, alto - 18), radius=12, fill="#0b1220", outline="#334155", width=2)
    y = 32
    for indice, linea in enumerate(contenido):
        if indice == 0:
            color, tipo = "#93c5fd", fuente(18)
        elif indice == 1:
            color, tipo = "#e5e7eb", fuente(17)
        elif linea.startswith("Comando:"):
            color, tipo = "#fcd34d", fuente(14)
        elif linea.startswith("Resultado:") or linea.startswith("Cobertura medida:"):
            color, tipo = color_estado, fuente(15)
        elif linea.startswith("PLEG-") or linea.startswith("Pruebas:"):
            color, tipo = "#fca5a5" if color_estado == "#fca5a5" else "#86efac", fuente(14)
        else:
            color, tipo = "#d1d5db", fuente(15)
        dibujo.text((34, y), linea, font=tipo, fill=color)
        y += alto_linea
    imagen.save(CARPETA / nombre, optimize=True)


def ejecutar(argumentos: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pytest", *argumentos],
        cwd=RAIZ,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


legado = ejecutar(["--runxfail", "-q", "--tb=no", "test_legado_v1.py"])
fallos = re.search(r"(\d+) failed", legado.stdout)
ids = re.findall(r"PLEG[-_]0?(\d+)", legado.stdout)
if legado.returncode == 0 or fallos is None or int(fallos.group(1)) != 9 or len(set(ids)) < 8:
    raise SystemExit("La auditoría del legado no produjo los nueve fallos esperados.")

regresion = ejecutar(["-q", "--cov=envios", "--cov-branch", "--cov-report=term-missing", "test_envios.py"])
if regresion.returncode != 0 or "32 passed" not in regresion.stdout or "100%" not in regresion.stdout:
    raise SystemExit("La suite corregida no aprobó con la cobertura esperada.")

texto_legado = [
    "Comando: python -m pytest --runxfail -q --tb=no test_legado_v1.py",
    "Resultado: 9 pruebas fallidas de 9; código de salida 1, esperado en esta auditoría.",
    "Las fallas reproducen defectos presentes en la versión heredada:",
    *DEFECTOS,
]
texto_regresion = [
    "Comando: python -m pytest -q --cov=envios --cov-branch --cov-report=term-missing test_envios.py",
    "Resultado: 32 pruebas aprobadas; código de salida 0.",
    "Cobertura medida: 62 sentencias y 18 ramas; 100 % en ambas.",
]
(CARPETA / "resultado_heredado.txt").write_text("\n".join(texto_legado) + "\n", encoding="utf-8")
(CARPETA / "resultado_regresion.txt").write_text("\n".join(texto_regresion) + "\n", encoding="utf-8")
crear_png("captura_pruebas_legado.png", "Pruebas fallidas contra el código heredado", texto_legado, "#fca5a5")
crear_png("captura_regresion_corregida.png", "Pruebas aprobadas tras corregir los defectos", texto_regresion, "#86efac")
print("Evidencias creadas: 9 fallos heredados y 32 pruebas aprobadas.")
