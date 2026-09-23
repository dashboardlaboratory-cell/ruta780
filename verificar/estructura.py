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


def revisa_progreso():
    """El contador de avance casa el data-leccion de cada fila con los data-ids
    de `index.qmd`. Existe porque falló: el 22-09-2026 diez filas de ML y de
    Python llevaban varias lecciones dentro de un solo data-leccion —el resto
    de un reemplazo sin anclar— y marcarlas no movía el contador, porque la
    cadena entera no coincidía con ningún id.

    Comprueba dos cosas distintas: las filas contra el `data-ids` de la portada,
    y las filas contra el `data-ids` del **propio** índice del módulo, que es el
    que mueve la barra de esa página. El segundo se añadió el 23-09-2026, porque
    también falló: `python/20` quedó publicada como fila y ausente de su propio
    `data-ids`, y la portada estaba bien, así que el gate daba verde."""
    fallos = []
    portada = (RAIZ / "index.qmd").read_text(encoding="utf-8")
    publicadas = {}
    for m in re.finditer(r'data-progreso="(\w+)"[^>]*?data-ids="([^"]*)"', portada, re.S):
        publicadas[m.group(1)] = [i.strip() for i in m.group(2).split(",") if i.strip()]

    for p in sorted(RAIZ.glob("*/index.qmd")):
        modulo = p.parent.name
        t = p.read_text(encoding="utf-8")
        vistos = []
        for l in t.split("\n"):
            m = re.search(r'data-leccion="([^"]*)"', l)
            if not m:
                continue
            ident = m.group(1)
            if "," in ident:
                fallos.append(f"{modulo}/index.qmd: data-leccion con varias lecciones: {ident}")
                continue
            vistos.append(ident)
            h = re.search(r'href="([^"]+)\.html"', l)
            if h and ident != f"{modulo}/{h.group(1)}":
                fallos.append(f"{modulo}/index.qmd: {ident} no casa con su enlace {h.group(1)}.html")
        # el data-ids del PROPIO indice del modulo, que es el que mueve la
        # barra de esa pagina. Se comprueba aparte porque puede quedarse
        # atras aunque el de la portada este bien: paso el 23-09-2026 con
        # python/20, y la barra del modulo habria contado 19 de 20.
        mp = re.search(r'data-progreso="\w+"[^>]*?data-ids="([^"]*)"', t, re.S)
        if mp is not None:
            propios = [i.strip() for i in mp.group(1).split(",") if i.strip()]
            if len(propios) != len(set(propios)):
                repes = sorted({i for i in propios if propios.count(i) > 1})
                fallos.append(f"{modulo}/index.qmd: data-ids con duplicados: {repes}")
            if sorted(set(propios)) != sorted(set(vistos)):
                sobran = sorted(set(vistos) - set(propios))
                faltan = sorted(set(propios) - set(vistos))
                if sobran:
                    fallos.append(f"{modulo}/index.qmd: fila publicada sin id propio: {sobran}")
                if faltan:
                    fallos.append(f"{modulo}/index.qmd: id propio sin fila publicada: {faltan}")
            mt = re.search(r'data-total="(\d+)"', t)
            if mt and int(mt.group(1)) < len(vistos):
                fallos.append(
                    f"{modulo}/index.qmd: data-total={mt.group(1)} y hay {len(vistos)} filas publicadas")

        esperadas = publicadas.get(modulo)
        if esperadas is None:
            continue
        if sorted(vistos) != sorted(esperadas):
            sobran = sorted(set(vistos) - set(esperadas))
            faltan = sorted(set(esperadas) - set(vistos))
            if sobran:
                fallos.append(f"{modulo}: en su indice pero no en data-ids de index.qmd: {sobran}")
            if faltan:
                fallos.append(f"{modulo}: en data-ids de index.qmd pero sin fila publicada: {faltan}")
    return fallos


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

    fallos += revisa_progreso()

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
