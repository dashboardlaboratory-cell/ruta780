#!/usr/bin/env python3
"""Resuelve cada «Machine Learning N» de las lecciones contra el titulo de la
fila N de ml/index.qmd.

Existe porque desglosar un capitulo de ISLP obliga a renumerar el indice, y con
el a subir todas las referencias cruzadas. Sin esto, una renumeracion deja
referencias que apuntan a la leccion equivocada sin que ningun gate se entere.

Sale con codigo 1 si alguna referencia apunta a una fila que no existe.
"""
import pathlib, re, sys
RAIZ = pathlib.Path(__file__).resolve().parent.parent
idx = (RAIZ / "ml" / "index.qmd").read_text(encoding="utf-8")
titulos = {}
for f in re.findall(r'<div class="fila[^>]*>.*?</div>', idx):
    n = int(re.search(r'num">(\d+)<', f).group(1))
    titulos[n] = re.search(r'class="tit">(?:<a[^>]*>)?([^<]*)', f).group(1)

malos = 0
for p in sorted(RAIZ.glob("*/[0-9]*.qmd")):
    if p.parent.name == "_templates":
        continue
    for linea in p.read_text(encoding="utf-8").split("\n"):
        m = re.search(r'\*\*Machine Learning ((?:\d+)(?:\s*(?:y|a|,)\s*\d+)*)\*\*:\s*(.{0,70})', linea)
        if not m:
            continue
        nums = [int(x) for x in re.findall(r'\d+', m.group(1))]
        for n in nums:
            if n not in titulos:
                print("  X %s: ML %d no existe en el indice" % (p.name, n)); malos += 1
        print("%-34s ML %-12s -> %s" % (p.name, m.group(1), " | ".join(titulos.get(n, "???") for n in nums)))
        print("%-34s    dice: %s" % ("", m.group(2).strip()))
print("\nreferencias a filas inexistentes:", malos)
sys.exit(1 if malos else 0)
