#!/usr/bin/env python3
"""
Quinto gate: comprueba que los visuales funcionan y que sus controles MUEVEN
el dibujo (regla 19b de CLAUDE.md).

Existe por un fallo que encontró Luis el 12-09-2026 en estadistica/08: los dos
paneles reescalaban sus ejes a la muestra, así que el botón «Otra muestra»
sorteaba datos nuevos y el dibujo salía idéntico. El control funcionaba; lo que
no hacía era notarse.

Lo importante y lo que costó aprender: **comprobar por firma del SVG no basta**.
En aquel caso las opacidades del mapa de calor cambiaban y la firma salía
distinta aunque nada se moviera en pantalla. Por eso este script mide dos cosas:

  1. que cada control produzca estados distintos (firma), y
  2. que la geometría se DESPLACE: se compara trazo a trazo, por índice, cuántos
     píxeles se mueve cada línea, círculo, rectángulo y curva entre un estado y
     otro. El marco fijo aporta cero; basta con que un trazo se mueva.

Si un control de verdad no cambia el dibujo porque la cantidad que representa no
depende de los datos, eso es contenido y se declara en QUIETOS, con su razón, y
la lección tiene que explicarlo.

Uso:
    python3 verificar/visuales.py              # informe completo
    python3 verificar/visuales.py --estricto   # falla el build si algo está roto
    python3 verificar/visuales.py estadistica/08-maxima-verosimilitud.qmd

Requiere playwright:
    python3 -m pip install playwright && python3 -m playwright install chromium
"""
import asyncio
import hashlib
import io
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TMP = RAIZ / "verificar" / "_visual_tmp.html"

# Variables del tema, para que el visual se dibuje igual que en la página.
CSS = """<style>:root{--r-linea:#ddd;--r-acento:#0F6E68;--r-tinta:#1a1a1a;
--r-tinta-suave:#555;--r-fondo:#fff;--bs-font-monospace:monospace;}
body{font-family:system-ui;margin:16px;max-width:860px}</style>"""

# Controles cuyo efecto es deliberadamente invisible. Cada uno con su razón:
# si un control está aquí, la lección tiene que explicar por qué no se mueve.
QUIETOS = {
    # estadistica/08: el panel derecho está en unidades de sigma sombrero, y ahí
    # la curva no depende de los datos. Es la Proposición 8.7 dibujada.
    ("estadistica/08-maxima-verosimilitud.qmd", "nv-rastro"):
        "el rastro solo existe tras pulsar «Otra muestra»",
}

JS_FIRMA = """(sel) => {
  const svg = document.querySelector(sel);
  if (!svg) return "SIN-SVG";
  const out = [];
  for (const e of svg.querySelectorAll('*')) {
    const a = [];
    for (const t of ['d','x','y','cx','cy','r','x1','y1','x2','y2','width','height',
                     'points','transform','fill','stroke','fill-opacity','opacity']) {
      const v = e.getAttribute(t);
      if (v !== null) a.push(t + '=' + v);
    }
    out.push(e.tagName + '{' + a.join(',') + '}');
  }
  return out.join('|');
}"""

# Posicion de CADA elemento dibujado, en el orden en que se creo. Al redibujar,
# los elementos se recrean en el mismo orden, asi que comparar por indice dice
# cuanto se ha movido cada trazo.
#
# La primera version de esto miraba solo circulos de radio >= 3, y daba falsos
# positivos en todo visual que dibuje con lineas o con puntos finos. La segunda
# miraba centroides y cajas, y los ahogaba el marco fijo. Por elemento es lo que
# funciona: si CUALQUIER trazo se mueve, el dibujo se mueve.
JS_MARCAS = """(sel) => {
  const svg = document.querySelector(sel);
  if (!svg) return [];
  const p = [];
  for (const e of svg.querySelectorAll('circle,line,rect,path')) {
    const g = (a) => parseFloat(e.getAttribute(a));
    switch (e.tagName) {
      case 'circle': p.push([g('cx'), g('cy')]); break;
      case 'line':   p.push([(g('x1') + g('x2')) / 2, (g('y1') + g('y2')) / 2]); break;
      case 'rect':   p.push([g('x') + (g('width') || 0) / 2,
                             g('y') + (g('height') || 0) / 2]); break;
      default: {
        const n = (e.getAttribute('d') || '').match(/-?\\d+(?:\\.\\d+)?/g);
        if (n && n.length >= 2) {
          p.push([+n[0], +n[1]]);
          const h = Math.floor(n.length / 4) * 2;
          if (h + 1 < n.length) p.push([+n[h], +n[h + 1]]);
          p.push([+n[n.length - 2], +n[n.length - 1]]);
        }
      }
    }
  }
  return p.filter(q => isFinite(q[0]) && isFinite(q[1]));
}"""

JS_CTRL = """() => [...document.querySelectorAll('input,select,button')]
  .filter(e => e.id)
  .map(e => ({tag: e.tagName.toLowerCase(), id: e.id, tipo: e.type || '',
              min: e.min || '', max: e.max || '',
              ops: e.tagName === 'SELECT' ? [...e.options].map(o => o.value) : null,
              txt: (e.textContent || '').trim().slice(0, 24)}))"""

# El valor con el que arrancó la página: option[selected] o defaultValue/defaultChecked,
# nunca el .value actual. Sirve para devolver los demás controles a un estado no
# degenerado antes de probar un botón (ver JS_CTRL y la restauración en audita()).
JS_DEFAULTS = """() => {
  const out = {};
  document.querySelectorAll('input,select').forEach(e => {
    if (!e.id) return;
    if (e.tagName === 'SELECT') {
      const opt = e.querySelector('option[selected]') || e.options[0];
      out[e.id] = opt ? opt.value : '';
    } else if (e.type === 'checkbox') {
      out[e.id] = e.defaultChecked ? '1' : '0';
    } else {
      out[e.id] = e.defaultValue;
    }
  });
  return out;
}"""

RESORTEO = re.compile(r"otra|nueva|tanda|muestra|remuestre|genera|mil|cien", re.I)


def visuales(ruta):
    """Los visuales completos de una lección, agrupando bloques {=html} adyacentes."""
    lineas = ruta.read_text(encoding="utf-8").split("\n")
    tramos, i = [], 0
    while i < len(lineas):
        if lineas[i].strip() == "```{=html}":
            j = i + 1
            while j < len(lineas) and lineas[j].strip() != "```":
                j += 1
            tramos.append((i, j, "\n".join(lineas[i + 1:j])))
            i = j + 1
        else:
            i += 1
    grupos, actual, ultimo = [], [], None
    for ini, fin, txt in tramos:
        if actual and ini - ultimo <= 2:
            actual.append(txt)
        else:
            if actual:
                grupos.append("\n".join(actual))
            actual = [txt]
        ultimo = fin
    if actual:
        grupos.append("\n".join(actual))
    return grupos


async def estable(pg, sel, tope_ms=3000):
    """Espera a que el dibujo deje de cambiar. Hay visuales que tardan ~1 s."""
    import time
    t0 = time.time()
    prev = await pg.evaluate(JS_FIRMA, sel)
    while (time.time() - t0) * 1000 < tope_ms:
        await pg.wait_for_timeout(180)
        ahora = await pg.evaluate(JS_FIRMA, sel)
        if ahora == prev:
            return ahora, (time.time() - t0) * 1000
        prev = ahora
    return prev, tope_ms


def recorrido(marcas):
    """El mayor desplazamiento que sufre un mismo trazo entre estados, en píxeles.

    Se compara por índice: el trazo k del estado A contra el trazo k del estado B.
    El marco fijo no se mueve y aporta cero; basta con que UN trazo se desplace
    para que el dibujo se note distinto. Ese es el criterio de la regla 19b.
    """
    utiles = [m for m in marcas if m]
    if len(utiles) < 2:
        return 0.0
    n = min(len(m) for m in utiles)
    if n == 0:
        # ningún estado dibuja nada, o el número de trazos cambia tanto que no
        # hay con qué comparar; que cambie el número ya es movimiento visible
        return 999.0 if len({len(m) for m in utiles}) > 1 else 0.0
    peor = 0.0
    for k in range(n):
        xs = [m[k][0] for m in utiles]
        ys = [m[k][1] for m in utiles]
        peor = max(peor, max(xs) - min(xs), max(ys) - min(ys))
    # si además cambia el número de trazos, el dibujo cambia de forma
    if len({len(m) for m in utiles}) > 1:
        peor = max(peor, 999.0)
    return peor


async def audita(pg, html, rel, idx, fallos, avisos, notas):
    TMP.write_text("<!doctype html><meta charset='utf-8'>" + CSS + html, encoding="utf-8")
    errs = []
    pg.once("pageerror", lambda e: errs.append(str(e)))
    await pg.goto("file://" + str(TMP))
    await pg.wait_for_timeout(400)

    etiqueta = f"{rel} [visual {idx}]"
    m = re.search(r'<svg id="([^"]+)"', html)
    if not m:
        if "<svg" in html:
            avisos.append((etiqueta, "-", "el svg no tiene id; no se puede auditar"))
        return
    sel = "#" + m.group(1)
    ctrls = await pg.evaluate(JS_CTRL)
    if not ctrls:
        notas.append((etiqueta, "-", "visual estático, sin controles"))
        return

    # despertar los visuales que arrancan vacíos
    for c in ctrls:
        if c["tag"] == "button" and RESORTEO.search(c["txt"]):
            try:
                await pg.click("#" + c["id"])
            except Exception:
                pass
    _, ms = await estable(pg, sel)
    if ms > 1500:
        avisos.append((etiqueta, "-", f"lento: {ms:.0f} ms por redibujo"))

    botones = []
    for c in ctrls:
        cid, firmas, marcas = c["id"], set(), []
        if (rel, cid) in QUIETOS:
            notas.append((etiqueta, cid, "quieto a propósito: " + QUIETOS[(rel, cid)]))
            continue
        try:
            if c["tag"] == "select" and c["ops"]:
                for v in c["ops"]:
                    await pg.select_option("#" + cid, v)
                    f, _ = await estable(pg, sel)
                    firmas.add(f)
                    marcas.append(await pg.evaluate(JS_MARCAS, sel))
            elif c["tipo"] == "range":
                lo, hi = float(c["min"] or 0), float(c["max"] or 1)
                for k in range(4):
                    v = lo + k * (hi - lo) / 3
                    await pg.eval_on_selector("#" + cid,
                        "(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));"
                        "e.dispatchEvent(new Event('change',{bubbles:true}))}", str(v))
                    f, _ = await estable(pg, sel)
                    firmas.add(f)
                    marcas.append(await pg.evaluate(JS_MARCAS, sel))
            elif c["tipo"] == "checkbox":
                for v in ["1", "0"]:
                    await pg.eval_on_selector("#" + cid,
                        "(e,v)=>{e.checked=(v=='1');e.dispatchEvent(new Event('change',{bubbles:true}))}", v)
                    f, _ = await estable(pg, sel)
                    firmas.add(f)
            elif c["tag"] == "button":
                botones.append(c)
                continue
            else:
                continue
        except Exception as e:
            fallos.append((etiqueta, cid, f"error al accionarlo: {str(e)[:60]}"))
            continue

        if len(firmas) <= 1:
            fallos.append((etiqueta, cid, "no cambia nada el dibujo"))
        elif marcas and recorrido(marcas) < 2.0 and c["tipo"] == "range":
            avisos.append((etiqueta, cid,
                           f"los marcadores apenas se mueven ({recorrido(marcas):.1f} px): "
                           "¿el eje está siguiendo a los datos? (regla 19b)"))

    # Antes de probar los botones, devolver selects y ranges a su valor por
    # defecto. Barrer un select hasta su última opción o un range hasta su
    # máximo puede dejar la página en una esquina degenerada del espacio de
    # parámetros —una matriz sin eigenvectores reales, un efecto tan grande
    # que el p-valor ya es cero en todos los casos— donde un botón que SÍ
    # mueve el dibujo en cualquier estado normal no tiene nada que mover. Esa
    # esquina no es un control roto: es el test midiendo en el punto
    # equivocado. Probar los botones desde el estado inicial de la página es
    # lo que de verdad corresponde a cómo se usa el visual.
    defaults = await pg.evaluate(JS_DEFAULTS)
    for c in ctrls:
        cid = c["id"]
        if c["tag"] == "button" or cid not in defaults:
            continue
        val = defaults[cid]
        try:
            if c["tag"] == "select":
                await pg.select_option("#" + cid, val)
            elif c["tipo"] == "checkbox":
                await pg.eval_on_selector("#" + cid,
                    "(e,v)=>{e.checked=(v=='1');e.dispatchEvent(new Event('change',{bubbles:true}))}", val)
            else:
                await pg.eval_on_selector("#" + cid,
                    "(e,v)=>{e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));"
                    "e.dispatchEvent(new Event('change',{bubbles:true}))}", val)
        except Exception:
            pass
    await estable(pg, sel)

    # Botones. Los de re-sorteo son los que la regla 19b vigila de cerca: tienen
    # que dejar el marcador principal en sitios distintos, no solo cambiar cifras.
    for c in botones:
        cid = c["id"]
        if (rel, cid) in QUIETOS:
            notas.append((etiqueta, cid, "quieto a propósito: " + QUIETOS[(rel, cid)]))
            continue
        try:
            if RESORTEO.search(c["txt"]):
                firmas, marcas = set(), []
                for _ in range(6):
                    await pg.click("#" + cid)
                    f, _ = await estable(pg, sel)
                    firmas.add(f)
                    marcas.append(await pg.evaluate(JS_MARCAS, sel))
                rec = recorrido(marcas)
                if len(firmas) <= 1:
                    fallos.append((etiqueta, cid, "«re-sortear» no cambia nada"))
                elif rec < 4.0:
                    fallos.append((etiqueta, cid,
                                   f"«re-sortear» cambia cifras pero el marcador solo se mueve "
                                   f"{rec:.1f} px: el marco está siguiendo a los datos (regla 19b)"))
            else:
                # reset y similares: mover algo antes, y ver si el botón lo revierte.
                # Subir los ranges al máximo no basta: si uno de ellos limpia el
                # estado como efecto lateral (p. ej. cambiar λ invalida las esperas
                # acumuladas), el "antes" queda vacío y el reset no tiene nada que
                # revertir. Un botón de re-sorteo, si lo hay, sí genera contenido
                # real sin ese efecto lateral — se pulsa después, para que quede
                # la última palabra antes de medir "antes".
                for d in ctrls:
                    if d["tipo"] == "range":
                        await pg.eval_on_selector("#" + d["id"],
                            "(e)=>{e.value=e.max;e.dispatchEvent(new Event('input',{bubbles:true}))}")
                for d in botones:
                    if RESORTEO.search(d["txt"]):
                        try:
                            await pg.click("#" + d["id"])
                        except Exception:
                            pass
                antes, _ = await estable(pg, sel)
                await pg.click("#" + cid)
                uno, _ = await estable(pg, sel)
                await pg.click("#" + cid)
                dos, _ = await estable(pg, sel)
                if antes == uno:
                    fallos.append((etiqueta, cid, "no hace nada al pulsarlo"))
                elif uno != dos:
                    avisos.append((etiqueta, cid, "no es idempotente: dos clics dan dos estados"))
        except Exception as e:
            fallos.append((etiqueta, cid, f"error al accionarlo: {str(e)[:60]}"))

    if errs:
        fallos.append((etiqueta, "-", f"ERROR DE JAVASCRIPT: {errs[0][:80]}"))


async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    estricto = "--estricto" in sys.argv
    if args:
        rutas = [RAIZ / a for a in args]
    else:
        rutas = sorted(p for p in RAIZ.glob("*/[0-9]*.qmd") if p.parent.name != "_templates")

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("playwright no está instalado. Este gate se salta.")
        print("  python3 -m pip install playwright && python3 -m playwright install chromium")
        return 0

    fallos, avisos, notas = [], [], []
    n_vis = 0
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page()
        for ruta in rutas:
            if not ruta.exists():
                continue
            rel = f"{ruta.parent.name}/{ruta.name}"
            for i, h in enumerate(visuales(ruta)):
                n_vis += 1
                await audita(pg, h, rel, i, fallos, avisos, notas)
        await b.close()
    if TMP.exists():
        TMP.unlink()

    print(f"lecciones revisadas : {len(rutas)}")
    print(f"visuales auditados  : {n_vis}")
    print(f"fallos              : {len(fallos)}")
    print(f"avisos              : {len(avisos)}")

    if fallos:
        print("\n=== FALLOS ===")
        for e, c, m in fallos:
            print(f"  ✗ {e:44s} {c:14s} {m}")
    if avisos:
        print("\n=== AVISOS ===")
        for e, c, m in avisos:
            print(f"  · {e:44s} {c:14s} {m}")
    if notas:
        print("\n=== NOTAS ===")
        for e, c, m in notas:
            print(f"    {e:44s} {c:14s} {m}")

    if not fallos:
        print("\nTodos los controles mueven el dibujo.")
    if estricto and fallos:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
