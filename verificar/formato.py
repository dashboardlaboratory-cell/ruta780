#!/usr/bin/env python3
"""
Cuarto gate: comprueba que cada lección cumple las reglas de escritura de
CLAUDE.md (14 a 21). No mira si el contenido es correcto —de eso se encargan
citas.py y salidas.py— sino si la lección tiene la forma acordada.

Existe porque las lecciones escritas antes del 12-09-2026 siguen otro molde y
hay que reescribirlas. Este script dice cuáles y qué les falta, en vez de
dejarlo a la memoria.

Sale con código 0 siempre: es un informe, no una valla. Para convertirlo en
valla, pasar --estricto y se exige que las lecciones ya migradas no retrocedan.
"""
import json
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# Regla 15: contexto de la empresa. Ninguna de estas palabras entra en una lección.
# «tienda» es ademas el subjuntivo de tender («que el ECM tienda a cero»), asi que
# se descarta cuando va seguido de «a» o «hacia»: ahi es verbo, no sustantivo.
EMPRESA = re.compile(
    r"\b(?:cbtl|coffee bean|multiplaza|sucursal(?:es)?|"
    r"tiendas?(?!\s+(?:al?|hacia)\s)|"
    r"tickets?|baristas?|pedidosya|spoonity|kronos|simphony)\b", re.I)

# Regla 14: registro de libro de texto, no de revista.
#
# Dos vicios que se pueden detectar sin ambigüedad y que se colaron al migrar
# lecciones viejas (lo encontró Luis en matematica/01 el 12-09-2026):
#
#   · la construcción de golpe «no es X: es Y», que la regla prohíbe por su
#     nombre. Las negaciones con «sino» NO entran: «el conjunto de soluciones
#     no es un subespacio sino uno trasladado» es una precisión matemática, no
#     un titular, y esas se dejan pasar a propósito;
#   · la segunda persona, que el molde nuevo no usa en ningún caso.
#
# Solo se mira la prosa: lo que va dentro de una valla ``` es código, y ahí
# «arrastra» es el nombre de una variable, no una orden al lector.
GOLPE = re.compile(r"\b[Nn]o (?:es|son|era|fue|fueron)\b(?![^.;:]*\bsino\b)"
                   r"[^.;:]{3,80}[:,]\s*(?:es|son|era|fue|fueron)\b")
# Solo formas inequívocamente imperativas o de tuteo. «se mira», «quien mira» y
# «mira dónde cae» son tercera persona y NO entran: la primera versión de esta
# expresión las cazaba y daba cuatro falsos positivos.
SEGUNDA_PERSONA = re.compile(
    r"(?:\b[Ff]íjate\b|\b[Rr]etén\b|\b[Dd]etente\b|\b[Ll]éelo\b|\bverás\b|"
    r"\bvas a (?:ver|usar|necesitar|encontrar|hacer)\b|\btus datos\b|\btu tabla\b|"
    r"(?:^|[.:;—]\s)(?:Mira|Arrastra|Dale|Toma|Prueba|Observa)\b)")


def prosa(texto):
    """El texto de la lección sin los bloques de código ni los visuales."""
    fuera, dentro = [], False
    for linea in texto.split("\n"):
        if linea.startswith("```"):
            dentro = not dentro
            continue
        if not dentro:
            fuera.append(linea)
    return fuera


# Lecciones que ya siguen el molde nuevo. El resto está pendiente de reescritura.
MIGRADAS = {
    "estadistica/01-variables-aleatorias.qmd",
    "estadistica/02-pmf-cdf.qmd",
    "estadistica/03-distribuciones-analiticas.qmd",
    "estadistica/04-esperanza-varianza-momentos.qmd",
    "estadistica/05-covarianza-correlacion.qmd",
    "estadistica/06-teorema-central-limite.qmd",
    "estadistica/07-estimacion.qmd",
    "estadistica/08-maxima-verosimilitud.qmd",
    "estadistica/09-intervalos-de-confianza.qmd",
    "estadistica/10-pruebas-de-hipotesis.qmd",
    "estadistica/11-bootstrap.qmd",
    "estadistica/12-normal-multivariante.qmd",
    "estadistica/13-regresion-primeros-principios.qmd",
    "estadistica/14-inferencia-coeficientes.qmd",
    "estadistica/15-datos-faltantes.qmd",
    "estadistica/16-calibracion.qmd",
    "estadistica/17-p-hacking.qmd",
    "estadistica/18-teorema-de-bayes.qmd",
    "estadistica/19-priors-conjugados.qmd",
    "estadistica/20-distribuciones-predictivas.qmd",
    "estadistica/21-comparacion-de-modelos.qmd",
    "estadistica/22-metropolis-hastings.qmd",
    "estadistica/23-gibbs-sampling.qmd",
    "estadistica/24-diagnostico-de-cadenas.qmd",
    "estadistica/25-sintesis-y-casos.qmd",
    "ml/01-aprendizaje-estadistico.qmd",
    "ml/02-diagnostico-regresion.qmd",
    "ml/03-regresion-logistica.qmd",
    "ml/04-modelos-generativos.qmd",
    "ml/05-modelos-lineales-generalizados.qmd",
    "ml/06-validacion-cruzada.qmd",
    "python/01-tipos-y-estructuras.qmd",
    "python/02-funciones-y-scope.qmd",
    "python/03-comprehensions.qmd",
    "python/04-archivos-y-errores.qmd",
    "python/05-entorno-uv-git.qmd",
    "python/06-numpy-primer-contacto.qmd",
    "python/07-ejes-y-reducciones.qmd",
    "python/08-reshape-orden-y-ventanas.qmd",
    "matematica/01-vectores-y-espacios.qmd",
    "matematica/02-matriz-como-transformacion.qmd",
    "matematica/03-espacio-columna.qmd",
    "matematica/04-producto-interno.qmd",
    "matematica/05-proyeccion-ortogonal.qmd",
    "matematica/06-minimos-cuadrados.qmd",
    "matematica/07-gram-schmidt-qr.qmd",
    "matematica/08-determinante.qmd",
    "matematica/09-eigenvalores.qmd",
    "matematica/10-diagonalizacion.qmd",
    "matematica/11-svd.qmd",
    "matematica/12-formas-cuadraticas.qmd",
    "matematica/13-derivada-gradiente.qmd",
    "matematica/14-hessiana-taylor.qmd",
    "matematica/15-convexidad.qmd",
    "matematica/16-descenso-de-gradiente.qmd",
    "matematica/17-metodo-de-newton.qmd",
    "matematica/18-lagrange-kkt.qmd",
}


def bloques_html(texto):
    """Devuelve los visuales completos, agrupando bloques {=html} adyacentes.

    En las lecciones viejas un visual está partido en tres bloques seguidos
    (marcado, <style>, <script>). Quarto los concatena al renderizar, así que
    son un solo visual aunque estén en tres vallas.
    """
    lineas = texto.split("\n")
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
    return grupos, len(tramos)


def revisa(ruta):
    rel = f"{ruta.parent.name}/{ruta.name}"
    t = ruta.read_text(encoding="utf-8")
    faltas = []

    # --- regla 18: hilo explícito ---
    if "{.hilo}" not in t:
        faltas.append("sin bloque .hilo (regla 18)")
    else:
        if "De dónde viene" not in t:
            faltas.append("el .hilo no tiene «De dónde viene» (regla 18)")
        if "Para qué sirve después" not in t:
            faltas.append("el .hilo no tiene «Para qué sirve después» (regla 18)")

    # --- regla 16: tabla de notación ---
    if "{.notacion}" not in t:
        faltas.append("sin tabla ::: {.notacion} (regla 16)")

    # --- regla 5: bloque de fuentes ---
    if "{#fuentes .fuentes}" not in t:
        faltas.append("sin bloque de Fuentes (regla 5)")

    # --- regla 14: registro de libro de texto ---
    n_def = len(re.findall(r"\*\*Definición \d", t))
    n_prop = len(re.findall(r"\*\*(?:Proposición|Teorema) \d", t))
    n_dem = t.count("{.demostracion}")
    if n_def + n_prop == 0:
        faltas.append("sin definiciones ni proposiciones numeradas (regla 14)")
    elif n_prop > 0 and n_dem == 0:
        faltas.append(f"{n_prop} proposiciones y ninguna demostración (regla 14)")

    # --- regla 17: términos marcados para el glosario ---
    marcas = re.findall(r"\[([^\]]+)\]\{\.g(?:\s+data-t=\"([^\"]+)\")?\}", t)
    if not marcas:
        faltas.append("ningún término marcado con {.g} (regla 17)")
    else:
        glos = json.loads((RAIZ / "glosario" / "glosario.json").read_text(encoding="utf-8"))
        claves = {k.lower() for k in glos}
        sueltos = sorted({(b or a).lower() for a, b in marcas} - claves)
        if sueltos:
            faltas.append(f"términos marcados que no están en el glosario: {', '.join(sueltos)}")

    # --- regla 14: registro de libro de texto, no de revista ---
    golpes, tuteos = [], []
    for i, linea in enumerate(prosa(t), 1):
        m = GOLPE.search(linea)
        if m:
            golpes.append(f"línea {i}: «{m.group(0)[:60]}…»")
        m = SEGUNDA_PERSONA.search(linea)
        if m:
            tuteos.append(f"línea {i}: «{m.group(0)}»")
    if golpes:
        faltas.append(f"prosa de golpe «no es X, es Y» (regla 14): {'; '.join(golpes[:3])}")
    if tuteos:
        faltas.append(f"segunda persona (regla 14): {'; '.join(tuteos[:3])}")

    # --- regla 15: cero contexto de la empresa ---
    hallado = sorted({m.group(0).lower() for m in EMPRESA.finditer(t)})
    if hallado:
        faltas.append(f"contexto de empresa (regla 15): {', '.join(hallado)}")

    # --- regla 19: citas con su referencia ---
    for m in re.finditer(r"\{\.cita-libro\}(.*?):::", t, re.S):
        if "{.ref}" not in m.group(1):
            faltas.append("una cita-libro sin su marca {.ref} (regla 19)")
            break

    # --- convención de visuales: un solo bloque {=html} por visual ---
    grupos, n_vallas = bloques_html(t)
    if n_vallas > len(grupos):
        faltas.append(f"{len(grupos)} visual(es) repartidos en {n_vallas} vallas "
                      f"{{=html}}; el molde nuevo usa una sola por visual")

    # --- regla 20: un visual por concepto ---
    if n_def + n_prop >= 4 and len(grupos) == 0:
        faltas.append(f"{n_def + n_prop} resultados y ningún visual (regla 20)")

    return rel, faltas, len(grupos), n_def, n_prop, n_dem


def main():
    estricto = "--estricto" in sys.argv
    lecciones = sorted(p for p in RAIZ.glob("*/[0-9]*.qmd") if p.parent.name != "_templates")

    pendientes, ok, regresiones = [], [], []
    for p in lecciones:
        rel, faltas, nvis, nd, np_, ndem = revisa(p)
        if faltas:
            (regresiones if rel in MIGRADAS else pendientes).append((rel, faltas, nvis, nd, np_))
        else:
            ok.append((rel, nvis, nd, np_, ndem))

    print(f"lecciones revisadas : {len(lecciones)}")
    print(f"al día              : {len(ok)}")
    print(f"por reescribir      : {len(pendientes)}")
    if regresiones:
        print(f"RETROCESOS          : {len(regresiones)}")

    if regresiones:
        print("\n=== RETROCESOS: lecciones ya migradas que han perdido algo ===")
        for rel, faltas, nvis, nd, np_ in regresiones:
            print(f"\n  {rel}")
            for f in faltas:
                print(f"      ✗ {f}")

    if pendientes:
        print("\n=== PENDIENTES DE REESCRITURA ===")
        for rel, faltas, nvis, nd, np_ in pendientes:
            print(f"\n  {rel}   ({nvis} visual(es), {nd} def, {np_} prop)")
            for f in faltas:
                print(f"      · {f}")

    if ok:
        print("\n=== AL DÍA ===")
        for rel, nvis, nd, np_, ndem in ok:
            print(f"  {rel:52s} {nvis} visual(es), {nd} def, {np_} prop, {ndem} dem")

    if estricto and regresiones:
        print(f"\n{len(regresiones)} lección(es) migrada(s) han retrocedido.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
