"""Prueba los ejercicios de las lecciones en el Pyodide real del sitio (regla 27).

Sirve `_site/` en un puerto local, abre cada lección en Chromium y, por cada
ejercicio, escribe en el editor y pulsa «Ejecutar», como haría quien estudia:

  solucion   la solución de la página debe salir en verde
  blanco     la celda con cada `______` cambiado por 0 no debe salir en verde
             (o la plantilla tal cual, si no tiene huecos)
  bien/mal   respuestas alternativas de un JSON opcional: las «bien» deben
             salir en verde y las «mal» no

Existe porque los gates locales no ven lo que solo pasa en el navegador: el
04-10-2026 encontró que `np.arange` da int32 en wasm32 y dos bucles que
colgaban la pestaña con un cuerpo erróneo. Si una prueba no termina, la página
se recarga y se sigue con la siguiente.

Requiere la lección renderizada (`quarto render ruta.qmd`) y Playwright. Desde
el sandbox de Claude Code hay que correrlo fuera de él (puerto y Chromium).

Uso:
    python3 verificar/pyodide.py fundamentos/02-condicionales-y-verdad.qmd
    python3 verificar/pyodide.py --alt dir_json --paralelo 3 lecciones...
      (dir_json/<modulo>-<NN>.json = {"ex_id": {"bien": [codigo], "mal": [codigo]}})
"""
import asyncio, functools, http.server, json, pathlib, socketserver, sys, threading

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ejecuta  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PONER = """([sel, code]) => { const v = document.querySelector(sel + ' .cm-content').cmView.view;
  v.dispatch({changes: {from: 0, to: v.state.doc.length, insert: code}}); }"""


class Callado(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def servir():
    h = functools.partial(Callado, directory=str(RAIZ / "_site"))
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv.server_address[1]


async def cargar(pg, url):
    await pg.goto(url)
    await pg.wait_for_selector(".exercise-editor .cm-content", timeout=180000)
    await pg.wait_for_timeout(6000)


async def correr(pg, sel, code, espera=60):
    await pg.evaluate("(s) => document.querySelectorAll(s + ' .exercise-grade').forEach(e => e.remove())", sel)
    await pg.evaluate(PONER, [sel, code])
    await pg.locator(sel + ' a[aria-label="Ejecutar"]').click()
    for _ in range(espera * 2):
        await pg.wait_for_timeout(500)
        g = await pg.evaluate("(s) => { const g = document.querySelector(s + ' .exercise-grade');"
                              " return g ? [g.className, g.innerText] : null }", sel)
        if g:
            return "alert-success" in g[0], g[1].strip()[:110]
    return None, "sin calificación"


async def leccion(navegador, puerto, qmd, alt):
    rel = qmd.relative_to(RAIZ)
    ej = {k: d for k, d in ejecuta.ejercicios(qmd.read_text(encoding="utf-8")).items()
          if "celda" in d and "sol" in d}
    url = f"http://127.0.0.1:{puerto}/{str(rel)[:-4]}.html"
    pg = await navegador.new_page()
    errores, lineas, malos = [], [], 0
    pg.on("pageerror", lambda e: errores.append(str(e)))
    try:
        await cargar(pg, url)
    except Exception as e:
        await pg.close()
        return [f"?? {rel}: no carga ({type(e).__name__})"], 1
    celdas = await pg.evaluate("""() => [...document.querySelectorAll('.exercise-cell')]
        .filter(c => c.querySelector('a[aria-label="Ver pista"]') || !c.closest('.exercise-solution'))
        .map(c => [c.id, c.querySelector('.cm-content') ? c.querySelector('.cm-content').innerText : ''])""")
    norma = lambda s: "".join(s.split())
    for ide, d in ej.items():
        cand = [cid for cid, txt in celdas if norma(txt) == norma(d["celda"])]
        if not cand:
            lineas.append(f"?? {rel} {ide}: celda no encontrada en la página")
            malos += 1
            continue
        sel = "#" + cand[0]
        pruebas = [("solucion", d["sol"], True)]
        pruebas.append(("blanco", d["celda"].replace("______", "0"), False) if "______" in d["celda"]
                       else ("plantilla", d["celda"], False))
        pruebas += [(f"bien{k}", c, True) for k, c in enumerate(alt.get(ide, {}).get("bien", []))]
        pruebas += [(f"mal{k}", c, False) for k, c in enumerate(alt.get(ide, {}).get("mal", []))]
        for nombre, code, quiere in pruebas:
            ok, msg = await correr(pg, sel, code)
            if ok is None:          # bucle sin fin: la pestaña queda ocupada
                await cargar(pg, url)
            if ok != quiere:
                # un hueco cuya respuesta correcta es 0 sale en verde con «blanco»: es un aviso
                malos += 1
                lineas.append(f"XX {rel} {ide} {nombre}: salió {ok} | {msg}")
    if errores:
        lineas.append(f"XX {rel}: errores de página: {errores[:2]}")
        malos += 1
    await pg.close()
    lineas.append(f"{'ok' if not malos else 'XX'} {rel}: {len(ej)} ejercicios, {malos} problemas")
    return lineas, malos


async def main():
    args = sys.argv[1:]
    alt_dir, paralelo = None, 2
    if "--alt" in args:
        i = args.index("--alt"); alt_dir = pathlib.Path(args[i + 1]); del args[i:i + 2]
    if "--paralelo" in args:
        i = args.index("--paralelo"); paralelo = int(args[i + 1]); del args[i:i + 2]
    rutas = [(RAIZ / a).resolve() for a in args]
    from playwright.async_api import async_playwright
    puerto = servir()
    sem = asyncio.Semaphore(paralelo)   # más de 3 a la vez agota los tiempos de carga
    total = 0
    async with async_playwright() as p:
        nav = await p.chromium.launch()

        async def una(q):
            alt = {}
            if alt_dir:
                f = alt_dir / f"{q.parent.name}-{q.name[:2]}.json"
                if f.exists():
                    alt = json.loads(f.read_text(encoding="utf-8"))
            async with sem:
                return await leccion(nav, puerto, q, alt)

        for lineas, malos in await asyncio.gather(*(una(q) for q in rutas)):
            print("\n".join(lineas))
            total += malos
        await nav.close()
    print(f"lecciones: {len(rutas)}, problemas: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
