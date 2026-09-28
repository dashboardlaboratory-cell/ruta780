#!/usr/bin/env python3
"""Comprueba los casos de ML aplicado (regla 26).

Para cada página `aplicado/caso-N-*.qmd`:

  setup       la celda de datos compartida (#| setup: true) se ejecuta sin error
  solucion    para cada pregunta, la solución de referencia (el bloque ```python
              dentro de ::: {.solution exercise="…"}) se ejecuta tras la celda de
              datos, y la comprobación, ejecutada después, da correct True
  vacio       la plantilla de cada pregunta, sin completar, no pasa
  trampa      el bloque <!-- verificacion … --> se ejecuta tras la celda de datos
              y todas sus aserciones se cumplen: la respuesta correcta sale de los
              datos y la trampa está donde el caso dice
  herramienta el enunciado de las preguntas no prescribe herramientas
  oculto      ninguna celda visible contiene el generador de los datos

Uso:
    python3 verificar/casos.py              # todos
    python3 verificar/casos.py ruta.qmd
"""
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from entregables import HERRAMIENTA  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SONDA = ("\nimport json as _j\nprint('@@FB@@' + _j.dumps({'c': bool(feedback['correct']),"
         " 'm': str(feedback['message'])}))\n")


CARPETA = RAIZ


def ejecuta(codigo):
    # se ejecuta desde la carpeta de la página: allí están los archivos de
    # datos que la página declara en «pyodide: resources»
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True,
                       timeout=900, cwd=CARPETA)
    return r.returncode, r.stdout, r.stderr


def resultado(codigo):
    c, out, err = ejecuta(codigo + SONDA)
    fb = re.search(r"@@FB@@(.*)", out)
    if c != 0 or not fb:
        return None, (err.strip().split("\n")[-1] if err.strip() else "sin feedback")
    d = json.loads(fb.group(1))
    return d["c"], d["m"]


def revisar(p):
    global CARPETA
    CARPETA = p.parent
    t = p.read_text(encoding="utf-8")
    h = []
    setup = re.search(r"```\{pyodide\}\n#\| exercise: \[[^\]]*\]\n#\| setup: true\n(.*?)```", t, re.S)
    if not setup:
        return [("forma", "falta la celda de datos compartida (#| setup: true)")]
    datos = setup.group(1)
    c, _, err = ejecuta(datos)
    if c != 0:
        return [("setup", "la celda de datos revienta: " + err.strip().split("\n")[-1])]

    # El mecanismo que genera los datos es lo que el caso pide descubrir: ninguna
    # celda visible puede traerlo. Va en una celda con «#| include: false».
    for c in re.findall(r"```\{pyodide\}\n(.*?)```", t, re.S):
        if not c.startswith("#|") and re.search(r"^def genera", c, re.M):
            h.append(("oculto", "una celda visible contiene el generador de los datos"))

    preguntas = t.split("## Preguntas", 1)[-1].split("## Rúbrica", 1)[0]
    for m in HERRAMIENTA.finditer(re.sub(r"```.*?```", "", preguntas, flags=re.S)):
        h.append(("herramienta", f"prescribe una herramienta: «{m.group(0)}»"))

    ids = re.findall(r"```\{pyodide\}\n#\| exercise: (\w+)\n(?!#\| check)(.*?)```", t, re.S)
    if not ids:
        h.append(("forma", "el caso no tiene preguntas con comprobación"))
    for ex, plantilla in ids:
        chk = re.search(r"```\{pyodide\}\n#\| exercise: %s\n#\| check: true\n(.*?)```" % ex, t, re.S)
        sol = re.search(r'::: \{\.solution exercise="%s"\}.*?```python\n(.*?)```' % ex, t, re.S)
        if not (chk and sol):
            h.append(("forma", f"{ex}: falta la comprobación o la solución de referencia"))
            continue
        ok, msg = resultado(datos + "\n" + sol.group(1) + "\n" + chk.group(1))
        if ok is None:
            h.append(("solucion", f"{ex}: la solución o la comprobación revientan: {msg}"))
        elif not ok:
            h.append(("solucion", f"{ex}: la comprobación rechaza la solución de referencia: {msg[:160]}"))
        ok2, _ = resultado(datos + "\n" + plantilla.replace("______", "None") + "\n" + chk.group(1))
        if ok2:
            h.append(("vacio", f"{ex}: la plantilla sin completar pasa la comprobación"))

    ver = re.search(r"<!-- verificacion\n(.*?)-->", t, re.S)
    if not ver:
        h.append(("trampa", "falta el bloque <!-- verificacion … --> que comprueba la trampa"))
    else:
        c, out, err = ejecuta(datos + "\n" + ver.group(1))
        if c != 0:
            h.append(("trampa", "la verificación falla: " + err.strip().split("\n")[-1]))
        else:
            for linea in out.strip().split("\n"):
                print("    ·", linea)
    return h


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    paginas = [pathlib.Path(a).resolve() for a in args] if args else sorted(RAIZ.glob("aplicado/caso-*.qmd"))
    total = 0
    for p in paginas:
        print(f"== {p.relative_to(RAIZ)}")
        h = revisar(p)
        for tipo, msg in h:
            print(f"  ✗ {tipo:11s} {msg}")
        total += len(h)
    print(f"\ncasos revisados: {len(paginas)} · problemas: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
