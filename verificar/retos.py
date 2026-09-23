#!/usr/bin/env python3
"""
Comprueba que el reto que cada lección promete existe de verdad.

Cada lección cierra con un bloque `## Reto` que dice, con nombre y apellido,
«En `proyectos/notebooks/F3-retos.ipynb`, sección **Series 4**». Nada comprobaba
que ese cuaderno tuviera esa sección.

Existe porque falló. El 20-09-2026 se descubrió que las once lecciones de Series
de tiempo remitían a secciones que no estaban escritas: `genera_retos.py` pide
la bandera `--escribe` y sin ella imprime lo que FALTA, no lo que hizo, y esa
salida se leyó al revés once veces seguidas. Once builds en verde no lo vieron
porque ninguna compuerta miraba el cuaderno.

Comprueba tres cosas y falla el build si alguna no se cumple:

  · la lección tiene bloque `## Reto` y nombra un cuaderno y una sección;
  · ese cuaderno existe y contiene un encabezado para esa sección;
  · el bloque tiene exactamente tres puntos numerados.
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# el nombre corto que usa la prosa -> el que lleva el encabezado del cuaderno
MODULOS = {
    "Mat": ("Matemática",),
    "Matemática": ("Matemática",),
    "Est": ("Estadística",),
    "Estadística": ("Estadística",),
    # SIN el alias "Lección": F0-retos.ipynb tiene «## Lección 1 — Tipos y
    # estructuras», que es python/01 y no fundamentos/01. Con el alias puesto
    # el gate daba VERDE sobre una sección que existe pero es de otra cosa.
    "Fundamentos": ("Fundamentos",),
    "Py": ("Python", "Lección"),
    "Python": ("Python", "Lección"),
    "ML": ("ML",),
    "Series": ("Series",),
}

REF = re.compile(
    r"En\s+`proyectos/notebooks/(?P<nb>[^`]+\.ipynb)`,\s*secci[oó]n\s*\*\*(?P<mod>[A-Za-zÁÉÍÓÚáéíóú]+)\s*(?P<num>\d+)\*\*"
)


def encabezados(ruta):
    """Los pares (modulo, numero) que el cuaderno ya tiene."""
    hay = set()
    d = json.loads(ruta.read_text(encoding="utf-8"))
    for c in d["cells"]:
        if c["cell_type"] != "markdown":
            continue
        for l in c["source"]:
            m = re.match(r"#{2,3}\s+([A-Za-zÁÉÍÓÚáéíóú]+)\s+(\d+)", l.strip())
            if m:
                hay.add((m.group(1), int(m.group(2))))
    return hay


def main():
    lecciones = sorted(
        p for p in RAIZ.glob("*/[0-9]*.qmd") if p.parent.name != "_templates"
    )
    cache = {}
    fallos, sin_reto, revisadas = [], [], 0

    for p in lecciones:
        rel = f"{p.parent.name}/{p.name}"
        texto = p.read_text(encoding="utf-8")
        m = re.search(r"^## Reto\s*$(.*?)^## ", texto, re.S | re.M)
        if not m:
            sin_reto.append(rel)
            continue
        bloque = m.group(1)
        revisadas += 1

        r = REF.search(bloque)
        if not r:
            fallos.append(f"{rel}: el bloque Reto no nombra cuaderno y sección")
            continue

        ruta = RAIZ / "proyectos" / "notebooks" / r.group("nb")
        if not ruta.exists():
            fallos.append(f"{rel}: nombra «{r.group('nb')}», que no existe")
            continue
        if ruta not in cache:
            cache[ruta] = encabezados(ruta)

        num = int(r.group("num"))
        nombres = MODULOS.get(r.group("mod"))
        if nombres is None:
            fallos.append(f"{rel}: módulo «{r.group('mod')}» desconocido en el bloque Reto")
            continue
        if not any((n, num) in cache[ruta] for n in nombres):
            fallos.append(
                f"{rel}: promete la sección «{r.group('mod')} {num}» de {r.group('nb')} "
                f"y ese cuaderno no la tiene"
            )
            continue

        puntos = len(re.findall(r"^\d+\.\s", bloque, re.M))
        if puntos != 3:
            fallos.append(f"{rel}: el bloque Reto tiene {puntos} puntos numerados y deben ser 3")

    print(f"lecciones con bloque Reto: {revisadas}")
    print(f"cuadernos consultados    : {len(cache)}")
    if sin_reto:
        print(f"sin bloque Reto ({len(sin_reto)}): {', '.join(sin_reto)}")
    if fallos:
        print()
        print("=== FALLOS ===")
        for f in fallos:
            print("  ✗ " + f)
        sys.exit(1)
    print()
    print("Cada reto prometido existe en su cuaderno.")


if __name__ == "__main__":
    main()
