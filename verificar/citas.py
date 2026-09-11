#!/usr/bin/env python3
"""
Comprueba que toda referencia bibliográfica de una lección existe de verdad.

Lee el campo `libro:` del frontmatter de cada lección y lo contrasta contra
verificar/indices.json, que contiene los índices traídos de la fuente publicada
de cada libro. Falla el build si:

  · se cita un libro cuyo índice no se ha verificado todavía
  · se cita una sección o capítulo que no existe en ese índice
  · el título escrito no coincide con el título real de esa sección

Existe porque en septiembre de 2026 se publicaron cinco citas inventadas: los
mapeos a Think Stats salieron de memoria de la 2ª edición y la 3ª había
reorganizado los capítulos. Un número de sección mal puesto es invisible; un
título que no coincide, no.
"""
import json
import pathlib
import re
import sys
import unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
IDX = json.loads((RAIZ / "verificar" / "indices.json").read_text(encoding="utf-8"))
LIBROS = {k: v for k, v in IDX.items() if not k.startswith("_")}

# alias → clave canónica, del más largo al más corto para que "Think Stats 3e"
# gane sobre "Think Stats"
ALIAS = {}
for clave, datos in LIBROS.items():
    ALIAS[clave] = clave
    for a in datos.get("alias", []):
        ALIAS[a] = clave
ORDEN = sorted(ALIAS, key=len, reverse=True)

REF = re.compile(
    r"(?P<libro>" + "|".join(re.escape(a) for a in ORDEN) + r")\s*"
    r"(?:(?P<tipo>§|cap\.\s*)\s*(?P<num>\d+(?:\.\d+)?)"
    r"(?:\s*[–-]\s*(?P<hasta>\d+(?:\.\d+)?))?"
    r"(?P<titulo>[^·§]*))?"
)


def normalizar(t):
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def rango(a, b):
    """Expande 3.1–3.4 o 2–4 a la lista de números intermedios."""
    if b is None:
        return [a]
    if "." in a and "." in b:
        ca, ia = a.split("."); cb, ib = b.split(".")
        if ca == cb:
            return [f"{ca}.{i}" for i in range(int(ia), int(ib) + 1)]
        return [a, b]
    if "." not in a and "." not in b:
        return [str(i) for i in range(int(a), int(b) + 1)]
    return [a, b]


def revisar(campo, donde, fallos):
    if campo.strip() in ("", "—", "-"):
        return 0
    vistos = 0
    reconocido = False
    for m in REF.finditer(campo):
        reconocido = True
        libro = ALIAS[m.group("libro")]
        datos = LIBROS[libro]
        if m.group("num") is None:
            continue
        es_seccion = "." in m.group("num")
        tabla = datos["secciones"] if es_seccion else datos["capitulos"]
        for num in rango(m.group("num"), m.group("hasta")):
            vistos += 1
            if num not in tabla:
                que = "sección" if es_seccion else "capítulo"
                if es_seccion and not datos["secciones"]:
                    fallos.append(
                        f"{donde}: «{libro} §{num}» — de ese libro solo hay índice a nivel de "
                        f"capítulo. Trae los títulos de sección antes de citarla."
                    )
                else:
                    fallos.append(f"{donde}: «{libro}» no tiene {que} {num} en el índice verificado")
                continue
            escrito = normalizar(m.group("titulo") or "")
            real = normalizar(tabla[num])
            if escrito and escrito not in real and real not in escrito:
                fallos.append(
                    f"{donde}: «{libro} {num}» lo titulas «{m.group('titulo').strip()}» "
                    f"y en el libro es «{tabla[num]}»"
                )
    if not reconocido:
        fallos.append(
            f"{donde}: «{campo.strip()}» no cita ningún libro con índice verificado. "
            f"Conocidos: {', '.join(sorted(LIBROS))}"
        )
    return vistos


def main():
    lecciones = sorted(
        p for p in RAIZ.glob("*/[0-9]*.qmd") if p.parent.name != "_templates"
    )
    fallos = []
    refs = 0
    for p in lecciones:
        texto = p.read_text(encoding="utf-8")
        m = re.search(r'^libro:\s*"(.*)"\s*$', texto, re.M)
        if not m:
            fallos.append(f"{p.parent.name}/{p.name}: sin campo `libro:` en el frontmatter")
            continue
        refs += revisar(m.group(1), f"{p.parent.name}/{p.name}", fallos)

    print(f"lecciones revisadas  : {len(lecciones)}")
    print(f"referencias contrastadas: {refs}")
    print(f"libros con índice verificado: {', '.join(sorted(LIBROS))}")

    if fallos:
        print(f"\n{len(fallos)} FALLO(S):")
        for f in fallos:
            print("  ✗", f)
        return 1
    print("\nTodas las citas existen y los títulos coinciden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
