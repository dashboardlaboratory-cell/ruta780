#!/usr/bin/env python3
"""
Verifica que los números que la prosa afirma siguen saliendo del código.

Extrae cada celda {pyodide} de cada lección, la ejecuta, y comprueba que la
salida contiene los fragmentos declarados en afirmaciones.json. Si una celda
revienta, o si un número citado deja de aparecer, sale con código 1 y el build
falla antes de publicar.

Se salta las celdas plantilla (las que tienen ______) y las de corrección
(#| check: true), que necesitan la variable `result` del alumno.
"""
import json
import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
AFIRM = json.loads((RAIZ / "verificar" / "afirmaciones.json").read_text(encoding="utf-8"))

CELDA = re.compile(r"```\{pyodide\}\n(.*?)\n```", re.S)


def celdas_ejecutables(texto):
    """Devuelve [(indice_original, codigo)] de las celdas que se pueden correr solas."""
    fuera = []
    for i, c in enumerate(CELDA.findall(texto)):
        if "______" in c:
            continue
        if "#| check: true" in c:
            continue
        cuerpo = "\n".join(l for l in c.split("\n") if not l.startswith("#|"))
        if cuerpo.strip():
            fuera.append((i, cuerpo))
    return fuera


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:                       # rutas sueltas: revisar solo esas lecciones
        lecciones = sorted((RAIZ / a).resolve() for a in args)
    else:
        lecciones = sorted(
            p for p in RAIZ.glob("*/[0-9]*.qmd") if p.parent.name != "_templates"
        )
    fallos = []
    corridas = 0
    comprobadas = 0

    for p in lecciones:
        rel = f"{p.parent.name}/{p.name}"
        texto = p.read_text(encoding="utf-8")
        esperado = {int(k): v for k, v in AFIRM.get(rel, {}).items()}
        salidas = {}

        for idx, codigo in celdas_ejecutables(texto):
            corridas += 1
            try:
                r = subprocess.run(
                    [sys.executable, "-c", codigo],
                    capture_output=True, text=True, timeout=300,
                )
            except subprocess.TimeoutExpired:
                fallos.append(f"{rel} celda {idx}: se pasó de 300 s")
                continue
            if r.returncode != 0:
                ultima = r.stderr.strip().split("\n")[-1]
                fallos.append(f"{rel} celda {idx}: REVENTÓ → {ultima}")
                continue
            salidas[idx] = r.stdout

        for idx, decl in esperado.items():
            if idx not in salidas:
                fallos.append(f"{rel} celda {idx}: declarada en afirmaciones.json pero no se ejecutó")
                continue
            salida = salidas[idx]

            # "contiene": para salidas reproducibles (True/False, racionales exactos,
            # resultados analíticos). Comparación literal de subcadena.
            for frag in decl.get("contiene", []):
                comprobadas += 1
                if frag not in salida:
                    fallos.append(
                        f"{rel} celda {idx}: la prosa dice «{frag}» y la salida ya no lo contiene"
                    )

            # "cumple": para cantidades que NO son reproducibles entre máquinas
            # (cancelación catastrófica, pérdida de ortogonalidad). Ahí no se puede
            # fijar el dígito: se fija la propiedad, que es lo que la prosa afirma.
            for expr in decl.get("cumple", []):
                comprobadas += 1
                try:
                    ok = bool(eval(expr, {"re": re, "float": float, "salida": salida}))
                except Exception as e:
                    fallos.append(f"{rel} celda {idx}: la propiedad «{expr}» no se pudo evaluar → {e}")
                    continue
                if not ok:
                    fallos.append(f"{rel} celda {idx}: la propiedad «{expr}» dejó de cumplirse")

    sin_declarar = [
        f"{p.parent.name}/{p.name}"
        for p in lecciones
        if celdas_ejecutables(p.read_text(encoding="utf-8"))
        and f"{p.parent.name}/{p.name}" not in AFIRM
    ]

    print(f"lecciones revisadas : {len(lecciones)}")
    print(f"celdas ejecutadas   : {corridas}")
    print(f"afirmaciones        : {comprobadas}")
    if sin_declarar:
        print(f"\nsin afirmaciones declaradas (solo se comprobó que no revientan):")
        for s in sin_declarar:
            print("  ·", s)

    if fallos:
        print(f"\n{len(fallos)} FALLO(S):")
        for f in fallos:
            print("  ✗", f)
        return 1

    print("\nTodo cuadra.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
