#!/usr/bin/env python3
"""Comprueba los casos de ML aplicado (regla 26).

Los casos se resuelven fuera de la página: la página da la situación, los datos
para descargar, las preguntas, los entregables, la rúbrica y una nota de
enseñanza plegada con los resultados de referencia. Para cada página
`aplicado/caso-N-*.qmd`:

  forma       tiene las secciones del formato y la nota de enseñanza plegada, y
              ninguna celda que corra en el navegador
  datos       cada archivo enlazado existe, está en `resources:` y no trae
              columnas ocultas (las que empiezan por «_»)
  herramienta las preguntas y los entregables no prescriben herramientas
  trampa      el bloque <!-- verificacion … --> se ejecuta desde `aplicado/`,
              con los generadores importables, y sus aserciones se cumplen
  cifras      cada cifra de la nota de enseñanza con decimales o de tres dígitos
              o más, que no esté ya en el enunciado, sale en la salida de la
              verificación

Antes de revisar, escribe los CSV de los casos sintéticos con
`aplicado/generadores/generar.py`.

Uso:
    python3 verificar/casos.py              # todos
    python3 verificar/casos.py ruta.qmd
"""
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from entregables import HERRAMIENTA  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
APLICADO = RAIZ / "aplicado"
SECCIONES = ["## Situación", "## Los datos", "## Preguntas", "## Entregables", "## Rúbrica"]
NOTA = re.compile(r'::: \{\.callout-note collapse="true" title="Nota de enseñanza[^"]*"\}\n(.*?)\n:::\n', re.S)
CIFRA = re.compile(r"(?<![\w/.,])[-−]?\d{1,3}(?:[  ]\d{3})+(?:,\d+)?|[-−]?\d+,\d+|[-−]?\d+\.\d+|\d+")


def ejecuta(codigo):
    r = subprocess.run([sys.executable, "-c",
                        "import sys; sys.path.insert(0, 'generadores')\n" + codigo],
                       capture_output=True, text=True, timeout=900, cwd=APLICADO)
    return r.returncode, r.stdout, r.stderr


def normaliza(s):
    s = s.replace("−", "-").replace(" ", "").replace(" ", "").replace(",", ".")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.lstrip("-")


def cifras(texto):
    for m in CIFRA.finditer(texto):
        crudo = m.group(0)
        n = normaliza(crudo)
        if "." in n or len(n) >= 3:
            yield crudo, n


def revisar(p):
    t = p.read_text(encoding="utf-8")
    h = []
    for s in SECCIONES:
        if f"\n{s}\n" not in t:
            h.append(("forma", f"falta la sección «{s[3:]}»"))
    if "{pyodide}" in t:
        h.append(("forma", "el caso trae celdas del navegador; se resuelve fuera de la página"))
    nota = NOTA.search(t)
    if not nota:
        h.append(("forma", "falta la nota de enseñanza plegada"))

    front = t.split("---", 2)[1]
    for ruta in sorted(set(re.findall(r"\]\((datos/[^)]+)\)", t))):
        archivo = APLICADO / ruta
        if not archivo.exists():
            h.append(("datos", f"{ruta} no existe"))
            continue
        if f"- {ruta}" not in front:
            h.append(("datos", f"{ruta} no está en resources: y no se publica"))
        cabecera = archivo.open(encoding="utf-8").readline().strip().split(",")
        ocultas = [c for c in cabecera if c.startswith("_")]
        if ocultas:
            h.append(("datos", f"{ruta} trae columnas ocultas: {ocultas}"))

    enunciado = t.split("## Preguntas", 1)[-1].split("## Rúbrica", 1)[0]
    for m in HERRAMIENTA.finditer(enunciado):
        h.append(("herramienta", f"prescribe una herramienta: «{m.group(0)}»"))

    ver = re.search(r"<!-- verificacion\n(.*?)-->", t, re.S)
    if not ver:
        h.append(("trampa", "falta el bloque <!-- verificacion … -->"))
        return h
    c, out, err = ejecuta(ver.group(1))
    if c != 0:
        h.append(("trampa", "la verificación falla: " + err.strip().split("\n")[-1]))
        return h
    for linea in out.strip().split("\n"):
        print("    ·", linea)

    if nota:
        fuera = t[:nota.start()] + t[nota.end():ver.start()]
        dadas = {n for _, n in cifras(fuera)}
        salida = {normaliza(x) for x in re.findall(r"-?\d+(?:\.\d+)?", out)}
        for crudo, n in cifras(nota.group(1)):
            if n not in dadas and n not in salida:
                h.append(("cifras", f"«{crudo}» de la nota no sale en la verificación"))
    return h


def main():
    r = subprocess.run([sys.executable, str(APLICADO / "generadores" / "generar.py")],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("✗ los generadores fallan:", r.stderr.strip().split("\n")[-1])
        return 1
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    paginas = [pathlib.Path(a).resolve() for a in args] if args else sorted(APLICADO.glob("caso-*.qmd"))
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
