# Ruta 780 — reglas de trabajo

Plataforma de estudio de Luis. 86 semanas, 2 h/día. Él estudia; yo construyo.

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

Índices ya verificados (11-09-2026): Think Stats 3e (capítulos + secciones de
1, 5, 6 y 7), Mathematics for ML (completo, del frontmatter de Cambridge),
McKinney 3E (capítulos), ISLP (solo capítulos: statlearning.com no publica los
títulos de sección). Pendientes, y por tanto **no citables** hasta traerlos:
ESL, Think Bayes, Causal Inference for the Brave and True, fast.ai.

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
