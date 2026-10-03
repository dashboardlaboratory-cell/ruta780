#!/usr/bin/env python3
"""Traduce al español los textos de la interfaz de quarto-live en el sitio
generado (post-render de Quarto).

quarto-live trae los botones y avisos en inglés, fijos en su código: unos en
`site_libs/quarto-contrib/live-runtime/live-runtime.js` y otros en los bloques
OJS que cada página lleva codificados en base64. Este script los sustituye
después del render. Si una cadena deja de existir en una versión nueva de la
extensión, el script lo dice y no falla, para no romper la publicación.

Uso (lo llama Quarto al terminar el render):
    python3 post/traduce_live.py
"""
import base64
import os
import pathlib
import re

SALIDA = pathlib.Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))

RUNTIME = [
    ('text:"Run Code"', 'text:"Ejecutar"'),
    ('text:"Start Over"', 'text:"Reiniciar"'),
    ('"Show Hint":"Next Hint"', '"Ver pista":"Siguiente pista"'),
    ('text:"Show Solution"', 'text:"Ver solución"'),
    ('defaultCaption="Python Code"', 'defaultCaption="Código Python"'),
    ('message:"Please replace ______ with valid code."', 'message:"Sustituir ______ por código válido."'),
]
OJS = [
    ("caption: 'Exercise'", "caption: 'Ejercicio'"),
    ("`Downloading Pyodide`", "`Descargando Pyodide`"),
    ("`Downloading package: ${pkg}`", "`Descargando el paquete ${pkg}`"),
    ("`Downloading package: micropip`", "`Descargando el paquete micropip`"),
    ("`Downloading resource: ${name}`", "`Descargando el archivo ${name}`"),
    ("`Pyodide environment setup`", "`Preparando el entorno de Python`"),
]
BLOQUE = re.compile(r'(<script type="ojs-module-contents">\s*)([A-Za-z0-9+/=]+)(\s*</script>)')


def runtime():
    ruta = SALIDA / "site_libs" / "quarto-contrib" / "live-runtime" / "live-runtime.js"
    if not ruta.exists():
        return 0
    t = ruta.read_text(encoding="utf-8")
    hechas = 0
    for a, b in RUNTIME:
        if a in t:
            t = t.replace(a, b); hechas += 1
        elif b not in t:
            print("aviso: no se encontró en live-runtime.js:", a)
    ruta.write_text(t, encoding="utf-8")
    return hechas


def paginas():
    tocadas = 0
    for p in SALIDA.rglob("*.html"):
        t = p.read_text(encoding="utf-8")
        if "ojs-module-contents" not in t:
            continue
        def cambia(m):
            texto = base64.b64decode(m.group(2)).decode("utf-8")
            for a, b in OJS:
                texto = texto.replace(a, b)
            return m.group(1) + base64.b64encode(texto.encode("utf-8")).decode("ascii") + m.group(3)
        nuevo = BLOQUE.sub(cambia, t)
        if nuevo != t:
            p.write_text(nuevo, encoding="utf-8"); tocadas += 1
    return tocadas


if __name__ == "__main__":
    print("traduce_live: %d cadenas en live-runtime.js, %d páginas" % (runtime(), paginas()))
