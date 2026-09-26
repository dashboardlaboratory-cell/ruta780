"""Comprueba que una edición de las celdas solo tocó sus `print`.

Para cada lección, compara cada celda ejecutable con su versión en git (HEAD
por defecto):

1. El código sin las llamadas a print debe ser idéntico (se compara el árbol
   sintáctico, así que da igual el formato).
2. Cada cifra que imprime la celda nueva debe estar entre las que imprimía la
   vieja: quitar comentarios impresos puede quitar cifras, nunca inventarlas.
3. El número de celdas no cambia.

Uso:
    python3 verificar/conserva_celdas.py ruta.qmd ...
    python3 verificar/conserva_celdas.py --ref=abc123 ruta.qmd
"""
import ast, re, sys, subprocess, collections, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from salidas import celdas_ejecutables

NUM = re.compile(r"[-−]?\d+(?:[.,]\d+)*(?:e[-+]?\d+)?")

class SinPrint(ast.NodeTransformer):
    def generic_visit(self, nodo):
        super().generic_visit(nodo)
        for campo in ("body", "orelse", "finalbody"):
            cuerpo = getattr(nodo, campo, None)
            if isinstance(cuerpo, list):
                nuevo = [s for s in cuerpo if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Call)
                                                   and getattr(s.value.func, "id", None) == "print")]
                if not nuevo and cuerpo: nuevo = [ast.Pass()]
                setattr(nodo, campo, nuevo)
        return nodo

def firma(codigo):
    return ast.dump(SinPrint().visit(ast.parse(codigo)))

def correr(codigo):
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout

def main():
    ref = "HEAD"; rutas = []
    for a in sys.argv[1:]:
        if a.startswith("--ref="): ref = a[6:]
        else: rutas.append(a)
    fallos = 0
    for r in rutas:
        viejo = subprocess.run(["git", "show", f"{ref}:{r}"], capture_output=True, text=True).stdout
        nuevo = pathlib.Path(r).read_text(encoding="utf-8")
        cv, cn = list(celdas_ejecutables(viejo)), list(celdas_ejecutables(nuevo))
        malos = []
        if [i for i, _ in cv] != [i for i, _ in cn]:
            malos.append(f"   cambió el número o el orden de las celdas: {len(cv)} → {len(cn)}")
        else:
            for (i, a), (_, b) in zip(cv, cn):
                if a == b: continue
                try:
                    if firma(a) != firma(b):
                        malos.append(f"   celda {i}: cambió código que no es print"); continue
                except SyntaxError as e:
                    malos.append(f"   celda {i}: no compila ({e})"); continue
                ea, sa = correr(a); eb, sb = correr(b)
                if eb != 0:
                    malos.append(f"   celda {i}: la versión nueva revienta"); continue
                sobran = collections.Counter(NUM.findall(sb)) - collections.Counter(NUM.findall(sa))
                if sobran:
                    malos.append(f"   celda {i}: imprime cifras que antes no imprimía: {list(sobran)[:6]}")
        if malos:
            fallos += 1; print(f"XX {r}"); print("\n".join(malos))
        else:
            print(f"ok {r}")
    return 1 if fallos else 0

if __name__ == "__main__":
    sys.exit(main())
