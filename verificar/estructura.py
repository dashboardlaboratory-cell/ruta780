#!/usr/bin/env python3
"""
Comprueba la estructura de cada leccion antes de renderizar.

Quarto no avisa de una valla ::: sin cerrar: genera la pagina con el bloque
abierto y el resto del contenido queda dentro de el. Esto lo caza antes.
"""
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ABRE = re.compile(r"^(:{3,})\s*\{")
CIERRA = re.compile(r"^(:{3,})\s*$")


def main():
    fallos = []
    archivos = sorted(
        [p for p in RAIZ.glob("*/[0-9]*.qmd") if p.parent.name != "_templates"]
        + list(RAIZ.glob("*.qmd"))
        + list(RAIZ.glob("*/index.qmd"))
    )
    for p in archivos:
        rel = f"{p.parent.name}/{p.name}" if p.parent != RAIZ else p.name
        t = p.read_text(encoding="utf-8")
        pila = []
        for i, l in enumerate(t.split("\n"), 1):
            m = ABRE.match(l)
            if m:
                pila.append((len(m.group(1)), i)); continue
            m = CIERRA.match(l)
            if m:
                if not pila:
                    fallos.append(f"{rel}:{i}: cierre ::: sin bloque abierto")
                else:
                    pila.pop()
        for n, i in pila:
            fallos.append(f"{rel}:{i}: bloque {':' * n} abierto y nunca cerrado")

        if t.count("```") % 2:
            fallos.append(f"{rel}: numero impar de vallas ```")
        if len(re.findall(r"<div\b", t)) != len(re.findall(r"</div>", t)):
            fallos.append(f"{rel}: <div> y </div> no cuadran")
        if p.name != "index.qmd" and p.parent != RAIZ and "engine: markdown" not in t:
            fallos.append(f"{rel}: falta `engine: markdown` en el frontmatter")

    print(f"archivos revisados: {len(archivos)}")
    if fallos:
        print(f"\n{len(fallos)} FALLO(S):")
        for f in fallos:
            print("  x", f)
        return 1
    print("\nEstructura correcta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
