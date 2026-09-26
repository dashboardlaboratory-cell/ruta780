"""Comprueba que una edición de los visuales solo tocó sus textos.

Compara cada bloque ```{=html} con su versión en git (HEAD por defecto). Dentro
de <script> vacía el contenido de las cadenas ("…", '…', `…`); fuera, vacía el
texto entre etiquetas. Lo que queda (código, etiquetas, atributos de estilo y
de datos) debe ser idéntico; aria-label, title y placeholder cuentan como texto, y las cifras de las cadenas no pueden cambiar.

Uso:
    python3 verificar/conserva_html.py ruta.qmd ...
"""
import re, sys, subprocess, pathlib, collections

CADENA = re.compile(r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\'|`(?:[^`\\]|\\.)*`')
NUM = re.compile(r"\d+(?:[.,]\d+)*")

def bloques(t):
    return re.findall(r"^```\{=html\}\n(.*?)^```", t, re.S | re.M)

def esqueleto(b):
    partes = re.split(r"(<script[^>]*>.*?</script>)", b, flags=re.S)
    out, cifras = [], []
    for p in partes:
        if p.startswith("<script"):
            cifras += [n for s in CADENA.findall(p) for n in NUM.findall(s)]
            out.append(CADENA.sub('""', p))
        else:
            sin_estilo = re.split(r"(<style[^>]*>.*?</style>)", p, flags=re.S)
            for q in sin_estilo:
                if q.startswith("<style"): out.append(q); continue
                cifras += [n for s in re.findall(r">([^<]*)<", q) for n in NUM.findall(s)]
                cifras += [n for s in re.findall(r'(?:aria-label|title|placeholder)="([^"]*)"', q) for n in NUM.findall(s)]
                q = re.sub(r'((?:aria-label|title|placeholder)=")[^"]*"', r'\1"', q)   # textos accesibles
                out.append(re.sub(r">[^<]*<", "><", q))
    return "".join(out), collections.Counter(cifras)

def main():
    ref = "HEAD"; rutas = [a for a in sys.argv[1:] if not a.startswith("--")]
    for a in sys.argv[1:]:
        if a.startswith("--ref="): ref = a[6:]
    fallos = 0
    for r in rutas:
        viejo = subprocess.run(["git", "show", f"{ref}:{r}"], capture_output=True, text=True).stdout
        nuevo = pathlib.Path(r).read_text(encoding="utf-8")
        bv, bn = bloques(viejo), bloques(nuevo); malos = []
        if len(bv) != len(bn):
            malos.append(f"   cambió el número de bloques HTML: {len(bv)} → {len(bn)}")
        else:
            for i, (a, b) in enumerate(zip(bv, bn)):
                if a == b: continue
                ea, ca = esqueleto(a); eb, cb = esqueleto(b)
                if ea != eb:
                    j = next((k for k in range(min(len(ea), len(eb))) if ea[k] != eb[k]), min(len(ea), len(eb)))
                    malos.append(f"   bloque {i}: cambió código o marcado: …{ea[max(0,j-50):j+40]!r} → …{eb[max(0,j-50):j+40]!r}")
                elif ca != cb:
                    malos.append(f"   bloque {i}: cambiaron cifras de los textos: faltan {list((ca-cb).elements())[:6]} · sobran {list((cb-ca).elements())[:6]}")
        if malos: fallos += 1; print(f"XX {r}"); print("\n".join(malos))
        else: print(f"ok {r}")
    return 1 if fallos else 0

if __name__ == "__main__":
    sys.exit(main())
