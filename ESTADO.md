# Estado de Ruta 780 y qué sigue

Última actualización: **12-09-2026**, tras publicar Estadística 15, 16 y 17 y
reescribir las nueve lecciones de Matemática desde Claude Code. **Estadística y
Matemática quedan completas y al día con el molde nuevo**; lo único que sigue
en el molde viejo son las seis lecciones de Python.

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
| Estadística | 17 | 17 (+8 bayesianas) | **17 de 17** |
| Matemática | 9 | 18 | **9 de 9** |
| Python | 6 | ~12 | 0 de 6 |

- **32 lecciones** publicadas, **26** cumplen el molde nuevo.
- **60 visuales**, todos auditados; ninguno con el fallo de la regla 19b.
- **332 afirmaciones numéricas** declaradas en `verificar/afirmaciones.json`.
- Glosario: **126 términos + 41 símbolos**.
- Lo único que queda en el molde viejo son `python/01` a `python/06`, y están
  detrás de la decisión del punto 6.
- Índices verificados: Think Stats 3e (75 secciones), MML (80), Think Bayes 2e
  (20 capítulos + cap. 2), McKinney 3E (capítulos + las 6 secciones del cap. 7,
  traídas el 12-09-2026) e ISLP (solo capítulos).

Para el estado exacto en cualquier momento:

```sh
python3 verificar/formato.py
```

---

## 3. Lo que sigue, en orden

### 3.1 Estadística fase 1: terminada

Las tres últimas se publicaron el 12-09-2026 desde Claude Code.

**Est 15 (Datos faltantes).** El eje es la Proposición 15.5,
$E[Y|R=1]-E[Y] = \text{Cov}(Y,R)/P(R=1)$: de ahí salen MCAR (covarianza cero,
solo cuesta precisión), MAR (la ley de $Y$ dado $X$ se conserva, así que la
regresión sobrevive y la media marginal no) y la reponderación por $1/q(X)$ con
positividad. Después, que rellenar con la media multiplica $s^2$ por
$(m-1)/(n-1)$ y hunde la cobertura del 95 % al 76 % **con datos MCAR**, y que
MNAR no es identificable: dos poblaciones con datos observados idénticos y
medias separadas por 484 unidades. Tres visuales.

**Est 16 (Calibración y lift).** Autocontenida: ningún libro con índice
verificado trata el tema, así que `libro: "—"` y se dice en Fuentes. Brier como
regla propia, la descomposición calibración − resolución + incertidumbre, el
techo del lift $\min(1/u, 1/\bar{y})$, y el resultado que une las dos mitades:
una transformación creciente no cambia ni el lift ni la resolución, solo la
calibración —de donde recalibrar por isotónica es gratis y lleva el Brier a su
suelo, incertidumbre − resolución—. Tres visuales; en el tercero el panel de la
derecha no se mueve **porque la Proposición 16.10 dice que no puede**, y la
prosa lo explica.

**Est 17 (P-hacking).** El menor de $m$ valores p es $\text{Beta}(1,m)$ con
media $1/(m+1)$: con $m=20$ el «hallazgo» es el valor esperado del
procedimiento. Bonferroni por Boole (sin independencia), Holm demostrado en un
párrafo y dominando a Bonferroni, BH enunciado con la demostración solo del caso
$m_0=m$ —el resto declarado en Fuentes—, y el vistazo repetido: del 5 % al 35 %
mirando entre $n=20$ y $n=400$. Tres visuales.

Quedan **Estadística 18–24, las bayesianas**, y están bloqueadas: de Think Bayes
2e solo se verificaron las secciones del capítulo 2. Traer el resto del índice es
el primer paso de esa fase, no el último.

### 3.2 Matemática: terminada

Las nueve publicadas están en el molde nuevo. El 12-09-2026 se reescribieron las
siete que faltaban:

- **01** define el espacio vectorial por sus dos operaciones, demuestra que dos
  vectores del plano con determinante no nulo generan todo $\mathbb{R}^2$ con
  coeficientes únicos, su recíproco, y que las coordenadas en una base son
  únicas —que es lo que justifica escribir un vector como una lista—.
- **02** demuestra que una transformación lineal queda determinada por las
  imágenes de la base, que por eso las columnas de la matriz son esas imágenes,
  que componer es multiplicar, y las tres restricciones que una transformación
  lineal no puede violar.
- **03** define espacio columna, rango y núcleo, demuestra el teorema del
  rango-nulidad y que el conjunto de soluciones es el núcleo trasladado. Los
  ejemplos de colinealidad se pasaron a peso/altura/IMC y a grupos, sin empresa.
- **04, 05 y 06**: el arco producto interno → proyección → mínimos cuadrados,
  descrito arriba.
- **07** demuestra que con base ortonormal la proyección es $QQ^\top$, deriva
  Gram-Schmidt con la triangularidad de $R$ **deducida** y no impuesta, y
  resuelve mínimos cuadrados con $R\hat{x}=Q^\top b$. La tabla de pérdida de
  ortogonalidad se declara por la regla 7: se afirma la propiedad, no los
  dígitos.

Quedan por escribir, no por reescribir, las lecciones 10 a 18 del módulo.

**Un fallo que encontró el gate durante esta tanda:** en `matematica/07` el
botón «Caso típico» no hacía nada, porque el estado inicial del visual **era**
ese preajuste. Se cambió el arranque a una posición que no coincide con ningún
preajuste. Es el mismo tipo de error que la regla 19b persigue, y esta vez lo
cazó `visuales.py` en vez de Luis.

### 3.3 Reescribir Python 01–06

Las más alejadas del molde y las que más contexto de empresa arrastran
(`python/03-comprehensions.qmd` es la peor). Ojo: el molde de
definición → proposición → demostración **no encaja** en una lección de
programación. Antes de tocarlas hay que decidir qué significa el molde aquí:
probablemente `.hilo` + notación + glosario sí, y definiciones numeradas no.
**Esa decisión está sin tomar y conviene tomarla con Luis.**

### 3.4 El orden acordado con Luis (12-09-2026)

Est 16 y 17 primero —hechas—, Estadística 01 y 02 de calentamiento —hechas—, y
Matemática 04 → 05 → 06 —hechas—. Lo que sigue, en este orden:

Matemática 03 → 02 → 01 → 07 también está hecha. Lo que sigue:

1. **La pasada de regla 15** sobre las cinco páginas de Python baratas (01, 02,
   04, 05 y 06): cambiar el ejemplo por dados, pesos al nacer o ingresos, sin
   tocar la estructura. Se puede hacer sin decidir nada del molde.
2. **Traer los índices de Think Bayes**, capítulos 3 al 20, para desbloquear
   Estadística 18–24.
3. **Decidir el molde de Python** (punto 6) y reescribir `python/01–06`.
4. **Seguir Matemática por la 10 en adelante**, que están sin escribir.

### 3.5 Estadística 01 y 02: hechas

Se juntaron las vallas `{=html}` de cada visual el 12-09-2026 y las dos entraron
en `MIGRADAS`. Con eso el módulo de Estadística está completo y al día: 17 de 17.

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

**Un botón de re-sorteo sobre un promedio de 4000 repeticiones no mueve nada.**
El primer visual de Est 17 dibujaba la acumulada del menor valor p sobre 4000
experimentos: tan estable que «Otra tanda» cambiaba el dibujo menos de 2 px, y
`visuales.py` lo habría marcado como control roto —con razón, porque en pantalla
no se notaba—. Bajar a 600 repeticiones lo dejó en 10,8 px y además es más
honesto: se ve que la curva es una medición, no una fórmula. Regla práctica: si
un botón promedia, hay que promediar poco, o el botón sobra.

**Una celda de 17 segundos es una celda rota.** La primera versión de la celda
de los tres mecanismos (Est 15) recorría 12 000 repeticiones en un bucle de
Python: 17,5 s en CPython, y en Pyodide eso es un múltiplo que nadie va a
esperar. Vectorizada a arreglos `(reps, n)` baja a 0,4 s con los mismos
resultados. Regla práctica: si una celda pasa de dos o tres segundos en local,
hay que reescribirla antes de publicarla, porque en el navegador se abandona.

**Heredar la prosa vieja al migrar una lección.** Al reescribir `matematica/01`
se conservó casi literal la frase de entrada de la versión anterior —«un vector
no es una lista de números: es un objeto que sabe hacer dos cosas…»—, que viola
la regla 14 por dos vías: la construcción «no es X, es Y» está prohibida
explícitamente, y el contenido es impreciso, porque las dos operaciones son del
**espacio**, no de cada vector. Lo encontró Luis leyendo la página, no ningún
gate. Migrar una lección es reescribir también sus párrafos de enlace, no solo
envolver el contenido viejo en el molde nuevo.

Barrido hecho el 12-09-2026 sobre todo el corpus: **veintiuna frases** con la
forma de golpe o con segunda persona, en once lecciones, todas corregidas. Y
para que no vuelva, `formato.py` lo comprueba desde entonces (regla 22): si una
lección migrada recupera el vicio, `--estricto` falla y el CI no publica.

De paso salieron dos cosas más. `estadistica/03` cumplía el molde desde hacía
tiempo y nunca se había añadido a `MIGRADAS`; ya está. Y `estadistica/01` y `02`
se habían añadido a esa lista tras arreglarles solo las vallas `{=html}`, sin
mirarles la prosa: el detector encontró en la 01 tres frases de golpe que venían
del molde viejo.

**El CI corre numpy 2 y esta máquina numpy 1.24: no fijar dígitos de un cero
de punto flotante.** El 12-09-2026 el build murió en `salidas.py` con dos
afirmaciones que pasaban en local: `error máximo : 0.0` salía `4.44e-16` con
numpy 2 —otro orden de suma— y `A^T e = [0. 0.]` salía `[ 0. -0.]`, porque el
signo del cero al redondear también cambió. Las dos eran `contiene` sobre
ceros. La corrección no fue tocar la afirmación sino **la celda**: imprimir la
propiedad (`max |A^T e| por debajo de 1e-12 : True`) en vez del número. Regla
práctica: si lo que se imprime es un cero numérico, se imprime la cota.

Para reproducir el entorno del CI antes de empujar:

```sh
python3 -m venv /tmp/ci-venv && /tmp/ci-venv/bin/pip install numpy
/tmp/ci-venv/bin/python verificar/salidas.py
```

**`np.math` no existe en numpy 2.** Usar `math.erf` de la biblioteca estándar.

**El harness de `visuales.py` medía en la esquina equivocada (van tres veces).**
Al primer uso real de `--estricto` sobre las 28 lecciones (12-09-2026), salieron
5 fallos. Dos eran bugs reales de regla 19b: en `estadistica/01` el `change`
del selector de $n$ y en `estadistica/03` el `input` del slider $\lambda$
limpiaban el estado acumulado antes de redibujar, así que el panel quedaba
vacío sin importar el valor —arreglado agregando una curva teórica que se
dibuja siempre, anclada al parámetro y no a los datos—. Los otros dos
(`estadistica/10` botón «Otra tanda», `matematica/09` botón «Llevar al
eigenvector») **no eran bugs de la lección**: el propio harness barre cada
select/range hasta su última opción o su máximo antes de probar los botones,
y eso dejaba la página en una esquina degenerada —una matriz de rotación sin
eigenvectores reales, un efecto y una $n$ tan grandes que el valor p ya es
cero siempre— donde el botón de verdad no tenía nada que mover. Se demostró
en píxeles que ambos botones sí mueven el dibujo en el estado por defecto de
la página, y el arreglo fue restaurar los controles a su valor por defecto
—`option[selected]`/`defaultValue`— antes de probar los botones, no tocar la
lección ni añadir a `QUIETOS`. `QUIETOS` es solo para controles que de verdad
no deben mover nada porque la cantidad no depende de los datos; una esquina
degenerada del rango es el test midiendo mal, no un control roto.

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
- **Est 12 y Est 14, y el teorema de Cochran.** Los dos usan sin demostrar que
  cierta suma de cuadrados dividida por $\sigma^2$ sigue una $\chi^2$ (con
  $n-1$ y $n-2$ grados respectivamente). Está declarado en Fuentes de las dos.
  Si alguna lección futura lo necesita demostrado, hay que decidir dónde va.
- **El cuaderno de retos va por Estadística 5.** Las lecciones 6 a 15 cierran
  con «en `proyectos/notebooks/F1-retos.ipynb`, sección **Est N**», y ese
  cuaderno solo tiene secciones hasta Estadística 5 y Matemática 7. O se
  escriben las diez que faltan —tres retos por lección, como las que ya están—,
  o se quita la referencia del bloque *Reto*. Encontrado al publicar Est 15;
  sin decidir.

- **Colisiones en `glosario/glosario.json` → `GLOSARIO_SIMBOLOS` (auditado
  12-09-2026, sin tocar todavía).** El enganche de `encabezado.html` es
  **global por carácter**, sin alcance por lección: si dos lecciones usan el
  mismo símbolo con significados distintos, el tooltip acierta en una y miente
  en la otra. Regla aclarada con Luis: **el glosario global solo admite un
  símbolo si significa lo mismo en todo el sitio; si el significado depende de
  la lección, va en la tabla `::: {.notacion}` de esa lección (ya obligatoria
  por la regla 16), no en el glosario.** Confirmado que `r` y `R²` **no** están
  en `GLOSARIO_SIMBOLOS` (no hay bug vivo ahí). Sí están, y con colisión
  confirmada por lección, contrastando código fuente contra código fuente:
    - **`T`**: registrado como «variable con distribución t de Student»
      (origen Est 09). Pero en `estadistica/10.qmd:511` (Demostración Prop.
      10.8) es el estadístico de prueba genérico —confirmado en vivo con
      Playwright que el tooltip equivocado se muestra ahí—, y en
      `matematica/02.qmd` es una transformación lineal.
    - **`Q`**: registrado como «suma de cuadrados centrada» (Est 08/11). En
      `matematica/07-gram-schmidt-qr.qmd` es la matriz ortogonal de $A=QR$.
    - **`B`**: registrado como «número de remuestreos bootstrap» (Est 11). Es
      una matriz cualquiera en `matematica/02` y `matematica/08`, una variable
      causal genérica en `estadistica/05:692`, el extremo aleatorio de un IC
      en `estadistica/09:65`, y un semieje de elipse en `estadistica/12:258`.
    - **`p`**: la propia entrada ya admite tres sentidos («según el
      contexto») — eso ya viola la regla aclarada. Además falta un cuarto
      sentido sin avisar: en `estadistica/10` es el valor p (la lección
      insiste en que **no** es una probabilidad, y el tooltip dice que sí lo
      es), y en `matematica/09-eigenvalores.qmd:319` es el polinomio
      característico $p(\lambda)$.
  Moderadas —el tooltip ya avisa «según el contexto» o «tiene dos usos», así
  que no miente sin matiz, pero igual violan «un símbolo, un significado»—:
  `α` (exponente de Pareto vs. nivel de significancia), `β` (coeficientes de
  regresión vs. error de tipo II), `δ` (tolerancia vs. tamaño de efecto), `θ`
  (ángulo entre vectores vs. parámetro a estimar), `ε` (épsilon de máquina vs.
  error del modelo). Pendiente decidir: ¿se sacan `T`, `Q`, `B`, `p` del
  glosario global y se dejan solo en la tabla de notación de cada lección
  (como ya se decidió para `r` y `R²`), y qué se hace con las cinco letras
  griegas moderadas?
