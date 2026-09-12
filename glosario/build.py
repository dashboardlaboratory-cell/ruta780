#!/usr/bin/env python3
"""
Genera, a partir de glosario.json:
  · glosario.js   — diccionario de términos y de símbolos para los tooltips
  · index.qmd     — la página del glosario, en dos secciones

Corre en cada build, antes de `quarto render`.
"""
import json
import pathlib
import unicodedata

AQUI = pathlib.Path(__file__).resolve().parent
datos = json.loads((AQUI / "glosario.json").read_text(encoding="utf-8"))
entradas = {k: v for k, v in datos.items() if not k.startswith("_")}
terminos = {k: v for k, v in entradas.items() if v.get("tipo", "termino") == "termino"}
simbolos = {k: v for k, v in entradas.items() if v.get("tipo") == "simbolo"}


def clave(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c)).strip()


# ── glosario.js ──
js_t = {clave(k): {"t": k, "d": v["def"], "s": v.get("simbolo", ""), "l": v.get("leccion", "")}
        for k, v in terminos.items()}
# los símbolos se buscan por el carácter tal cual, sin normalizar: μ y m son distintos
js_s = {k: {"t": k, "d": v["def"], "s": v.get("lee", ""), "l": v.get("leccion", "")}
        for k, v in simbolos.items()}
(AQUI / "glosario.js").write_text(
    "window.GLOSARIO = " + json.dumps(js_t, ensure_ascii=False) + ";\n"
    "window.GLOSARIO_SIMBOLOS = " + json.dumps(js_s, ensure_ascii=False) + ";\n",
    encoding="utf-8")

# ── index.qmd ──
def fila(k, v, es_simbolo):
    extra = v.get("lee") if es_simbolo else v.get("simbolo")
    marca = f' <span class="simb">{extra}</span>' if extra else ""
    lec = v.get("leccion", "")
    if lec:
        mod, arch = lec.split("/")
        enlace = f' <a class="donde" href="../{lec}.html">{mod} {arch[:2]}</a>'
    else:
        enlace = ""
    cls = ' class="es-simbolo"' if es_simbolo else ""
    return (f'<dt id="g-{clave(k).replace(" ", "-")}"{cls}>{k}{marca}</dt>',
            f'<dd>{v["def"]}{enlace}</dd>')

L = ["---", 'title: "Glosario"',
     'subtitle: "Términos y símbolos, con la lección donde se introducen"',
     "toc: true", "engine: markdown", "---", "",
     "Los mismos textos que aparecen al pasar el cursor sobre un término subrayado o sobre un "
     "símbolo de una fórmula. Son definiciones de trabajo: para la definición formal, la lección.",
     "", "## Símbolos", "", "```{=html}", '<dl class="glosario simbolos">']
for k in sorted(simbolos, key=lambda x: (len(x), clave(x))):
    L.extend(fila(k, simbolos[k], True))
L += ["</dl>", "```", "", "## Términos", "", "```{=html}", '<dl class="glosario">']
for k in sorted(terminos, key=clave):
    L.extend(fila(k, terminos[k], False))
L += ["</dl>", "```", ""]
(AQUI / "index.qmd").write_text("\n".join(L), encoding="utf-8")

print(f"glosario: {len(terminos)} términos + {len(simbolos)} símbolos → glosario.js, index.qmd")
