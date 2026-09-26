"""Detector de tono (regla 14b). Cuenta, solo en la prosa, los vicios de estilo
que Luis marcó el 26-09-2026: contrastes «no es X sino Y», rayas como conector,
sentencias y metáforas, intensificadores, negrita sobre frases enteras y títulos
que afirman una tesis en vez de nombrar un tema.

Uso:
    python3 verificar/tono.py                 # resumen por módulo
    python3 verificar/tono.py ruta.qmd ...    # detalle línea a línea
    python3 verificar/tono.py --estricto      # falla si una lección de LIMPIAS tiene vicios
"""
import re, sys, pathlib, collections

RAIZ = pathlib.Path(__file__).resolve().parent.parent

VICIOS = {
    "contraste": re.compile(r"\bno (?:es|son|era|está|están|hace|mide|dice|depende|viene|cambia|basta|hay|se|lo|la|le|tiene|sirve|significa|consiste|trata|falla|importa)\b[^.;:\n]{0,90}?\bsino\b|\bno es [^.\n]{2,60}\. (?:Es|Son) ", re.I),
    "raya": re.compile(r"—"),
    "intensificador": re.compile(r"\b(?:exactamente|justo|(?<!valor )de verdad|(?<!longitud )de paso|precisamente|literalmente|simplemente|sin más|de golpe|de siempre|a secas)\b", re.I),
    "sentencia": re.compile(r"\b(?:el cimiento|el piso|el techo|el hallazgo|la moraleja|el secreto|el truco|lo que importa|lo único que|de una línea|la cuenta honesta|lo que se quiere|el precio de|la lección es|la pregunta es|el problema nunca|nunca fue)\b", re.I),
    "valorativo": re.compile(r"\b(?:(?<!árboles )(?<!árbol )(?<!bosques )honest[oa]s?|limpi[oa]s?|barat[oa]s?|ridícul[oa]s?|elegante|brutal|mágic[oa]|obvi[oa]s?|trivialmente)\b", re.I),
}
NEGRITA = re.compile(r"\*\*(.+?)\*\*")
ETIQUETA = re.compile(r"^(?:Definición|Proposición|Procedimiento|Algoritmo|Teorema|Lema|Corolario|Ejemplo|Observación|Modo de falla|Ejercicio|Preguntas|Lo que NO se afirma|Nota de versión|Lo que esta página|Lo que se usa|Lo que viene|Lo que se enuncia|Lo que es mío)\b")
TITULO = re.compile(r"^(#{2,4}) +(.*)$")
TITULO_TESIS = re.compile(r"\b(?:es|son|pone|decide|manda|gana|pierde|miente|engaña|no|sin el cual|nunca|siempre)\b", re.I)

def prosa(texto):
    """Devuelve (numero_de_linea, linea) solo de la prosa."""
    fuera = False; html = False; fm = False; mathblk = False; cita = 0
    for n, l in enumerate(texto.split("\n"), 1):
        if n == 1 and l == "---": fm = True; continue
        if fm:
            if l == "---": fm = False
            continue
        if l.startswith("```"):
            fuera = not fuera; continue
        if fuera: continue
        if l.strip() == "$$": mathblk = not mathblk; continue
        if mathblk or l.strip().startswith("$$"): continue
        if l.startswith("|") or l.startswith("<"): continue
        if l.startswith("[") and "{.item}" in l: continue
        if l.startswith("::: {.cita-libro"): cita = 1; continue
        if cita:
            if l.startswith(":::"): cita = 0
            continue
        yield n, re.sub(r"\$[^$\n]+\$", "§", re.sub(r"`[^`\n]+`", "§", l))

def revisar(ruta):
    halla = []
    for n, l in prosa(ruta.read_text(encoding="utf-8")):
        m = TITULO.match(l)
        if m:
            t = re.sub(r"^\d+(?:\.\d+)*\.? *", "", m.group(2))
            if len(m.group(1)) == 2 and TITULO_TESIS.search(t) and not ETIQUETA.match(t) and not t.startswith(("Ejercicio", "Del libro", "Para el", "Lo que esta lección no")):
                halla.append((n, "título-tesis", t))
        for k, rx in VICIOS.items():
            for x in rx.finditer(l):
                halla.append((n, k, l[max(0, x.start()-40): x.end()+40]))
        for x in NEGRITA.finditer(l):
            if len(x.group(1)) >= 40 and not ETIQUETA.match(x.group(1)):
                halla.append((n, "negrita-frase", x.group(1)[:80]))
    return halla

def lecciones():
    for p in sorted(RAIZ.glob("*/*.qmd")):
        if p.parts[-2] in ("_site", "brain", "_templates", "grafo", "glosario"): continue
        yield p
    yield RAIZ / "index.qmd"

LIMPIAS = [
]

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        for a in args:
            h = revisar(pathlib.Path(a))
            print(f"== {a}: {len(h)}")
            for n, k, t in h: print(f"  {n:5d} {k:15s} {t}")
        return 0
    tot = collections.Counter(); mod = collections.defaultdict(collections.Counter); malas = []
    for p in lecciones():
        c = collections.Counter(k for _, k, _ in revisar(p))
        rel = str(p.relative_to(RAIZ)); tot += c; mod[rel.split("/")[0]] += c
        if rel in LIMPIAS and c: malas.append((rel, dict(c)))
    for m, c in sorted(mod.items()): print(f"{m:12s} {sum(c.values()):6d}  {dict(c)}")
    print(f"{'total':12s} {sum(tot.values()):6d}")
    for rel, c in malas: print("  RETROCEDE", rel, c)
    return 1 if ("--estricto" in sys.argv and malas) else 0

if __name__ == "__main__":
    sys.exit(main())
