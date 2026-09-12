# Estado de Ruta 780 y qué sigue

Última actualización: **12-09-2026**, al migrar de Cowork a Claude Code.

`CLAUDE.md` tiene las reglas, que cambian poco. Este archivo tiene el estado y
la lista de trabajo, que cambia cada semana. Si los dos se contradicen, manda
`CLAUDE.md`.

---

## 1. Poner en marcha Claude Code

El repo está en el Mac. Desde la carpeta del repo:

```sh
# Quarto: sin esto no se puede renderizar ni previsualizar
brew install --cask quarto
quarto add r-wasm/quarto-live --no-prompt

# Python: lo que usan los gates
python3 -m pip install numpy playwright
python3 -m playwright install chromium

# comprobar que todo responde
quarto --version
python3 verificar/estructura.py
python3 verificar/citas.py
python3 verificar/salidas.py
python3 verificar/formato.py
python3 verificar/visuales.py
```

`scipy` **no hace falta** y no debe aparecer en ninguna celda: el runner de CI
no lo instala y Pyodide tampoco lo trae por defecto. Cuando una lección necesita
una distribución que no está en numpy, se calcula a mano —la $t$ de Student por
Simpson en `estadistica/09`, la binomial con `log_gamma` en la misma— y se
contrasta contra scipy **fuera** del repo, en un borrador.

### Lo que Cowork no podía hacer y Claude Code sí

Toda esta plataforma se escribió desde Cowork, con el repo montado por el puente
de dispositivos. Dos cosas no se pudieron hacer nunca desde ahí, y son las que
hay que empezar a hacer:

1. **Renderizar.** La VM del puente no tiene Quarto. Las 28 lecciones se
   verificaron con los gates y con Playwright sobre fragmentos extraídos, pero
   **la página completa no se miró nunca en local**: solo la construye el CI.
   Con `quarto preview` se ve al instante. Conviene mirar una lección ya migrada
   entera antes de escribir la siguiente, sobre todo los tooltips del glosario y
   KaTeX, que solo existen en la página real.
2. **Editar sin round-trip.** Cada archivo viajaba por `stage` y `commit`. Eso
   ya escribió una vez una versión vieja de `afirmaciones.json` en silencio, y
   solo se detectó al correr el gate. En local no puede pasar.

---

## 2. Dónde está el trabajo

| Módulo | Publicadas | Total | Al día con el molde |
|---|---|---|---|
| Estadística | 13 | 17 (+8 bayesianas) | 11 de 13 |
| Matemática | 9 | 18 | 2 de 9 |
| Python | 6 | ~12 | 0 de 6 |

- **28 lecciones** publicadas, **13** cumplen el molde nuevo.
- **51 visuales**, todos auditados; ninguno con el fallo de la regla 19b.
- **173 afirmaciones numéricas** declaradas en `verificar/afirmaciones.json`.
- Glosario: **76 términos + 41 símbolos**.
- Índices verificados: Think Stats 3e (75 secciones), MML (80), Think Bayes 2e
  (20 capítulos + cap. 2), McKinney 3E y ISLP (solo capítulos).

Para el estado exacto en cualquier momento:

```sh
python3 verificar/formato.py
```

---

## 3. Lo que sigue, en orden

### 3.1 Terminar Estadística (4 lecciones)

| # | Lección | Depende de | Notas |
|---|---|---|---|
| 14 | Inferencia sobre los coeficientes | Est 12 ✓, Est 13 ✓ | Ya se puede: la $t$ quedó demostrada en la 12 |
| 15 | Datos faltantes: MCAR, MAR, MNAR | Est 13 ✓ | Sin bloqueo |
| 16 | Calibración y curvas de lift | Est 10 ✓ | Sin bloqueo |
| 17 | P-hacking y errores frecuentes | Est 10 ✓ | La Prop 10.9 es el motor; ya está |

La 14 es la siguiente natural: cierra el arco 9 → 12 → 13 → 14.

### 3.2 Reescribir Matemática 01–07

Son las más viejas y las que peor están. Les falta **todo** el molde: sin
`.hilo`, sin tabla de notación, sin definiciones ni proposiciones numeradas,
sin términos marcados para el glosario. Además:

- **Mat 01** y **Mat 03** tienen contexto de la empresa (regla 15).
- **Mat 01–05** tienen el visual partido en tres vallas `{=html}`.

Orden recomendado, que es el de dependencia: **04 → 05 → 06 → 03 → 02 → 01 → 07**.
La 04 (producto interno) y la 05 (proyección ortogonal) son las que más citan
las lecciones nuevas, así que arreglarlas primero paga de inmediato.

### 3.3 Reescribir Python 01–06

Las más alejadas del molde y las que más contexto de empresa arrastran
(`python/03-comprehensions.qmd` es la peor). Ojo: el molde de
definición → proposición → demostración **no encaja** en una lección de
programación. Antes de tocarlas hay que decidir qué significa el molde aquí:
probablemente `.hilo` + notación + glosario sí, y definiciones numeradas no.
**Esa decisión está sin tomar y conviene tomarla con Luis.**

### 3.4 Estadística 01 y 02

Solo les falta juntar los bloques `{=html}` de cada visual en uno. Es mecánico
y no toca el contenido.

---

## 4. Cómo se escribe una lección

El orden importa y está probado. Saltarse el paso 1 es lo que produjo las cinco
citas inventadas de septiembre.

1. **Traer las fuentes primero.** Abrir el capítulo, sacar los títulos de sección
   reales, meterlos en `verificar/indices.json` con su URL y la fecha. Solo
   entonces se puede citar. Si el texto no se puede extraer de forma verificable
   —MML no es descargable—, se cita número y título y **no se pone texto en boca
   del libro**; se dice en el bloque de Fuentes.
2. **Construir los visuales y verificarlos antes de escribir.** Cada visual se
   prueba con Playwright contra numpy o scipy en **todas** las combinaciones de
   sus controles. Varias proposiciones de este plan salieron de aquí: la 8.7
   apareció verificando el visual de la normal.
3. **Escribir la lección** siguiendo el molde. El patrón de referencia es
   `estadistica/04-esperanza-varianza-momentos.qmd`, y los más completos
   `estadistica/12` y `estadistica/13`.
4. **Correr las celdas** y comprobar cada número que la prosa afirma.
5. **Declarar los números** en `verificar/afirmaciones.json`. Usar `contiene`
   solo para salidas reproducibles; `cumple` para todo lo demás.
6. **Glosario**: añadir términos y símbolos nuevos, correr `glosario/build.py`.
7. **Publicar** la lección: fila en el índice del módulo, `data-ids` del módulo
   y de la portada, barra lateral de `_quarto.yml`, `grafo/build_graph.py`.
8. **Los cinco gates**, y `quarto preview` para ver la página de verdad.

```sh
python3 verificar/estructura.py && \
python3 verificar/citas.py     && \
python3 verificar/salidas.py   && \
python3 verificar/formato.py   && \
python3 verificar/visuales.py --estricto
```

---

## 5. Errores que ya se cometieron

No repetirlos sale más barato que volver a encontrarlos.

**Citas inventadas (5).** Los mapeos a *Think Stats* salieron de memoria de la
2ª edición y la 3ª había reorganizado los capítulos. De ahí `citas.py`.

**Ejes que siguen a los datos.** En `estadistica/08` los dos paneles se
reescalaban a la muestra: el botón sorteaba datos nuevos y el dibujo salía
idéntico. Lo encontró Luis usando la página, no ningún test. De ahí la regla 19b
y `visuales.py`. **Comprobar por firma del SVG no basta**: las opacidades
cambiaban y la firma salía distinta aunque nada se moviera.

**Una celda que concluía lo contrario de lo que imprimía.** En `estadistica/07`
el óptimo del encogimiento caía fuera de la rejilla que la propia celda
recorría, y el texto afirmaba lo contrario del resultado. Correr la celda y
**leer su salida** es parte de escribirla.

**Números escritos a ojo.** La potencia de un ejercicio de `estadistica/10` se
escribió 0,9123 cuando era 0,7749; el ángulo de la elipse en `estadistica/12`,
37,98° cuando era 21,51°. Los dos los cazó la celda al correrla.

**Asserts con el índice de columna corrido.** En `estadistica/13` dos
comprobaciones de `afirmaciones.json` apuntaban a la columna equivocada; una
«pasaba» comparando dos signos `=` entre sí. Al escribir un `cumple` con
`split()`, contar las columnas sobre la salida real.

**Correlación serial del PRNG.** El contraejemplo de `estadistica/12` daba
ρ = −0,10 en vez de 0 porque el signo salía del mismo flujo del generador que
los datos. Cuando dos cantidades deben ser independientes, hay que sortearlas de
flujos distintos.

**`np.math` no existe en numpy 2.** Usar `math.erf` de la biblioteca estándar.

**Un `:::` sin cerrar no rompe el render**: Quarto publica la página con el
bloque abierto y no avisa. De ahí `estructura.py`.

**`url()` dentro de un data URI en SCSS**: Quarto lo lee como ruta de archivo y
falla el build. Codificar el SVG en base64.

---

## 6. Decisiones pendientes

- **Qué molde usan las lecciones de Python.** Definición → proposición →
  demostración no encaja en programación. Hay que decidirlo antes de reescribir
  `python/01–06`.
- **Fase 2 y libros sin verificar.** ESL, *Causal Inference for the Brave and
  True* y fast.ai **no son citables** hasta traer sus índices. Think Bayes 2e
  solo tiene verificadas las secciones del capítulo 2; para las lecciones 18–24
  hay que traer el resto.
- **Est 12 y el teorema de Cochran.** Se usa sin demostrar que
  $(n-1)s^2/\sigma^2 \sim \chi^2_{n-1}$. Está declarado en Fuentes. Si alguna
  lección futura lo necesita demostrado, hay que decidir dónde va.
