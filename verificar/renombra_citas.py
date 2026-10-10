"""Localiza (y con --aplicar corrige) citas a resultados que cambiaron de etiqueta.

Cuando una lección renombra un resultado, por ejemplo «Proposición 2.6» que
pasa a «Regla 2.6» (regla 27, 04-10-2026), las demás lecciones, entregables y
cuadernos de retos siguen citándolo con el nombre viejo. Este script busca
cada mención «<Vieja> N.M» y la cambia por «<Nueva> N.M» si en la lección N del
módulo ese resultado ya se llama así.

El módulo de cada mención se resuelve así: «… de Fundamentos K» o «… de
Python K» explícito; si no, el módulo de la carpeta del archivo; en los
cuadernos `proyectos/notebooks/*.ipynb`, el último encabezado «<Módulo> K»
anterior. Menciones de otros módulos se ignoran. Un plural con mezcla de
etiquetas se informa y no se toca.

Las celdas de código también se corrigen (comentarios «Proposicion 1.3»). Eso
cambia el código de la celda pero no su posición, así que no hace falta
reindexar afirmaciones.json; sí conviene correr `salidas.py`.

Uso:
    python3 verificar/renombra_citas.py                    # informe
    python3 verificar/renombra_citas.py --aplicar
    python3 verificar/renombra_citas.py --de Proposición --a Regla --modulos fundamentos,python
"""
import pathlib, re, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
NOMBRES = {"fundamentos": "Fundamentos", "python": "Python", "estadistica": "Estadística",
           "matematica": "Álgebra", "ml": "Machine Learning", "series": "Series",
           "causal": "Causal", "atributos": "Atributos", "aplicado": "Aplicado"}


def opcion(nombre, defecto):
    return sys.argv[sys.argv.index(nombre) + 1] if nombre in sys.argv else defecto


def main():
    vieja = opcion("--de", "Proposición")
    nueva = opcion("--a", "Regla")
    modulos = opcion("--modulos", "fundamentos,python").split(",")
    aplicar = "--aplicar" in sys.argv
    MOD = {NOMBRES[m]: m for m in modulos}

    destino = set()
    for m in modulos:
        for p in (RAIZ / m).glob("[0-9]*.qmd"):
            for a, b in re.findall(r"\*\*" + nueva + r" (\d+)\.(\d+)", p.read_text(encoding="utf-8")):
                destino.add((m, int(a), int(b)))

    raiz_v = vieja[:-2] if vieja.endswith("ón") else vieja          # Proposici(ón|on|ones)
    patron = raiz_v + (r"(?:ón|on|ones)" if vieja.endswith("ón") else r"s?")
    MEN = re.compile(r"(" + patron + r")((?:\s*(?:,|y)?\s*\d+\.\d+)+)"
                     r"(\s+de\s+([A-ZÁÉÍÓÚ][\wáéíóú]+(?: [A-Z][\w]+)?)\s+(\d+))?")

    archivos = [p for p in RAIZ.rglob("*.qmd")
                if "_site" not in p.parts and ".claude" not in p.parts]
    archivos += list((RAIZ / "proyectos" / "notebooks").glob("*.ipynb"))
    total = 0
    for f in sorted(archivos):
        t = f.read_text(encoding="utf-8")
        trozos, ult = [], 0
        for m in MEN.finditer(t):
            nums = [(int(a), int(b)) for a, b in re.findall(r"(\d+)\.(\d+)", m.group(2))]
            if m.group(3):
                if m.group(4) not in MOD:
                    continue
                mod = MOD[m.group(4)]
            elif f.parent.name in modulos:
                mod = f.parent.name
            elif f.suffix == ".ipynb":
                h = list(re.finditer(r"(" + "|".join(MOD) + r") \d+", t[:m.start()]))
                if not h:
                    continue
                mod = MOD[h[-1].group(1)]
            else:
                continue
            estado = [(mod, n, k) in destino for n, k in nums]
            if not any(estado):
                continue
            linea = t.count("\n", 0, m.start()) + 1
            if not all(estado):
                print(f"MEZCLA {f.relative_to(RAIZ)}:{linea}: {m.group(0)[:80]}")
                continue
            plural = len(nums) > 1 and m.group(1).endswith(("es", "s"))
            rep = (nueva + ("s" if plural else "")) + m.group(2) + (m.group(3) or "")
            print(f"{f.relative_to(RAIZ)}:{linea}: «{m.group(0)[:60]}» -> «{rep[:60]}»")
            trozos += [t[ult:m.start()], rep]
            ult = m.end()
            total += 1
        if aplicar and trozos:
            trozos.append(t[ult:])
            f.write_text("".join(trozos), encoding="utf-8")
    print(f"menciones: {total}" + (" (corregidas)" if aplicar else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
