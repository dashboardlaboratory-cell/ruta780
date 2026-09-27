"""Comprueba los entregables (regla 25).

Para cada página `*/entregable-NN.qmd`:

  solucion   la solución de referencia (el bloque ```python del callout) se
             ejecuta sin error, y la celda de comprobación, ejecutada después,
             da correct True
  vacio      la plantilla del ejercicio, sin completar, no pasa la comprobación
  herramienta el enunciado no prescribe herramientas: no dice «usar una lista»,
             «con un bucle while», «mediante un diccionario», etc. Decide quien
             resuelve.
  requisitos la especificación tiene requisitos numerados

Uso:
    python3 verificar/entregables.py              # todos
    python3 verificar/entregables.py ruta.qmd
"""
import re, sys, pathlib, subprocess, json

RAIZ = pathlib.Path(__file__).resolve().parent.parent
HERRAMIENTA = re.compile(
    r"\b(?:us(?:ar|ando|e|a)|mediante|con (?:un|una|el|la)|calculad[oa]s? con|debe calcularse con|implementad[oa] con|a través de)\s+"
    r"(?:un |una |el |la |los |las )?(?:bucle|ciclo|`?while`?|`?for`?|lista|listas|diccionario|diccionarios|tupla|tuplas|"
    r"conjunto|conjuntos|comprehension|condicional|condicionales|funci[oó]n lambda|numpy|pandas|groupby|`np\.|`pd\.)",
    re.I)

def partes(t):
    esp = t.split("## Especificación", 1)[-1].split("## Rúbrica", 1)[0]
    ej = re.search(r"```\{pyodide\}\n#\| exercise: (\S+)\n(.*?)```", t, re.S)
    chk = re.search(r"```\{pyodide\}\n#\| exercise: \S+\n#\| check: true\n(.*?)```", t, re.S)
    sol = re.search(r"::: \{\.callout-note[^}]*\}.*?```python\n(.*?)```", t, re.S)
    return esp, ej, chk, sol

def ejecuta(codigo):
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True, timeout=600)
    return r.returncode, r.stdout, r.stderr

SONDA = "\nimport json as _j\nprint('@@FB@@' + _j.dumps({'c': bool(feedback['correct']), 'm': str(feedback['message'])}))\n"

def revisar(p):
    t = p.read_text(encoding="utf-8"); h = []
    esp, ej, chk, sol = partes(t)
    if not re.search(r"^1\. ", esp, re.M):
        h.append(("requisitos", "la especificación no tiene requisitos numerados"))
    for m in HERRAMIENTA.finditer(esp):
        h.append(("herramienta", f"prescribe una herramienta: «{m.group(0)}»"))
    if not (ej and chk and sol):
        h.append(("forma", "falta la celda del ejercicio, la comprobación o la solución de referencia")); return h
    c, out, err = ejecuta(sol.group(1) + "\n" + chk.group(1) + SONDA)
    fb = re.search(r"@@FB@@(.*)", out)
    if c != 0 or not fb:
        h.append(("solucion", "la solución o la comprobación revientan: " + (err.strip().split("\n")[-1] if err else "sin feedback")))
    elif not json.loads(fb.group(1))["c"]:
        h.append(("solucion", "la comprobación rechaza la solución de referencia: " + json.loads(fb.group(1))["m"][:160]))
    c2, out2, _ = ejecuta(ej.group(2).replace("______", "None") + "\n" + chk.group(1) + SONDA)
    fb2 = re.search(r"@@FB@@(.*)", out2)
    if fb2 and json.loads(fb2.group(1))["c"]:
        h.append(("vacio", "la plantilla sin completar pasa la comprobación"))
    return h

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    rutas = [pathlib.Path(a) for a in args] or sorted(RAIZ.glob("*/entregable-*.qmd"))
    malos = 0
    for p in rutas:
        h = revisar(p)
        print(("ok " if not h else "XX ") + str(p.relative_to(RAIZ) if p.is_absolute() else p))
        for k, m in h: print(f"   {k:11s} {m}")
        malos += bool(h)
    print(f"entregables: {len(rutas)}, con problemas: {malos}")
    return 1 if malos else 0

if __name__ == "__main__":
    sys.exit(main())
