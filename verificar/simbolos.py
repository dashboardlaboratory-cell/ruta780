"""Audita la regla 21b: que lecciones usan cada simbolo en formula y cuales lo
declaran en su tabla de notacion.

No es un gate -no falla el build- sino la herramienta para decidir si una entrada
del glosario global puede afirmar un significado o tiene que ceder a la tabla de
cada leccion. Existe porque el enganche del tooltip es GLOBAL POR CARACTER: lo que
diga la entrada se muestra en todo el sitio.

Uso:
    python3 verificar/simbolos.py            # los que estan en el glosario
    python3 verificar/simbolos.py T Q B      # los que se le pidan
"""
import re, pathlib, sys
RAIZ = pathlib.Path(__file__).resolve().parent.parent
import json
if sys.argv[1:]:
    SIMBOLOS = sys.argv[1:]
else:
    _g = json.loads((RAIZ / "glosario" / "glosario.json").read_text(encoding="utf-8"))
    SIMBOLOS = [k for k, v in _g.items() if isinstance(v, dict) and v.get("tipo") == "simbolo"
                and len(k) == 1 and k.isalpha()]

def bloques_math(t):
    """Trozos que KaTeX renderiza: $...$ y $$...$$."""
    return re.findall(r"\$\$(.+?)\$\$", t, re.S) + re.findall(r"(?<!\$)\$([^$\n]+?)\$(?!\$)", t)

def notacion(t):
    m = re.search(r"::: \{\.notacion\}(.*?):::", t, re.S)
    return m.group(1) if m else ""

# En el .qmd las griegas se escriben \alpha, no el caracter, asi que hay que
# buscar las dos formas o el recuento sale cero y parece que nadie las usa.
LATEX = {"α":"alpha","β":"beta","γ":"gamma","δ":"delta","ε":"epsilon","θ":"theta",
         "λ":"lambda","μ":"mu","ν":"nu","ρ":"rho","σ":"sigma","τ":"tau","φ":"phi",
         "χ":"chi","ω":"omega","Σ":"Sigma","Φ":"Phi","Δ":"Delta","Ω":"Omega",
         "κ":"kappa","π":"pi","ξ":"xi","η":"eta","ζ":"zeta"}

def patron(s):
    # La constante pi no es notacion de nadie: en 2\pi de la densidad normal no
    # hay nada que declarar. Solo cuenta cuando actua como funcion, pi(theta).
    if s == "\u03c0":
        return re.compile(r"\\pi\s*[\(\{]|\\pi_")
    formas = [r"(?<![A-Za-z\\])" + re.escape(s) + r"(?![A-Za-z])"]
    if s in LATEX:
        formas.append(r"\\" + LATEX[s] + r"(?![A-Za-z])")
    return re.compile("|".join(formas))

for s in SIMBOLOS:
    pat = patron(s)
    usa, declara, falta = [], [], []
    for p in sorted(RAIZ.glob("*/[0-9]*.qmd")):
        rel = f"{p.parent.name}/{p.name}"
        t = p.read_text(encoding="utf-8")
        if not any(pat.search(b) for b in bloques_math(t)):
            continue
        usa.append(rel)
        (declara if pat.search(notacion(t)) else falta).append(rel)
    print(f"=== {s} === usado en {len(usa)} lecciones")
    print(f"   lo declara en su notacion: {len(declara)}")
    if falta:
        print(f"   NO lo declara ({len(falta)}):")
        for r in falta: print("      ", r)
    print()
