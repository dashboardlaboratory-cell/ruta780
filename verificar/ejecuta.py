"""Ejecuta cada ejercicio de las lecciones como lo haría quarto-live (regla 27).

Por cada celda `#| exercise: id` que no es comprobación:

  solucion   la solución (la celda pyodide dentro de `.solution`) corre sin
             error, y la comprobación, ejecutada después, da correct True
  vacio      la celda sin completar, con cada `______` cambiado por None, no
             da correct True
  forma      el ejercicio no tiene solución o no tiene comprobación

La comprobación corre como en el navegador: los globales son una copia del
espacio de nombres del ejercicio más `user_code` y `result` (el valor de la
última expresión), y los nombres que define la comprobación van a un
diccionario aparte. Una función auxiliar definida en la comprobación no ve
esos nombres, igual que en Pyodide (03-10-2026). Las celdas `#| setup: true`
del mismo ejercicio se ejecutan antes.

Por defecto revisa Fundamentos y Python; `--todo` revisa todas las lecciones.

Uso:
    python3 verificar/ejecuta.py                 # Fundamentos y Python
    python3 verificar/ejecuta.py ruta.qmd        # detalle de una lección
    python3 verificar/ejecuta.py --todo
    python3 verificar/ejecuta.py --estricto      # falla si hay alguno
"""
import concurrent.futures, json, os, pathlib, re, subprocess, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CELDA = re.compile(r"^```\{pyodide\}\n(.*?)^```", re.S | re.M)


def celdas(t):
    """(opciones, cuerpo, en_solucion) de cada celda pyodide."""
    out = []
    for m in CELDA.finditer(t):
        texto = m.group(1)
        ops, cuerpo = {}, []
        for linea in texto.split("\n"):
            mm = re.match(r"#\|\s*([\w-]+):\s*(.*)$", linea)
            if mm and not cuerpo:
                ops[mm.group(1)] = mm.group(2).strip()
            else:
                cuerpo.append(linea)
        antes = t[:m.start()]
        abre = antes.rfind("::: {.solution")
        en_sol = None
        if abre != -1 and antes.rfind("\n:::\n", abre) == -1:
            en_sol = re.match(r'::: \{\.solution exercise="([^"]+)"', antes[abre:]).group(1)
        out.append((ops, "\n".join(cuerpo), en_sol))
    return out


def ejercicios(t):
    """{id: {"celda", "check", "sol", "setup"}}"""
    ej = {}
    for ops, cuerpo, en_sol in celdas(t):
        ide = ops.get("exercise")
        if en_sol:
            ej.setdefault(en_sol, {})["sol"] = cuerpo
            continue
        if not ide:
            continue
        d = ej.setdefault(ide, {})
        if ops.get("check") == "true":
            d["check"] = cuerpo
        elif ops.get("setup") == "true":
            d["setup"] = d.get("setup", "") + cuerpo + "\n"
        else:
            d["celda"] = cuerpo
    return ej


PROGRAMA = r'''
import ast, copy, contextlib, io, json, sys
setup, usuario, comprobacion = json.loads(sys.stdin.read())
G = {"__name__": "__main__"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(setup, "setup", "exec"), G)
    arbol = ast.parse(usuario)
    ultimo = None
    if arbol.body and isinstance(arbol.body[-1], ast.Expr):
        cuerpo = ast.Module(body=arbol.body[:-1], type_ignores=[])
        exec(compile(cuerpo, "usuario", "exec"), G)
        ultimo = eval(compile(ast.Expression(arbol.body[-1].value), "usuario", "eval"), G)
    else:
        exec(compile(arbol, "usuario", "exec"), G)
G2 = dict(G)
G2.update(user_code=usuario, result=ultimo, last_value=ultimo)
L = {}
arbol = ast.parse(comprobacion)
with contextlib.redirect_stdout(io.StringIO()):
    if arbol.body and isinstance(arbol.body[-1], ast.Expr):
        exec(compile(ast.Module(body=arbol.body[:-1], type_ignores=[]), "comprobacion", "exec"), G2, L)
        fb = eval(compile(ast.Expression(arbol.body[-1].value), "comprobacion", "eval"), G2, L)
    else:
        exec(compile(arbol, "comprobacion", "exec"), G2, L)
        fb = L.get("feedback", G2.get("feedback"))
print("@@FB@@" + json.dumps({"c": bool(fb.get("correct")), "m": str(fb.get("message"))[:200]}))
'''


def corre(setup, usuario, comprobacion, tope=60):
    try:
        r = subprocess.run([sys.executable, "-c", PROGRAMA], input=json.dumps([setup, usuario, comprobacion]),
                           capture_output=True, text=True, timeout=tope)
    except subprocess.TimeoutExpired:
        return None, f"no termina en {tope} s"
    m = re.search(r"@@FB@@(.*)", r.stdout)
    if not m:
        ultima = (r.stderr.strip().split("\n") or [""])[-1]
        return None, ultima
    d = json.loads(m.group(1))
    return d["c"], d["m"]


def uno(ide, d):
    if "check" not in d or "sol" not in d:
        return [(ide, "forma", "falta " + ("la comprobación" if "check" not in d else "la solución"))]
    h = []
    setup = d.get("setup", "")
    ok, msg = corre(setup, d["sol"], d["check"])
    if ok is None:
        h.append((ide, "solucion", "revienta: " + msg))
    elif not ok:
        h.append((ide, "solucion", "la comprobación rechaza la solución: " + msg))
    if "______" in d["celda"]:
        # una celda en blanco puede no terminar (un while con None): eso no pasa
        ok2, _ = corre(setup, d["celda"].replace("______", "None"), d["check"], tope=10)
        if ok2:
            h.append((ide, "vacio", "la celda sin completar pasa la comprobación"))
    return h


def revisar(ruta, pool):
    ej = {k: d for k, d in ejercicios(ruta.read_text(encoding="utf-8")).items() if "celda" in d}
    futuros = [pool.submit(uno, ide, d) for ide, d in ej.items()]
    return len(ej), futuros


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        rutas = [pathlib.Path(a) for a in args]
    else:
        mods = ("*",) if "--todo" in sys.argv else ("fundamentos", "python")
        rutas = sorted(p for m in mods for p in RAIZ.glob(f"{m}/[0-9]*.qmd")
                       if p.parent.name not in ("_site", "_templates"))
    n = malos = 0
    # cada ejercicio es un proceso aparte: se reparten entre los núcleos
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        pendientes = []
        for r in rutas:
            k, futuros = revisar(r, pool)
            n += k
            pendientes.append((r, futuros))
        for r, futuros in pendientes:
            for f in futuros:
                for ide, tipo, msg in f.result():
                    print(f"  {r.parent.name}/{r.name} {ide:20s} {tipo:9s} {msg}")
                    malos += 1
    print(f"ejercicios ejecutados: {n}, con problemas: {malos}")
    return 1 if ("--estricto" in sys.argv and malos) else 0


if __name__ == "__main__":
    sys.exit(main())
