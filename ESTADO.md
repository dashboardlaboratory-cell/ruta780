# Estado de Ruta 780 y qué sigue

Última actualización: **13-09-2026**, tras reescribir las seis lecciones de
Python al molde nuevo. **Los tres módulos escritos quedan completos y al día:
48 lecciones de 48.** No queda ninguna lección en el molde viejo.

Antes de esto, el 12-09-2026 se habían publicado Estadística 18 a 24 —las
bayesianas, desbloqueadas al verificar el índice entero de Think Bayes— y
Matemática 10 a 18, que cerraron ese módulo.

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
| Estadística | 24 | 24 | **24 de 24** |
| Matemática | 18 | 18 | **18 de 18** |
| Python | 6 | 6 | **6 de 6** |

- **48 lecciones** publicadas, **48** cumplen el molde nuevo. Cero pendientes.
- **102 visuales** auditados por `visuales.py`; ningún fallo de la regla 19b.
  Quedan tres avisos de no idempotencia, todos anteriores a esta tanda.
- **818 afirmaciones numéricas** declaradas en `verificar/afirmaciones.json`,
  sobre **225 celdas** que el gate ejecuta en cada build.
- Glosario: **236 términos + 43 símbolos**. Las **41 entradas** que añadió la
  tanda de Python son todas de tipo `termino`: no se añadió ningún símbolo
  global, que es donde están las colisiones ya auditadas del punto 6.
- Índices verificados: Think Stats 3e (75 secciones), MML (80), **Think Bayes 2e
  (20 capítulos y 193 secciones, traídas enteras el 12-09-2026; el capítulo 19
  publica las suyas sin numerar)**, McKinney 3E (capítulos + las 6 secciones del
  cap. 7) e ISLP (solo capítulos).

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

**Estadística 18–24, las bayesianas, ya están publicadas.** Estaban bloqueadas
por el índice de Think Bayes 2e, del que solo se había verificado el capítulo 2;
se trajo el índice entero y se escribieron las siete: teorema de Bayes, priors
conjugados, distribuciones predictivas, comparación de modelos,
Metropolis-Hastings, Gibbs y diagnóstico de cadenas. Con ellas el módulo queda
en 24 de 24.

### 3.2 Matemática: terminada, 18 de 18

Las nueve primeras se reescribieron el 12-09-2026 y ese mismo día se añadieron
las nueve restantes, de la 10 a la 18: diagonalización, SVD, formas cuadráticas,
derivada y gradiente, hessiana y Taylor, convexidad, descenso de gradiente,
método de Newton y Lagrange con KKT. Lo que sigue describe la primera tanda:

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

### 3.3 Python 01–06: hechas, y el molde que se decidió

Reescritas el 13-09-2026. La duda era si definición → proposición → demostración
encajaba en programación. **Sí encaja, y la decisión tomada fue mantener el molde
entero, definiciones numeradas incluidas**, con esta lectura:

- las **definiciones** enuncian la semántica del lenguaje —objeto, vínculo,
  mutabilidad, ámbito, iterador, gestor de contexto, array— tomando la
  especificación como el sistema de partida, igual que un curso de matemática
  toma unos axiomas;
- las **proposiciones** son invariantes que se siguen de esa semántica, no
  descripciones de comportamiento: que la asignación no copia, que la
  clasificación de un nombre como local ocurre al compilar, que una cláusula
  `except` situada tras una superclase suya es inalcanzable, que la indexación
  avanzada no puede devolver una vista;
- las **demostraciones** se apoyan en esa especificación y, cuando el resultado
  es de coste, en aritmética corriente —la serie geométrica del `append`
  amortizado, la aritmética módulo $2^b$ del `int8`—;
- **todo se comprueba contando, nunca cronometrando** (regla 7): una clase que
  cuenta sus comparaciones en lugar de un `timeit`, `co_varnames` leído antes de
  la primera llamada, `np.shares_memory`, `__defaults__` antes y después.

Lo que este molde aporta sobre el anterior es que las reglas dejan de ser
consejos. «Captura lo específico primero» pasa a ser un resultado de
alcanzabilidad; «no uses un default mutable» pasa a ser un corolario de que las
expresiones por defecto se evalúan una vez; «borrar un dato luego no basta» pasa
a ser un corolario de que el identificador de un commit depende de su contenido.

Tres resultados se demuestran como **imposibilidades**, que es lo que mejor
explica las asimetrías del lenguaje: una lista no puede ser clave sin dejar la
entrada inalcanzable (1.11), una cláusula tras su superclase no la alcanza
ninguna excepción (4.4), y una selección arbitraria no admite descripción con
paso constante y por eso no puede ser vista (6.3).

Detalles de la tanda:

- **01** objetos, nombres y estructuras: 8 proposiciones, incluido el `append`
  amortizado con la cota $g/(g-1)$ y el caso degenerado $g\to1$ medido.
- **02** ámbito y cierres: el `UnboundLocalError` demostrado desde el momento de
  la compilación, y el encuentro entre las Proposiciones 2.7 y 2.9 —el mecanismo
  que causa el problema del default mutable es el que resuelve el de la captura
  en un bucle—.
- **03** iteradores, comprehensions y generadores: el cortocircuito con la cuenta
  exacta $k+1$ frente a $n$, y el corolario que separa «la comprehension abre un
  ámbito» de «ese ámbito es uno, no uno por iteración».
- **04** archivos, excepciones y contextos: la cláusula inalcanzable, el `return`
  en `finally`, y la ventana entre comprobar y abrir medida borrando el archivo
  dentro de esa misma ventana.
- **05** entorno reproducible: `id_blob` con `hashlib` reproduce byte a byte lo
  que devuelve `git hash-object`, contrastado contra la herramienta, y de ahí
  sale por inducción que alterar un commit cambia el id de todos sus
  descendientes.
- **06** NumPy: las seis proposiciones salen de una sola fórmula, la del
  desplazamiento de un elemento.

**Dos cosas que encontró el gate durante la tanda**, y que conviene recordar:

1. En `python/05` el visual de la cadena de commits cambiaba de color pero no
   movía un solo píxel. `visuales.py` lo marcó, y es exactamente el fallo de la
   regla 19b: la firma del SVG cambiaba y el dibujo no. Se arregló añadiendo un
   marcador que se desplaza con el control.
2. El ejercicio 2 de `python/06` traía de la versión vieja un `check` que
   esperaba `2750.0` cuando la suma correcta es `1800.0`. El mensaje de acierto
   ya decía «solo pasa la segunda», así que el número llevaba mal desde el
   principio y nadie lo había corrido.

**Y una colisión de glosario, esta vez de término y no de símbolo:** `parámetro`
ya existía con el sentido estadístico («un número que describe a la población,
como μ o σ»), así que marcarlo en Python habría puesto un tooltip que miente.
Se aplicó la regla del punto 6: fuera del glosario global, y declarado en la
tabla `::: {.notacion}` de la lección. Conviene barrer el resto de términos
buscando el mismo problema.

### 3.4 Qué sigue ahora (13-09-2026)

Los cuatro puntos del plan anterior están hechos: la pasada de regla 15 sobre
Python, los índices de Think Bayes, el molde de Python con sus seis lecciones, y
Matemática de la 10 a la 18. **No queda nada pendiente de los módulos escritos.**

Lo que sigue, en orden de coste creciente:

1. **Las decisiones del punto 6 que siguen abiertas**, y son baratas: las
   colisiones de `T`, `Q`, `B` y `p` en el glosario global, el barrido de
   términos en busca de más colisiones como la de `parámetro`, y qué hacer con
   el cuaderno de retos, que solo llega a Est 5 y Mat 7 mientras las lecciones
   lo citan mucho más adelante. Ahora son **catorce** secciones de retos
   pendientes: las diez de antes más las de Py 1 a Py 6, que las lecciones
   nuevas ya citan.
2. **Series de tiempo, ML e Inferencia causal** están vacías en el sidebar. ML
   necesita ISLP, cuyo índice está verificado solo a nivel de capítulo; causal
   necesita *Causal Inference for the Brave and True*, que no está verificado y
   por tanto no es citable.
3. **Fase 2**: traer los índices de ESL y fast.ai antes de citarlos.

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

**El harness de visuales medía cada deslizador desde donde lo dejó el anterior
(van cuatro veces).** El 12-09-2026, `matematica/12` disparó un aviso falso: el
gate barre λ₁ y λ₂ hasta su máximo antes de probar el giro, y con los dos
eigenvalores iguales la forma es un círculo, donde girar de verdad no cambia
nada. Ya existía la restauración de valores por defecto, pero solo antes de
probar los **botones**. Ahora `visuales.py` restaura antes de **cada** control.

El cambio destapó de inmediato un fallo real que el orden viejo escondía: en
`estadistica/16`, el deslizador «Fuerza» no hacía nada con el pronóstico «fiel»
seleccionado, que era el valor por defecto. Se rediseñó el control —la opción
«fiel» desaparece y es simplemente fuerza cero—, y ahora el deslizador siempre
mueve el dibujo.

**`np.linalg.eig` devuelve complejos en numpy 2 aunque los eigenvalores sean
reales.** Segunda vez que la diferencia de versiones rompe el build, ahora en
`matematica/10`: en local imprimía `[5. 2.]` y en el CI `[5.+0.j 2.+0.j]`. La
corrección es explícita y además enseña algo: comprobar que la parte imaginaria
es cero y quedarse con `.real`. Con `eigh` —matrices simétricas— no pasa, porque
ahí los eigenvalores son reales por construcción.

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

- ~~**Qué molde usan las lecciones de Python.**~~ **Decidido el 13-09-2026**: se
  mantiene el molde completo, definiciones numeradas incluidas, leyendo la
  especificación del lenguaje como el sistema de partida. El detalle está en el
  punto 3.3, y las seis lecciones ya están escritas así.
- **Barrer el glosario buscando colisiones de término**, no solo de símbolo. Al
  escribir Python 2 apareció una: `parámetro` estaba registrado con el sentido
  estadístico y habría puesto un tooltip falso en la lección de funciones. Se
  resolvió sacándolo de esa lección y declarándolo en su tabla de notación, que
  es la misma regla acordada para los símbolos. Falta comprobar si hay más:
  candidatos probables son `función`, `argumento`, `dominio`, `imagen`, `error`
  y `varianza`.
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
