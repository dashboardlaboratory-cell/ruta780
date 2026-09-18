"""Genera en los cuadernos las secciones de retos que falten.

El contenido NO se inventa: cada leccion ya lleva sus tres retos escritos en su
bloque ## Reto, y este script los traslada al cuaderno con el molde de las
secciones que ya existian -encabezado, un titulo y una celda por reto, y el
cierre "Que me costo / que aprendi".

Existe porque la deuda llego a 33 secciones: las lecciones citaban una seccion
que no estaba, y rellenarlas a mano era la excusa para no hacerlo. Correrlo al
publicar una leccion nueva cuesta un segundo.

Uso:
    python3 proyectos/genera_retos.py              # informe: que falta
    python3 proyectos/genera_retos.py --escribe    # lo escribe

Es idempotente: las secciones que ya existen no se vuelven a anadir."""
import json, pathlib, re, sys
RAIZ = pathlib.Path(__file__).resolve().parent.parent
MOD = {"estadistica": "Estadística", "matematica": "Matemática",
       "python": "Python", "ml": "ML"}

def secciones_existentes():
    hay = set()
    for nb in ("F0-retos", "F1-retos", "F2-retos"):
        d = json.loads((RAIZ/"proyectos"/"notebooks"/f"{nb}.ipynb").read_text(encoding="utf-8"))
        for c in d["cells"]:
            if c["cell_type"] != "markdown": continue
            for l in c["source"]:
                m = re.match(r"##\s+(Matemática|Estadística|Python|ML)\s+(\d+)", l.strip())
                if m: hay.add((m.group(1), int(m.group(2))))
                m = re.match(r"##\s+Lección\s+(\d+)", l.strip())
                if m: hay.add(("Python", int(m.group(1))))
    return hay

def retos_de(p):
    t = p.read_text(encoding="utf-8")
    m = re.search(r"^## Reto\s*\n(.*?)^## ", t, re.S | re.M)
    if not m: return None, None, []
    cuerpo = m.group(1)
    nb = re.search(r"notebooks/(F\d-retos)\.ipynb`, sección \*\*([^*]+)\*\*", cuerpo)
    if not nb: return None, None, []
    puntos = re.findall(r"^\d+\.\s+(.+?)(?=^\d+\.\s|\Z)", cuerpo, re.S | re.M)
    return nb.group(1), nb.group(2).strip(), [re.sub(r"\s+", " ", x).strip() for x in puntos]

def titulo(p):
    m = re.search(r'^title:\s*"(.*)"', p.read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else p.stem

GRIEGAS = {"alpha":"α","beta":"β","gamma":"γ","delta":"δ","epsilon":"ε","zeta":"ζ",
           "eta":"η","theta":"θ","iota":"ι","kappa":"κ","lambda":"λ","mu":"μ","nu":"ν",
           "xi":"ξ","pi":"π","rho":"ρ","sigma":"σ","tau":"τ","phi":"φ","chi":"χ",
           "psi":"ψ","omega":"ω","Sigma":"Σ","Delta":"Δ","Phi":"Φ","Omega":"Ω",
           "Gamma":"Γ","Lambda":"Λ","Theta":"Θ","Pi":"Π"}
OPERADORES = {"dots":"…","ldots":"…","cdots":"…","ge":"≥","geq":"≥","le":"≤","leq":"≤",
              "neq":"≠","approx":"≈","times":"×","cdot":"·","pm":"±","to":"→","infty":"∞",
              "in":"∈","subset":"⊂","sim":"~","propto":"∝","sum":"Σ","int":"∫",
              "sqrt":"raíz de","log":"log","exp":"exp","min":"min","max":"max",
              "mid":"|","cap":"∩","cup":"∪","perp":"⊥","forall":"para todo",
              "ell":"ℓ","top":"ᵀ","partial":"∂","nabla":"∇","langle":"⟨",
              "rangle":"⟩","lVert":"‖","rVert":"‖","vert":"|","circ":"∘",
              "otimes":"⊗","odot":"⊙","quad":" ","prime":"′","left":"",
              "right":"","mathbf":"","ast":"*","binom":"C"}

def limpia(s):
    """Pasa el marcado de Markdown y LaTeX a texto legible en una celda de codigo.

    Quitar las barras a secas dejaba 'dots', 'ge' y 'bar{X}_n', que no se leen.
    """
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"`([^`]*)`", r"\1", s)
    # acentos sobre un simbolo: \bar{X} -> X barra, \hat{p} -> p gorro
    s = re.sub(r"\\bar\{([^{}]*)\}", r"\1 barra", s)
    s = re.sub(r"\\hat\{([^{}]*)\}", r"\1 gorro", s)
    s = re.sub(r"\\tilde\{([^{}]*)\}", r"\1 tilde", s)
    s = re.sub(r"\\(?:mathbb|mathsf|mathcal|text|mathrm|operatorname)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", s)
    def sustituye(m):
        n = m.group(1)
        return GRIEGAS.get(n) or OPERADORES.get(n) or n
    s = re.sub(r"\\([A-Za-z]+)", sustituye, s)
    s = s.replace("$", "").replace("\\", "")
    # un operador pegado a la palabra anterior no se lee: "n tilde∈{1,5}"
    s = re.sub(r"(?<=[A-Za-zÀ-ÿ])([∈≥≤≠≈→⊂∝])", r" \1", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()

def envuelve(s, ancho=76, sangria="# "):
    palabras, linea, out = s.split(), "", []
    for w in palabras:
        if len(linea) + len(w) + 1 > ancho - len(sangria):
            out.append(sangria + linea); linea = w
        else:
            linea = (linea + " " + w).strip()
    if linea: out.append(sangria + linea)
    return "\n".join(out)

hay = secciones_existentes()
pendientes = {}
for p in sorted(RAIZ.glob("*/[0-9]*.qmd")):
    nb, etiqueta, puntos = retos_de(p)
    if not nb: continue
    mm = re.match(r"(Est|Mat|Py|Python|ML|Estadística|Matemática)\s*(\d+)", etiqueta)
    if not mm: continue
    mod = {"Est":"Estadística","Mat":"Matemática","Py":"Python"}.get(mm.group(1), mm.group(1))
    num = int(mm.group(2))
    if (mod, num) in hay: continue
    pendientes.setdefault(nb, []).append((mod, num, titulo(p), puntos, p))

for nb, items in sorted(pendientes.items()):
    print(f"{nb}: {len(items)} secciones -> {[f'{m} {n}' for m,n,_,_,_ in items]}")
print()
total = sum(len(v) for v in pendientes.values())
print("total a generar:", total)
sin_tres = [(m,n) for v in pendientes.values() for m,n,_,pts,_ in v if len(pts) != 3]
print("secciones cuyo bloque Reto no tiene exactamente 3 puntos:", sin_tres or "ninguna")

# ---------- generacion ----------
def celdas_de(mod, num, tit, puntos):
    def md(x): return {"cell_type":"markdown","metadata":{},"source":[x]}
    def code(x): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":[x]}
    out = [md(f"## {mod} {num} — {tit}")]
    for i, punto in enumerate(puntos, 1):
        # el encabezado es la primera frase; el cuerpo entero va de comentario
        corte = punto.find(". ")
        cabeza = punto if corte < 0 else punto[:corte]
        out.append(md(f"**{i}.** {cabeza.rstrip('.')}"))
        out.append(code(envuelve(limpia(punto)) + "\n"))
    out.append(md("**Qué me costó / qué aprendí:**"))
    return out

if "--escribe" in sys.argv:
    for nb, items in sorted(pendientes.items()):
        ruta = RAIZ/"proyectos"/"notebooks"/f"{nb}.ipynb"
        d = json.loads(ruta.read_text(encoding="utf-8"))
        for mod, num, tit, puntos, _ in sorted(items, key=lambda x: (x[0], x[1])):
            d["cells"].extend(celdas_de(mod, num, tit, puntos))
        ruta.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{nb}: +{len(items)} secciones, ahora {len(d['cells'])} celdas")
