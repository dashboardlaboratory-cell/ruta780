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

# Lecciones con 0 marcas tras la auditoría del 26-09-2026: --estricto falla si retroceden.
LIMPIAS = [
    "atributos/01-que-hace-un-atributo.qmd",
    "atributos/02-el-proceso-y-la-fuga.qmd",
    "atributos/03-visualizar-para-proponer.qmd",
    "atributos/04-transformaciones-1a1.qmd",
    "atributos/05-escalado-y-centrado.qmd",
    "atributos/06-de-uno-a-muchos.qmd",
    "atributos/07-de-muchos-a-muchos.qmd",
    "atributos/08-categoricas-ficticias.qmd",
    "atributos/09-codificacion-supervisada.qmd",
    "atributos/index.qmd",
    "causal/01-resultados-potenciales.qmd",
    "causal/02-dags-y-puerta-trasera.qmd",
    "causal/05-potencia-y-mde.qmd",
    "causal/07-multi-brazo.qmd",
    "causal/08-interferencia.qmd",
    "causal/16-metalearners.qmd",
    "causal/17-double-machine-learning.qmd",
    "causal/18-r-learner-y-r-score.qmd",
    "causal/21-evaluacion-de-politicas.qmd",
    "causal/index.qmd",
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
    "estadistica/index.qmd",
    "fundamentos/01-valores-nombres-y-tipos.qmd",
    "fundamentos/02-condicionales-y-verdad.qmd",
    "fundamentos/03-el-bucle-while.qmd",
    "fundamentos/04-listas-y-sus-metodos.qmd",
    "fundamentos/05-for-y-range.qmd",
    "fundamentos/06-tuplas-y-desempaquetado.qmd",
    "fundamentos/07-diccionarios.qmd",
    "fundamentos/08-conjuntos.qmd",
    "fundamentos/09-cadenas.qmd",
    "fundamentos/10-funciones.qmd",
    "fundamentos/11-comprehensions.qmd",
    "fundamentos/12-pensar-el-algoritmo.qmd",
    "fundamentos/index.qmd",
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
    "matematica/index.qmd",
    "ml/01-aprendizaje-estadistico.qmd",
    "ml/02-diagnostico-regresion.qmd",
    "ml/03-regresion-logistica.qmd",
    "ml/04-modelos-generativos.qmd",
    "ml/05-modelos-lineales-generalizados.qmd",
    "ml/06-validacion-cruzada.qmd",
    "ml/07-seleccion-de-subconjuntos.qmd",
    "ml/08-ridge-y-lasso.qmd",
    "ml/09-alta-dimension.qmd",
    "ml/10-bases-y-splines.qmd",
    "ml/11-suavizado-y-gams.qmd",
    "ml/12-arboles-de-decision.qmd",
    "ml/13-bagging-bosques-y-boosting.qmd",
    "ml/14-margen-maximo.qmd",
    "ml/15-nucleos-y-perdida-bisagra.qmd",
    "ml/16-redes-neuronales.qmd",
    "ml/17-censura-y-kaplan-meier.qmd",
    "ml/18-riesgos-proporcionales-y-cox.qmd",
    "ml/19-pca.qmd",
    "ml/20-pcr-y-pls.qmd",
    "ml/21-clustering.qmd",
    "ml/22-pruebas-multiples.qmd",
    "ml/23-panorama-supervisado.qmd",
    "ml/24-geometria-minimos-cuadrados.qmd",
    "ml/25-least-angle-regression.qmd",
    "ml/26-metodos-lineales-clasificacion.qmd",
    "ml/27-expansiones-en-base.qmd",
    "ml/28-seleccion-de-modelos.qmd",
    "ml/29-sesgo-varianza-formal.qmd",
    "ml/30-algoritmo-em.qmd",
    "ml/31-aditivos-y-mars.qmd",
    "ml/32-boosting-descenso-funcional.qmd",
    "ml/34-clustering-avanzado.qmd",
    "ml/35-por-que-funciona-random-forest.qmd",
    "ml/36-backpropagation.qmd",
    "ml/37-red-densa-desde-cero.qmd",
    "ml/38-inicializacion-y-activaciones.qmd",
    "ml/39-optimizadores.qmd",
    "ml/40-regularizacion-y-dropout.qmd",
    "ml/41-convolucion-y-vision.qmd",
    "ml/index.qmd",
    "python/01-tipos-y-estructuras.qmd",
    "python/02-funciones-y-scope.qmd",
    "python/03-comprehensions.qmd",
    "python/05-entorno-uv-git.qmd",
    "python/06-numpy-primer-contacto.qmd",
    "python/07-ejes-y-reducciones.qmd",
    "python/08-reshape-orden-y-ventanas.qmd",
    "python/09-pandas-series-dataframe.qmd",
    "python/10-carga-formatos-y-limpieza.qmd",
    "python/11-wrangling-joins-y-reshape.qmd",
    "python/12-groupby-y-agregacion.qmd",
    "python/13-visualizacion.qmd",
    "python/14-series-de-tiempo.qmd",
    "python/15-rendimiento.qmd",
    "python/16-anatomia-de-un-proyecto.qmd",
    "python/17-clases-y-protocolos.qmd",
    "python/18-decoradores.qmd",
    "python/19-tipado-gradual.qmd",
    "python/20-texto-unicode-y-regex.qmd",
    "python/21-sql-desde-python.qmd",
    "python/22-http-y-apis.qmd",
    "python/23-parquet-y-arrow.qmd",
    "python/24-pruebas.qmd",
    "python/25-depuracion.qmd",
    "python/28-datos-que-no-caben.qmd",
    "python/29-categoricos-e-indices.qmd",
    "python/30-zonas-horarias.qmd",
    "python/index.qmd",
    "series/01-descomposicion.qmd",
    "series/02-estacionariedad.qmd",
    "series/03-autocorrelacion.qmd",
    "series/04-arima.qmd",
    "series/05-suavizado-exponencial.qmd",
    "series/06-calendario.qmd",
    "series/07-validacion-temporal.qmd",
    "series/08-boosting.qmd",
    "series/09-prophet.qmd",
    "series/10-jerarquicos.qmd",
    "series/11-evaluacion.qmd",
    "series/index.qmd",
    "index.qmd",
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
