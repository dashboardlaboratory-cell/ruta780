"""Comprueba que una reescritura de estilo no cambió el contenido.

Compara cada .qmd con su versión en git (HEAD por defecto) y falla si cambió
algo que no es prosa: el frontmatter, los bloques de código y de HTML, las
fórmulas, los números de la prosa, los términos de glosario marcados, los
enlaces, las etiquetas de definiciones y proposiciones o el número de secciones.

Uso:
    python3 verificar/conserva.py ruta.qmd ...        # contra HEAD
    python3 verificar/conserva.py --ref=abc123 ruta.qmd
"""
import re, sys, subprocess, collections, pathlib

def partes(t):
    fm = re.match(r"^---\n.*?\n---\n", t, re.S)
    fm = fm.group(0) if fm else ""
    cuerpo = t[len(fm):]
    bloques = re.findall(r"^```.*?^```", cuerpo, re.S | re.M)
    prosa = re.sub(r"^```.*?^```", "", cuerpo, flags=re.S | re.M)
    formulas = re.findall(r"\$\$.*?\$\$|\$[^$\n]+\$", prosa, re.S)
    sin_f = re.sub(r"\$\$.*?\$\$|\$[^$\n]+\$", " ", prosa, flags=re.S)
    sin_f = re.sub(r"`[^`\n]*`", " ", sin_f)
    sin_f = re.sub(r"\]\([^)]*\)", "]", sin_f)                  # destinos de enlace aparte
    numeros = re.findall(r"(?<![\w.])[−-]?\d+(?:[.,]\d+)*(?:\s?%)?", sin_f)
    numeros = [n.replace(" ", "") for n in numeros]
    return {
        "frontmatter": [fm],
        "bloques de código/HTML": bloques,
        "fórmulas": sorted(formulas),
        "código en línea": sorted(re.findall(r"`[^`\n]+`", prosa)),
        "números de la prosa": sorted(numeros),
        "términos de glosario": sorted(re.findall(r"\[[^\]\[\n]+\]\{\.g[^}]*\}", prosa)),
        "enlaces": sorted(re.findall(r"\]\(([^)]*)\)", prosa)),
        "etiquetas": sorted(re.findall(r"\*\*((?:Definición|Proposición|Teorema|Lema|Corolario|Ejemplo) [\d.]+)", prosa)),
        "vallas :::": sorted(re.findall(r"^:{3,}.*$", prosa, re.M)),
        "secciones": [len(re.findall(r"^## ", prosa, re.M))],
    }

def main():
    ref = "HEAD"; rutas = []
    for a in sys.argv[1:]:
        if a.startswith("--ref="): ref = a[6:]
        else: rutas.append(a)
    fallos = 0
    for r in rutas:
        try:
            viejo = subprocess.run(["git", "show", f"{ref}:{r}"], capture_output=True, text=True, check=True).stdout
        except subprocess.CalledProcessError:
            print(f"?? {r}: no está en {ref}"); continue
        nuevo = pathlib.Path(r).read_text(encoding="utf-8")
        a, b = partes(viejo), partes(nuevo)
        malos = []; avisos = []
        for k in a:
            if a[k] != b[k]:
                ca, cb = collections.Counter(map(str, a[k])), collections.Counter(map(str, b[k]))
                falta = list((ca - cb).elements())[:6]; sobra = list((cb - ca).elements())[:6]
                if k == "bloques de código/HTML" and ca == cb: continue
                linea = f"   {k}: faltan {falta} · sobran {sobra}" if (falta or sobra) else f"   {k}: cambió el orden"
                (avisos if k in ("fórmulas", "código en línea") else malos).append(linea)
        if malos:
            fallos += 1; print(f"XX {r}"); print("\n".join(malos))
        else:
            print(f"ok {r}")
        for x in avisos: print("   aviso" + x[2:])
    return 1 if fallos else 0

if __name__ == "__main__":
    sys.exit(main())
