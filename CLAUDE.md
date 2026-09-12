# Ruta 780 — reglas de trabajo

Plataforma de estudio de Luis. 86 semanas, 2 h/día. Él estudia; yo construyo.

**Este archivo tiene las reglas, que cambian poco. El estado del proyecto, la
lista de lo que falta y cómo poner el entorno en marcha están en
[`ESTADO.md`](ESTADO.md), que cambia cada semana. Leer los dos antes de empezar.**

Antes de cada commit, los cinco gates:

```sh
python3 verificar/estructura.py && \
python3 verificar/citas.py     && \
python3 verificar/salidas.py   && \
python3 verificar/formato.py   && \
python3 verificar/visuales.py --estricto
```

Y `quarto preview` para ver la página de verdad: los tooltips del glosario y
KaTeX solo existen ahí, no en el `.qmd` ni en un visual suelto.

## Reglas de citación (no negociables)

Estas existen porque ya fallaron. En septiembre de 2026 se publicaron cinco
citas inventadas: los mapeos a *Think Stats* se armaron desde la memoria de la
**2ª edición** y la 3ª había reorganizado los capítulos.

1. **Ninguna pregunta de lectura se escribe sin abrir antes ese capítulo.**
   Nada de "¿qué ejemplo usa el autor?" si no se ha verificado que el ejemplo
   existe en esa edición.
2. **Las referencias llevan el título exacto de la sección**, no solo el número.
   `MML §3.8 *Orthogonal Projections*`, no `MML 3.8`. Un número mal puesto se
   detecta de un clic cuando el título no coincide.
3. **Si una fuente no se puede verificar, no se cita.** Preferir una lección
   autocontenida a una referencia inventada.
4. **Solo bibliografía abierta.** El plan es gratis y open source; citar un
   libro de pago es un callejón sin salida.
5. Cada lección cierra con un bloque `::: {#fuentes .fuentes}` que separa
   *lo que la página demuestra sola* / *lo que viene de los libros* /
   *lo que es mío, no del libro*.

**Esto ya no depende de la disciplina: `verificar/citas.py` lo comprueba en
cada build.** Contrasta el campo `libro:` de cada lección contra
`verificar/indices.json` y falla si el libro no está verificado, si la sección
no existe, o si el título escrito no coincide con el real.

Índices ya verificados (12-09-2026): Think Stats 3e (14 capítulos + 60 secciones
de los capítulos 1–8 y 14), Mathematics for ML (12 capítulos + las 80 secciones,
del índice del PDF oficial), Think Bayes 2e (20 capítulos + las 7 secciones del
cap. 2), McKinney 3E (capítulos), ISLP (solo capítulos: statlearning.com no
publica los títulos de sección). Pendientes, y por tanto **no citables** hasta
traerlos: ESL, Causal Inference for the Brave and True, fast.ai, y las secciones
de los capítulos de Think Bayes distintos del 2.

Tener el índice verificado permite citar **número y título**; no permite citar
texto. Para lo segundo hay que poder extraer el texto de la fuente. Cuando no
se puede —MML no es descargable desde este entorno— la lección lo dice en su
bloque de Fuentes y no pone palabras en boca del libro. Ver `estadistica/08`.

Para añadir un libro: traer su índice de la fuente publicada, meterlo en
`indices.json` con su URL y la fecha, y recién entonces citarlo.

## Reglas de escritura (crítica de Luis, 12-09-2026)

14. **Registro de libro de texto, no de revista.** Definición numerada →
    proposición → demostración → ejemplo. Sin títulos-golpe, sin "no es X,
    es Y", sin "Fíjate", sin párrafos de una línea para efecto, sin
    metáforas apiladas. El molde es `estadistica/04`.
15. **Cero contexto de su empresa.** Nada de CBTL, tiendas, tickets,
    sucursales, Multiplaza, café. Ejemplos neutros y clásicos: dados, pesos
    al nacer, ingresos, los datasets que usan los propios libros.
16. **Todo símbolo se declara** en la tabla `::: {.notacion}` al inicio y
    en su primer uso. `n` = tamaño de la muestra, siempre.
17. **Todo término técnico va al glosario** (`glosario/glosario.json`) y se
    marca en el texto como `[término]{.g}` (o `[flexión]{.g data-t="clave"}`).
18. **Hilo explícito** con `:::: {.hilo}`: *De dónde viene* (lecciones y
    resultados concretos que usa) y *Para qué sirve después* (lecciones y
    métodos concretos que lo necesitan). Nombrados, no vagos.
19. **Citar textualmente, no parafrasear**, en `::: {.cita-libro}` con
    sección y licencia. Think Stats es CC BY-NC-SA: se puede citar con
    libertad. MML, ISLP y McKinney tienen copyright: solo definiciones de
    una o dos frases, con atribución. Si no se puede extraer el texto de
    forma verificable, no se cita y se dice.

19b. **Un control que no mueve el dibujo es un control roto.** Encontrado por
    Luis el 12-09-2026 en `estadistica/08`: los dos paneles reescalaban sus
    ejes a la muestra, así que «Otra muestra» sorteaba datos nuevos y el
    dibujo salía idéntico. **El marco se ancla a la población o a una
    constante, nunca a los datos que se están dibujando.**

    Comprobarlo por firma del SVG NO basta: en ese caso las opacidades
    cambiaban y la firma salía distinta aunque nada se moviera. Hay que medir
    **píxeles del marcador concreto**: un botón de re-sorteo debe dejar su
    marcador principal en posiciones distintas, con recorrido de decenas de
    px. Ver el test de `estadistica/08` (12 posiciones en 12 muestras,
    recorrido 82×106 px).

    Si una cantidad de verdad no depende de los datos, eso es contenido y se
    dice: el panel derecho de `estadistica/08` no se mueve **porque** la
    Proposición 8.7 dice que no puede, y la prosa lo explica.

20. **Un visual por concepto que lo admita, no uno por página.** Si una
    definición o una proposición se puede ver, se ve. `estadistica/04` tiene
    cuatro: esperanza como promedio ponderado sobre una viga, varianza como
    área de cuadrados, media contra mediana con fulcro, y el sesgo de n vs
    n−1 acumulando muestras. Un visual que solo decora no entra.
21. **Todo símbolo que aparezca en una fórmula está en
    `glosario/glosario.json` con `"tipo": "simbolo"`.** El tooltip se engancha
    solo sobre lo que KaTeX renderiza; basta con que la entrada exista.

## Reglas de números

6. **Todo número que la prosa afirme se declara en `verificar/afirmaciones.json`.**
   `python3 verificar/salidas.py` corre las celdas y falla el build si deja de
   cuadrar.
7. **Nunca citar dígitos de un cálculo numéricamente inestable.** Cancelación
   catastrófica, pérdida de ortogonalidad y similares dan resultados distintos
   en cada máquina y en el navegador. Afirmar el orden de magnitud o la
   propiedad, y declararla en `afirmaciones.json` bajo `cumple`, no `contiene`.

## Reglas de construcción

22. **`verificar/formato.py` dice si una lección cumple el molde** (reglas 14 a
    21) y separa las que ya están migradas de las que siguen el molde viejo.
    Cuando se termina de reescribir una, se añade a la lista `MIGRADAS` de ese
    archivo: a partir de ahí, `--estricto` falla si retrocede.

    Desde el 12-09-2026 comprueba además dos vicios de la regla 14 sobre la
    **prosa** —nunca sobre el código—: la construcción de golpe «no es X, es Y»
    y la segunda persona. Las negaciones con «sino» se dejan pasar a propósito,
    porque suelen ser precisiones matemáticas («no es un subespacio sino uno
    trasladado») y no titulares.

23. **`verificar/visuales.py` comprueba la regla 19b en píxeles.** Acciona cada
    control de cada visual y mide cuánto se desplaza la geometría, trazo a
    trazo. Si un control de verdad no debe mover nada porque la cantidad que
    representa no depende de los datos, se declara en `QUIETOS` con su razón
    **y la lección tiene que explicarlo en la prosa**.

    Requiere Playwright. Si no está instalado, el gate se salta con un aviso en
    vez de fallar, para que el CI no se rompa; pero en local hay que instalarlo.


8. **`python3 verificar/estructura.py` antes de cada commit.** Una valla
    `:::` sin cerrar no rompe el render: Quarto publica la página con el
    bloque abierto y todo lo demás dentro. Corre también en CI.
9. **Verificar cada visual sin navegador antes de publicar**: extraer los
   bloques ` ```{=html} `, montar un HTML suelto, correrlo con Playwright y
   comprobar cero `pageerror` y las lecturas de todos los presets.
10. **Nada que pueda dejar contenido invisible.** Sin animaciones de entrada
   con `opacity: 0`: si el observer no dispara, el índice desaparece. Ya pasó.
11. **Widgets siempre dentro de ` ```{=html} `**, o Quarto los renderiza como
    texto literal.
12. `engine: markdown` en el frontmatter de **cada** `.qmd`; a nivel de
    proyecto no se propaga.
13. **Nada de `url()` dentro de un data URI en el SCSS**: Quarto escanea el CSS
    compilado y lo toma por una ruta de archivo. Usar base64.
14. **Datos de CBTL jamás al repo.** Es público. Datos públicos o sintéticos.

## Dónde está cada cosa

- `verificar/` — el verificador de salidas y las afirmaciones declaradas
- `verificacion.qmd` — la página que le explica a Luis qué puede comprobar él
- `grafo/build_graph.py` — grafo desde el frontmatter, corre en cada build
- `brain/` — vault de Obsidian, no se renderiza
- `proyectos/notebooks/F1-retos.ipynb` — una sección por lección publicada
