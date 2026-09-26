"""Comprueba que el enunciado de cada ejercicio corresponda a lo que pide su celda
(regla 24, 26-09-2026, a partir de una revisión del ejercicio de Estadística 11).

Por cada ejercicio (la celda con `#| exercise:` que no es `check`) y su enunciado
(el texto entre el título «### Ejercicio» y la celda):

  verbo      el enunciado dice «devolver» y la celda no tiene `return`
  hueco      una variable que se completa (`nombre = ______`) no se nombra en el
             enunciado entre comillas invertidas
  metodo     el código que sigue al hueco llama a un método de la variable
             (`nombre.std()`), que falla si la respuesta natural es una lista
  criterio   el enunciado no dice qué resultado se espera
  check      la comprobación no usa la variable que se completa
  ancho      una línea de la celda del ejercicio o de su solución pasa de 72
             caracteres y obliga a desplazarse
  referencia el código llama «verdadero» a un valor que se obtiene simulando

Uso:
    python3 verificar/ejercicios.py              # resumen
    python3 verificar/ejercicios.py ruta.qmd     # detalle
    python3 verificar/ejercicios.py --estricto   # falla si hay alguno
"""
import re, sys, pathlib, collections

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ANCHO = 72
CRITERIO = re.compile(r"\b(?:debe|deben|debería|deberían|esperad[oa]s?|se espera|cerca de|próxim[oa] a|igual a|coincid\w*|tiene que|ha de)\b", re.I)

def ejercicios(t):
    """(id, enunciado, celda, pista, solucion) de cada ejercicio."""
    out = []
    for m in re.finditer(r"^### Ejercicio[^\n]*\n(.*?)^```\{pyodide\}\n#\| exercise: (\S+)\n(.*?)^```", t, re.S | re.M):
        enun, ide, celda = m.group(1), m.group(2), m.group(3)
        if "#| check: true" in celda: continue
        pista = re.search(r'::: \{\.hint exercise="' + re.escape(ide) + r'"\}\n(.*?)\n:::', t, re.S)
        sol = re.search(r'::: \{\.solution exercise="' + re.escape(ide) + r'"\}\n```\{pyodide\}\n(.*?)^```', t, re.S | re.M)
        out.append((ide, enun, celda, pista.group(1) if pista else "", sol.group(1) if sol else ""))
    return out

def revisar(ruta):
    t = ruta.read_text(encoding="utf-8"); h = []
    for ide, enun, celda, pista, sol in ejercicios(t):
        if re.search(r"\bdevolver\b|\bque devuelva\b", enun, re.I) and "return" not in celda:
            h.append((ide, "verbo", "el enunciado dice «devolver» y la celda no tiene return"))
        huecos = re.findall(r"^\s*([A-Za-z_]\w*)\s*=\s*_{4,}", celda, re.M)
        for v in huecos:
            if f"`{v}`" not in enun:
                h.append((ide, "hueco", f"la variable `{v}` que se completa no se nombra en el enunciado"))
            despues = celda.split("______", 1)[-1]
            mm = re.search(r"\b" + re.escape(v) + r"\.(\w+)\(", despues)
            if mm:
                h.append((ide, "metodo", f"`{v}.{mm.group(1)}()` falla si la respuesta es una lista"))
        if not CRITERIO.search(enun):
            h.append((ide, "criterio", "el enunciado no dice qué resultado se espera («debe dar…», «debe quedar cerca de…»)"))
        chk = re.search(r"^```\{pyodide\}\n#\| exercise: " + re.escape(ide) + r"\n#\| check: true\n(.*?)^```", t, re.S | re.M)
        if chk:
            # vale si usa la variable o algo calculado despues del hueco (que depende de ella)
            despues = celda.split("______", 1)[-1]
            derivadas = set(huecos) | set(re.findall(r"^\s*([A-Za-z_]\w*)\s*(?:,\s*\w+\s*)*=", despues, re.M))
            derivadas |= set(re.findall(r"\b([A-Za-z_]\w*)\.(?:append|extend)\(", despues))   # listas que se llenan
            antes = celda.split("______", 1)[0]
            derivadas |= set(re.findall(r"^def\s+(\w+)", antes.split("\ndef ")[-1] if "\ndef " in antes else "", re.M))
            m_def = list(re.finditer(r"^def\s+(\w+)", antes, re.M))
            if m_def: derivadas.add(m_def[-1].group(1))                  # hueco dentro de una funcion
            derivadas |= {"result"} if re.search(r"^\S", despues.strip().split("\n")[-1] if despues.strip() else "") else set()
            if huecos and not any(re.search(r"\b" + re.escape(d) + r"\b", chk.group(1)) for d in derivadas):
                h.append((ide, "check", "la comprobación no usa la variable que se completa ni nada calculado con ella"))
        for nombre, cuerpo in (("ejercicio", celda), ("solución", sol)):
            largas = [l for l in cuerpo.split("\n") if len(l) > ANCHO]
            if largas:
                h.append((ide, "ancho", f"{len(largas)} línea(s) de la {nombre} pasan de {ANCHO} caracteres"))
        if re.search(r"#[^\n]*\bverdader[oa]\b|\bverdad\s*=", celda):
            h.append((ide, "referencia", "llama «verdadero» a un valor de la celda; si se simula, es un valor de referencia"))
    return h

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    rutas = [pathlib.Path(a) for a in args] or sorted(p for p in RAIZ.glob("*/[0-9]*.qmd") if p.parent.name not in ("_site", "_templates"))
    tot = collections.Counter(); n = 0; por = collections.Counter()
    for r in rutas:
        h = revisar(r); n += len(ejercicios(r.read_text(encoding="utf-8")))
        for ide, k, msg in h:
            tot[k] += 1; por[str(r.relative_to(RAIZ) if r.is_absolute() else r)] += 1
            if args: print(f"  {r} {ide:18s} {k:10s} {msg}")
    print(f"ejercicios revisados: {n}")
    for k, v in tot.most_common(): print(f"  {k:10s} {v}")
    print(f"lecciones con algún problema: {len(por)}")
    return 1 if ("--estricto" in sys.argv and tot) else 0

if __name__ == "__main__":
    sys.exit(main())
