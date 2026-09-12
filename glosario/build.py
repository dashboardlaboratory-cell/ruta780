#!/usr/bin/env python3
"""
Genera, a partir de glosario.json:
  · glosario.js   — el diccionario que lee el tooltip en cada página
  · index.qmd     — la página del glosario completo, ordenada alfabéticamente

Corre en cada build, antes de `quarto render`.
"""
import json
import pathlib
import unicodedata

AQUI = pathlib.Path(__file__).resolve().parent
datos = json.loads((AQUI / "glosario.json").read_text(encoding="utf-8"))
terminos = {k: v for k, v in datos.items() if not k.startswith("_")}


def clave(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return "".join(c for c in t if not unicodedata.combining(c)).strip()


# ── glosario.js ──
js = {clave(k): {"t": k, "d": v["def"], "s": v.get("simbolo", ""), "l": v.get("leccion", "")}
      for k, v in terminos.items()}
(AQUI / "glosario.js").write_text(
    "window.GLOSARIO = " + json.dumps(js, ensure_ascii=False) + ";\n", encoding="utf-8")

# ── index.qmd ──
def orden(k):
    return clave(k)

lineas = [
    "---",
    'title: "Glosario"',
    'subtitle: "Cada término, en una o dos frases, con la lección que lo introduce"',
    "toc: false",
    "engine: markdown",
    "---",
    "",
    "Los mismos textos que aparecen al pasar el cursor sobre un término subrayado en las lecciones. "
    "Son definiciones de trabajo, no las formales: para la formal, la lección.",
    "",
    '```{=html}',
    '<dl class="glosario">',
]
for k in sorted(terminos, key=orden):
    v = terminos[k]
    simb = f' <span class="simb">{v["simbolo"]}</span>' if v.get("simbolo") else ""
    lec = v.get("leccion", "")
    enlace = f' <a class="donde" href="../{lec}.html">{lec.split("/")[1][:2]} · {lec.split("/")[0]}</a>' if lec else ""
    lineas.append(f'<dt id="{clave(k).replace(" ", "-")}">{k}{simb}</dt>')
    lineas.append(f'<dd>{v["def"]}{enlace}</dd>')
lineas += ["</dl>", "```", ""]
(AQUI / "index.qmd").write_text("\n".join(lineas), encoding="utf-8")

print(f"glosario: {len(terminos)} términos → glosario.js, index.qmd")
