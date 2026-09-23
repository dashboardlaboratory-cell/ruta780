# Estado de Ruta 780 y qué sigue

Última actualización: **19-09-2026**, tras una sesión larga que publicó **veintitrés
lecciones** y cerró **cinco deudas**.

Las lecciones: **ML 7** (selección de subconjuntos, ISLP §6.1), **ML 8**
(encogimiento, §6.2), **ML 9** (alta dimensión, §6.4), **ML 10** (bases y
splines, §7.1–7.4), **ML 11** (suavizado y GAMs, §7.5–7.7), **ML 12** (árboles de
decisión, §8.1), **ML 13** (bagging, bosques e impulso, §8.2), **ML 14** (margen
máximo, §9.1–9.2), **ML 15** (núcleos y pérdida bisagra, §9.3–9.5), **ML 16** (redes neuronales,
§10.1–10.2, §10.6 y §10.8), **ML 17** (censura y Kaplan-Meier, §11.1–11.4), **ML 18** (riesgos proporcionales
y Cox, §11.5–11.7), **ML 19** (PCA, §12.1–12.3), **ML 20** (PCR y PLS, §6.3), **ML 21** (clustering, §12.4), **ML 22** (pruebas múltiples, §13.3–13.5), y
**Python 10** a **16** (carga y limpieza, uniones y reshape,
groupby, visualización, series de tiempo, rendimiento y anatomía de un proyecto).

**Las 81 publicadas cumplen el molde: 81 de 81.**

Tres hitos de esta sesión:

- **El módulo de Python queda CERRADO en 16 de 16**, el tercero tras Estadística
  y Álgebra.
- **ISLP: los capítulos 2 a 9 quedan cubiertos SIN NINGÚN HUECO** desde el
  19-09-2026. El último que faltaba era §6.3, pendiente desde ML 8 porque
  necesitaba componentes principales, y lo cubre **ML 20**. El reparto: el 2 en
  ML 1, el 3 en ML 2, el 4 en ML 3, 4 y 5, el 5 en ML 6, el **6 en ML 7, 8, 9 y
  20**, el 7 en ML 10 y 11, el 8 en ML 12 y 13, y el 9 en ML 14 y 15.
- Del **capítulo 10**, ML 16 cubre §10.1–10.2, §10.6 y §10.8; el resto está
  repartido entre las lecciones 36 a 41 de la Fase 4, salvo §10.4 y §10.5, que
  **no están en el plan** y quedan anotadas como omisión deliberada. El
  **capítulo 11 queda cubierto entero**: §11.1–11.4 en ML 17 y §11.5–11.7 en
  ML 18, con tres subsecciones de §11.7 nombradas como omisión deliberada. Del
  **12 queda cubierto entero**: §12.1–12.3 en ML 19 y §12.4 en ML 21. Y el **13**
  se reparte entre Estadística 17 —§13.1 a §13.3— y **ML 22** —§13.3.3 a §13.5—.
  **Con ML 22 se cierra la Fase 2 de ISLP entera.**
- **Las tres deudas abiertas se cerraron**: las colisiones del glosario (punto 6),
  las 33 secciones de retos y los 106 símbolos sin declarar.

Eso es una afirmación sobre el **molde**, no sobre el plan. Del plan siguen
faltando lecciones por escribir: **ML va por 27 de 90**, **Series de tiempo
está **completo, 11 de 11**, e **Inferencia causal sigue vacío**. El detalle está en la tabla del punto 2.

El 16-09-2026 se habían publicado Python 7, 8 y 9 y ML 4, 5 y 6.

Antes de esto, el 12-09-2026 se habían publicado Estadística 18 a 24 —las
bayesianas, desbloqueadas al verificar el índice entero de Think Bayes— y
Álgebra 10 a 18, que cerraron ese módulo.

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
python3 verificar/referencias.py
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

| Módulo | Publicadas | Planeadas | Al día con el molde | Falta escribir |
|---|---|---|---|---|
| Estadística | 25 | 25 | **25 de 25** | — |
| Álgebra | 18 | 18 | **18 de 18** | — |
| Python | 18 | 30 | **18 de 18** | 12 de ingeniería de datos |
| Series de tiempo | 11 | 11 | **11 de 11** | — |
| Machine Learning | 36 | 90 | **36 de 36** | deep learning, de la 37 en adelante |
| Inferencia causal | 0 | 14 | — | todas |

Los totales planeados salen de `data-total` en `index.qmd`, y las publicadas de
`data-ids`; el descuadre entre ambos es lo que mide la barra de progreso, así que
**no es un error**.

- **109 lecciones** publicadas, **109** cumplen el molde nuevo: cero pendientes
  de reescritura. Pendientes de **escribir** quedan 79 según el plan, que son
  más que antes porque el plan de Python creció en catorce.
- **Tres módulos cerrados**: Estadística 25/25, Álgebra 18/18 y **Series de
  tiempo 11/11**. Python dejó de estarlo el 22-09-2026: pasó de 16 a 30 (punto 3.54).
- **El capítulo 4 de ISLP quedó desglosado en tres lecciones** el 15-09-2026, con
  el método acordado de decidirlo justo antes de escribir: **03** regresión
  logística (§4.1–4.3, publicada), **04** modelos generativos (§4.4) y **05**
  modelos lineales generalizados (§4.6). El índice del módulo se renumeró hasta
  la 16.
- **`C=np.inf`, no `penalty=None`.** Es la única forma de apagar la penalización
  de `LogisticRegression` que aceptan a la vez el scikit-learn 0.24 de la máquina
  de trabajo y el 1.9 del CI; `penalty=None` no existe en el primero y está
  deprecado en el segundo. Anotado porque volverá a hacer falta en ML 04 y 05.

  **Segundo caso, 22-09-2026, ML 31:** el criterio de `DecisionTreeRegressor` se
  llamaba `"mse"` hasta la 1.0 y `"squared_error"` desde entonces, y las dos
  máquinas están a un lado y otro de ese cambio. La salida es **no nombrarlo**:
  el error cuadrático es el valor por omisión en las dos versiones. La regla
  general que va quedando es preferir el valor por omisión a escribir su nombre
  cuando el nombre ha cambiado de versión.
- **Las 16 lecciones de nivel L3 tienen sección «Contraste con la librería»**
  (13-09-2026). Ese nivel promete «lo implementas en NumPy puro y empatas con la
  librería a 6 decimales», y hasta esa fecha la promesa era **incomprobable**,
  porque no había ninguna librería instalada. El CI instala ahora `numpy`,
  `scipy` y `scikit-learn`, y cada lección declara en su frontmatter solo lo que
  usa: la descarga pasa de 3,1 MB a unos 25 **únicamente** en las páginas que lo
  necesitan. Est 16, que es L4, lleva además el supuesto roto y el modo de falla.

  Tres decisiones que conviene no repensar desde cero:
  `statsmodels` se descartó porque la versión de la máquina de trabajo está rota
  con numpy 1.24 y no se publica código que no se haya ejecutado; Est 22 y 23 no
  tienen contraste posible —PyMC no está en Pyodide, verificado contra el
  `pyodide-lock.json`— y lo dicen, apoyándose en que se verifican contra las
  marginales exactas, que es más fuerte que cualquier librería; y `np.trapz` se
  retiró del espacio de nombres en NumPy 2.0, así que las celdas nuevas no lo
  usan.
- **207 visuales** auditados por `visuales.py`; ningún fallo de la regla 19b.
  Siguen los mismos cuatro avisos, todos anteriores: tres de no idempotencia
  —Est 03, Est 22 y Mat 10— y uno que conviene mirar, `ml/03` visual 1,
  control `sp-i`: sus marcadores se mueven 0,3 px, que es justo el síntoma que
  la regla 19b persigue. Los visuales de esta tanda no añaden ninguno.
- **2399 afirmaciones numéricas** declaradas en `verificar/afirmaciones.json`,
  sobre **592 celdas** que el gate ejecuta en cada build, y comprobadas **con las
  dos parejas de versiones** (ver el punto 5). El 22-09-2026 se rehízo el
  entorno de contraste —la limpieza de `/tmp` de macOS se había llevado su
  `pyvenv.cfg` y casi todo numpy— y todas vuelven a cuadrar en Python 3.8 con
  numpy 1.24 y en Python 3.14 con numpy 2.5.3. **Al rehacerlo faltaba
  `scikit-learn`**, y el gate lo dijo en vez de callarse: las celdas que lo
  importan salieron como REVENTÓ, no como aprobadas.
- Glosario: **450 términos + 40 símbolos**. Los símbolos bajaron de 43 el
  18-09-2026 al sacar `T`, `Q` y `B`, cuyos tooltips mentían fuera de su lección
  de origen; la regla está en `CLAUDE.md` como **21b** y el detalle en el punto 6.
  **Las lecciones nuevas no añaden símbolos globales**: los suyos se declaran en
  su tabla `::: {.notacion}` y no salen de ahí.
- Índices verificados: Think Stats 3e (75 secciones), MML (80), **Think Bayes 2e
  (20 capítulos y 193 secciones, traídas enteras el 12-09-2026; el capítulo 19
  publica las suyas sin numerar)**, McKinney 3E (capítulos + las secciones de los
  capítulos 6 a 11; las subsecciones de casi todos no llevan número en el sitio
  publicado, así que no se registran ni se citan) e **ISLP (13 capítulos, 81 secciones N.M y 176 sub-subsecciones N.M.K —257 entradas— traídas el 13-09-2026 de los
  marcadores del PDF oficial)**. Desde esa fecha `citas.py` admite **tres niveles**: se puede citar
  `ISLP §10.7.1 Backpropagation`. La función `rango()` se generalizó a cualquier profundidad, porque la anterior
  desempaquetaba dos valores del `split` y reventaba con el tercer nivel; se comprobó que los casos de dos niveles
  siguen expandiéndose igual. Y **ESL (18 capítulos y 134 secciones, traídas el
  20-09-2026 con dos fuentes independientes** —los marcadores del PDF y el
  índice impreso de las páginas 9 a 18— **porque los marcadores están
  corrompidos**: meten tabuladores dentro de los números y pierden la sección
  18.8. De las 133 comparables, 126 coinciden literalmente y las 7 restantes
  difieren solo en los puntos suspensivos del impreso.

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

### 3.2 Álgebra: terminada, 18 de 18

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
Álgebra de la 10 a la 18. **No queda nada pendiente de los módulos escritos.**

Lo que sigue, en orden de coste creciente:

1. **Las decisiones del punto 6 que siguen abiertas**, y son baratas: las
   colisiones de `T`, `Q`, `B` y `p` en el glosario global, el barrido de
   términos en busca de más colisiones como la de `parámetro`, y qué hacer con
   el cuaderno de retos. **El número real, contado el 17-09-2026, es 33**, no
   catorce: la cuenta que venía arrastrándose estaba mal. Lo que falta es Python
   5, Matemática 8 a 18, Estadística 6 a 16 y 18 a 25, y ML 1 y 2. Lo que sí
   está cubierto es Python 1 a 4 y 6 a 10, Matemática 1 a 7, Estadística 1 a 5
   y 17, y ML 3 a 7. Para recontarlo sin fiarse de esta línea:

   ```sh
   python3 - <<'EOF'
   import json, pathlib, re
   hay = set()
   for nb in ['F0-retos','F1-retos','F2-retos']:
       d = json.load(open(f'proyectos/notebooks/{nb}.ipynb', encoding='utf-8'))
       for c in d['cells']:
           for l in (c['source'] if c['cell_type']=='markdown' else []):
               m = re.match(r'##\s+(Matemática|Estadística|Python|ML)\s+(\d+)', l.strip())
               if m: hay.add((m.group(1), int(m.group(2))))
               m = re.match(r'##\s+Lección\s+(\d+)', l.strip())
               if m: hay.add(('Python', int(m.group(1))))
   falta = []
   for p in sorted(pathlib.Path('.').glob('*/[0-9]*.qmd')):
       m = re.search(r'retos\.ipynb`, sección \*\*(\w+)\s*(\d+)\*\*', p.read_text(encoding='utf-8'))
       if not m: continue
       mod = {'Est':'Estadística','Mat':'Matemática','Py':'Python'}.get(m.group(1), m.group(1))
       if (mod, int(m.group(2))) not in hay: falta.append(f'{mod} {m.group(2)}')
   print(len(falta), 'pendientes:', falta)
   EOF
   ```
2. **ML: el plan listado está incompleto, y el propio plan ya lo sabía.**
   Anotado el 13-09-2026 al traer el tercer nivel del índice de ISLP.

   `ml/index.qmd` enumeraba **33 filas**, de las que 14 se repartían los 13
   capítulos de ISLP. Pero `data-total` del plan dice **90**. Faltaban 57 filas
   por escribir en el índice, y ese número no es casual: ISLP tiene exactamente
   **57 secciones sustantivas de nivel N.M**. A razón de una lección por
   sección —que es el ritmo real de las lecciones ya escritas, que citan una o
   dos secciones cada una— ISLP pide unas 57, y con las 33 listadas salen las
   90. Quien escribió el plan ya había hecho la cuenta: **las 14 filas son el
   esqueleto, un título por capítulo, pendiente de desglosar.**

   **Al día de hoy son 40 filas** —21 de ISLP en Fase 2, 13 de ESL y 6 de deep
   learning en Fase 4—, porque se han desglosado los capítulos 4, 6, 7, 8 y 9.
   Luis preguntó el 18-09-2026 por qué la barra decía 90 con 39 filas a la vista, y
   la decisión fue **dejar el 90 y explicarlo en la página**: `ml/index.qmd`
   lleva ahora un `callout-important` que dice cuántas están desglosadas,
   cuántas publicadas y por qué los capítulos sin desglosar aparecen con una
   sola fila de esqueleto. Bajar el total a 39 se descartó porque haría que el
   progreso fuese hacia atrás cada vez que se parte un capítulo.

   La medida del problema, con el tercer nivel a la vista: **199 unidades
   enseñables contra 14 lecciones, o sea 14,2 por lección.** Los peores son el
   capítulo 4 (*Classification*) y el 10 (*Deep Learning*), con 23 unidades
   cada uno para una sola lección. El 5 (*Resampling*) es el más holgado, con
   9. El capítulo 1 no necesita lección: es *Introduction*, material de
   presentación sin resultados.

   **La decisión acordada es no desglosar los trece de golpe**, que sería
   planificar en el vacío, sino **capítulo a capítulo justo antes de
   escribirlo**: al llegar al 4, mirar sus 23 unidades y decidir si son tres
   lecciones o cinco. Lo que sí conviene es actualizar `ml/index.qmd` con las
   filas nuevas según se decidan, para que el índice no siga mintiendo.

   Aviso para el capítulo 11, *Survival Analysis*: tiene 17 unidades, una sola
   lección, y **no reaparece en ninguna fase posterior**. Deep Learning al
   menos se retoma en las lecciones 28 a 33; supervivencia no tiene red.

3. **Series de tiempo está completo**: las once lecciones se publicaron el
   19 y el 20-09-2026, y ninguna cita un libro porque ninguno de los
   verificados cubre el tema;
   **Inferencia causal sigue vacía** en el sidebar.
   **ML ya no tiene bloqueo de citación**: el índice de ISLP se completó el
   13-09-2026 con sus 81 secciones, así que se puede citar `§4.3 Logistic
   Regression` y no solo el capítulo. Causal sigue necesitando *Causal Inference
   for the Brave and True*, que no está verificado y por tanto no es citable.
4. **Fase 2**: el índice de ESL ya está traído y verificado (20-09-2026), así
   que las lecciones 23 a 35 son citables. Falta el de fast.ai.

### 3.5 Estadística 01 y 02: hechas

Se juntaron las vallas `{=html}` de cada visual el 12-09-2026 y las dos entraron
en `MIGRADAS`. Con eso el módulo de Estadística está completo y al día: 17 de 17.

---

### 3.6 Python 7 y ML 4: hechas (16-09-2026)

Dos lecciones nuevas, las dos de nivel L3 y por tanto con sección **Contraste
con la librería**.

**Python 7, «NumPy: ejes y reducciones».** Continúa la 6 sin repetirla: la 6
define el array y la difusión, y esta saca las consecuencias. Dos definiciones,
seis proposiciones y dos visuales. El eje del que cuelga todo es que **la regla
de alineación por la derecha decide qué resta compila**, y de ahí salen los tres
resultados que valen la pena:

- la **Proposición 7.2**, el corrimiento de los ejes: `a.sum(axis=0).sum(axis=1)`
  reduce los ejes 0 y **2** del original. El caso que despista es
  `.sum(axis=0).sum(axis=0)`, que sí equivale a `axis=(0,1)` y hace creer que la
  lectura de izquierda a derecha funciona siempre;
- la **Proposición 7.4**, que es el hallazgo de la lección: `a - a.mean(axis=1)`
  falla ruidosamente **salvo cuando la matriz es cuadrada**, y entonces resta las
  medias por fila a las columnas sin avisar. Demostrado, y medido: con una $4×4$
  las medias por fila quedan $-6$, $-2$, $2$ y $6$ en vez de ceros;
- la **Proposición 7.8**, que deduce el valor de una reducción sobre un eje
  vacío exigiendo compatibilidad con la concatenación: está forzado a ser un
  elemento neutro, y por eso `sum` responde sobre un eje de tamaño cero y `max`
  lanza `ValueError`.

**ML 4, «Modelos generativos», ISLP §4.4.** Una definición, seis proposiciones,
dos visuales. LDA, QDA y naive Bayes salidos del mismo desarrollo: se escribe la
normal multivariante, se descartan los términos comunes a las clases, y lo que
sobrevive decide la forma de la frontera. La **Proposición 4.7** es propia y es
la que sostiene el segundo visual: con covarianzas isotrópicas la frontera de
QDA es una esfera con centro y radio en forma cerrada, y la recta de LDA es su
caso degenerado, no un método aparte —al acercar las varianzas el radio diverge—.

**Un hallazgo sobre `scikit-learn` que conviene no volver a descubrir:** el
atributo `covariance_` que guarda `LinearDiscriminantAnalysis` divide entre $n$,
y la matriz que su solver usa para predecir divide entre $n-K$. Difieren en el
factor exacto $n/(n-K)$ —comprobado a $10^{-12}$— así que las predicciones de una
implementación propia con denominador $n-K$ coinciden con las suyas aunque el
atributo no coincida. Leer `covariance_` creyendo que es la matriz del modelo
mete un sesgo, del 0,33 % con $n=600$ y $K=2$, y mayor cuantas más clases haya.

**Dos decisiones tomadas al escribir, en la línea de las ya acordadas:**

1. **`eje` no entra en el glosario global.** Tiene otro sentido en Estadística 12
   (el semieje de una elipse) y en cualquier gráfico, así que se declara en la
   tabla `::: {.notacion}` de la lección. Es la misma regla que se aplicó a
   `parámetro` en la tanda de Python. Sí entraron, por ser inequívocos:
   `reducción`, `elemento neutro`, `modelo generativo`, `análisis discriminante
   lineal` y `naive Bayes`.
2. **ML 4 cita también §4.5.1 *An Analytical Comparison***, que el plan no había
   asignado a ninguna lección. Es donde ISLP compara LDA con la logística, y esa
   comparación pertenece a la lección que acaba de presentar LDA. §4.5.2 queda
   libre para quien desglose el capítulo 5.

**Los cuadernos de retos, al día con lo que las lecciones citan.** Se añadieron
las secciones **Python 7** y **Python 8** a `F1-retos.ipynb` y se creó
`F2-retos.ipynb` con **ML 3**, **ML 4** y **ML 5**. La de ML 3 hacía falta desde
el 15-09: la lección citaba un cuaderno que no existía. Las catorce secciones
pendientes del punto 1 de abajo siguen pendientes; esto solo evita que la deuda
crezca.

### 3.7 Python 8 y ML 5, y la decisión de alcance de la 8 (16-09-2026)

**Python 8 se redefinió antes de escribirla, y conviene saber por qué.** El plan
la listaba como «NumPy: indexado avanzado, vistas y strides», y eso **ya estaba
publicado**: la Definición 6.1 son los pasos, la Proposición 6.2 es la rebanada
como vista y la 6.3 es la indexación avanzada como copia. Escribirla como estaba
habría repetido la 6 con otro título. Se aplicó el mismo método acordado para los
capítulos de ISLP —decidir justo antes de escribir— y quedó como **«Reshape,
orden y ventanas»**, que es lo que de verdad falta entre la 6 y pandas:

- **orden C y orden F** por sus pasos, y que transponer intercambia el uno por el
  otro (Proposición 8.2);
- **el criterio de la vista** para `reshape` (Proposición 8.3), con la
  imposibilidad demostrada sobre un caso concreto: los desplazamientos del
  recorrido por filas de la transpuesta son $0, 32, 64, 8, 40, 72, \dots$ y sus
  diferencias valen $32, 32, -56$, que no son constantes, así que ningún paso
  único las genera y NumPy tiene que copiar. De ahí sale la diferencia entre
  `ravel` y `flatten`, y que `ravel(order='F')` sí devuelva vista;
- **las ventanas deslizantes** (Proposición 8.6), que es el resultado más
  rentable del módulo y se demuestra en dos líneas: $V_{ij}=x_{i+j}$ tiene
  desplazamiento $(i+j)s = is+js$, luego los pasos son $(s,s)$ y la ventana es
  una vista. Forma $(7,4)$ y $28$ elementos sobre un búfer de $80$ bytes, sin
  copiar ninguno;
- **la cota del último byte** (Proposición 8.7), $\sum(n_k-1)s_k + t$, que es lo
  que `as_strided` no comprueba: una fila de más pide el byte $88$ de un búfer de
  $80$ y la construiría igual. Comprobarla cuesta una línea, y es lo que separa
  un truco de algo publicable.

**El índice del módulo se actualizó** con el título nuevo, siguiendo la misma
regla que se fijó para `ml/index.qmd`: que el índice no siga mintiendo.

### 3.8 ML 6 y Python 9 (16-09-2026)

**ML 6 quedó en §5.1, no en el capítulo 5 entero.** El plan la listaba como
«Remuestreo: validación cruzada y bootstrap», y la segunda mitad —§5.2 *The
Bootstrap*— **ya está escrita**: es Estadística 11, con la distribución
empírica, el error estándar, los intervalos por percentiles, un caso donde el
método falla y las pruebas de permutación. Es la misma situación que la de
Python 8, y se resolvió igual: la lección se queda con §5.1 y sus cinco
subsecciones, el bootstrap se enhebra a Estadística 11 por el `.hilo` y por
Fuentes, y la fila del índice pasa a «Validación cruzada» con libro `ISLP 5.1`.

Lo que sostiene la lección:

- la **Proposición 6.2** da el optimismo en forma **exacta**, no como advertencia:
  $E[\text{Ent}]=\sigma^2(n-p-1)/n$ y $E[\text{Prueba}]=\sigma^2(n+p+1)/n$, de
  donde la brecha es $2\sigma^2(p+1)/n$ y cada parámetro cuesta $2\sigma^2/n$ de
  optimismo. Sale de la traza de la matriz sombrero, o sea del mismo $p+1$ que
  reaparece en el apalancamiento medio;
- la **Proposición 6.4**, dejar uno fuera en forma cerrada, demostrada por
  sustitución de la respuesta por su propia predicción en vez de por la fórmula
  de actualización de rango uno. Los $60$ reajustes y el ajuste único dan
  $1{,}6362840333$ los dos;
- la **Proposición 6.6**, que enuncia la fuga de información como una condición
  sobre el procedimiento entero y la demuestra con un contraejemplo **medido**:
  sobre $1500$ columnas de ruido y etiquetas independientes, seleccionar fuera
  de la validación declara $82{,}5$ % de aciertos donde la verdad es $50$ %.

**Python 9 abre pandas, y con ella una dependencia nueva en el CI.** El workflow
instalaba `numpy`, `scipy`, `scikit-learn` y `playwright`; ahora instala también
**`pandas`**, o el gate de salidas no podría ejecutar ninguna celda de las
lecciones 9 a 14.

Aviso de versiones, que conviene tener presente al escribir las que faltan: la
máquina de trabajo tiene **pandas 1.2.4** y el runner instala la 2.x. Las celdas
de esta lección se escribieron a propósito dentro del subconjunto que se comporta
igual en las dos —alineación, `.loc` contra `.iloc`, promoción de dtype— y
**imprimen escalares y booleanos, nunca la representación de un DataFrame**, que
sí cambia de formato entre versiones.

La lección es de nivel **L4**, así que cada resultado va con su modo de falla y
su diagnóstico. El que más rinde es la **Proposición 9.6**: un solo faltante
convierte una columna `int64` en `float64`, y por encima de $2^{53}$ eso hace
indistinguibles dos identificadores distintos. Encadena con la Proposición 6.8 de
la lección de NumPy, y el remedio de producción es el dtype `Int64`, con
mayúscula. También queda medida la **Proposición 9.5**: dos tablas de cuatro
celdas suman una de nueve con **una sola** celda con valor.

**ML 5, «Modelos lineales generalizados», ISLP §4.6.** Dos definiciones, seis
proposiciones, dos visuales. El arco es el del libro: primero qué rompe la recta
sobre conteos, después Poisson, después el marco común.

- La **Proposición 5.1** convierte «predice valores negativos» en un resultado
  geométrico: el conjunto donde la recta ajustada es negativa es un semiespacio,
  y existe siempre que algún coeficiente no sea nulo. Lo que depende de los datos
  es cuántas observaciones caen dentro: aquí $55$ de $800$, la menor en $-2{,}185$.
- La **Proposición 5.5** es la 3.8 de la lección 3 con otra media: $X^\top(y-\hat\mu)=0$,
  y con intercepto los conteos ajustados suman exactamente lo observado. Medido:
  $8700$ y $8700$.
- La **Proposición 5.8** sostiene §4.6.3 con una sola función: el paso
  $\beta \leftarrow \beta + (X^\top WX)^{-1}X^\top(y-\mu)$ resuelve los tres modelos
  cambiando solo el par $(g,V)$, y en el caso lineal converge en **una** iteración
  porque el término en $\beta$ se cancela. La sección de contraste llama a esa
  función tres veces y empata con OLS, con `LogisticRegression` y con
  `PoissonRegressor`.

Dos detalles de implementación que volverán a hacer falta: el IRLS de Poisson
necesita arrancar con el intercepto en $\log\bar{y}$ —partir de cero pone todas
las medias ajustadas en $1$ y la primera hessiana queda mal escalada—, y
`PoissonRegressor` apaga su penalización con `alpha=0.0`, que es el análogo del
`C=np.inf` ya anotado para la logística.

### 3.9 ML 7 y Python 10, y el desglose de ISLP 6 (17-09-2026)

**ISLP capítulo 6 se partió en tres lecciones, y una cuarta queda aplazada.**
Con el método acordado de decidirlo justo antes de escribir: **07** selección de
subconjuntos (§6.1), **08** encogimiento, ridge y lasso (§6.2), y **09**
regresión en alta dimensión (§6.4). **§6.3 *Dimension Reduction Methods* no se
puede escribir todavía**, porque la regresión sobre componentes principales es
PCA seguida de mínimos cuadrados y la lección de PCA no existe; queda como fila
**17** del índice, justo detrás de la de PCA, que pasó a ser la 16.

**Eso obligó a renumerar `ml/index.qmd` entero**, de la 08 a la 38, y a corregir
las referencias cruzadas que quedaban mintiendo en lecciones ya publicadas: ML 4
(«14 y 15» → «16 y 18»), ML 5 («7» → «8», «8» → «10»), ML 6 («7» → «7 y 8»,
«8 a 12» → «10 a 14», «16» → «19») y Python 8 («35» → «38»). **Conviene contar
con este coste cada vez que se desglose un capítulo**: es mecánico, pero si se
salta, el hilo de las lecciones apunta a lecciones que no son.

Lo que sostiene **ML 7**:

- la **Proposición 7.2** demuestra que el RSS no crece entre modelos anidados,
  con la caída exacta $\langle r,z\rangle^2/\lVert z\rVert^2$, y de ahí que
  elegir por RSS o por $R^2$ devuelva **siempre** el modelo completo;
- la **Proposición 7.4** sale de restar las dos esperanzas de la Proposición 6.2
  de ML 6. Se define $C_p$ sobre $d+1$ parámetros y no sobre $d$ como el libro:
  la diferencia es constante y no cambia el ganador, pero con $d+1$ el criterio
  es **insesgado exacto**. Medido con $20\,000$ muestras: sesgo $-0{,}00220$
  frente al $-0{,}21345$ del error de entrenamiento;
- la **Proposición 7.5** ordena $C_p$ y BIC por un argumento de intercambio que
  no usa nada de la forma del RSS: sumar las dos desigualdades de optimalidad
  cancela los ajustes y deja $(\lambda_2-\lambda_1)(c(d_2)-c(d_1))\le 0$. De
  ahí que el BIC **nunca** elija un modelo mayor que el $C_p$ en cuanto
  $n\ge 8$, que es donde $\log n>2$;
- la **Proposición 7.6** convierte el $R^2$ ajustado en un umbral explícito:
  sube al añadir una variable **si y solo si** su $t^2>1$. El ruido puro pasa
  ese umbral el $32{,}88$ % de las veces medido, contra el $32{,}17$ % de la cola
  exacta de la $t$ con $55$ grados de libertad, calculada por Simpson sin scipy;
- la **Proposición 7.8** exhibe un diseño construido con tres vectores
  ortonormales donde la selección hacia adelante devuelve $\text{RSS}=9/17$ y el
  mejor par ajusta **sin error**. Los tres números —$0{,}72$, $9/17$ y $0$— son
  exactos y se demuestran; no se sortearon.

**El contraste L3 de ML 7 necesitó un truco que conviene recordar.**
`SequentialFeatureSelector` elige por validación cruzada, así que por omisión
resuelve otro problema y no puede empatar con una selección por RSS. Pasándole
`cv=[(todo, todo)]` —una partición que entrena y mide sobre todas las
observaciones— su puntuación pasa a ser el $R^2$ de entrenamiento y los dos
criterios coinciden. Con eso empata, y además **comete el mismo error** sobre el
diseño de la Proposición 7.8, que es lo que demuestra que el fallo es del
procedimiento y no de la implementación.

**Python 10 se quedó con §6.1 del capítulo 6 y con §7.1, §7.2 y §7.4 del 7.**
El resto del capítulo 6 —§6.2 binarios, §6.3 APIs web, §6.4 bases de datos— **no
se puede ejecutar en esta página**: Pyodide corre en el navegador, sin sistema de
archivos persistente, sin red y sin base de datos, y no se publica código que no
se haya corrido. §7.3 ya está en Python 9 y §7.5 espera a Python 12.

- la **Proposición 10.2** es la que más rinde: la ida y vuelta por CSV **no es la
  identidad pero es idempotente**, $\varphi^2=\varphi$. Los `float64` vuelven
  exactos y la clave `"01"` vuelve como el entero $1$;
- la **Proposición 10.3** enuncia la inferencia por bloques como propiedad y no
  como advertencia: la misma columna sale `int64`, `int64` y `object` leída en
  bloques de $10\,000$, y `object` leída entera;
- la **Proposición 10.5** mide la pérdida silenciosa de `groupby`: $137$ claves
  faltantes de $1000$ filas, la suma de los conteos da $863$, y la media se mueve
  $0{,}0095$ **aunque la columna resumida no tenga ni un faltante**;
- la **Proposición 10.6** demuestra que la unión interna tiene
  $\sum_k m_1(k)m_2(k)$ filas y que normalizar las claves **nunca** puede
  reducir ese número, con la condición exacta de igualdad. Medido: de $4$ filas
  a $10$, desglosadas en $3\times3$ y $1\times1$.

**Dos cosas que se arreglaron de paso, y que estaban mal desde antes:**

1. **Los `data-ids` de la portada estaban atrasados.** `index.qmd` listaba 6
   lecciones de Python y 3 de ML cuando había 9 y 6 publicadas, así que la barra
   de progreso de la portada llevaba semanas mintiendo. El paso 7 del método
   dice «`data-ids` del módulo **y de la portada**»; se saltó la segunda mitad en
   las dos tandas anteriores. Ahora están las 10 y las 7.
2. **Dos filas del índice arrastraban dos lecciones en un solo `data-leccion`**
   —`python/08` y `ml/05`—, con lo que marcar una marcaba la otra.

**El índice de McKinney creció.** Se trajeron las secciones del capítulo 6 desde
<https://wesmckinney.com/book/accessing-data>: §6.1 a §6.5. Sus **subsecciones no
llevan número** en el sitio publicado, así que no se registran y no son citables,
igual que pasa con el capítulo 19 de Think Bayes. Con eso, de McKinney hay
secciones verificadas de los capítulos 6 y 7, y capítulos del resto.

**Aviso de versiones, otra vez.** Las celdas de Python 10 se escribieron dentro
del subconjunto que se comporta igual en pandas 1.2.4 (la máquina) y 2.x (el CI):
`groupby(dropna=...)` existe desde 1.1, `read_csv(chunksize=)` se itera igual en
las dos, y **ninguna celda imprime la representación de un DataFrame**. La
afirmación de que los `float64` sobreviven a la ida y vuelta se declara como
booleano calculado, no como dígitos, precisamente para que el gate la compruebe en
las dos versiones en vez de fijar el formato de una.


### 3.10 ML 8 y Python 11 (17-09-2026)

**ML 8, «Encogimiento: ridge y lasso», ISLP §6.2.** Dos definiciones, cinco
proposiciones, tres visuales. Lo que la sostiene:

- la **Proposición 8.2** convierte «ridge funciona con $p>n$» en un enunciado
  sobre la hessiana: los eigenvalores de $X^\top X$ son $\ge 0$ y sumar
  $\lambda I$ los desplaza a $\ge\lambda>0$, así que la función objetivo es
  estrictamente convexa y el mínimo es único **para todo** $\lambda>0$. Medido
  con $n=20$ y $p=50$: el rango pasa de $19$ a $50$, y $31$ de los $50$
  eigenvalores eran cero;
- la **Proposición 8.4** da las dos formas cerradas en diseño ortonormal. Ridge
  multiplica por $1/(1+\lambda)$ —las cinco razones salen $0{,}588235$— y el
  lasso es el umbral suave, que deja dos ceros exactos y mueve los otros tres
  exactamente $\lambda/2$. Se añade que, **en general**, $\hat\beta_{\text{ridge}}=0$
  solo si $X^\top y=0$: ridge no puede anular un coeficiente sin anularlos todos;
- la **Proposición 8.5** lee ridge en la base de la SVD: encoge la dirección $j$
  por $d_j^2/(d_j^2+\lambda)$, y los **grados de libertad efectivos** son la suma
  de esos factores. Sobre un diseño con $d_6/d_1\approx 1/122$, con $\lambda=1$
  las cinco direcciones informativas conservan factores $\ge 0{,}9856$ y la
  colineal cae a $0{,}0114$: se pierde un grado de libertad entero, y lo pierde
  la dirección que no llevaba información. Ese número continuo **ocupa el lugar
  del $d+1$ de ML 7**;
- la **Proposición 8.6** es el teorema del encogimiento, con todo explícito:
  $\text{ECM}(\lambda)=(\lambda^2\lVert\beta\rVert^2+p\sigma^2)/(1+\lambda)^2$,
  derivada en cero $-2p\sigma^2<0$, óptimo en $\lambda^{*}=p\sigma^2/\lVert\beta\rVert^2$
  y razón $\lVert\beta\rVert^2/(\lVert\beta\rVert^2+p\sigma^2)$. Es la
  Proposición 7.4 de Estadística 7 con un vector en lugar de un escalar. Medido:
  $1{,}374$ contra $4{,}050$, razón $0{,}339315$ en simulación y en fórmula.

**La Proposición 8.7 es la que conviene no perder.** En un diseño casi colineal,
mínimos cuadrados devuelve $\hat\beta_1=-0{,}62$ y $\hat\beta_6=2{,}15$ donde la
verdad es $1{,}5$ y $0$; ridge con el $\lambda$ de validación cruzada devuelve
$0{,}70$ y $0{,}82$. **El error de los coeficientes mejora un factor $2{,}63$ y el
error de prueba mejora $0{,}000079$**, o sea nada. Las dos cosas son ciertas a la
vez porque los dos errores se cancelan al predecir, y esa es la dirección de
valor singular pequeño de la 8.5. Separar las dos preguntas —interpretar contra
predecir— es lo que explica que la regularización parezca imprescindible en unos
problemas e irrelevante en otros. El libro no lo separa.

**Convenciones de scikit-learn, que hay que traducir.** `Ridge(alpha)` minimiza
$\lVert y-X\beta\rVert^2+\alpha\lVert\beta\rVert^2$, así que $\alpha=\lambda$.
Pero `Lasso(alpha)` minimiza $\frac{1}{2n}\lVert y-X\beta\rVert^2+\alpha\lVert\beta\rVert_1$,
de donde **$\lambda=2n\alpha$**. Comparar un $\lambda$ propio con un $\alpha$ de la
librería sin traducirlo produce discrepancias que parecen errores de
implementación y son de unidades.

**Python 11, «wrangling, joins y reshape», McKinney §8.** Una definición, tres
proposiciones, dos visuales. Nivel L4, con modo de falla y diagnóstico en cada
resultado:

- la **Proposición 11.2** completa las cuatro uniones con el mismo argumento de
  la 10.6, unificadas con $\max\{m,1\}$, y saca el corolario comprobable de una
  línea: `left` conserva las filas de la izquierda **si y solo si** la clave es
  única en la derecha. Medido: $4$, $7$, $5$ y $8$ filas, con la fórmula
  acertando en los cuatro tipos;
- la **Proposición 11.3** dice que pasar a la forma ancha crea exactamente
  $i\cdot j-n$ faltantes, y **cuándo la vuelta no recupera el original**: si la
  columna de valores tenía $f$ faltantes propios, la vuelta devuelve $n-f$ filas,
  porque el hueco estructural y el dato perdido son indistinguibles en una celda
  vacía. Un cauce que va y vuelve entre las dos formas pierde filas en cada
  viaje sin que ningún paso parezca roto;
- la **Proposición 11.4** lee el choque de claves como un problema de señal:
  `pivot` falla y `pivot_table` calla, así que **el remedio evidente es el que
  borra el aviso**. Medido: $9$ filas, $8$ pares distintos, y la celda en choque
  pasa a valer $50{,}5$, la media de un $2$ y un $99$.

**Un aviso de la regla 19b que costó una segunda pasada.** El visual de la
densidad de Python 11 tenía un control —el número de celdas observadas— que solo
cambiaba el **relleno** de las celdas, no su posición. Es exactamente el caso que
la regla persigue, y `visuales.py` lo cazó con «los marcadores apenas se mueven
(0.0 px)». Se arregló añadiendo una barra de densidad cuyo ancho depende de
$n/(i\cdot j)$, que sí es geometría. **Colorear no es mover**: si un control solo
cambia opacidades o rellenos, el gate lo va a marcar, y tiene razón.

**El índice de McKinney creció otra vez.** Se trajeron las secciones del capítulo
8 desde <https://wesmckinney.com/book/data-wrangling>: §8.1 a §8.4. Sus
subsecciones tampoco llevan número, igual que las del 6, así que no se registran.


### 3.11 ML 9 y Python 12 (18-09-2026)

Escritas ya con la disciplina nueva del punto 5: **cada celda se corre con las
dos parejas de versiones antes de declarar nada**, y tiene que salir byte a byte
idéntica. Eso cazó tres fragilidades durante la escritura, ninguna de las cuales
habría aparecido corriendo solo en local:

1. En ML 9, la base del núcleo que devuelve la SVD **no es única** —cualquier
   rotación dentro del núcleo vale— y LAPACK devuelve una distinta en cada
   versión. Se arregló usando el **proyector** sobre el núcleo,
   $I-X^{+}X$, que sí lo es. Es exactamente lo que avisa la regla 7.
2. En ML 9, `np.linalg.lstsq` y `LinearRegression` **no coinciden** en scikit-learn
   0.24 y sí en 1.9: cambió el solucionador. Se sustituyó el contraste por
   `pinv(X) @ y`, que es la definición de la solución de norma mínima.
3. En Python 12, un `dict(cuentas)` imprimía escalares de NumPy y un `%.12f`
   imprimía `-0.000000000000` en una versión y `0.000000000000` en la otra. Los
   dos se sustituyeron por enteros de Python y por un booleano.

**ML 9, «Regresión en alta dimensión», ISLP §6.4.** Una definición, cuatro
proposiciones, dos visuales.

- la **Proposición 9.2** es el resultado que ordena la lección: si el diseño tiene
  rango $n$, su espacio columna **es** $\mathbb{R}^n$ y la proyección de $y$ es
  $y$. De ahí RSS cero y $R^2=1$, **por dimensión y no por contenido**: medido con
  $n=30$, el ajuste pasa a ser exacto justo en $p=29$ sobre ruido puro;
- la **Proposición 9.3** da la fórmula cerrada $E[R^2]=p/(n-1)$ para predictores
  sin ninguna relación, demostrada por simetría esférica. Con $n=40$, doce
  columnas de ruido explican de media el $30{,}8$ % de la varianza y veinte llegan
  al $50$ %. Es Estadística 17 contada con dimensiones en vez de valores p;
- la **Proposición 9.4** dice qué se pierde exactamente: el conjunto de ajustes
  perfectos es un **trasladado del núcleo**, así que los datos determinan $X\beta$
  y no determinan $\beta$. Medido: el mismo coeficiente vale $0{,}9276$,
  $16{,}2702$ y $-0{,}0036$ en tres ajustes igual de perfectos, siendo $2$ el
  verdadero. Y como $n-p-1\le 0$, **$C_p$ y BIC de ML 7 no se pueden calcular**,
  mientras que la validación cruzada de ML 6 sí;
- la **Proposición 9.5** trata la forma dual de ridge como resultado y no como
  truco: $(X^\top X+\lambda I_p)^{-1}X^\top=X^\top(XX^\top+\lambda I_n)^{-1}$,
  un sistema $40\times 40$ donde el primal es $300\times 300$.

La sección 4 mide lo que sí funciona: con $n=60$, $p=200$ y solo cuatro
predictores verdaderos, mínimos cuadrados ajusta sin error y comete $6{,}24$ de
error de prueba; el lasso con $\alpha$ por validación cruzada comete $0{,}43$ y
recupera los cuatro. Queda anotado que declara $23$ variables donde importan $4$:
predice bien, no descubre la verdad.

**Python 12, «groupby y agregación», McKinney §10.** Nivel L4, una definición,
tres proposiciones, dos visuales.

- la **Proposición 12.2** convierte la distancia entre la media global y la media
  de las medias en una **covarianza exacta**:
  $\mu-\bar{u}=\frac{1}{n}\sum_k(n_k-\bar{n})(m_k-\bar{u})$. De ahí sale sola la
  condición de igualdad, y la paradoja de Simpson deja de ser una curiosidad.
  Medido: $1{,}9468$ contra $4{,}7465$, y la covarianza reproduce la diferencia
  $-2{,}7997$ a $10^{-12}$;
- la **Proposición 12.3** separa `agg` de `transform` por la **forma** del
  resultado —$g$ filas contra $n$ con el índice conservado—, y añade la partición
  $\text{SC total}=\text{SC dentro}+\text{SC entre}$, que es la de Estadística 13
  con los grupos en el papel del modelo;
- la **Proposición 12.4** es donde un informe pierde la diferencia entre «cero» y
  «no hay dato»: agrupar por categóricas devuelve $i\cdot j$ grupos, y en los
  vacíos **la suma devuelve $0$ y la media devuelve faltante**. El primero no se
  distingue de un cero medido.

**Dos infracciones propias que cazó `formato.py`**, y conviene recordar que las
caza: la construcción de golpe «no es X, es Y» de la regla 14, y la palabra
*sucursal* de la regla 15. Las dos en Python 12, las dos en prosa que sonaba
bien al escribirla.

**Y un número escrito a ojo**, del tipo que el punto 5 ya tenía anotado: el
ejercicio 1 de Python 12 decía $2{,}7267$ y $-3{,}6067$ cuando eran $2{,}64$ y
$-3{,}6933$. Lo cazó `salidas.py`. La lección es la de siempre: **correr la celda
y leer su salida es parte de escribirla**, también en los ejercicios.


### 3.12 ML 10, y el desglose de ISLP 7 (18-09-2026)

**ISLP capítulo 7 se parte en dos.** El corte está donde el libro cambia de
estrategia: hasta §7.4 se **construye una base** y se ajusta por mínimos
cuadrados; de §7.5 en adelante se **penaliza o se localiza**. Así:

- **ML 10**, §7.1–7.4: polinomios, funciones escalón, el marco de las funciones
  base y los splines de regresión. Publicada.
- **ML 11**, §7.5–7.7: splines de suavizado, regresión local y GAMs. Pendiente.

Eso obligó a renumerar `ml/index.qmd` de la 11 a la 39 y a corregir **15
referencias cruzadas**. Esta vez la comprobación **no se hizo de memoria**: hay un
script que lee el índice, resuelve cada «Machine Learning N» contra el título de
la fila N y las imprime en paralelo para leerlas de un vistazo. Merece la pena
rehacerlo en cada desglose:

```sh
python3 - <<'EOF'
import re, pathlib
RAIZ = pathlib.Path(".")
idx = (RAIZ/"ml"/"index.qmd").read_text(encoding="utf-8")
filas = {int(m.group(1)): m.group(2) for m in re.finditer(
    r'<span class="num">(\d+)</span>.*?<span class="tit">(?:<a [^>]*>)?(.*?)(?:</a>)?</span>', idx)}
for p in sorted(RAIZ.glob("*/[0-9]*.qmd")):
    for m in re.finditer(r"Machine Learning (\d+)(?:\s*(?:a|y)\s*(\d+))?\*\*: ([^\n.]{0,70})",
                         p.read_text(encoding="utf-8")):
        nums = [int(m.group(1))] + ([int(m.group(2))] if m.group(2) else [])
        print(f"{p.parent.name}/{p.name:44s} ML {nums} -> "
              f"{' / '.join(filas.get(n,'??') for n in nums)[:50]:52s} | dice: {m.group(3).strip()[:44]}")
EOF
```

**Lo que sostiene ML 10:**

- la **Proposición 10.2** parte la elección de base en dos mitades que suelen
  confundirse: **el espacio decide el ajuste y la base decide el
  condicionamiento**. Medido: la base de potencias pasa de $10^{0}$ a $10^{5}$ de
  condición entre el grado 1 y el 15, la base ortonormal de la QR se queda en
  $10^{0}$, y las dos dan el **mismo ajuste** a $10^{-6}$. Enlaza directamente con
  lo aprendido rompiendo el CI en ML 9;
- la **Proposición 10.3** demuestra que ajustar funciones escalón **devuelve las
  medias por tramo**, leyendo las ecuaciones normales componente a componente. Une
  la regresión con la agregación de Python 12, y da la base mejor condicionada de
  la lección: $1{,}2634$;
- la **Proposición 10.5** cuenta $4(K+1)-3K=K+4$ y demuestra que el coeficiente
  de un nudo es **el salto de la tercera derivada dividido entre seis**. Medido
  estrechando el intervalo: los saltos de $f$, $f'$ y $f''$ se dividen por diez al
  dividir $h$ por diez, y el de $f'''$ se queda clavado en $-1{,}697943$. La
  lectura que deja: **un nudo no rompe la curva, le da permiso para cambiar de
  curvatura**.

**Una afirmación que NO se escribió, y por qué.** El plan era demostrar que los
splines se portan mejor que los polinomios cerca de los bordes, que es lo que
sugiere §7.4.5. **Se midió antes de escribirlo y los datos no lo sostienen**: con
regresión sobre $300$ observaciones ruidosas, el barrido de grados de libertad de
$6$ a $20$ sale mezclado, porque el fenómeno de Runge es de **interpolación** y se
atenúa mucho al ajustar por mínimos cuadrados con muchos puntos. La proposición se
retiró, el bloque de Fuentes lleva un apartado **«Lo que NO se afirma»** diciéndolo,
y el reto 2 pide reproducir la medición y contrastarla con el caso de
interpolación. Conviene conservar ese apartado como recurso: es mejor que una
proposición endeble.

**Otra fragilidad de versión cazada por el contraste.** `float()` sobre un array
de **un** elemento dejó de funcionar en NumPy 2. Se arregla con `.item()`. Van
tres clases distintas ya: el `repr` de los escalares, el renombrado de dtypes, y
esta.


### 3.13 Python 13, y matplotlib en el CI (18-09-2026)

**Dependencia nueva en el workflow.** El CI instalaba numpy, scipy, scikit-learn,
pandas y playwright; ahora instala también **matplotlib**, o el gate de salidas no
podría ejecutar ninguna celda de esta lección. Es el mismo trámite que hizo falta
para pandas con Python 9, y conviene recordarlo para Python 14 en adelante.

**El riesgo de versión aquí era el mayor de todos y salió bien.** La máquina tiene
matplotlib **3.3.4** y el runner instala la **3.11.2**: ocho años de diferencia,
con cambios de estilo por omisión en medio. Antes de escribir una sola línea se
probaron seis candidatas a afirmación en las dos versiones, y **las seis salieron
idénticas**: los bordes explícitos de un histograma, los diez bins por omisión, los
límites automáticos con su margen del 5 %, los datos recuperados de un artista, las
posiciones de las marcas y el recuento de artistas. Esa comprobación previa es lo
que permitió escribir la lección con dígitos en vez de con vaguedades.

**Lo que sostiene Python 13:**

- la **Proposición 13.2** enuncia lo que esta plataforma ya practicaba sin
  escribirlo: **un gráfico se puede comprobar sin mirarlo**, porque el artista
  guarda los arreglos y no los píxeles. Es el principio de `verificar/visuales.py`,
  y ahora está dicho en una lección;
- la **Proposición 13.3** da la fórmula exacta de los límites automáticos,
  $[\min-0{,}05R,\ \max+0{,}05R]$, de donde el alto del panel vale siempre
  $1{,}1R$. La consecuencia medida: una subida real del $10$ % ocupa el $90{,}9$ %
  del panel, un factor de exageración de **9,1**, que baja a $0{,}83$ fijando el eje
  en $(0,12)$;
- la **Proposición 13.4** muestra que el ancho de bin por omisión depende **solo de
  dos observaciones**. Una única observación en $30$ multiplica el ancho por más de
  cinco y deja el $99{,}8$ % de los datos apretado en $3$ barras de $10$;
- la **Proposición 13.5** explica el eje actual como variable global y por qué el
  mismo fragmento dibuja en sitios distintos según la historia del programa.

El bloque de Fuentes dice explícitamente que el margen del $5$ % y los diez bins
son **valores de configuración de la biblioteca**, no resultados: se afirman porque
se midieron en las dos versiones, y si una futura los cambia, el gate de salidas lo
detectará. Esa es la forma honesta de citar un valor por omisión.

**§9.3 no se trata**, porque enumera bibliotecas que esta página no puede ejecutar.
Queda dicho en la lección, con la razón.


### 3.14 ML 11 y Python 14 (18-09-2026)

**ISLP capítulo 7 queda cubierto entero.** ML 10 hizo §7.1–7.4 y ML 11 hace
§7.5–7.7. Esta vez **no hubo que renumerar**: la fila 11 ya estaba reservada al
partir el capítulo.

**ML 11 se organiza alrededor de una sola definición.** La de **suavizador
lineal**, $\hat{y}=Sy$ con $S$ independiente de $y$, que convierte tres métodos
aparentemente distintos en un objeto y explica por qué los árboles de la lección
12 quedan fuera: su matriz dependería de la respuesta y la traza dejaría de contar
parámetros.

- la **Proposición 11.2** trabaja la versión **discreta** del spline de suavizado,
  con $\lVert Dg\rVert^2$ en lugar de la integral, porque así todo es calculable.
  $S_\lambda=(I+\lambda D^\top D)^{-1}$ es simétrica, sus eigenvalores son
  $1/(1+\lambda\mu_j)$ y los grados de libertad su suma. **El paralelo con ridge
  es exacto**: allí los factores eran $d_j^2/(d_j^2+\lambda)$. El límite es
  $\dim\ker(D)=2$, y $2$ es la dimensión de las funciones lineales;
- la **Proposición 11.3** demuestra que la regresión local es un suavizador lineal
  cuya matriz **no** es simétrica, y que reproduce constantes y rectas;
- la **Proposición 11.5** da la identificabilidad —cada $f_j$ salvo una constante—
  y la convergencia del backfitting, que en el caso lineal llega a mínimos
  cuadrados. Medido: converge en $7$ iteraciones y coincide a $10^{-8}$.

**El contraste L3 de ML 11 vale la pena recordarlo.** Si un método es lineal en
$y$, alimentarlo con los **vectores unitarios** devuelve las columnas de su matriz.
Con eso se extrae la matriz de un suavizador de la librería sin abrir su código, y
de ahí sale que los grados de libertad de $k$ vecinos uniformes valen
**exactamente** $n/k$, porque cada punto es vecino de sí mismo. El reto 2 pide
aplicar la misma técnica a un árbol y comprobar que **falla**, que es la manera de
ver qué significa «no lineal».

**Python 14 no necesitó dependencias nuevas.** Lo que sostiene la lección:

- la **Proposición 14.2** lee el remuestreo como el `groupby` de Python 12 con los
  intervalos como clave, así que no rehace nada; y separa bajar de frecuencia, que
  agrega, de subir, que **no produce datos**: $58$ faltantes de $61$ posiciones, y
  rellenarlos los hace desaparecer junto con la señal de que ahí no se midió;
- la **Proposición 14.3** da el retraso de una media móvil en forma cerrada,
  $b(k-1)/2$, con una demostración de una línea: una función afín conmuta con la
  media, y la media de los instantes de la ventana es $t-(k-1)/2$. Medido: $2{,}5$
  exactos, y centrando desaparece. Además **la media móvil es un suavizador
  lineal**, comprobado con la técnica de ML 11, con $\operatorname{tr}(L)=(n-k+1)/k$;
- la **Proposición 14.4** cierra con el cambio de hora: el 27 de octubre de 2024 en
  Madrid tiene **25 horas**, y la librería **se niega** a convertir una hora
  ambigua en lugar de adivinar.

**Cuatro fragilidades de versión cazadas en esta tanda**, todas por el contraste
previo y ninguna por el CI:

1. La **fórmula** de los grados de libertad se vuelve inestable a $\lambda$ enorme:
   los eigenvalores «nulos» valen $10^{-15}$ y multiplicarlos por $10^{12}$ los
   resucita. El límite se cuenta, no se evalúa.
2. Imprimir el **mayor de los eigenvalores nulos** es ruido: hasta cambia de signo
   entre versiones.
3. Un residuo de convergencia a $10^{-13}$ y unos ceros con signo, otra vez.
4. En Python 14, dos de una clase nueva: **`.loc` por rango sobre un índice
   desordenado cambió de conducta** entre pandas 1.x y 3.0 —permitía y ahora
   levanta error—, y la **clase de la excepción** de una hora ambigua cambió al
   pasar de `pytz` a `zoneinfo`. Las celdas no afirman ninguna de las dos: ordenan
   antes y capturan sin nombrar la clase. **Pero la lección lo cuenta en prosa**,
   porque saberlo es contenido útil y está medido.

Ese último punto merece quedarse como criterio: **cuando una conducta depende de la
versión, la celda no la afirma y la prosa la explica.**


### 3.15 Python 15 y 16: el módulo queda cerrado (18-09-2026)

**Python 16 de 16.** Con estas dos se cierra la Fase 1, y con ella el tercer
módulo del plan, detrás de Estadística y Álgebra.

**Python 15, «Rendimiento», tenía un problema de diseño que merece quedarse
escrito.** El nivel L3 pide medir, y la regla 7 prohíbe citar dígitos de algo que
dependa de la máquina —y **un cronómetro es exactamente eso**—. La salida fue
**medir lo contable en vez de lo cronometrable**:

- la **Proposición 15.2** cuenta pasos del intérprete: $200\,000$ contra **cero**,
  con el mismo resultado. El escalar de Python ocupa $32$ bytes y el valor dentro
  del arreglo, $8$;
- la **Proposición 15.3** separa **reservas** de **tráfico de memoria**: la
  expresión suelta pide dos arreglos enteros de más y la que escribe en un destino
  ya creado pide cero, con las mismas lecturas y escrituras;
- la **Proposición 15.4** demuestra con la suma de Gauss que crecer de uno en uno
  cuesta $n(n-1)/2$ copias, comprobado exacto en cuatro tamaños;
- la **Proposición 15.5** dice explícitamente **qué se puede publicar de una
  medición de tiempo**: la propiedad —«más rápida», «por más de un factor diez»—
  y el recuento de operaciones, nunca los segundos. Por eso la lección **no
  contiene un solo dato en segundos**.

**Python 16, «Anatomía de un proyecto», usa esta plataforma como ejemplo
trabajado.** Sus tres resultados:

- la **16.1**: fijar la semilla **no basta**. La suma en coma flotante no es
  asociativa, así que barajar las filas cambia un total —por debajo de $10^{-9}$
  relativo, pero no cero—. Reproducible exige datos, código, versiones, semilla
  **y orden**;
- la **16.2**: la huella como contrato, con la condición que se olvida: cambia
  también al **reordenar**, aunque el conjunto de filas sea el mismo;
- la **16.4**: el cauce es un grafo, y existe orden de ejecución **si y solo si**
  es acíclico. Un paso que lee lo que otro posterior escribe cierra el ciclo.

Las tres se leen sobre el propio repo: `afirmaciones.json` es un manifiesto de
grano fino, `salidas.py` lo comprueba en cada construcción, y
`grafo/build_graph.py` construye el grafo de la 16.4 con las lecciones como pasos.

**Un descuido propio que conviene no repetir.** El visual de las huellas se
escribió con resúmenes **inventados** para los casos modificados. Se detectó al
releer, se calcularon los reales con el mismo código de la celda y se comprobó que
son idénticos en las dos versiones de pandas. **Un visual no puede enseñar un
número que no se haya calculado**, igual que una celda. No hay gate que lo
compruebe: `visuales.py` mide que los controles muevan el dibujo, no que los
números dibujados sean ciertos.

**El generador de retos ya funciona solo.** Las secciones de Python 15 y 16 las
escribió `proyectos/genera_retos.py` al publicarlas, sin intervención, y el
auditor de símbolos cazó el único que faltaba declarar. Las dos deudas cerradas
hoy siguen en cero sin esfuerzo.


### 3.16 ML 12, y la medición que rompió el CI (18-09-2026)

**ML 12, «Árboles de decisión», cubre ISLP §8.1 entera.** Cinco resultados, y el
orden invierte a propósito el del libro: la **caída del RSS se calcula primero**,
porque de esa fórmula salen todas las preferencias del método.

- la **12.2b**: partir un nodo baja el RSS en exactamente
  $\frac{n_I n_D}{n_I+n_D}(\bar{y}_I-\bar{y}_D)^2$. Dicho así, el algoritmo no
  busca «donde cambia la tendencia» sino **medias distintas con lados
  equilibrados**: un corte que deja una sola observación aparte pesa casi $1$ por
  extrema que sea, y uno que parte por la mitad pesa $n/4$;
- la **12.3**: hay datos donde **todos** los cortes tienen caída exactamente $0$
  y un árbol de dos niveles llega a RSS $0$ —la respuesta en diagonal sobre dos
  variables binarias—. Ahí queda demostrado por qué el árbol se crece de más y se
  poda después, en vez de pararlo por el camino;
- la **12.5**: el tamaño del subárbol óptimo **no crece** al subir el precio de
  una hoja. **Es la Proposición 7.5 de ML 7** con hojas en lugar de predictores:
  aquella lección anunció que el argumento valía para cualquier ajuste penalizado
  linealmente por un coste creciente, y aquí se cobra la promesa. La página lo
  dice en el enunciado y en Fuentes, en vez de presentarlo como resultado nuevo;
- la **12.7**: cualquier impureza cóncava mejora al partir (Jensen), y el error
  de clasificación, por ser **lineal a trozos**, da ganancia cero en cortes donde
  Gini gana. En $20\,000$ cortes al azar el error se queda en cero $10\,174$
  veces y Gini solo $12$. Eso es el reparto de papeles del libro: Gini o entropía
  para crecer, error para podar;
- la **12.8**: el árbol **no** es un suavizador lineal, que es la deuda que dejó
  abierta la Definición 11.1. Con la partición fija el ajuste es una proyección
  de traza $J$; con la partición elegida mirando $y$, deja de ser lineal. La
  «matriz» que se obtiene alimentándolo con los vectores unitarios tiene traza
  $54{,}566667$ para un árbol de **cuatro** hojas y ni siquiera reproduce su
  propia predicción.

**La sucesión de podas se calcula sin tantear $\alpha$.** Enumerando los $26$
subárboles del árbol crecido y quedándose con la **frontera inferior** de los
puntos $(\lvert T\rvert,\text{RSS})$ salen los siete que llegan a ganar y los
valores exactos donde cambia el ganador. El tramo de $3$ hojas va de $1{,}3777$ a
$76{,}8005$, y los datos se generaron con tres tramos.

**Lo que se comprueba y no se demuestra queda dicho.** Que la sucesión de
subárboles óptimos está **encajada** se verifica por enumeración completa sobre un
árbol concreto; la demostración general es de Breiman y no cabe aquí. Lo que sí se
demuestra en general es que el tamaño no crece.

#### El CI se rompió por una medición, y la causa vale más que el arreglo

El empujón anterior (`28a83c9`) reventó el gate de salidas con **una sola**
afirmación: Python 15 decía «la expresión `(a*b) + (c*d)` reserva 2 arreglos
enteros de más» y en el runner ya no lo decía. La celda medía el **pico de
memoria** con `tracemalloc` y dividía por el tamaño de un arreglo.

Eso es exactamente lo que la Proposición 15.5 de esa misma lección prohíbe: un
número que depende del asignador, de la versión y del sistema. Las dos parejas de
versiones locales no lo cazaron porque **las dos son macOS**; el runner es Linux y
usa Python 3.12 para el verificador, no el 3.14 del entorno de contraste.

El arreglo no fue subir una tolerancia sino **dejar de medir**: un `np.ndarray`
derivado que implementa `__array_ufunc__` cuenta los arreglos que cada operación
pide **antes de que ocurra**. Una operación sin destino crea uno; con `out=` no
crea ninguno. La expresión suelta crea $3$ —el resultado y dos temporales— y la
versión con destinos crea $0$, y esos números son los mismos en cualquier máquina
porque ya no se miden: se cuentan. La regla se aplicó también al ejercicio 2, que
pedía los temporales de $4$ operaciones y contaba $4$ arreglos en vez de $3$.

**La lección de método:** *medir* produce afirmaciones que el gate romperá tarde o
temprano; *contar* produce afirmaciones que aguantan. Cuando una celda necesite un
número que salga de un reloj o de un asignador, la salida es interceptar la
operación, no cronometrarla mejor.

**Y una limitación del contraste de dos versiones, ya vista dos veces.** En ML 9
fue el mismo LAPACK en los dos entornos; aquí, el mismo sistema operativo. El
contraste local es necesario y **no es suficiente**: lo que de verdad decide es si
la afirmación depende de algo que el código no controla.

### 3.17 ML 13, y una afirmación del libro que la medición no sostiene (18-09-2026)

**ML 13 cubre ISLP §8.2 entera** y con ella el capítulo 8. Cinco resultados:

- la **13.2**: la varianza del promedio de $B$ ajustes de varianza $\sigma^2$ y
  correlación $\rho$ vale $\rho\sigma^2+(1-\rho)\sigma^2/B$. La parte (c) es la que
  ordena el capítulo: **la fracción del camino recorrido hasta el suelo vale
  $1-1/B$ y no depende de $\rho$**. O sea, $B$ decide la velocidad —con $100$
  árboles se ha recorrido el $99\,\%$ siempre— y $\rho$ decide dónde está el suelo.
  Por eso el resto de la lección no trata de poner más árboles;
- la **13.3**: qué estima exactamente el error fuera de la bolsa. Cada
  observación queda fuera de unos $B/e$ árboles, así que la estimación evalúa un
  bosque de ese tamaño y **no** del que se va a usar. Medido: $74{,}03$ veces
  fuera contra las $73{,}39$ previstas, con $B=200$ y $n=200$;
- la **13.5**: un predictor está disponible en un nodo con probabilidad $m/p$
  —cuenta de subconjuntos— y **existen datos donde bajar $m$ mejora y datos donde
  empeora**;
- la **13.7**: un paso de impulso baja el RSS en exactamente
  $(2\lambda-\lambda^2)\lVert g\rVert^2$, porque el ajuste por hojas cumple
  $\langle r,g\rangle=\lVert g\rVert^2$. De ahí sale la condición exacta de
  convergencia, $0<\lambda<2$, en lugar de «la tasa debe ser pequeña». La
  identidad se comprueba en $190$ pasos, **incluida la tasa que diverge**;
- la **13.8**: ninguna combinación de árboles deja de ser escalonada, con a lo
  sumo $\sum_b(J_b-1)+1$ tramos. Medido: $8$, $101$ y $31$ tramos contra cotas de
  $8$, $421$ y $61$.

#### Lo que la medición no sostuvo

ISLP motiva el bosque aleatorio con **un predictor muy fuerte**: los árboles del
bagging lo usarían todos, quedarían muy parecidos y promediarlos serviría de
poco. El razonamiento sobre $\rho$ es correcto, pero **la conclusión sobre el
error no se sigue**, y al medirlo sale al revés: con una variable insustituible,
bajar $m$ empeora el error en todos los valores probados, aunque $\rho$ caiga de
$0{,}95$ a $0{,}16$.

Lo que sí funciona es el caso de los **sustitutos**: cuatro predictores que miden
lo mismo por caminos distintos. Ahí $m<p$ gana en las tres semillas probadas y el
bagging no gana ninguna. La página enuncia eso como Proposición 13.5b —una
afirmación de existencia, demostrable exhibiendo los dos conjuntos— y lo dice en
«Del libro» y en Fuentes.

**El método que evitó el error**: antes de escribir la sección se probaron seis
configuraciones y se comprobó el hallazgo en varias semillas. La primera versión
del experimento, con un solo diseño, habría «confirmado» lo que el libro dice sin
que fuera cierto. Es el mismo caso que ML 10 con los splines y Runge.

**Otro descuido propio, del mismo tipo que los ya anotados.** La prosa citaba
$0{,}0887$ y $0{,}2396$ como prueba de que el impulso sobreajusta, de una fila que
se había quitado de la tabla al reorganizarla. Se rehízo la tabla para que el
sobreajuste **se midiera**: con $\lambda=1$ el entrenamiento recorre
$0{,}2136\to0{,}0475$ mientras la prueba toca fondo en $0{,}2378$ y vuelve a subir
a $0{,}2572$, y la celda lo afirma con dos booleanos. **Ninguna cifra de la prosa
puede quedar huérfana de su celda.**

**Y una divergencia que no se puede citar.** Con $\lambda=2{,}5$ el residuo se
dispara a $10^{23}$ y sus dígitos difieren entre entornos. La celda no los
imprime: comprueba la identidad en **relativo** y afirma solo el signo, que es
exacto. Es la regla 7 aplicada a un caso donde la cifra existe pero no significa
nada.

### 3.18 ML 14, el desglose del capítulo 9 y tres solvers tirados a la basura (18-09-2026)

**El capítulo 9 se parte en dos**, como se hizo con el 4, el 6, el 7 y el 8. Tiene
$13$ unidades enseñables y el ritmo real de estas páginas es de una lección por
cada cuatro o cinco:

- **ML 14** (esta): §9.1–9.2, el margen máximo y el clasificador de soporte
  vectorial;
- **ML 15**: §9.3–9.5, los núcleos, las más de dos clases y la pérdida bisagra.

Eso obligó a **renumerar el índice de ML de la 15 a la 39**, que pasan a 16–40, y
a subir en uno las $18$ referencias cruzadas «Machine Learning N» con $N\ge 15$
repartidas por nueve lecciones. Se hizo con script y se verificó con otro que
**resuelve cada referencia contra el título de la fila que apunta**: las $34$
referencias del sitio resuelven, y ninguna apunta a una fila inexistente. Ese
script **ya no es de usar y tirar**: quedó como `verificar/referencias.py` y corre
en el CI justo después de las citas, así que la próxima renumeración que deje una
referencia colgando rompe la construcción en lugar de pasar inadvertida.

#### El resultado que hace calculable el capítulo

El libro plantea el problema del margen máximo y lo deja en manos de un
solucionador de optimización convexa. Esta página añade la **Proposición 14.4**:

> el margen máximo vale la mitad de la distancia entre las envolventes convexas
> de las dos clases, y el hiperplano óptimo es la **mediatriz** del segmento más
> corto entre ellas.

La cota superior sale de Cauchy-Schwarz en tres líneas; que se alcanza, de un
argumento de convexidad. Con eso el margen se **calcula exactamente** con
geometría de instituto: envolvente convexa por cadena monótona, distancia
punto-segmento y mediatriz. El valor exacto sale $0{,}933609$ y probando $4000$
direcciones al azar el mejor margen hallado es $0{,}933589$: se acerca por debajo
y nunca lo pasa. De paso explica **por qué** los vectores de soporte son los que
son, y la Proposición 14.6 queda como corolario geométrico en lugar de salir de
las condiciones de complementariedad.

#### Tres intentos de resolver el margen blando, y por qué se abandonaron

Para §9.2 hacía falta el óptimo del programa cuadrático con holguras. Se
intentaron tres caminos y **los tres se tiraron**:

1. un SMO propio sin el término independiente en los errores: hueco de dualidad
   enorme y la búsqueda al azar encontraba soluciones mejores;
2. el SMO corregido con el término incluido: seguía sin converger, con huecos de
   hasta $48$;
3. un barrido por direcciones con malla adaptativa: el refinamiento estaba mal
   planteado y para $C$ grandes el óptimo hallado era peor que el de la búsqueda
   al azar por un factor de cuatro.

A la tercera se paró, que es lo que manda el procedimiento de depuración: tres
arreglos fallidos son un problema de arquitectura, no de detalle. **Y la
arquitectura equivocada era intentar resolver el problema.**

La Proposición 14.8 —al subir $C$, la holgura total no sube y el margen no
crece— se demuestra con el mismo argumento de intercambio de la Proposición 7.5
de ML 7, y **ese argumento no usa en ningún paso que la familia sea el conjunto
de todos los hiperplanos**. Vale para cualquier familia, finita incluida. Así que
la celda minimiza sobre una lista de $1\,449\,000$ hiperplanos fijada de
antemano, la misma para todos los $C$, y la comprobación es **exacta**, no
aproximada. El texto, la celda y el bloque de Fuentes dicen que eso es lo que se
calcula, y el reto 3 pide medir qué se pierde al confundirlo con la solución del
problema continuo.

**La lección de método**: cuando un cálculo se resiste, conviene mirar si el
enunciado que hay que comprobar necesita de verdad ese cálculo. Aquí no lo
necesitaba, y el enunciado sale reforzado por ser más general.

### 3.19 ML 15, y dos afirmaciones del libro precisadas (18-09-2026)

**Con ML 15 queda cubierto el capítulo 9 entero**, y con él todo ISLP de la 2 a
la 9 salvo §6.3, que sigue esperando a la lección de componentes principales.

El resultado que sostiene la lección es la **Proposición 15.1**: el $\beta$ óptimo
está en el subespacio generado por los datos, porque la componente ortogonal no
cambia ninguna restricción y solo engorda la norma. Sale en cuatro líneas con
Pitágoras, y de ahí se deduce que $f(x)=\beta_0+\sum_i c_i\langle x_i,x\rangle$.
**El libro da eso por sabido**, y sin la demostración el truco del núcleo parece
una casualidad afortunada en lugar de lo único que puede pasar.

Lo demás de la lección:

- la **15.3**: el núcleo polinómico y su mapa explícito, con la cuenta que enseña
  el tamaño del ahorro: con $p=1000$ y $d=5$ el espacio ampliado tiene
  $8\,459\,043\,543\,951$ coordenadas y evaluar el núcleo sigue costando mil
  multiplicaciones;
- la **15.4**: la matriz de Gram como criterio de descarte, con dos funciones que
  circulan como núcleos y **no lo son** —$\langle x,z\rangle-1$ y el «sigmoide»
  $\tanh(\langle x,z\rangle+1)$, con autovalores de $-7{,}61$ y $-1{,}58$—;
- la **15.6**: uno contra uno entrena $\binom{K}{2}$ clasificadores y uno contra
  todos $K$, pero el primero toca $(K-1)n$ observaciones y el segundo $Kn$. Con
  $K=26$: $325$ clasificadores contra $26$, y sin embargo $195\,000$
  observaciones contra $202\,800$. La intuición de que más clasificadores es más
  trabajo falla, y el libro no hace la cuenta;
- la **15.7**: la bisagra se anula exactamente en $y f\ge 1$ y la logística no lo
  hace nunca. Medido sobre $200$ puntos: los $159$ cómodos aportan $0$ al criterio
  con la bisagra y $21{,}008896$ con la logística. Ahí está, en una línea, por qué
  un método tiene vectores de soporte y el otro no.

#### Dos precisiones que la medición obligó a hacer

**La primera.** El libro presenta la bisagra y la logística como dos pérdidas muy
parecidas, las dibuja juntas y las llama sustitutas del error $0$–$1$. Al
comprobarlo sobre una malla de $24\,001$ puntos sale que **la logística en base
$e$ no acota al error $0$–$1$**: en $y f=0$ vale $\log 2=0{,}693\ldots$, por debajo
del escalón. Dividida por $\log 2$ sí lo acota, y con igualdad justo en el cero.
La página lo enuncia como Proposición 15.7c y lo dice en «Del libro».

**La segunda.** El término «núcleo» ya estaba en el glosario con el sentido de
Álgebra 3 —el espacio nulo de una matriz—. Un tooltip que dijera eso al pasar por
encima de «núcleo» en ML 15 sería falso. Se aplicó la **regla 21b**, que hasta
ahora solo se había usado con símbolos: la entrada global dice que el término está
sobrecargado, nombra los dos sentidos y remite a la lección. Es el primer caso de
21b aplicada a un término y no a un símbolo, y conviene recordar que la regla
cubre los dos.

#### Lo que no se demuestra, dicho donde toca

El **teorema de Mercer** —que la semidefinición positiva es también **suficiente**
para que exista el mapa— se usa implícitamente al llamar núcleos al radial y al
polinómico, y no se demuestra: exige teoría de operadores. Lo que sí queda
demostrado es la dirección necesaria, que es la que permite **descartar**, y para
el polinómico el mapa se construye a mano, así que ahí el teorema no hace falta.
Queda escrito en Fuentes.

### 3.20 ML 16, el capítulo más largo y la regla 7 aplicada a un pico (18-09-2026)

**El capítulo 10 no se desglosa: ya estaba repartido.** Tiene $18$ unidades
enseñables y el plan ya reservaba seis lecciones de Fase 4 para deep learning
(filas 35 a 40). Así que ML 16 cubre lo que **no** está ahí —§10.1, §10.2, §10.6
y §10.8— y la sección 5 de la lección dice en voz alta dónde va el resto:

- §10.3 *Convolutional Neural Networks* → ML 40;
- §10.7 *Fitting a Neural Network* → ML 35 a 39;
- §10.4 *Document Classification* y §10.5 *Recurrent Neural Networks* → **no
  están en el plan de ninguna fase**. Queda escrito en la lección para que la
  omisión sea una decisión y no un olvido.

No hizo falta renumerar nada.

#### Los cuatro resultados

- la **16.2**: con activación afín, una red de cualquier profundidad calcula una
  función afín. Medido: $88$ parámetros que se reducen a $4$. El libro dice que
  «colapsa»; aquí se demuestra por composición y se comprueba a $10^{-10}$;
- la **16.3**: en una variable, una capa de $K$ unidades ReLU es **exactamente**
  la familia de funciones lineales a trozos con a lo sumo $K$ quiebres. Las dos
  direcciones: la cota, porque cada unidad aporta un quiebre; y la
  representación, con la fórmula de reconstrucción por bisagras y $K+2$ unidades.
  Eso es más fuerte que «aproxima cualquier función» en este caso, y enlaza con
  los splines de ML 10: **la misma base, con los nudos aprendidos**;
- la **16.4**: el **pliegue** $P(x)=2\max(0,x)-4\max(0,x-\tfrac12)$ compuesto
  $d$ veces da exactamente $2^d$ trozos con $2d$ unidades; una sola capa
  necesitaría $2^d-1$. Con $16$ unidades en $8$ capas, $256$ trozos. En
  parámetros: $2^{20}$ trozos cuestan $120$ en profundidad y $3\,145\,726$ en
  anchura. La lección **avisa explícitamente** de que de ahí no se sigue que lo
  profundo sea mejor, solo que hay funciones baratas en profundidad;
- la **16.5**: el doble descenso, medido y declarado como medición.

#### La regla 7 aplicada al pico, que es el caso interesante

El error de prueba del ajuste de norma mínima **revienta** cerca de $d=n$: llega
al orden de $10^{12}$. La primera versión de la celda imprimía esas cifras con
cuatro decimales y **el contraste de versiones la cazó**: en $d=42$ salía
$9\,013\,768{,}3690$ en una y $9\,013\,768{,}3692$ en la otra.

Lo importante es *por qué*, porque no es un accidente: **el pico y el mal
condicionamiento son el mismo fenómeno**. La matriz llega a condición
$1{,}1\times10^{8}$ justo donde el error se dispara. Pedirle dígitos ahí es
pedirle precisión exactamente a lo que no la tiene.

La celda quedó así: **mide el condicionamiento antes de decidir cuántos dígitos
tiene derecho a imprimir**. Con condición por debajo de $10^3$ publica cuatro
decimales; por encima, solo el orden de magnitud. Y las afirmaciones fuertes son
comparaciones, que sí son reproducibles. Eso convierte la advertencia de ML 9 en
una práctica dentro de la celda, y no en algo que haya que recordar.

**Y una comparación que salió `False` y se quedó.** El segundo descenso baja
mucho —de $10^{12}$ a $0{,}6484$— pero **no** por debajo del mejor modelo
pequeño, que es el de $d=10$ con $0{,}0498$. La celda lo imprime y la prosa lo
dice: el doble descenso explica por qué un modelo enorme no es un desastre, no
por qué sería la mejor opción.

#### Un falso positivo de la regla 15 que valió la pena

`formato.py` rechazó la lección por **contexto de empresa**: la palabra
«tienda». Era la *tienda de campaña*, el nombre habitual de $T(x)$ en español. En
lugar de añadir una excepción al filtro, la función pasó a llamarse **pliegue**,
que además describe mejor lo que hace —dobla $[0,1]$ por la mitad— y encaja con
el verbo que la prosa ya usaba. El filtro se queda tal cual: un falso positivo
que se arregla con una palabra mejor no justifica debilitar la regla.

### 3.21 ML 17, el capítulo sin red de seguridad (19-09-2026)

**El capítulo 11 se parte en dos**, y esta vez el motivo estaba anotado desde el
13-09 en el punto 6: tiene $17$ unidades enseñables, una sola lección asignada, y
**no reaparece en ninguna fase posterior**. Deep learning tenía seis lecciones de
red en la Fase 4; supervivencia no tiene ninguna. Dejarlo en una lección habría
sido garantizar una pasada superficial sobre el único tema de ISLP que no vuelve.

- **ML 17**: §11.1–11.4, el caso sin covariables;
- **ML 18**: §11.5–11.7, la función de riesgo, Cox y su regularización.

Renumeración de la 18 a la 40, que pasan a 19–41, con $27$ referencias cruzadas
subidas en nueve lecciones. El gate `referencias.py` que se escribió para la
renumeración anterior hizo su trabajo a la primera.

**Y cazó dos referencias que el script no toca**, porque estaban en prosa y no
en el formato `**Machine Learning N**`:

- ML 16 decía «§10.3 va a la lección 40, §10.7 se reparte entre las lecciones 35
  y 39» en «Del libro», con los números de antes de la renumeración anterior;
- ML 04 tenía «**ESL, lección 20**», que apuntaba a una numeración de hace dos
  renumeraciones.

Las dos se reescribieron **en el formato que el gate sí verifica**. La lección de
método: al renumerar, revisar también las menciones en prosa, o mejor, escribirlas
siempre con el patrón que el gate reconoce.

#### Los tres resultados

- la **17.2**: los tres atajos para librarse de la censura, con el sesgo de cada
  uno calculado. El mejor de los tres, tratar la censura como suceso, converge
  **exactamente** a $S(t)G(t)$: el factor perdido es la supervivencia de la
  censura y tiene nombre. Medido con $200\,000$ sujetos: sigue a $S(t)G(t)$ con
  error máximo $0{,}0020$ mientras se aparta de $S(t)$ hasta $0{,}1452$. **No
  estima mal $S$: estima otra cosa, y la estima bien**;
- la **17.4**: Kaplan-Meier por dos caminos. Sin censura telescopa hasta la
  supervivencia empírica —comprobado en $601$ instantes a $10^{-12}$—, y con
  censura es **exactamente repartir a la derecha** la masa de cada censurado
  —comprobado en $1200$ instantes a $10^{-12}$—. De la segunda lectura se lee sin
  esfuerzo por qué la curva se queda en $0{,}194444$ y no llega a cero: el último
  dato es un censurado y su masa no tiene a quién repartirse;
- la **17.6**: la media y la varianza del log-rank salen de una hipergeométrica, y
  se comprueban **enumerando los $21$ repartos posibles** de un instante.

#### La calibración, medida en vez de prometida

El libro dice que el estadístico se distribuye «aproximadamente» como una
$\chi^2$. La página lo mide con $4000$ ensayos de $60$ sujetos y el resultado
obliga a matizar: rechaza el $11{,}10$ al $10\,\%$, el $6{,}02$ al $5$ y el $1{,}55$
al $1$. **Los tres por encima**, a $2{,}3$, $3{,}0$ y $3{,}5$ errores típicos.

La primera redacción decía «al 10 y al 5 la aproximación aguanta», y los números
la desmintieron: también están fuera. La versión publicada dice lo que hay —es
optimista en todo el rango— y añade lo que de verdad cambia con el nivel: el
**exceso relativo** crece del $11\,\%$ al $55\,\%$. Con la tabla va el error típico
del ensayo, para que se vea que no es ruido.

Es la tercera vez en la sesión que una redacción cómoda no sobrevive a la
medición, después del bosque aleatorio de ML 13 y de los dos textos del visual de
ML 12. El patrón es siempre el mismo: **escribir la conclusión antes de mirar la
tabla**.

### 3.22 ML 18: el capítulo 11 cerrado, y dos capítulos que eran el mismo (19-09-2026)

Con ML 18 **queda cubierto el capítulo 11 entero**, el que no reaparece en
ninguna fase posterior. Cinco resultados:

- la **18.2**: riesgo y supervivencia son la misma información. Comprobado en las
  dos direcciones con tres formas de riesgo distintas;
- la **18.4**: la proporcionalidad implica $S=S_0^{\theta}$, y de ahí que **las
  curvas del modelo no se crucen jamás**. Con un contraejemplo donde sí se cruzan
  —cociente de riesgos que pasa de $2{,}6667$ a $0{,}4000$, cruce en $t=7{,}55$ con
  las dos curvas en $0{,}1038$—, que es lo que convierte «hay que comprobar la
  proporcionalidad» en algo que se ve;
- la **18.5**: la verosimilitud parcial cancela el riesgo base. Y aquí está lo
  que más me gusta de la lección: en vez de repetir la cancelación, se **deduce
  una consecuencia comprobable**. Si solo entra el orden de los tiempos, entonces
  pasar todos los tiempos por cualquier función creciente tiene que dejar el
  ajuste idéntico. Cuatro transformaciones tan distintas como $t^3$ y $\log(1+t)$,
  y el mismo $\beta$ a $10^{-10}$;
- la **18.6**: el log-rank de ML 17 **es** la prueba de puntuación de Cox en
  $\beta=0$. Sin empates coinciden a $10^{-10}$ en cuatro tamaños; con $17$
  empates se separan —$1{,}207554$ contra $1{,}160413$— y el culpable tiene
  nombre: el factor de población finita. El libro los presenta en dos secciones
  distintas sin decir que son el mismo estadístico;
- la **18.7**: el índice de concordancia y lo que la censura le quita. Con censura
  fuerte quedan $2632$ pares de $7140$: se pierde el $63{,}1\,\%$ de las
  comparaciones y el índice se sigue calculando sobre lo que queda.

#### Otro número escrito a mano

El ejercicio 2 llevaba $0{,}343207$ como respuesta esperada y la celda da
$0{,}358358$. Lo cazó la ejecución de las celdas antes de registrar las
afirmaciones, no la relectura. Es el mismo error que ya está anotado en el punto
5 desde Python 12: **una cifra calculada de cabeza en un bloque de comprobación**.
El procedimiento lo caza siempre, pero conviene no escribirlas de cabeza.

#### Qué queda del capítulo, dicho en la lección

De §11.7 quedan fuera tres subsecciones y la lección las nombra una por una:
§11.7.2 queda cubierta de refilón por la invariancia de la 18.5; §11.7.3
—covariables que cambian con el tiempo— exige cambiar la maquinaria del conjunto
en riesgo; y §11.7.5 —árboles de supervivencia— no está en el plan de ninguna
fase. Se escribe para que la omisión sea una decisión.

### 3.23 ML 19: PCA, el signo arbitrario y §6.3 desbloqueado (19-09-2026)

Cinco resultados, y dos de ellos son identidades exactas que el libro presenta
como «dos puntos de vista»:

- la **19.2**: las componentes son los eigenvectores de la covarianza y la
  varianza proyectada es el eigenvalor. Comprobado contra $200\,000$ direcciones
  al azar, cuya mejor marca es $5{,}651898$ contra $5{,}653235$ y se queda a
  $1{,}09$ grados;
- la **19.3**: las $k$ primeras componentes dan la **mejor** aproximación de rango
  $k$, con error igual a la suma de los $\sigma^2$ descartados. Comprobado contra
  $3000$ subespacios al azar en rango uno y dos: **ninguno** mejora;
- la **19.4**: la varianza acumulada **es** el complemento del error relativo. No
  algo parecido: la misma cuenta escrita al revés, comprobada a $10^{-10}$;
- la **19.5**: multiplicar una columna por mil —la misma medida en otra unidad—
  lleva la primera componente de $[0{,}6165,\ 0{,}6836,\ 0{,}3906]$ a ser esa
  columna sola con el $99{,}9998\,\%$ de la varianza. Estandarizando, la respuesta
  no se mueve y la varianza total vale exactamente $p$;
- la **19.6**: el criterio del completado no sube. Baja de $96{,}938400$ a
  $23{,}290645$ en $40$ pasos, y el error en las casillas ocultas mejora un
  $91{,}5\,\%$ frente a rellenar con la media. Pero la última tabla enseña lo que
  la proposición **no** garantiza: con rango $8$ sobre $8$ columnas el error
  vuelve al de partida.

#### El signo de una componente es arbitrario

Si $\varphi$ es una componente, $-\varphi$ también, con la misma varianza
explicada. Dos versiones de la misma biblioteca pueden devolver una u otra, las
dos correctas, y cualquier cifra publicada de sus coeficientes dejaría de
cuadrar. La celda **fija el signo** —que la coordenada de mayor magnitud sea
positiva— antes de imprimir nada, y la lección lo explica donde toca.

Ningún libro lo menciona y es exactamente el tipo de detalle que rompe una
afirmación en el gate meses después.

#### §6.3 queda desbloqueado

*Dimension Reduction Methods* quedó fuera de ML 8 porque necesitaba componentes
principales. Con ML 19 ya se puede escribir **ML 20**, y con ella los capítulos
del 2 al 9 de ISLP quedarán cubiertos **sin ningún hueco**.

### 3.24 ML 20: §6.3 cerrado y los capítulos 2 a 9 sin huecos (19-09-2026)

**Se cierra una deuda de hace once lecciones.** §6.3 quedó fuera de ML 8 porque
necesitaba componentes principales; con ML 19 publicada, ML 20 la cubre y **los
capítulos 2 a 9 de ISLP quedan cubiertos sin ningún hueco**. El reparto completo
está en el punto 2 y en la sección 4 de la propia lección.

El resultado que ordena la lección es la **Proposición 20.2**: los tres métodos
se escriben con el mismo molde, $\hat{y}=\sum_j u_j f_j u_j^\top y$, y lo único
que cambia es $f_j$:

| método | $f_j$ |
|---|---|
| mínimos cuadrados | $1$ |
| ridge | $d_j^2/(d_j^2+\lambda)$ |
| PCR con $M$ | $1$ si $j\le M$, $0$ si no |

Dicho así, **PCR es ridge con el mando en dos posiciones**. El libro lo presenta
como método aparte con su propia motivación, y esa lectura ahorra memorizar dos
historias. El visual los pone lado a lado sobre el mismo eje.

Lo demás:

- la **20.3**: PCR elige sin mirar $y$, con el conjunto que lo hace caro —seis
  variables con un factor común y una respuesta que depende de un contraste—.
  La primera componente se lleva el $88{,}70\,\%$ de la varianza con correlación
  $-0{,}0800$; la segunda, el $3{,}15\,\%$ con $0{,}9714$. PLS se queda a un $5\,\%$
  de mínimos cuadrados con **3** componentes y PCR necesita las **6**;
- la **20.5**: la primera dirección de PLS es $X^\top y$ normalizado, comprobado a
  $10^{-10}$, y con todas las componentes los dos métodos coinciden con mínimos
  cuadrados;
- la sección 3 mide **los dos regímenes con el mismo código**: con la señal en la
  dirección de máxima varianza los dos dan $0{,}0918$ fuera de la muestra; con la
  señal en un contraste, PCR se queda en $3{,}0658$ y PLS baja a $0{,}0931$. El
  libro dice que PLS «no suele ser mejor»; aquí se ve **de qué depende**.

#### La advertencia de ML 19 mordiendo en ML 20

La primera versión de la celda de la sección 2 **falló el contraste de versiones**:
las correlaciones de cada componente con $y$ salían con signos opuestos en los dos
entornos. Causa: el signo de un vector singular es arbitrario, que es exactamente
lo que ML 19 acababa de anotar. Se aplicó la misma convención —coordenada de mayor
magnitud positiva, fijando también la columna de $U$— y quedó estable.

Sirve de confirmación de que la advertencia valía la pena: **apareció en la
lección siguiente**.

#### El mismo descuido, por cuarta vez

El ejercicio 1 llevaba $3{,}743017$ y el intérprete daba $3{,}495813$. Y esta vez
con agravante: el valor correcto se había calculado **en la misma orden** que
escribía el bloque, de modo que estaba a la vista y aun así se escribió el otro.

La costumbre que hay que adoptar, y que no basta con anotar: **calcular primero en
una orden aparte, leer el resultado, y solo entonces escribir el bloque**. Las
cuatro veces las cazó el procedimiento antes de publicar, pero el procedimiento no
debería tener que cazarlas.

### 3.25 ML 21: el capítulo 12 cerrado, y la costumbre que sí funcionó (19-09-2026)

Cuatro resultados, y dos de ellos convierten advertencias del libro en números:

- la **21.2**: las dos formas del criterio de K-means son la misma suma. El libro
  la da como ecuación sin demostrar, y de ella depende que el algoritmo tenga
  sentido: sin ella, recalcular centros no tendría por qué bajar nada. Aquí sale
  en cuatro líneas;
- la **21.3**: baja en cada paso y termina;
- la **21.4**: termina en un óptimo **local**, y esta vez **medido contra la
  verdad**. Sobre nueve puntos se enumeran las $18\,150$ asignaciones sin grupos
  vacíos —$3025$ particiones, que coincide con $S(9,3)$— y se obtiene el mínimo
  exacto $1{,}54666667$. Un arranque concreto termina en $77{,}70333333$: **un
  factor de cincuenta**. La advertencia del libro deja de ser un consejo;
- la **21.6**: dos núcleos unidos por un puente, donde el enlace simple y el
  completo dan particiones distintas en $K=2$ **y** en $K=3$.

Y la sección 4 pone **la misma tabla sobre ruido puro y sobre grupos reales**: las
bajadas del criterio son $39{,}8$, $27{,}9$, $21{,}1$, $18{,}4$, $15{,}2$ por
ciento cuando no hay nada, y $52{,}8$, **$84{,}5$**, $14{,}7$ cuando hay tres
grupos. Esa diferencia es todo lo que hay para elegir $K$, y es un juicio sobre
una curva.

#### La costumbre nueva funcionó a la primera

Tras cuatro números escritos de cabeza, esta lección se hizo al revés:
**calcular los valores de los ejercicios en una orden aparte, leerlos, y después
escribir el bloque `check`**. Los dos ejercicios cuadraron a la primera —$32{,}0$
y $9330$— y el auditor de símbolos tampoco encontró descuadres.

Merece quedar escrito porque el coste es cero: una orden más, antes en lugar de
después.

#### El primer intento de la 21.6 no discriminaba

La primera versión del contraejemplo —una cadena de cinco puntos y un par
apartado— daba **la misma partición con los tres enlaces**, y la celda lo dijo
con un `False`. Hubo que buscar el diseño: dos núcleos compactos unidos por un
puente de dos puntos sueltos, que separa simple de completo en dos valores de $K$
a la vez.

Es el mismo patrón de ML 13 y ML 17: **la conclusión se escribe después de mirar
la tabla, no antes**.

### 3.26 ML 22: la Fase 2 de ISLP cerrada, y otra deuda pagada (19-09-2026)

**Con ML 22 se cierra la Fase 2 de ISLP entera**: los trece capítulos quedan
cubiertos o repartidos, con las omisiones nombradas una por una en las lecciones
que tocan.

Y se paga la segunda deuda declarada del proyecto. Estadística 17 enunció
Benjamini-Hochberg y **demostró solo el caso en que todas las nulas son
ciertas**, dejando el general escrito en su bloque de Fuentes como pendiente.
ML 22 lo demuestra.

#### La lección se diseñó para NO repetir

Lo primero fue comprobar qué había ya en Estadística 17: FWER, Bonferroni, Holm,
la definición del FDR, el enunciado de BH y un visual con los cuatro umbrales.
Escribir ISLP 13 entero habría duplicado media lección. Así que ML 22 cubre
**solo lo que añade**: §13.3.3, §13.4.2 en su caso general y §13.5. Se dice en
«Del libro» y en el `.hilo`.

Conviene recordar este paso: **antes de escribir una lección de un capítulo que
toca un tema ya tratado, leer la lección anterior y decidir qué se añade.**

#### La demostración

La clave es un lema que hace elemental todo lo demás:

> **22.1**: si Benjamini-Hochberg rechaza la hipótesis $i$, sustituir $p_i$ por
> $0$ deja el mismo número de rechazos.

Con él, el suceso $\{p_i\le t_k,\ R=k\}$ se reescribe como
$\{p_i\le t_k,\ R^{0}_i=k\}$, donde $R^{0}_i$ **no depende de $p_i$**, y ahí ya
se puede usar la independencia. La suma $\sum_k \frac1k\cdot\frac{\alpha k}{m}$
colapsa a $\alpha/m$ por hipótesis cierta, y sumando salen $\alpha m_0/m$.

El lema se comprueba por fuerza bruta en $2449$ casos sacados de $20\,000$
tandas, **sin un solo fallo**. Y la cota resulta **casi exacta**: $0{,}0978$
contra $0{,}1000$, $0{,}0747$ contra $0{,}0750$, $0{,}0496$ contra $0{,}0500$.

#### Dos cosas medidas que el libro dice más flojo

**BH no controla el FWER**, y la tabla enseña cuánto: $0{,}1782$ y $0{,}3083$
frente a los $0{,}036$ de Bonferroni. A cambio, potencia $0{,}8068$ contra
$0{,}5837$.

**El remuestreo no es solo para supuestos dudosos.** §13.5.3 lo presenta así, y
la medición es más rotunda: con ocho observaciones por grupo la fórmula normal se
pasa **también con datos normales** —rechaza el $1{,}75$ al nivel del $1$—,
porque el estadístico no es normal con esa muestra. Falla el supuesto que nadie
duda.

#### El contraste de versiones, otra vez útil

La primera versión del valor p por permutación difería en un ensayo de $2000$
entre los dos entornos. Causa: alguna barajada reproduce la muestra original y
ahí $t$ iguala al observado salvo por el último bit. La comparación «al menos tan
extremo» se hizo con tolerancia, que además es **la convención correcta**: el
empate cuenta.

#### La costumbre nueva, dos de dos

Los valores de los dos ejercicios se calcularon en una orden aparte antes de
escribir los bloques `check`, y cuadraron a la primera —$0{,}0375$ y $99$—. Van
dos lecciones seguidas sin corrección.

### 3.27 Series de tiempo 01: el módulo vacío arranca (19-09-2026)

El sidebar tenía dos módulos sin una sola página. Uno de los dos ya no.

**Series de tiempo 01 — «Descomposición: tendencia, estacionalidad y residuo»** es
la primera lección del proyecto que **no sigue ningún libro**. Los cuatro módulos
anteriores se apoyan en un índice verificado —ISLP, MML, McKinney, Think Bayes,
Think Stats—; aquí no hay ninguno que cubra el tema, así que cada resultado se
enuncia y se demuestra o se mide en la página. El bloque «Del libro» lo dice con
todas las letras y remite a lo más cercano que sí existe en el sitio: ML 11 —la
media móvil como suavizador lineal— y Python 14 —ventanas móviles con pandas—.

#### Lo que la lección añade

La descomposición suele presentarse como una receta. Aquí se presenta como un
problema mal planteado que hay que cerrar:

> **1.2**: la definición por sí sola **no determina** las componentes. Si
> $(T,S,R)$ sirve, $(T+c,\ S-c,\ R)$ también, y $(y_t,0,0)$ siempre cumple.

Sin una restricción no hay nada que decidir, y de ahí sale la convención de que
el perfil estacional sume cero.

La pieza con contenido es la **1.4**, que trata la media móvil como filtro y dice
exactamente qué le hace a cada frecuencia: **anula** el periodo $m$ sin error,
**reproduce** las rectas, a $t^2$ le suma una constante que con $m$ par vale
$\frac{m^2-4}{12}+\frac12$ —$12{,}166667$ para $m=12$— y **encoge** los ciclos de
otro periodo por un factor que depende solo de $p$ y $m$. Eso es lo que convierte
la elección del orden en una decisión con consecuencias calculables, en lugar de
en un número redondo.

La **1.5** cobra el precio —$\lfloor m/2\rfloor$ instantes perdidos en cada
extremo— y enseña el arreglo del logaritmo para el caso multiplicativo.

#### Un control roto, cazado por la regla 19b

El primer visual tenía un desplegable para poner o quitar la restricción de suma
cero. Con la constante en su valor por defecto —cero— poner y quitar la
restricción **daba el mismo dibujo**, y `visuales.py --estricto` lo marcó:

```
✗ series/01-descomposicion.qmd [visual 0]   de-r   no cambia nada el dibujo
```

No era un falso positivo: era la regla 19b en su forma más pura. Un control que
en su estado inicial no mueve un pixel es un control que el lector no aprende a
usar. Se arregló por dos lados a la vez: la constante arranca en $2{,}5$, de modo
que el desplegable siempre separa dos dibujos distintos, y con la restricción
puesta aparece además **la línea del cero del perfil estacional**, que es
justamente lo que la restricción fija. Ahora el control enseña lo que hace.

#### El módulo, cableado entero

Arrancar un módulo vacío es más que escribir una página: hubo que crear
`proyectos/notebooks/F3-retos.ipynb`, añadir `"F3-retos"` al bucle de
`proyectos/genera_retos.py` y enseñarle a la expresión de módulos a reconocer
`Series`. Sin eso el reto de la lección no habría llegado a ningún cuaderno.

### 3.28 Series de tiempo 02: las tablas de valores críticos, reconstruidas (19-09-2026)

La lección 2 programa **ADF y KPSS desde cero, sin `statsmodels`**, y en lugar
de copiar sus valores críticos los **vuelve a calcular simulando la hipótesis
nula**. Cincuenta líneas de numpy y veinte mil series de $250$ puntos devuelven
$-3{,}4392$, $-2{,}8596$ y $-2{,}5543$ donde las tablas publicadas traen
$-3{,}43$, $-2{,}86$ y $-2{,}57$.

Eso convierte un número memorizado en algo que el lector puede comprobar, y de
paso deja medir lo que cuesta equivocarse: usar el valor crítico normal
$-1{,}6449$ rechaza la raíz unitaria en el $45{,}27\,\%$ de las series que sí la
tienen. Una prueba anunciada al $5\,\%$ que falla cuarenta y cinco veces de cada
cien.

El KPSS cuadra al $90\,\%$ y al $95\,\%$ y **falla en el $99\,\%$** —$0{,}6949$
contra $0{,}739$—, porque la tabla publicada es asintótica y con $n=250$ la cola
no ha llegado. Se dice en la prosa en lugar de esconderlo.

#### El hallazgo de la lección

La tabla de la sección 5 cruza dos procesos con tres remedios, y la fila que
importa es la última: diferenciar una serie de tendencia determinista deja
$\rho_1=-0{,}4964$ —la firma exacta de la Proposición 2.4— mientras **el ADF
rechaza el $100\,\%$ de las veces y el KPSS no rechaza nunca**. Las dos pruebas
dan el visto bueno a una serie estropeada. El único aviso está en la
autocorrelación de retardo uno, que ninguna de las dos mira.

Al lado, la zona gris medida: con $\varphi=0{,}95$ la serie **es** estacionaria,
el ADF lo detecta el $46{,}60\,\%$ de las veces y el KPSS afirma lo contrario el
$66{,}36\,\%$. De ahí sale la tabla de cuatro filas con la celda «la muestra no
alcanza» dicha con todas las letras.

#### Tres cosas que el procedimiento cazó

**El valor del ejercicio 1 estaba mal.** La primera escritura ponía $591$; la
condición $t/(t+12)>0{,}9801$ se cumple desde $t>591{,}0151$, así que el primer
entero es **592**. Calculado en una orden aparte antes de escribir el bloque
`check`, como manda la costumbre nueva.

**Las celdas no corrían solas.** `salidas.py` ejecuta **cada celda en su propio
proceso**, así que las funciones definidas en una no existen en la siguiente.
Las celdas 4, 5 y 6 heredaban `adf_lote` y compañía de la 3. Se repiten las
definiciones con un comentario que lo dice, que además es la convención del
sitio: cada celda del sitio arranca con su `import numpy as np`.

**Faltaban las dos etiquetas `</script>`.** El fuente salió sin ellas, y pandoc
**reparó el HTML mal formado cerrando secciones**: el `viewBox` bajó a
minúsculas, el `<h2>` perdió su clase de ancla y los dos visuales quedaron
muertos. `visuales.py` marcó solo dos controles del segundo visual; **quien lo
cazó de verdad fue la comprobación en el navegador**, con `Unexpected token
'<'` en la consola. Conviene recordarlo: el gate de visuales monta cada bloque
en un HTML suelto y no ve lo que el render completo hace con un bloque roto.

#### La regla 16, siete veces

`verificar/simbolos.py` encontró $\mu$, $\alpha$, $\gamma$, $\theta$,
$\delta$, $L$ y $z$ usados en fórmula y sin declarar en la tabla de notación.
Ese script no es un gate de CI, y merece correrse a mano en cada lección nueva.

### 3.29 Series de tiempo 03: una identidad que no depende de los datos (19-09-2026)

La lección abre con un resultado que casi nunca se enuncia y que ordena todo lo
demás:

> **3.2**: para **cualquier** serie de $n$ números, $\sum_{h=1}^{n-1}\hat\rho_h
> = -1/2$ exactamente.

Se demuestra en cinco renglones agrupando los pares $(t,s)$ por su diferencia, y
se comprueba sobre cinco series que no se parecen en nada —ruido blanco, un
paseo aleatorio, un seno puro y siete números escritos a mano—: las cinco dan
$-0{,}500000000000$. **Es álgebra, no estadística**, y explica de una vez por
qué la ACF muestral tira hacia abajo: en la misma tabla de la lección, el
$\text{AR}(1)$ medido da $0{,}690121$ donde la teoría dice $0{,}700000$.

El segundo visual la dibuja: la suma acumulada de la ACF, que los dibujos
habituales cortan en el retardo veinte o treinta, llevada hasta $n-1$ para ver
que **siempre aterriza en $-1/2$**.

#### El espejo, medido

La segunda tabla pone las cuatro columnas juntas sobre veinte mil réplicas: la
ACF del $\text{MA}(2)$ se corta a $-0{,}002249$ tras el retardo dos mientras su
PACF arrastra $+0{,}251687$, $-0{,}328103$, $+0{,}193680$; la PACF del
$\text{AR}(1)$ cae a $-0{,}002800$ en el retardo dos mientras su ACF sigue viva
en $0{,}474800$. La recursión de Durbin-Levinson está programada en la página.

#### La banda que mide otra cosa

Todo dibujo de ACF trae $\pm1{,}96/\sqrt{n}$, y esa banda supone **ruido
blanco**. Sobre un $\text{MA}(1)$ con $\theta=0{,}8$, donde los retardos del dos
en adelante son cero de verdad, marca el $9{,}83\,\%$ en lugar del $5\,\%$; la
banda de Bartlett lo devuelve a $4{,}47\,\%$, y el control de ruido blanco sale
en $4{,}56\,\%$. Traducido a la unidad que importa: **dos marcas espurias por
cada veinte retardos dibujados**, cada una invitando a añadir un término al
modelo.

#### Sobre el proceso

Las tres celdas se escribieron ya autocontenidas, con las funciones repetidas
donde hacían falta, después de lo aprendido en la lección 2. Al darle semilla
propia a la tercera celda las tasas cambiaron —$0{,}0972$ pasó a $0{,}0983$—, y
eso arrastraba el valor del ejercicio 2, de $1{,}944$ a $1{,}966$: se corrigió
**antes** de publicar porque los números se leyeron de la corrida, no de la
memoria. Y `simbolos.py`, ya nombrado en `CLAUDE.md`, encontró $\sigma$ sin
declarar.

### 3.30 Series de tiempo 04: un modelo de dos parámetros que es ruido blanco (19-09-2026)

ARIMA suele presentarse como una caja con tres números que hay que acertar. La
lección lo presenta con el resultado que explica por qué acertarlos no siempre
es posible:

> **4.3**: en un $\text{ARMA}(1,1)$ con $\theta=-\varphi$, la serie es
> $y_t=\varepsilon_t$ **exactamente**, para cualquier $\varphi$.

Se demuestra cancelando el factor común en un renglón, y se mide: sobre veinte
mil réplicas, la ACF de ese modelo sale $-0{,}001085$ y la del ruido blanco puro
$-0{,}002722$. **Son la misma serie.** Ningún criterio de información arregla
eso, porque no hay nada que separar; la identificación de la lección 3 supone
que los polinomios no comparten raíces, y ese supuesto es una hipótesis de
trabajo.

#### La tabla que traduce la decisión sobre $d$

La otra pieza central enfrenta las dos fórmulas de la anchura del intervalo:

| $h$ | AR(1), $\varphi=0{,}7$ | paseo aleatorio |
|---|---|---|
| 1 | $3{,}920000$ | $3{,}920000$ |
| 50 | $5{,}489098$ | $27{,}718586$ |

A un paso son idénticas. A cincuenta pasos el modelo estacionario sigue clavado
en su techo $2\cdot1{,}96\,\sigma/\sqrt{1-\varphi^2}$ y el paseo va camino de
infinito. **Esa es toda la diferencia práctica entre $d=0$ y $d=1$**: no cambia
tanto el pronóstico central como lo que el modelo promete sobre él. Las dos
fórmulas se demuestran desde la representación de media móvil y se comprueban
por simulación sobre cuarenta mil series —$1{,}956300$ contra $1{,}960783$ y
$19{,}965410$ contra $20$—.

#### Yule-Walker, con la maquinaria de la lección anterior

El sistema de Yule-Walker es el mismo que la recursión de Durbin-Levinson
resuelve paso a paso, así que estimar un $\text{AR}(p)$ reutiliza lo ya
construido. La tabla enseña la convergencia con todas sus letras: el error
típico cae de $0{,}100122$ a $0{,}011944$, **dividiéndose por dos cada vez que
$n$ se multiplica por cuatro**, que es $1/\sqrt{n}$ y nada más.

Y $1-L^{s}$ recibe el mismo trato que la diferencia ordinaria: aniquila el
periodo $s$ por debajo de $10^{-12}$, deja $bs$ sobre una recta, y sobre ruido
blanco duplica la varianza dejando $-0{,}4780$ en el retardo doce. **La firma
$-1/2$ de la Proposición 2.4, ahora en el retardo estacional.**

#### La regla 19b otra vez, y por qué el arreglo mejoró la lección

El segundo visual tenía un control de semilla, y la serie por defecto
—estacionalidad pura— es determinista: la semilla no movía un píxel.
`visuales.py` lo marcó.

El arreglo no fue cambiar la serie por defecto sino **cambiar el control**: en
su lugar hay un deslizador de *ruido añadido*. Con el ruido en cero la
Proposición 4.7a se ve al pie de la letra —la diferencia estacional deja cero
exacto— y subiéndolo se ve que **la aniquilación es exacta solo mientras el
perfil lo sea**, que es justamente la advertencia que la sección necesitaba.
Un control roto obligó a encontrar el control que faltaba.

### 3.31 Series de tiempo 05: tres descripciones del mismo objeto (19-09-2026)

El suavizado exponencial suele aparecer como una receta simpática, aparte de los
modelos con nombre. La lección demuestra que es **el mismo objeto visto desde
tres sitios**, y lo hace en las dos direcciones en lugar de mencionarlo:

> **5.3**: el pronóstico de un $\text{ARIMA}(0,1,1)$ con $\theta=-(1-\alpha)$
> coincide con el del suavizado exponencial de factor $\alpha$.

Comprobado con diferencia máxima $0{,}000000000000$ sobre dos mil instantes y
tres factores distintos.

> **5.5**: la ganancia del filtro de Kalman del modelo de nivel local, en
> régimen, vale $(-q+\sqrt{q^{2}+4q})/2$, que es ese mismo $\alpha$.

Se demuestra resolviendo la ecuación de Riccati escalar —queda $x^2-qx-q=0$— y
se comprueba iterándola dos mil veces: las dos columnas coinciden a diez
decimales en cinco valores de $q$. Con $q=1$ sale $0{,}6180339887$, la razón
áurea menos uno.

#### La consecuencia que cambia cómo se usa

De ahí sale $q=\alpha^{2}/(1-\alpha)$, y con ella la frase que ordena la
lección: **elegir $\alpha$ no es ajustar un parámetro, es afirmar una razón
señal-ruido**. Poner $\alpha=0{,}3$ por costumbre equivale a declarar que el
nivel se mueve casi ocho veces menos que el ruido de medición, y eso ya es una
afirmación que se puede discutir con datos.

La otra traducción útil es la memoria: retardo medio $(1-\alpha)/\alpha$ y
semivida $\log(1/2)/\log(1-\alpha)$. Con $\alpha=0{,}1$ son $9$ instantes y
$6{,}578813$; con $0{,}8$, $0{,}25$ y $0{,}430677$.

Y la Proposición 5.7 deja una asimetría que conviene ver: la varianza del error
a $h$ pasos vale $\sigma^2(1+(h-1)\alpha^2)$, así que a veinte pasos
$\alpha=0{,}2$ da $1{,}7600$ y $\alpha=0{,}5$ da $5{,}7500$. **Un suavizado más
reactivo pronostica peor a largo plazo**, porque cada sacudida que mete en el
nivel se queda ahí para siempre.

#### Sobre el proceso

Dos cosas se cazaron antes de publicar. El prerrequisito `estadistica/12` estaba
mal —ese número es la normal multivariante, la regresión es la 13—, y la regla
14 marcó un «no son parecidos, son la misma cuenta» en la prosa. Las dos
salieron de correr las compuertas antes del commit, no después.

### 3.32 Series de tiempo 06: el calendario como columnas, con las dos cuentas (20-09-2026)

La elección entre indicadores y armónicos suele contarse como una preferencia de
escuela. La lección la convierte en **un intercambio con dos cantidades
calculables**, y empieza quitando de en medio la falsa alternativa:

> **6.3**: los $s-1$ indicadores y los $s-1$ armónicos completos generan el
> mismo subespacio, así que dan el mismo ajuste.

Comprobado en $s=7$, $12$ y $52$: mismo rango y ajustes iguales por debajo de
$10^{-10}$. **Mientras no se trunquen, los armónicos son un cambio de base.**

#### Las dos cantidades

> **6.4**: la desviación de un coeficiente indicador vale $\sigma\sqrt{2/a}$ y
> la de uno de armónico $\sigma\sqrt{2/n}$, con cociente **exactamente
> $\sqrt{s}$**.

La columna del cociente sale $7{,}2111$ en las cuatro filas de la tabla, que es
$\sqrt{52}$ y no depende de cuántos años haya. De ahí la frase que decide el
diseño antes de mirar los datos: **un indicador semanal se estima con tantas
observaciones como años haya**. Con tres años su desviación es $0{,}816497$
veces la del ruido; el mismo perfil en tres armónicos se estima con
$0{,}113228$. Para una precisión de $0{,}1\sigma$ con indicadores harían falta
doscientos años.

> **6.5**: truncar es proyectar, y Parseval dice cuánto queda fuera.

Sobre un perfil anual con una punta de dos semanas: $K=26$ explica el
$100{,}0000\,\%$ —la 6.3 otra vez— y $K=3$ solo el $46{,}2060\,\%$, con error
máximo $4{,}669436$ en la semana $51$. **Los armónicos bajos no saben dibujar
una punta**, y eso es lo que se paga por la banda estrecha.

#### El feriado móvil tiene fórmula

> **6.6**: un evento de efecto $\delta$ que visita $m$ posiciones aparece en el
> perfil estacional como $\delta/m$ en cada una.

Medido sobre doscientas réplicas de cuarenta ciclos: $0{,}830802$ contra los
$0{,}833333$ predichos, y $5{,}002083$ cuando se le da su propia columna. El
perfil no ignora el evento móvil, **lo reparte**, que es la peor manera de
verlo. De ahí la regla que la lección justifica: todo lo que se mueve respecto
al ciclo necesita su propia columna.

Y la 6.7 cierra con la trampa inversa: un evento anclado a una posición del
ciclo es colineal con su indicador —deficiencia uno de ocho columnas—, y basta
**una excepción en $364$ observaciones** para que el rango vuelva a ser completo
y ninguna biblioteca se queje: el número de condición pasa de $7{,}8730$ a
$29{,}0505$, y el coeficiente pasa a depender de esa única observación.

#### Dos cosas del procedimiento

El valor del ejercicio 2 estaba escrito a mano en $15$ y la corrida dio **$4$**.
Van tres lecciones en las que el orden «calcular aparte, leer, después escribir
el bloque `check`» caza un número inventado.

Y la primera versión de la celda 0 imprimía la diferencia entre los dos ajustes,
$0{,}00000000000001$ en una versión y $0{,}00000000000002$ en la otra: **regla 7
en estado puro**. Se cambió por una afirmación de propiedad —¿por debajo de
$10^{-10}$?— y las dos versiones volvieron a coincidir.

El gate de visuales avisó de que el control de años no movía ningún trazo,
porque las bandas de incertidumbre estaban dibujadas como `rect`. Se pasaron a
trazo, que además se ve mejor.

### 3.33 Series de tiempo 07: la validación cruzada no está rota, contesta otra pregunta (20-09-2026)

La lección podía haberse escrito como una advertencia —«no uses k-fold en
series»— y en su lugar mide el fenómeno y nombra su mecanismo.

> **7.2**: repartiendo los índices al azar en $k$ partes, el vecino de
> entrenamiento queda a distancia media $\approx1{,}04$, así que el informe
> contesta una pregunta **a un paso** mientras dice $h$.

La tabla tiene tres filas y la tercera es la que sostiene el argumento:

| serie | RMSE k-fold | RMSE a 12 pasos | cociente |
|---|---|---|---|
| paseo aleatorio | $1{,}016005$ | $3{,}402812$ | $3{,}3492$ |
| AR(1) $\varphi=0{,}95$ | $1{,}030932$ | $3{,}025224$ | $2{,}9345$ |
| **ruido blanco** | $1{,}413577$ | $1{,}430459$ | $\mathbf{1{,}0119}$ |

**Sobre ruido blanco no hay optimismo ninguno.** Sin esa fila la conclusión
sería que la validación cruzada aleatoria está rota; con ella queda claro que
falla exactamente en la medida en que haya memoria que filtrar. El control que
prueba el mecanismo vale más que el efecto.

#### La fuga, convertida en fórmula

> **7.4**: una ventana **centrada** de anchura $w$ explica exactamente $1/w$ de
> la varianza de una serie impredecible.

Medido: $0{,}334614$, $0{,}141940$ y $0{,}066782$ contra $1/3$, $1/7$ y $1/15$,
con la ventana retrasada en $0{,}000421$. La serie es ruido blanco, así que
**nadie puede predecirla**, y aun así la columna centrada regala un tercio de
$R^2$. Eso permite reconocer una fuga sin razonar sobre el flujo de datos: si
una columna se contiene a sí misma con peso $1/w$, ahí está el $R^2$.

#### Cuántos pronósticos valen de verdad

> **7.5**: los errores de pronósticos solapados repiten información.

Con orígenes separados por el horizonte salen $16$ pronósticos; acercándolos al
paso uno salen $188$ —doce veces más trabajo— y **equivalen a unos $25$
independientes**. La consecuencia es que un backtesting con cien pronósticos
solapados puede no tener potencia para separar dos modelos que difieren en un
cinco por ciento.

#### El control muerto, otra vez, y otra vez mejoró el visual

`visuales.py` marcó el deslizador de horizonte: en el esquema por defecto
—k-fold— el horizonte no significa nada, así que no movía un píxel. Cierto y
además **es el punto de la lección**.

El arreglo fue dibujar, debajo de los cortes y en todos los esquemas, **dos
barras**: la del horizonte que el informe promete y la de la pregunta que el
esquema contesta de verdad. Con origen móvil coinciden; con k-fold la primera
mide $h$ y la segunda $1{,}04$, y la distancia entre las dos barras **es** la
Proposición 7.2 dibujada. Van dos lecciones seguidas en que un control roto
obligó a encontrar el control que faltaba.

Y el valor del ejercicio 1 estaba escrito a mano en $2{,}033888$; la corrida dio
$1{,}897905$.

### 3.34 Series de tiempo 08: boosting, y la lección de cuándo NO usarlo (20-09-2026)

La lección aplica a series lo que Machine Learning 13 dejó dicho, y el resultado
es que **la limitación conocida de los árboles se vuelve decisiva**:

> **8.2**: un conjunto de árboles es constante fuera del rango que vio. Para
> todo $x$ mayor que todos los cortes, $f(x)$ no depende de $x$.

Medido: el objetivo más alto en entrenamiento vale $16{,}150797$, el pronóstico
a sesenta pasos llega como máximo a $15{,}792824$ y la serie llega a
$19{,}023694$. **El pronóstico no se equivoca por ruido sino por construcción.**
Con el objetivo diferenciado el mismo modelo alcanza $18{,}650203$ y el RMSE
baja de $1{,}929395$ a $0{,}422776$: la tendencia no se aprende, se quita.

#### El experimento se diseñó para que el boosting perdiera

El proceso de la segunda sección es un $\text{AR}(2)$, o sea **lineal**, y esa
elección es deliberada: es la única manera de que el lector aprenda cuándo *no*
usar boosting. El resultado honesto es que pierde a un paso y empata a
horizontes largos, porque por la Proposición 4.4 todo converge a la media.

#### El absurdo que introdujo las barras de error

Varios RMSE del backtesting caen **por debajo del óptimo teórico**: $1{,}2493$
contra $1{,}2832$ en el horizonte seis, cosa imposible para un pronóstico. En
lugar de esconderlo, la lección lo señala y añade la fila del error típico,
$0{,}0396$: la diferencia es de menos de una desviación. **Esa tabla no se puede
leer sin sus barras**, que es la Proposición 7.5 de la lección anterior en
acción.

> **8.5**: la diferencia de dos RMSE no lleva incertidumbre; la media de las
> diferencias pareadas sí, y además cancela la variación común.

Con el pareado, lo que la tabla no resolvía se decide: contra el modelo lineal
el boosting pierde a un paso con cociente $2{,}99$, y a horizontes largos los
cocientes bajan a $0{,}29$, $0{,}47$ y $0{,}85$. Entre recursivo y directo salen
$-2{,}16$, $-2{,}09$ y $-1{,}67$: **gana el recursivo**, en contra de la
costumbre, con margen modesto.

#### Sobre el proceso

Primero se montó el experimento con treinta réplicas y el error a doce pasos
salió **menor** que a seis, cosa imposible: eran treinta muestras por celda. Se
rehízo como backtesting de $476$ orígenes sobre una sola serie larga, que es
más barato y mucho más preciso —y además es lo que la lección 7 enseña—.

Y el valor del ejercicio 2 estaba escrito a mano en $137$; la corrida dio
$138$. Van cuatro lecciones seguidas en que ese paso caza un entero inventado.

### 3.35 Series de tiempo 09: Prophet reconstruido desde sus piezas (20-09-2026)

La lección no describe la biblioteca: **reconstruye el modelo** y demuestra las
dos cosas que su documentación presenta como convenciones.

> **9.3**: la tendencia por tramos es continua **si y solo si**
> $\gamma_j=-s_j\delta_j$.

Medido con $\varepsilon=10^{-9}$: con la corrección el salto vale
$0{,}000000003$, y sin ella $4{,}000000003$ y $17{,}999999998$, o sea
exactamente $\lvert s_j\delta_j\rvert$. Es un teorema de una línea.

> **9.4**: la prior de Laplace sobre los cambios de pendiente es una
> penalización $L_1$ con $\lambda=2\sigma^2/\tau$.

De veinticinco candidatos sobreviven $25$, $10$, $7$, $4$ y $0$ según sube
$\lambda$. **El parámetro que Prophet llama flexibilidad de la tendencia es un
lasso con otro nombre**, y hereda todo lo que ML 9 dice sobre él.

#### La comparación directa con la lección anterior

> **9.5**: pasado el último corte la tendencia es **afín**, así que no está
> acotada.

Sobre **la misma serie** de la lección 8 —misma semilla, misma pendiente, mismo
ruido— esta tendencia pronostica $18{,}985036$ contra un verdadero
$19{,}023694$, con RMSE $0{,}307414$. Allí el boosting daba $1{,}929395$ sobre
el nivel y $0{,}422776$ sobre la diferencia. La ventaja no está en el ajuste
sino en **la forma de la función**, y poder enfrentar las dos cifras en la misma
serie es lo que convierte el contraste en un dato.

#### La banda que no sale de los datos

> **9.6**: la parte de tendencia del intervalo se obtiene simulando cortes
> futuros.

Con frecuencia supuesta cero mide **exactamente $0{,}000000$**; duplicando la
observada llega a $0{,}520906$. Ese parámetro no se estima: es una declaración
sobre cuántas veces cambiará la pendiente en el futuro, y la banda contesta a
esa declaración.

#### Tres cosas del procedimiento

La primera comprobación de la continuidad estaba **mal escrita**: medía
`searchsorted`, que devuelve el índice donde $t$ vale exactamente $s$, mientras
la condición del código era `t > s`. Los dos casos daban $0{,}018$ —el
incremento normal de la rejilla— y parecía que la corrección no hacía nada. Se
rehizo midiendo el límite por los dos lados con $\varepsilon$ explícito.

La penalización tampoco hacía nada al principio: las columnas $(t-s_j)_+$ iban
de norma $49{,}7$ a $4268{,}3$, así que un solo $\lambda$ no podía umbralarlas.
Escalar el tiempo a $[0,1]$ —que es lo que hace Prophet— lo arregló.

Y el gate de visuales avisó de que el deslizador de evento movía tres vértices
perdidos en un trazo de ciento cuarenta puntos. Ahora los eventos tienen tallo
propio, con su altura escrita al lado.

### 3.36 Series de tiempo 10: reconciliar es proyectar, con su teorema (20-09-2026)

La reconciliación jerárquica suele contarse como un arreglo para que los
números cuadren en un informe. La lección la presenta como lo que es: **una
proyección ortogonal, con la garantía que eso trae**.

> **10.5**: si $y$ es la verdad, que es coherente, y $P$ la proyección
> ortogonal sobre el subespacio coherente, entonces
> $\lVert P\hat y-y\rVert\le\lVert\hat y-y\rVert$, **siempre**.

La demostración cabe en dos renglones —$Py=y$, y proyectar no aleja— y la
comprobación sale sin excepciones: de veinte mil casos, el error total mejora
en **los veinte mil**, con reducción media $4{,}335308$.

#### La cifra que explica la desconfianza

En el **$99{,}86\,\%$ de los casos alguna serie individual queda peor**. Quien
mira una sola serie ve empeoramientos reales y tiene razón; quien mira el
conjunto ve una mejora garantizada y también la tiene. Poner las dos cifras
juntas es lo que convierte una discusión de pasillo en un hecho.

#### Y el régimen donde abajo-arriba gana

| régimen | base | ols | ponderada | abajo-arriba |
|---|---|---|---|---|
| ruido igual | $12{,}9689$ | $8{,}6041$ | $8{,}6041$ | $26{,}0637$ |
| ruido ~ √nivel | $25{,}9346$ | $15{,}8869$ | $13{,}4198$ | $26{,}0637$ |
| ruido ~ nivel | $86{,}3830$ | $50{,}5957$ | $19{,}7488$ | $\mathbf{26{,}0637}$ |

La proyección ortogonal **siempre** bate al pronóstico base, que es el teorema;
pero en la última fila **abajo-arriba la bate a ella**, porque con agregados muy
ruidosos lo razonable es descartarlos. Enseñar ese régimen evita confundir «no
puede empeorar» con «es lo mejor».

#### Dos controles muertos, y la misma causa

`visuales.py` marcó los deslizadores de ruido de **los dos** visuales. La causa
era la misma y es exactamente la que la regla 19b nombra: **el marco seguía a
los datos**. Los errores escalan con $\sigma^2$ y el marco también, así que
mover el ruido dejaba el dibujo idéntico.

En el primero el control pasó a ser **dónde está el ruido** —cuánto más ruidoso
es el total que las hojas—, con el marco anclado a una constante; en el segundo,
la escala se sustituyó por el **número de grupos**, y las barras se miden contra
el error del pronóstico base, que es una cantidad determinada por los parámetros
y no por los datos dibujados. Los dos cambios mejoraron lo que el visual enseña.

### 3.37 Series de tiempo 11: el módulo cerrado, y la métrica como decisión (20-09-2026)

La última lección del módulo trata las métricas como lo que son: **la
definición de qué pronóstico se considera bueno**. La forma precisa de decirlo
es preguntar qué constante minimiza cada una.

> **11.2**: el error cuadrático se minimiza en la media, el absoluto en la
> mediana, y el porcentual en la mediana ponderada por $1/y$, que en una
> distribución asimétrica cae **por debajo**.

Sobre una lognormal los tres mínimos salen $1{,}3710$, $0{,}9980$ y $0{,}5260$
contra una media de $1{,}370637$: **optimizar MAPE pide un pronóstico un
$61{,}6\,\%$ por debajo de la media**. No es un sesgo corregible después; es lo
que la métrica premia.

> **11.3**: el sMAPE no es simétrico. Quedarse corto puntúa peor que pasarse en
> la misma cantidad, con cociente $(2a+d)/(2a-d)$.

Con desvío $90$ sobre verdad $100$ el cociente llega a $2{,}636364$. Y el sesgo
va al revés que el del MAPE, de modo que las dos métricas tiran en direcciones
opuestas.

> **11.4**: para una serie de conteo con media por debajo de $\log 2 =
> 0{,}693147$, el pronóstico óptimo en error absoluto es **cero**.

Medido: con $\lambda=0{,}4$ el óptimo es cero con error $0{,}3969$, mejor que el
$0{,}5339$ del pronóstico que acierta la media. **Una métrica puede premiar no
pronosticar nada**, y en demanda intermitente eso no es una anécdota.

#### La cifra del título

Cinco series de **la misma calidad** y distinta escala dan MAPE de $0{,}025380$
a $0{,}871477$. El promedio de los cinco vale $0{,}269435$ y el MAPE del total
agregado $0{,}035924$: **un factor de $7{,}50$**, y las dos cifras se presentan
como «el error del pronóstico». La serie más pequeña aporta el
$\mathbf{64{,}69\,\%}$ del promedio y el $\mathbf{2{,}66\,\%}$ del error real.
Los MASE, en cambio, salen entre $0{,}706690$ y $0{,}717086$: casi idénticos,
porque miden calidad y no escala.

#### El módulo, cerrado

**Once lecciones en dos días, ninguna citando un libro**, porque ninguno de los
índices verificados cubre series de tiempo. Todo lo que afirman está demostrado
o medido en la propia página, y el verificador reejecuta cada número en cada
publicación.

Las once se sostienen sobre la misma idea: cada elección técnica —el orden de
una media móvil, el número de diferencias, los armónicos, el esquema de
validación, la métrica— **es una afirmación sobre los datos que se puede
escribir, demostrar o medir**.

El procedimiento cazó un valor escrito a mano en **siete** de las once
lecciones, y la regla 19b marcó controles muertos en **cinco**; en todos los
casos el arreglo mejoró lo que el visual enseñaba, en lugar de limitarse a
silenciar el aviso.

### 3.38 El índice de ESL, con dos fuentes porque una no bastaba (20-09-2026)

ML 23 a 35 llevaban bloqueadas desde el principio por la regla 3: sin índice
verificado no se cita. Traerlo costó más de lo previsto y por una razón que
merece quedar escrita.

El PDF oficial —enlazado desde `hastie.su.domains/ElemStatLearn/download.html`,
que redirige a Google Drive, 764 páginas— **tiene los marcadores corrompidos**:

- meten tabuladores dentro de los números, de modo que `7.1\t0.1` es en realidad
  la sección **7.10.1**;
- anidan ramas enteras donde no van, hasta siete niveles de profundidad bajo una
  sección que no es su padre;
- y por esa vía **pierden la sección 18.8**, que queda colgada bajo el capítulo 7.

Una extracción ingenua de los marcadores daba un índice con secciones
inventadas: la 7.1 salía titulada «1.1 Example (Continued)», que es un trozo de
la 7.11.1.

#### La regla que sale de aquí

**Cuando una fuente sola es dudosa, la respuesta es traer la segunda, no elegir
entre las dos.** Se extrajo aparte el **índice impreso** de las páginas 9 a 18
del mismo PDF, uniendo las líneas partidas, y se contrastaron:

- 126 de 133 secciones coinciden **literalmente**;
- las 7 restantes difieren solo en los puntos suspensivos del índice impreso,
  que el lector de líneas no recortó;
- 8 secciones faltaban en el impreso por líneas partidas, y 1 —la 18.8— faltaba
  en los marcadores.

Además, cada capítulo da una secuencia de secciones **sin huecos**, de 1 a N, lo
que es una comprobación de consistencia interna que una extracción rota no
pasaría.

El resultado: **18 capítulos y 134 secciones**, en `indices.json` con las dos
fuentes y la fecha. ESL queda citable a nivel de sección, como ISLP.

### 3.39 ML 23: la maldición de la dimensión con presupuesto (20-09-2026)

Primera lección sobre ESL. Reúne en **una sola proposición con demostración** las
tres cuentas que §2.5 presenta como ejemplos numéricos sueltos:

> **23.3**: el lado del vecindario es $r^{1/p}$; la distancia mediana al vecino
> más cercano es $(1-2^{-1/N})^{1/p}$; la densidad va como $N^{1/p}$.

La segunda se **comprueba por simulación**, cosa que el libro no hace: $0{,}517822$
medido contra $0{,}517792$ calculado con $p=10$ y $N=500$.

Y el cruce de la Proposición 23.5 se **tabula** en lugar de dibujarse: sobre una
verdad que depende de una sola coordenada, el vecino más cercano gana con
cociente $0{,}2140$ en $p=5$, empata en $p=10$ y pierde $2{,}0382$ a uno en
$p=20$, mientras el modelo lineal mal especificado se queda clavado en
$0{,}25$ para toda $p$. **En dimensión alta hay que suponer algo**; la elección
es qué.

#### Un fallo mío que llevaba dos días publicado

`genera_retos.py` necesita `--escribe` para escribir: sin esa bandera imprime lo
que **falta**, no lo que hizo. Lo leí al revés once veces seguidas, así que las
once lecciones de Series de tiempo remiten a secciones de `F3-retos.ipynb` que
**no existían**; el cuaderno solo tenía la de Series 1.

Al escribirlas apareció un segundo fallo, este en el propio guion: su detector de
secciones ya existentes conocía `Matemática|Estadística|Python|ML` y **no
`Series`**, de modo que duplicó la única que sí estaba. Las dos cosas quedan
arregladas y el cuaderno tiene ahora sus once secciones sin repetidos.

La lección práctica: **un guion que informa de lo pendiente y otro que informa
de lo hecho no deben parecerse tanto**. Conviene mirar el archivo, no la salida.

### 3.40 La séptima compuerta: que el reto prometido exista (20-09-2026)

El fallo de `genera_retos.py` dejó una pregunta más útil que el propio fallo:
**¿por qué once builds en verde no lo vieron?** Porque ninguna compuerta abría
el cuaderno. Cada lección promete «En `proyectos/notebooks/F3-retos.ipynb`,
sección **Series 4**» y eso era una promesa que nadie cobraba.

`verificar/retos.py` la cobra. Por cada lección con bloque `## Reto`:

- lee el cuaderno y la sección que nombra;
- comprueba que el cuaderno existe y tiene un encabezado para esa sección,
  con el alias correcto —la prosa dice «Mat 5» y el cuaderno «Matemática 5»—;
- comprueba que el bloque tiene exactamente tres puntos numerados.

**Al estrenarla encontró dos huecos más**, y de otra clase: `estadistica/01` y
`estadistica/02` nombran `F0-retos.ipynb` y sus secciones están en
`F1-retos.ipynb`. Llevaban así desde que se escribieron. Un lector que siguiera
la instrucción habría abierto el cuaderno equivocado.

Se comprobó **en negativo**: quitando a propósito la sección de Series 4 del
cuaderno, la compuerta falla nombrando `series/04-arima.qmd`. Sin esa prueba no
se sabe si una compuerta comprueba algo o solo dice que sí.

#### Y el guion que engañaba

`genera_retos.py` imprimía «total a generar: 11», que suena a informe de lo
hecho y era la lista de lo que faltaba. Ahora dice **«FALTAN 11 SECCIONES POR
ESCRIBIR. Esto es un simulacro»**, o «no falta ninguna sección: los cuadernos
están al día». La regla general: **un mensaje sobre lo pendiente y otro sobre lo
hecho no deben poder confundirse leyendo por encima**.

### 3.41 ML 24: qué es de verdad un coeficiente (20-09-2026)

La lección se apoya en un resultado de ESL §3.2.3 que casi nunca se enseña como
lo que es:

> **24.2**: el coeficiente de mínimos cuadrados de la columna $j$ es la
> regresión **simple** de $y$ sobre $z_j$, lo que esa columna tiene y las demás
> no.

Eso convierte «controlar por las demás variables» de fórmula hecha en
definición exacta, y repetido columna a columna **es** Gram-Schmidt. Comprobado
sobre cinco columnas: los coeficientes coinciden por los dos caminos por debajo
de $10^{-10}$.

De ahí sale la segunda, que es la que da el diagnóstico:

> **24.3**: $\operatorname{Var}(\hat\beta_j)=\sigma^2/\lVert z_j\rVert^2$.

Comprobada contra la diagonal de $(X^{\top}X)^{-1}$, que coincide a ocho
decimales. Con una columna que es casi copia de otra, $\lVert z_j\rVert^2$ cae
de $227{,}1063$ a $1{,}5533$ y la varianza sube de $0{,}00440322$ a
$0{,}64379892$: **un factor de ciento cuarenta y seis**. El VIF lo resume en
$137{,}3682$, y esa cifra tiene traducción a presupuesto: harían falta $137$
veces más datos.

#### La letra pequeña de Gauss-Markov

El teorema se demuestra por Pitágoras en tres renglones, y la lección se detiene
en sus dos palabras: **lineales** e **insesgados**. Quitando la segunda, la
Proposición 24.5 exhibe un estimador mejor: con $\lambda=0{,}2$ el error baja de
$1{,}310782$ a $0{,}967835$, y con $0{,}5$ a $0{,}985342$, **un $24{,}8\,\%$
menos**. No hay contradicción —ridge es sesgado y no compite en esa categoría—,
y lo que el resultado dice es que la categoría estaba mal elegida.

Donde más gana es **precisamente donde la Proposición 24.3 hacía explotar la
varianza**, de modo que las dos primeras secciones explican por qué existe el
capítulo siguiente del libro.

#### La regla 21b, otra vez con un término

La entrada «colinealidad» del glosario decía solo el caso exacto —una columna es
combinación lineal de otras, baja el rango—, y esta lección la usa en el caso
aproximado. Como el enganche del glosario es global, la entrada habría mentido
en esta página. Ahora cubre los dos casos y nombra la fórmula del segundo.

### 3.42 ML 25: LAR, y dos fallos que encontraron los verificadores (20-09-2026)

La lección programa Least Angle Regression desde cero, demuestra su invariante y
comprueba la equivalencia con el lasso **contra un solucionador que no comparte
nada con LAR**.

> **25.2**: la dirección equiangular cumple $X_{\mathcal{A}}^{\top}u=Gw=
> A_{\mathcal{A}}\mathbf{1}$, así que todas las correlaciones activas bajan la
> misma cantidad y el empate se mantiene durante el paso.

Comprobado en los ocho pasos del ejemplo, con las activas empatadas por debajo
de $10^{-9}$ mientras la correlación común baja de $23{,}029164$ a cero, y con
el último punto coincidiendo con `lstsq` por debajo de $10^{-10}$.

> **25.4**: con una comprobación de más —sacar del conjunto activo el
> coeficiente que cruce el cero— el camino es el del lasso.

Los once puntos de quiebre coinciden con un **descenso por coordenadas**, todos
por debajo de $10^{-9}$, incluido el paso 10, donde el conjunto activo pierde
una variable y en el 11 entra otra.

#### El primer fallo: mi LAR-lasso estaba mal

La primera implementación rederivaba el conjunto activo de las correlaciones en
cada iteración. Como la variable que acaba de salir **sigue empatada en
correlación**, volvía a entrar en el paso siguiente y el borrado no servía de
nada. El descenso por coordenadas lo delató: en el último punto encontraba un
objetivo menor —$35{,}4460$ contra $35{,}4470$— con otro conjunto activo.

Se rehízo llevando el conjunto activo de forma explícita, con una variable
prohibida durante un paso. La lección de esto: **tener un oráculo independiente
convierte un error silencioso en un error visible**. Sin el descenso por
coordenadas, la tabla de la lección habría salido publicada con números
plausibles y equivocados.

#### El segundo: un bucle infinito en el visual

El gate de visuales se colgó al cargar. La causa era de libro: en el segundo
visual, el bucle interno de la función que resuelve el lasso usaba `k`, **la
misma variable del bucle exterior** que recorría la rejilla de $\lambda$. Cada
llamada devolvía `k` a 5 y el bucle de fuera no llegaba nunca a 40.

Merece registrarse porque el gate **no lo detectó fallando sino colgándose**, y
un tiempo de espera agotado es fácil de leer como un problema del entorno. El
arreglo fue declarar locales todas las variables de bucle, y de paso salieron
otros dos descuidos del mismo tipo en la misma página.

### 3.43 ML 26: el enmascaramiento, demostrado en vez de ilustrado (21-09-2026)

ESL abre su capítulo 4 con una figura: tres clases alineadas y la del medio que
nunca gana. La lección lo **demuestra** en el caso simétrico, que es lo que
permite decir por qué no se arregla con más datos.

> **26.2**: con tres clases igualmente espaciadas y del mismo tamaño, la
> covarianza entre la indicadora de la clase del medio y $x$ vale **cero**, así
> que su recta ajustada es la constante $1/3$.

Medido: la clase del medio se predice **cero veces de novecientas**, los
aciertos se quedan en $0{,}6667$ —la fracción exacta de las otras dos— y en su
propio centro los tres valores son $0{,}3286$, $0{,}3332$ y $0{,}3382$: pierde
por tres milésimas. **No hay ruido ni escasez de datos**; con mil veces más
observaciones pasaría lo mismo.

#### Dos métodos que son el mismo

> **26.3**: con dos clases, la dirección de la regresión de la indicadora es
> proporcional a la de LDA.

Comprobado: el cociente vale $0{,}156211$ **idéntico en las cuatro
componentes**, por debajo de $10^{-10}$. Dos métodos presentados en capítulos
distintos —uno por mínimos cuadrados, otro por un modelo de probabilidad— dan
el mismo vector. Y eso explica de paso por qué el enmascaramiento aparece con
tres clases y no con dos: con $K=2$ hay una sola dirección que decidir.

#### La cota de Novikoff, con su hipótesis al lado

> **26.5**: el perceptrón hace como mucho $(R/\gamma)^2$ correcciones, sea cual
> sea el orden de recorrido.

Se cumple en los cuatro márgenes probados y con holgura: con $\gamma=0{,}1$ la
cota permite $1340{,}9$ y bastan $22$. Pero la lección pone al lado el caso **no
separable**, donde el algoritmo no termina en dos mil pasadas y nada dentro de
él lo detecta. Sin ese contraste la cota parece una garantía general y es
**condicional**.

#### El control muerto, y lo que enseñó al arreglarlo

`visuales.py` marcó el deslizador de orden de recorrido: cambiaba el número de
correcciones pero la recta apenas se movía, porque el separador verdadero es
vertical y el ruido es simétrico.

El arreglo fue marcar con un anillo **los puntos sobre los que el algoritmo
corrigió**. Esos sí cambian por completo con el orden, y enseñan algo que la
prosa solo afirmaba: la respuesta del perceptrón la deciden un puñado de puntos
que resultó encontrar primero. Van seis lecciones en que un control roto obligó
a encontrar el control que faltaba.

### 3.44 ML 27: splines, y una lección sobre cómo se cita un número (21-09-2026)

ML 11 usaba el spline de suavizado como suavizador lineal. Esta lección lo
**construye**: la base natural, la matriz de penalización y el suavizador, pieza
a pieza.

> **27.2**: la penalización $\Omega$ anula **exactamente** las funciones
> lineales.

Comprobado con norma $0{,}000\cdot10^{0}$ para la constante y la identidad, y
dos autovalores nulos exactos. Esa propiedad decide el límite: **por mucho que
se penalice, una recta sale gratis**, así que el ajuste más rígido posible es
una recta y no una constante.

> **27.4**: el suavizador tiene **exactamente dos** autovalores iguales a uno,
> y su traza son los grados de libertad efectivos.

Medido: dos, siempre, con la traza cayendo de $10{,}2116$ a $2{,}0000$.

> **27.5**: al crecer $\lambda$ el ajuste tiende a la recta a velocidad
> $O(1/\lambda)$.

La distancia sale $6{,}540\cdot10^{-4}$, $6{,}547\cdot10^{-6}$,
$6{,}547\cdot10^{-8}$: **la misma mantisa tres veces**, que es la firma exacta
de ese orden.

#### Lo que el verificador de dos versiones enseñó

La primera versión calculaba la segunda derivada por **diferencias finitas**, y
el núcleo de $\Omega$ salía de dimensión doce cuando debe ser dos: cancelación
catastrófica al restar cubos. Se rehízo en forma cerrada —la segunda derivada de
esta base es lineal a trozos— y de paso quedó claro que la regla de Simpson en
cada tramo es **exacta**, porque el integrando es cuadrático a trozos.

Aun así, el contraste entre las dos versiones de Python **falló en dos filas**:
con $\lambda$ pequeño el mayor autovalor salía $1{,}73624572$ en una versión y
$1{,}00060368$ en la otra. Un autovalor mayor que uno es imposible para este
suavizador, y el culpable es la base de potencias truncadas, con
$\operatorname{cond}(N^{\top}N)$ por encima de $10^{18}$.

La solución no fue esconder las filas sino **dejar de imprimir sus dígitos**: la
celda calcula el número de condición, decide si el resultado es de fiar y
escribe `---` donde no lo es. Así el lector ve el fallo, ve por qué, y no ve
ningún número que cambie con la versión de la biblioteca.

Eso convierte una nota al pie del libro —que las implementaciones usan
B-splines— en **una lección sobre cómo se cita un número**.

### 3.45 ML 28: de dónde sale el 2 de AIC (22-09-2026)

Los criterios de información se suelen presentar como recetas con una constante
puesta a mano. Esta lección los **deriva**, y el camino pasa por una identidad
que casi nunca se comprueba.

> **28.2**: el optimismo del error de entrenamiento vale
> $\frac{2}{N}\sum_i\operatorname{Cov}(\hat y_i,y_i)$, **sin suponer nada
> sobre el modelo**.

> **28.3**: para un ajuste lineal $\hat y=Hy$ esa suma vale
> $\sigma^2\operatorname{tr}(H)$, y para una proyección sobre $d$ columnas,
> $d\sigma^2$.

Medido sobre veinte mil repeticiones: la suma de covarianzas contra
$d\sigma^2$ da cociente entre $0{,}995123$ y $1{,}008548$ en cuatro tamaños de
modelo, y el optimismo sigue a $2d\sigma^2/N$. Con $d/N=1/4$ la fórmula da
medio $\sigma^2$, y lo medido es $1{,}11933$ frente a $1{,}12500$.

De ahí sale $C_p$ despejando, y AIC con él. **El $2$ es el $2$ de la
Proposición 28.2**, no una constante de ajuste.

#### El círculo que cierra con ML 27

> **28.4**: para un suavizador $\hat y=Sy$, la misma cuenta da
> $\sigma^2\operatorname{tr}(S)$.

Cocientes entre $0{,}994545$ y $1{,}008602$, con trazas de $19{,}383$ a
$1{,}491$. En ML 27 la traza apareció como la suma de los autovalores y se
anunció como grados de libertad efectivos; aquí queda demostrado **por qué**
merece ese nombre: es la cantidad exacta que el optimismo pide cuando no hay
columnas que contar.

#### «Consistente», convertido en tabla

> **28.6**: BIC elige el modelo verdadero con probabilidad que tiende a uno;
> AIC no.

Mil repeticiones en cinco tamaños de muestra, con la verdad en tres columnas de
diez candidatas:

| $N$ | AIC acierta | BIC acierta |
|---|---|---|
| 50 | $0{,}6640$ | $0{,}9200$ |
| 1600 | $0{,}7010$ | $0{,}9940$ |
| 3200 | $0{,}6900$ | $0{,}9950$ |

**AIC no mejora.** Se queda entre $0{,}6640$ y $0{,}7010$ por grande que sea la
muestra, porque una columna inútil mejora el ajuste en algo del orden de una
unidad y el $2$ de AIC tampoco crece. El $\log N$ de BIC sí.

La lección dice en seguida lo que eso **no** significa: AIC estima error de
predicción, no identifica el modelo verdadero. Cada criterio es óptimo para su
pregunta.

#### El tercer criterio del título

La primera versión se llamaba «AIC, BIC y MDL derivados» y **no derivaba MDL**:
lo nombraba en la lista de lo que la lección no resuelve. Un título que promete
algo que la página no entrega es una cita inventada en pequeño, así que se
escribió la sección.

> **28.8**: con los parámetros transmitidos a precisión $1/\sqrt N$, la longitud
> de descripción vale $\text{BIC}/2$.

El $\tfrac12$ no se elige: sale de que el error de un estimador va como
$1/\sqrt N$, y transmitir más decimales es pagar por dígitos que los datos no
respaldan. Eso ordena los tres criterios en **dos familias** —bayesiana y de
compresión dan la misma fórmula; predicción da otra— y explica por qué la tabla
separa a AIC de BIC y no a BIC de MDL. La lección declara en Fuentes los dos
ingredientes que da por buenos: el teorema de codificación de Shannon y la
convención de la precisión.

#### Lo que costó que la tabla existiera

La primera versión ajustaba los diez modelos anidados uno a uno con `lstsq`:
**8 m 41 s**. Con la descomposición QR el residuo de los diez modelos sale de
una sola factorización —$\lVert y\rVert^2$ menos la suma acumulada de los
coeficientes al cuadrado—, y baja a **11 s**. La celda comprueba antes que el
atajo da lo mismo que ajustar cada modelo, porque un atajo sin oráculo es una
suposición.

El visual del optimismo empezó con un control de $\sigma$ y se quitó: como las
dos curvas y el marco escalan todos con $\sigma^2$, mover ese control no movía
nada. Es la regla 19b vista desde el otro lado —el marco no seguía a los datos,
pero la cantidad dibujada era invariante—, y la respuesta fue quitar el control,
no anclarlo.

`verificar/formato.py` encontró además un retroceso en `series/03`: la frase
«la estacionariedad, sin la cual $\rho_h$ no es una sola función, es de Series
de tiempo 2» disparaba el detector de la regla 14. Falso positivo del detector
—el «es» era de otra oración—, pero la frase quedó mejor reescrita.

---

### 3.46 ML 29: lo que la lección 1 dejaba a medias (22-09-2026)

Machine Learning 1 descompone el error en **un** punto y con polinomios. Esta
lección promedia sobre el diseño, parte el sesgo en dos y enseña dónde la
descomposición deja de servir.

> **29.1**: la varianza del $k$-NN vale $\sigma^2/k$ **exactamente**, sea cual
> sea $f$, y su traza vale $n/k$.

La demostración ocupa dos renglones —la varianza de un promedio de $k$ variables
incorreladas— y la medición la confirma: $0{,}159757$ contra $0{,}160000$ con un
vecino, $0{,}007997$ contra $0{,}008000$ con veinte. Lo interesante es el enlace
con ML 28: el número efectivo de parámetros del $k$-NN es $n/k$, de modo que
**la traza de la lección anterior sale aquí de contar vecinos**.

Con un vecino el sesgo es $0{,}000007$, o sea cero: el ajuste interpola. El
fondo de la U resulta plano —$0{,}194514$ con cinco vecinos y $0{,}194581$ con
diez—, lo que explica que errar el $k$ por poco cueste poco.

#### El sesgo no es una cosa, son dos

> **29.3**: sesgo total = sesgo de modelo + sesgo de estimación, punto a punto.

El de modelo se queda clavado en $0{,}003944$ para los cinco valores de $\alpha$:
mide la distancia entre $f$ y una clase que no ha cambiado. El de estimación
arranca en $0{,}000000$ exacto —mínimos cuadrados apunta al mejor miembro de la
clase— y sube a $0{,}188665$ mientras la varianza baja de $0{,}010667$ a
$0{,}002810$. Ese $0{,}010667$ es $p\sigma^2/n$, que es la Proposición 28.3 otra
vez.

La lectura práctica es que **los dos sesgos se curan con cosas distintas**: el de
estimación aflojando $\alpha$, el de modelo solo cambiando la clase, y ninguno
de los dos con más datos.

Un detalle de la regla 21b encontrado al releer: la lección usaba $p$ para el
número de columnas en la sección 2 y para la probabilidad de la clase 1 en la
3, dos secciones seguidas. El número de columnas pasó a $d$, que es como lo
llama ML 28.

#### Donde la descomposición deja de servir

> **29.4**: con pérdida 0-1 y dos clases, el error en $x_0$ vale
> $p+(1-2p)q$, con $q=P(\hat p(x_0)>1/2)$.

El error es **afín en $q$**, y $q$ es lo único que ve de la distribución de
$\hat p$. De ahí que un sesgo que empuje $\hat p$ hacia el lado correcto no
cueste nada al clasificar y cueste cada vez más al medir distancias. Medido: el
error cuadrático toca fondo con veinte vecinos y el 0-1 sigue bajando hasta
cuarenta, donde el cuadrático es **9,51 veces el mínimo y aun así clasifica
mejor**, a medio punto del suelo de Bayes.

Y el extremo enseña lo contrario: con sesenta vecinos el promedio cae justo
sobre $1/2$, el desempate manda todo a una clase y el error salta a
$0{,}500000$. La curva del 0-1 no es una U sino una caída seguida de un
desplome, y la caída no avisa.

#### El contraste de versiones encontró un bit

La primera versión elegía los vecinos por distancia. El gate de las dos
versiones falló en una sola fila: $0{,}080589$ contra $0{,}080584$. La causa no
era el promedio sino el umbral: **en la rejilla de sesenta puntos hay 518 pares
de vecinos simétricos cuya distancia no empata en coma flotante**, así que el
vecino elegido lo decidía el último bit, y después `p̂ > 0.5` lo amplificaba a un
cambio de clase.

La respuesta no fue dejar de imprimir el dígito. Sobre una rejilla uniforme los
$k$ puntos más cercanos son los $k$ **índices** más cercanos, así que la
vecindad se decide con enteros; y la clasificación compara `2*cuenta > k`, que
también es entera. Con eso desaparecen el empate y la fragilidad, no solo el
síntoma. Está anotado en el bloque de Fuentes de la lección.

---

### 3.47 ML 30: EM, y por qué el empate con la librería hay que provocarlo (22-09-2026)

Primera lección **L3** de la tanda, así que lleva contraste con la librería. Y
ahí apareció lo que más enseña.

> **30.4**: $F(q,\theta)\le\ell(\theta)$ siempre, con igualdad si y solo si $q$
> es la posterior.
> **30.5**: de ahí, $\ell(\theta_{t+1})\ge F(q_t,\theta_{t+1})\ge F(q_t,\theta_t)=\ell(\theta_t)$.

La demostración se escribió también **en números**: una tabla de medios pasos
donde tras cada paso E las dos columnas coinciden dígito a dígito
—$-1890{,}878975$ y $-1890{,}878975$— y tras cada paso M la cota se queda por
debajo —$-1874{,}329573$ contra $-1870{,}224378$—. Ese hueco es justo lo que el
siguiente paso E recupera. Sesenta pasos, ninguna bajada, de $-2535{,}646645$ a
$-1777{,}786097$.

#### La verosimilitud no tiene máximo, y se mide a qué velocidad

> **30.6**: con $\mu_1=x_1$ y $\sigma_1\to0$, la verosimilitud diverge.

Medido: las subidas por década valen $2{,}302581$ y luego $2{,}302585$ tres
veces, contra $\log 10=2{,}302585$. **Cada división de $\sigma$ por diez suma
exactamente $\log 10$, y no para.** El régimen limpio empieza por debajo de la
distancia de $x_1$ a su vecino, $0{,}000020$ en ese diseño, y la celda imprime
esa distancia para que se vea de dónde sale el codo de la tabla.

El corolario es que **«el estimador de máxima verosimilitud» de una mezcla no
existe**. Lo que EM encuentra es un máximo local, y con cuatro componentes
solo **3 de 60** arranques al azar dan con el mejor.

Y la Proposición 30.7 cierra el círculo con ML 21: K-means es EM con
desviaciones comunes en el límite $\sigma\to0$, porque las responsabilidades se
vuelven ceros y unos.

#### Lo que costó empatar con scikit-learn

Al principio el empate salía a **seis cifras, no a diez**, y la causa no era un
error: cada implementación paraba con su propio criterio sobre la
verosimilitud. `GaussianMixture` se detiene cuando la verosimilitud deja de
moverse, y la verosimilitud es **cuadrática cerca del óptimo**, así que un error
$\varepsilon$ en los parámetros se nota como $\varepsilon^2$ en el objetivo.
Parar por el objetivo deja los parámetros mil veces menos determinados que él.

La celda lo mide: mover $\mu_1$ una milésima lleva la verosimilitud de
$-1777{,}785945$ a $-1777{,}786045$, o sea la cuarta cifra decimal. Con el mismo
arranque, `tol=0.0`, el mismo número de pasos y `reg_covar=0`, las seis
cantidades coinciden en los diez decimales impresos.

Eso deja una regla para las lecciones L3 que vengan: **para empatar con una
librería hay que fijar el número de pasos, no la tolerancia**, siempre que el
objetivo sea plano en el óptimo. Y `reg_covar` merece nombrarse en la prosa:
existe precisamente para tapar la Proposición 30.6.

---

### 3.48 ML 31: el backfitting es Gauss-Seidel y CART es MARS (22-09-2026)

Dos resultados del capítulo 9 de ESL que el libro enuncia de pasada y aquí se
miden.

> **31.1**: el backfitting es Gauss-Seidel sobre
> $\begin{pmatrix}I & S_1\\ S_2 & I\end{pmatrix}$.
> **31.2**: el error se multiplica en cada vuelta por $S_1S_2$, así que la
> velocidad es $\rho(S_1S_2)$.

Comprobado resolviendo el sistema de $2n$ ecuaciones de golpe: el punto fijo del
backfitting lo resuelve a diez decimales. Y la velocidad, que es lo que se puede
usar: el radio espectral vale $0{,}745725$ y la razón medida entre errores
consecutivos vale $0{,}745725$, **los seis decimales impresos**. El error cae de
$2{,}705\cdot10^{-1}$ a $7{,}187\cdot10^{-7}$ en cuarenta vueltas.

Eso convierte la **concurvidad** en un número: si dos variables se parecen, los
rangos de sus suavizadores se solapan, el radio se acerca a uno y el algoritmo
se arrastra. En el límite el radio vale uno, y entonces no diverge pero el
reparto entre $f_1$ y $f_2$ deja de estar determinado.

#### El techo de lo aditivo, medido

Con una verdad que incluye $2{,}5\,x_1x_2$, el paso hacia adelante de MARS con
grado uno da $R^2$ de $0{,}894886$, $0{,}899814$ y $0{,}903098$ al pasar de cinco
a trece términos: **duplicar los términos mueve cuatro milésimas**. Con grado
dos, el tercer par elegido multiplica dos bisagras y el $R^2$ salta a
$0{,}980471$ y $0{,}987375$. El estancamiento es la definición de aditivo puesta
en números.

#### El contraste con la librería, que aquí es el resultado

> **31.5**: MARS con escalones en vez de bisagras, y con el hijo sustituyendo al
> padre, **es** el árbol de regresión por mejor-primero.

Programado a mano y enfrentado a `DecisionTreeRegressor`: las predicciones
coinciden **punto a punto** en cinco tamaños, de dos hojas a treinta y dos, con
el RSS bajando de $100{,}563416$ a $7{,}361585$. El libro dice que MARS
generaliza a CART; aquí deja de ser una frase.

Para que un empate así sea posible tienen que coincidir tres cosas, y la lección
las nombra: el crecimiento por mejor-primero —que es lo que hace `scikit-learn`
cuando se le fija `max_leaf_nodes`—, los umbrales en los puntos medios entre
valores consecutivos distintos, y el desempate por orden de columna. Si
cualquiera fallara, los dos árboles serían igual de buenos y distintos, y habría
que comparar RSS en vez de predicciones.

De paso apareció el segundo caso de nombres que cambian entre versiones de
`scikit-learn`, anotado en el punto 2: `"mse"` contra `"squared_error"`. La
salida fue no nombrar el criterio.

---

### 3.49 ML 32: AdaBoost no era una receta (22-09-2026)

El capítulo 10 de ESL se sostiene sobre un resultado que reordena todo lo
anterior, y la lección lo mide en vez de derivarlo y dar por buena la
derivación.

> **32.2**: AdaBoost **es** el ajuste por etapas hacia adelante con pérdida
> exponencial, con $\alpha_m=2\beta_m$.

Programados los dos algoritmos **por separado** —uno con pesos, como se publicó;
otro minimizando $\sum_i e^{-y_iF(x_i)}$ sin nombrar AdaBoost— y enfrentados
etapa a etapa: las doce reglas coinciden, $\alpha=2\beta$ a diez decimales
—$0{,}86322176$ en la primera etapa, $0{,}55831525$ en la última— y las
predicciones coinciden en los trescientos puntos.

#### Las dos pérdidas apuntan al mismo sitio

> **32.3**: el minimizador de población de la exponencial y el de la desvianza
> es $\tfrac12\log\frac{p}{1-p}$, el mismo.

Medido en cinco valores de $p$, con los tres números iguales a seis decimales.
Así que **elegir entre las dos no es elegir objetivo**: se diferencian en el
camino, y ahí está la robustez. Con margen $-6$ la exponencial cobra
$403{,}4288$ y la desvianza $12{,}0000$; con $-4$, $54{,}5982$ contra $8{,}0003$.
Un punto mal etiquetado tiene margen muy negativo por construcción, de modo que
bajo pérdida exponencial acapara los pesos.

#### La robustez se paga

> **32.5**: la pérdida solo decide a qué se ajusta el árbol: el residuo con la
> cuadrática, su signo con la absoluta.

El experimento va en dos mitades, que es lo que lo hace informativo. Con nueve
puntos desplazados doce unidades, la absoluta deja $0{,}128660$ de error y la
cuadrática $0{,}407457$: **tres veces más**. Sin esos puntos el orden se
invierte, $0{,}107446$ contra $0{,}129528$. Decir que una pérdida es robusta sin
la segunda mitad esconde lo que cuesta.

#### Tres condiciones para empatar, y la tercera es la que enseña

El contraste con `GradientBoostingRegressor` empata a diez decimales en
entrenamiento y en prueba, pero solo si se aciertan tres cosas: que arranca en
**la media de $y$**, que el árbol usa **`friedman_mse`** por dentro, y que el
azar es **un solo objeto compartido por las sesenta etapas**, no una semilla por
etapa.

La tercera es la interesante porque **su incumplimiento no se nota en
entrenamiento**: con semilla por etapa las predicciones sobre los datos siguen
coincidiendo y solo se separan **3 de 500** puntos nuevos, los que caen junto a
un empate que un árbol de los sesenta rompió del otro lado. Es el aviso de ML 31
visto de cerca: con empates, «el mismo algoritmo» no garantiza «el mismo
resultado» fuera de los datos de ajuste.

#### El gate de visuales cazó lo que antes cazaba el navegador

Los dos visuales salieron **muertos**: los cuatro controles sin mover nada.
Faltaba el `</script>` de cierre en los dos bloques, así que el navegador se
tragaba el código como texto. Es el mismo fallo de `series/02` que está anotado
en la regla 9, con una diferencia que conviene registrar: **allí lo encontró la
comprobación con navegador y aquí lo encontró `visuales.py`**, que es más barato
y corre antes. El orden bueno de la tubería sigue siendo el mismo, pero la red
tiene ahora dos mallas en vez de una.

---

### 3.50 ML 33: cuando no hay librería contra la que empatar (22-09-2026)

Reglas de asociación, primera lección donde **el contraste con la librería no
se puede hacer como siempre**: `scikit-learn` no trae apriori y no hay otra cosa
en el entorno que lo haga.

La salida no fue rebajar el nivel sino buscar un oráculo **más fuerte** que una
librería: enumerar los $65535$ subconjuntos sin podar nada. Apriori mira $290$
de ellos, el $0{,}4425\ \%$, y encuentra los **mismos $145$ conjuntos
frecuentes con los mismos soportes**. La poda deja de ser una promesa y pasa a
ser una identidad comprobada. Es el mismo razonamiento que ya se había usado en
Est 22 y 23 con PyMC: cuando no hay librería, se busca algo exacto.

Y la librería sí entra donde tiene algo que hacer, que es la reformulación de
ESL §14.2.

> **33.4**: con dos muestras del mismo tamaño, los momios de «este dato es
> real» valen $p(x)/p_0(x)$, o sea el lift de la cesta entera.

Comprobado con un árbol **sin límite de profundidad**, que tiene una hoja por
patrón y cuyos momios son por tanto el cociente de cuentas exacto —a diez
decimales—. Esos momios siguen al lift verdadero con correlación $0{,}998665$ en
el logaritmo, y los cinco patrones de mayor lift llevan todos los tres artículos
que se plantaron.

#### La confianza, medida

> **33.2**: una regla informa solo si su confianza supera la frecuencia del
> consecuente.

Con una trampa puesta a propósito: $\{7\}\Rightarrow\{5\}$ tiene confianza
$0{,}850560$ y lift $0{,}913599$. Y el recuento que conviene recordar: de las
$58$ reglas con confianza por encima de $0{,}8$, **$28$ tienen lift menor que
uno**. Casi la mitad de lo que un umbral de confianza habría sacado a la luz son
señales negativas disfrazadas.

#### Dos colisiones de glosario en una sola lección

`soporte` ya significa el soporte de una distribución en ocho lecciones, y
`confianza` aparece dentro de «intervalo de confianza» en varias más. Las dos
salen del glosario global por la regla 21b y viven en la tabla de notación, que
ahora dice explícitamente «nada que ver con la de un intervalo de confianza» y
«no es el soporte de una distribución».

`lift` sí estaba, con el sentido de evaluación de Est 16. Ahí no hacía falta
sacarlo: **son la misma idea** —lo observado dividido por lo que habría al
azar—, así que la entrada pasó a nombrar los dos usos en vez de elegir uno.

#### El aviso de la regla 19b, atendido en vez de declarado

El visual del retículo pasó el gate pero con dos avisos: los nodos cambiaban de
color y **no se movían ni un píxel**. Era cierto, y la respuesta no fue
declararlos en `QUIETOS`: el radio de cada nodo pasó a ser su soporte y se añadió
una tira donde los quince soportes caen sobre un eje con el umbral marcado. Ahora
los dos controles mueven geometría, y de paso el dibujo enseña **por qué** cae
cada nodo en vez de solo que cae.

---

### 3.51 ML 34: tres métodos, tres proposiciones, y un signo que cambia de máquina (22-09-2026)

Espectral, SOM y factorización no negativa. Cada uno con un resultado que se
puede demostrar en dos renglones y medir en uno.

> **34.2**: $f^{\top}Lf=\tfrac12\sum_{i,j}W_{ij}(f_i-f_j)^2$, así que el
> laplaciano es semidefinido positivo y **la multiplicidad de su cero cuenta las
> componentes conexas**.

Comprobado en cuatro grafos: con tres vecinos el grafo se rompe en $16$ trozos y
hay $16$ autovalores nulos; con cuarenta queda conectado y hay uno. Y la
consecuencia sobre dos anillos concéntricos: **K-means acierta $0{,}520000$ —lo
que acierta una moneda— y el espectral $1{,}000000$**, sin tocar K-means: solo
cambiando las coordenadas por los autovectores.

> **34.4**: un SOM con radio cero **es** K-means en línea.

Programados los dos por separado: los mismos prototipos a diez decimales. Y el
precio de la topología, medido con dos números que se mueven en direcciones
contrarias: al subir el radio de cero a tres el error pasa de $0{,}006769$ a
$0{,}021949$ mientras la cadena se acorta de $5{,}212029$ a $0{,}908162$. Eso es
lo que cuesta poder dibujar el mapa.

> **34.6** y **34.7**: la actualización multiplicativa no sube el error; la SVD
> del mismo rango siempre gana en error.

Cuatrocientos pasos sin una sola subida, de $2155{,}380989$ a $0{,}995285$,
contra $0{,}949855$ de la SVD. Lo que la SVD no gana es en lectura: **dos de sus
tres componentes tienen entradas de los dos signos**, con un $31{,}57\ \%$ de la
masa en el minoritario; la factorización, cero de tres.

#### El orden de dos líneas decide el empate

El contraste con `sklearn.decomposition.NMF` empata **a diez decimales en los
factores y en el producto**, pero la primera versión no: daba $0{,}996205$
contra $0{,}995285$, con los factores separados por ocho décimas. La causa era el
**orden** de las dos actualizaciones multiplicativas. La librería mueve $W$ y
después $H$; la celda lo hacía al revés. Las dos versiones son la misma
proposición, y solo una es el mismo algoritmo.

Va quedando una lista de condiciones para que un empate L3 sea posible, y cada
lección añade una: el arranque y `reg_covar` en ML 30, el número de pasos en vez
de la tolerancia también en ML 30, `friedman_mse` y el generador compartido en
ML 32, y ahora el orden de las actualizaciones.

#### Y un caso donde buscar el empate no tiene sentido

`SpectralClustering` normaliza el laplaciano y arranca su K-means de otro modo,
así que no hay empate dígito a dígito. Lo que sí hay es **la misma partición,
punto por punto**. Cuando un método termina en una decisión discreta, la
comparación correcta es la decisión.

#### El signo de la SVD, otra vez

La primera versión de la celda contaba entradas negativas en las componentes de
la SVD: **$44$ en una máquina y $48$ en la otra**. Es el aviso que ya estaba en
el punto 5 —una base de la SVD no es única, LAPACK devuelve otra por versión—
aplicado a algo que no parecía una base.

La salida fue medir algo **invariante al volteo de cada componente**: cuántas
filas tienen entradas de los dos signos, y qué fracción de la masa se lleva el
signo minoritario. Las dos cuentas no cambian si se multiplica una fila entera
por $-1$, y las dos versiones vuelven a coincidir.

---

### 3.52 ML 35: cinco arreglos para que un árbol dé lo mismo dos veces (22-09-2026)

Cierra ESL. Dos proposiciones cortas y una tabla que las junta.

> **35.2**: $\operatorname{Var}(\bar Z)=\rho\sigma^2+\frac{1-\rho}{B}\sigma^2$.
> **35.3**: $\mathbb{E}[\bar Z]=\mathbb{E}[Z_1]$, así que el sesgo de un bosque
> es el de **un** árbol aleatorizado.

La primera se comprueba sobre cuatrocientas mil repeticiones de un modelo donde
$\rho$ y $\sigma^2$ **se conocen**: ocho combinaciones que coinciden en la
tercera cifra. Los árboles se dejan para lo que solo ellos pueden dar, que es
medir cómo se mueven $\rho$ y $\sigma^2$ de verdad. Separar así las dos cosas
evitó lo que la primera versión hacía: comprobar una identidad algebraica contra
sí misma.

La segunda se mide con el sesgo al cuadrado quieto en $0{,}397403$ y $0{,}379543$
mientras la varianza **se divide por $11{,}72$**. De ahí que $B$ no se ajuste.

#### Los dos regímenes de m, en la misma tabla

Con **tres relevantes de doce**, $\sigma^2$ casi se duplica al bajar $m$ —de
$0{,}619405$ a $1{,}136664$— porque los cortes se gastan en columnas sin señal, y
el mejor $m$ queda cerca de $p$. Con **los doce relevantes**, $\sigma^2$ se
queda entre $2{,}481136$ y $2{,}513107$, un uno por ciento, así que
descorrelacionar sale gratis y el mejor $m$ baja a cuatro. La recomendación de
$\sqrt p$ es un punto de partida, no un resultado.

#### El árbol tuvo que escribirse a mano, y costó cinco arreglos

La primera versión usaba `DecisionTreeRegressor`, y **las tres celdas daban
números distintos en las dos versiones de Python**: el constructor de árboles de
`scikit-learn` cambió entre 0.24 y 1.9. Un árbol de veinte líneas en NumPy lo
arregla, pero conseguir que diera lo mismo dos veces pidió cinco cosas, y cada
una es una trampa reutilizable:

1. **El árbol, a mano**, porque el de la librería no es reproducible entre esas
   dos versiones.
2. **`rng.choice(p, m, replace=False)` fuera**, sustituido por
   `np.argsort(rng.random(p))[:m]`: el sorteo sin reemplazo cambió de algoritmo.
3. **La ganancia de un corte, sin la resta.** El RSS escrito como
   $\sum y^2 - s_1^2/k - (t_1-s_1)^2/(n-k)$ cancela los términos de cuadrados, de
   modo que basta maximizar los dos últimos. Escrito con la resta, la
   cancelación entre cantidades grandes y parecidas movía el corte elegido.
4. **`rng.uniform` fuera**, sustituido por `a + (b-a)*rng.random(forma)`. Este es
   el hallazgo que vale para todo el proyecto y está anotado en el punto 5:
   `uniform` con forma **no da los mismos bits** en numpy 1.24 y 2.5.3, mientras
   que `random`, `normal`, `standard_normal` e `integers` sí.
5. **Los empates, por posición.** Entre cortes que empatan hasta una
   milmillonésima se elige el primero; con `argmax` a secas la elección quedaba
   en el último bit.

Los cuatro primeros se encontraron a ciegas y el quinto por eliminación,
comparando hashes de cada paso intermedio hasta ver que **X ya difería antes de
tocar el árbol**. Esa técnica —hashear los intermedios en vez de mirar la salida
final— es lo que conviene recordar del episodio.

---

### 3.53 ML 36: la regla de la cadena, contada en pasadas (22-09-2026)

Empieza la parte de aprendizaje profundo. ML 16 decía **qué** calcula una red;
esta dice cómo se le saca el gradiente y qué cuesta.

> **36.2**: para una capa $z=aW+b$,
> $\partial L/\partial W=a^{\top}\delta$, $\partial L/\partial b=\sum_i\delta_i$
> y $\partial L/\partial a=\delta W^{\top}$.

Escritas en forma matricial, que es como se programan, y no por índices como en
el libro. Comprobadas contra diferencias centradas con error relativo **menor
que $10^{-8}$** sobre los $71$ parámetros.

> **36.3**: el gradiente cuesta una pasada de ida y una de vuelta; por
> diferencias centradas cuesta $2P$.

Medido en pasadas, no en segundos —los segundos dependen de la máquina—:
**$142$ contra $2$** en una red de $71$ parámetros, con el cociente creciendo
como $P$. Con un millón de parámetros el cociente es un millón, y ahí está la
razón de que el aprendizaje profundo sea posible.

#### La cota 1/4, convertida en medición

> **36.4**: $\sigma'=\sigma(1-\sigma)\le\tfrac14$.

Nueve capas con sigmoide: la primera recibe $2{,}161\cdot10^{-6}$ y la última
$5{,}393\cdot10^{-2}$, una razón de $4{,}006\cdot10^{-5}$ contra la cota
$0{,}25^8=1{,}526\cdot10^{-5}$. Y el número que cierra la proposición: **la
mediana del cociente entre capas consecutivas vale $0{,}2445$**. Con ReLU todas
las capas se quedan en el mismo orden de magnitud.

La lectura, que es la que justifica las lecciones 37 a 41: la primera capa de
una red profunda con sigmoide **no aprende**, y no por falta de datos ni de
tiempo, sino porque no le llega nada que aprender.

#### Un contraste L3 con los papeles al revés

`scipy.optimize.check_grad` es la librería adecuada aquí, y el contraste tiene
una particularidad que conviene anotar para las lecciones que vengan: **la
referencia exacta es la implementación propia**, no la de la librería.
Backpropagation da la derivada sin error de aproximación; `check_grad` la
compara con diferencias hacia adelante, que sí truncan. Lo que sobra viene de
ella.

Por eso la celda imprime **órdenes de magnitud y no dígitos**: los dígitos
serían los de la aproximación y no los del resultado. Es la regla 7 aplicada al
revés de lo habitual — no porque el cálculo propio sea inestable, sino porque lo
es el de la referencia.

---

### 3.54 Python crece de 16 a 30, porque estaba pobre (22-09-2026)

Luis dijo que las clases de Python se sentían **pobres frente a los cursos de
DataCamp**. Al medirlo resultó cierto por dos vías distintas, y conviene
guardar las dos porque son problemas diferentes.

#### Cobertura

Buscando tema por tema en las dieciséis lecciones, estos aparecían en **cero**:
SQL y bases de datos, expresiones regulares, peticiones HTTP y APIs,
anotaciones de tipo, perfilado, zonas horarias, concurrencia y `dataclass`.
Clases y objetos, solo de pasada en tres; `pytest`, en una mención suelta. No
estaban tratados por encima: **no estaban**.

#### Profundidad desigual

Contando definiciones y proposiciones por lección, las **1–8** —lenguaje y
NumPy— promedian $3{,}3$ y $5{,}6$; las **9–16** —pandas, visualización,
proyecto— promedian $1{,}1$ y $3{,}6$. La mitad de pandas derivó hacia recorrido
de API, que es justo lo que el molde quería evitar. Las más flojas son la 11, la
12, la 14 y la 16, con una definición y tres proposiciones cada una.

Lo que **no** era el problema: el tamaño. Las lecciones existentes van de $540$ a
$840$ líneas con $9$ a $16$ celdas.

#### El plan

Python pasa a **30** con una sección nueva, «Ingeniería de datos — Fase 2»:
17 clases y protocolos, 18 decoradores, 19 tipado gradual, 20 texto y regex,
21 SQL desde Python, 22 HTTP y APIs, 23 Parquet y Arrow, 24 pruebas,
25 depuración, 26 perfilado, 27 el GIL, 28 datos que no caben, 29 categóricos e
índices, 30 zonas horarias. Y queda pendiente **una pasada de profundidad sobre
la 11, 12, 14 y 16**.

### 3.55 Python 17: el contrato del hash, medido (22-09-2026)

Primera de la tanda nueva. Nivel **L4**, con modo de falla en cada resultado.

> **17.3**: si $a=b$ entonces `hash(a)` debe valer `hash(b)`. Definir `__eq__`
> sin `__hash__` deja la clase sin hash; definir un `__hash__` incoherente hace
> que el diccionario guarde **dos entradas para claves iguales**.

Los cuatro estados en una sola tabla, y el remate: con la clase de hash roto,
`a == b` vale `True` y `b in d` vale `False`. Ninguna excepción, ningún aviso.

> **17.4** y **17.6**: `for`, `len` e `in` piden métodos, no una lista; y
> `__slots__` quita el diccionario de instancia.

Medido: una clase que funciona con ocho operaciones distintas sin guardar sus
elementos, y que ocupa **$56$ bytes con diez elementos y con cien mil**, frente
a los $800\,056$ de la lista. Más el detalle que se usa de verdad: definir
`__contains__` no añade una operación, **cambia el coste** de una que ya existía.

> **17.7** y **17.8**: el orden de resolución es `D -> B -> C -> A -> object`, y
> el cuerpo de la clase se ejecuta una vez.

#### Lo que hubo que corregir en el camino

La primera versión salió con **una definición y cuatro proposiciones**, que es
exactamente el nivel de la mitad floja que se acababa de criticar. Se añadieron
dos definiciones y una proposición con contenido real —qué es un método
especial, por qué un protocolo no exige heredar, qué hace `__slots__`— hasta
llegar a **3 y 5**.

Dos detalles más: el bloque de Reto decía «sección **Lección 17**» y `retos.py`
lo rechazó, porque el módulo se nombra **Python**; y el mensaje del `TypeError`
de una jerarquía imposible **cambia entre versiones de Python**, así que la
celda imprime solo el tipo de la excepción.

La lección **no cita ningún libro**: McKinney no trata el modelo de objetos y
ningún texto con índice verificado lo hace. Queda como decisión abierta traer la
documentación oficial de Python como fuente verificada, que dejaría a las
catorce nuevas citando capítulo y sección.

---

### 3.56 Python 18: el coste, contado en llamadas (22-09-2026)

Segunda de la tanda nueva, y la que cierra el bloque de lenguaje que empezó la
17.

> **18.2**: `@d` es exactamente `f = d(f)`.
> **18.3**: el envoltorio tapa el nombre, la documentación y **la firma**.
> **18.4**: el decorador corre al definir; el envoltorio, en cada llamada.
> **18.6**: `@d(x)` es `f = d(x)(f)`, de ahí el tercer nivel.
> **18.8**: una caché es un diccionario, así que hereda el contrato del hash.

Dos cosas del método merecen quedarse.

#### El coste se mide en llamadas, no en segundos

Sin caché, `fib(25)` ejecuta el cuerpo **$242\,785$ veces**; con caché, **$26$**.
El cociente es $9337{,}9$ a $1$ y es un número **citable**, porque las llamadas
no dependen de la máquina y los segundos sí. Es la misma decisión que en ML 36,
donde el coste de backpropagation se contó en pasadas.

Y el contraste con la librería sigue la misma idea: la caché propia y
`functools.lru_cache` coinciden en **$23$ aciertos y $26$ fallos**. Comparar
contadores es más fuerte que comparar relojes.

#### Tres reglas que son una

La Proposición 18.4 dice lo mismo que la 17.8 —el cuerpo de una clase se
ejecuta una vez— y que los valores por defecto de Python 2: **lo que está en el
sitio de definir se evalúa al definir**. La lección las pone juntas a propósito,
para que se recuerden como una sola.

#### Lo que los gates corrigieron, por segunda vez seguida

La lección salió con **una definición y dos demostraciones**, que es el nivel
flojo que se acababa de criticar en el punto 3.54. Subió a **3 y 4** añadiendo
la fábrica de decoradores, la memorización y las dos demostraciones que
faltaban. Conviene anotarlo como patrón: **una lección nueva tiende a salir por
debajo del molde**, y el recuento de `formato.py` es lo que lo detecta.

Y el visual de las capas cambiaba de tamaño **sin mover ningún marcador**, como
el retículo de ML 33. Rehecho como el recorrido de la llamada atravesando una
caja por capa: ahora la función se desplaza al añadir capas, y el dibujo enseña
mejor lo que pasa.

---

### 3.57 Python 19: la anotación que no comprueba nada (22-09-2026)

Cierra el bloque 17–19. La lección se sostiene sobre una sola exhibición: una
función anotada `(base: float, altura: float) -> float` a la que se le pasa
`('ab', 3)` y devuelve `'ababab'`, una cadena. La anotación se guarda y no se
mira. De ahí salen las seis proposiciones, incluida la que mide el coste de
convertirla en comprobación de verdad: **2000 comprobaciones en 1000 llamadas**
de una función de dos parámetros, es decir 2,0 por llamada, constante respecto
al tamaño de los datos.

**Lo que encontró el trabajo.** Dos diferencias entre versiones, las dos
invisibles hasta que se imprimen:

· `typing.Optional[int]` se muestra como `typing.Union[int, NoneType]` en 3.8 y
como `int | None` en 3.14. La celda no imprime el repr: imprime el número de
ramas, si `int` está entre ellas y si `Optional[int] == Union[int, None]`. Tres
hechos estables que dicen lo mismo.

· Una referencia adelantada **sin comillas** levanta `NameError` al definir en
3.8 y no levanta nada en 3.14, por la evaluación diferida de la PEP 649. Eso no
se puede imprimir sin romper el gate de las dos versiones, así que **se enseña
en prosa, citando la PEP y la versión**, y la celda demuestra solo la práctica
que funciona igual en las dos: entrecomillar y resolver con `get_type_hints`.

Es la primera vez que una diferencia entre versiones entra en una lección como
**contenido** en vez de como problema que esquivar.

**Un error propio para poder medir.** El comprobador levanta `TipoInvalido`, una
subclase de `TypeError`, y no `TypeError` a secas. Con `TypeError` el `except`
de la celda atrapaba también el error que revienta **dentro** del cuerpo y lo
etiquetaba como si lo hubiera rechazado la puerta, que es justo la distinción
que la Proposición 19.9 quiere enseñar: `[1.0, 'dos', None]` **es** una lista,
pasa la comprobación, y falla después al sumar. Tener clase propia separó los
dos casos.

**El molde, otra vez por debajo al primer borrador.** Tercera vez seguida
(17, 18, 19). Salió con 3 def / 5 prop / 4 dem y subió a **3 / 6 / 6**. Conviene
contar antes de dar la lección por escrita.

**Dos deslices de plomería del molde**, los dos del gate y no del navegador: el
marcador de celda plantilla son **seis** guiones bajos `______` y no cuatro —con
cuatro, `salidas.py` intenta ejecutar el hueco y revienta con `NameError`—, y el
bloque de respuesta es `::: {.solution}` en inglés, no `.solucion`. Además el
primer bloque `## Reto` nombró `F1-retos.ipynb` cuando a Python 19 le toca
`F2-retos.ipynb`; el generador ya había escrito la sección en el cuaderno
equivocado y hubo que quitarla a mano.

### 3.58 Nace Fundamentos, porque el curso no tenía piso de abajo (22-09-2026)

Luis precisó la crítica del punto 3.54: lo que echaba en falta no eran temas
avanzados sino **las bases**, «metodos arrays while for truplas». La primera
medición había buscado lo contrario y por eso no lo vio.

**Cómo se midió bien.** Contar apariciones sobre el `.qmd` entero da basura: los
visuales llevan `while (svg.firstChild)` y `svg.appendChild`, así que `while`
salía en 19 de 19 lecciones y `.append` también. Midiendo **solo dentro de las
celdas `{pyodide}`**, que es lo que se enseña:

| | aparece en |
|---|---|
| `while` | 4 de 19 |
| `enumerate` | 1 de 19 |
| métodos de cadena | 4 de 19 |
| conjuntos | 5 de 19 |
| recursión | 0 |
| `break` / `continue` | 0 |

**Pero el conteo no era lo importante.** Lo decisivo es dónde arranca la lección
1: su primer objetivo es «enunciar qué es un objeto (identidad, tipo y valor)» y
el cuarto «demostrar que un tipo mutable con igualdad por contenido no puede ser
hashable». La 3 empieza por el protocolo de iteración. Eso no es el capítulo 1
de un curso: los bucles y las listas **se usan** en todas partes y no **se
enseñan** en ninguna.

**Decisión.** Un módulo nuevo `fundamentos/`, 12 lecciones L1–L2, antes de
Python en el índice, con la vía de lógica y algoritmos como cierre (lección 12).
Las 30 de Python no se tocan y no hay que renumerar nada. Sigue el mismo molde
—definición, proposición, demostración, celdas que corren, dos visuales— pero al
nivel que le toca: se demuestra que `0.1 + 0.2 != 0.3`, no la asimetría de `+=`.

**Un módulo nuevo toca seis sitios**: `grafo/build_graph.py` (`MODULOS`),
`verificar/retos.py` (`MODULOS`, sin copiar alias ajenos), `proyectos/genera_retos.py`
(dos alternancias escritas a mano, más `MOD`), `_quarto.yml`, `index.qmd` (la fila
del módulo con su `data-ids`) y el `index.qmd` propio. `estructura.py` y
`formato.py` lo descubren solos por glob.

**Fundamentos 1, «Valores, nombres y tipos».** 3 def / 7 prop / 7 dem. Se apoya
en tres exhibiciones: `2 ** 100` exacto terminando en 6; `0.1` impreso con veinte
decimales dando `0.10000000000000000555`; y `a = 5 ; b = a ; a = 7` dejando `b`
en 5. La identidad `a == (a // b) * b + (a % b)` se comprueba en los cuatro pares
de signos. El visual de los bits dibuja las marcas que el binario puede
representar entre 0 y 1 y enseña que 0,1 cae entre dos, con el mismo mecanismo
que el `float` real a 52 bits.

Se eligió exhibir `'ab' * 3 == 'ababab'` aquí a propósito: es la misma
exhibición sobre la que se apoya Python 19 para demostrar que una anotación no
comprueba nada, ochenta semanas más adelante.

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
   y de la portada, barra lateral de `_quarto.yml`, `grafo/build_graph.py`, y
   **`python3 proyectos/genera_retos.py --escribe`**, que añade su sección al
   cuaderno de retos. Ese último paso se saltó durante semanas y la deuda llegó
   a 33 secciones.
8. **Los cinco gates**, y `quarto preview` para ver la página de verdad.

```sh
python3 verificar/estructura.py  && \
python3 verificar/citas.py       && \
python3 verificar/referencias.py && \
python3 verificar/salidas.py     && \
python3 verificar/formato.py     && \
python3 verificar/visuales.py --estricto
```

---

## 5. Errores que ya se cometieron

No repetirlos sale más barato que volver a encontrarlos.

**`rng.uniform(a, b, forma)` no da los mismos bits en todas las versiones de
NumPy (22-09-2026).** Encontrado al escribir ML 35: con la misma semilla,
`rng.uniform(-1.5, 1.5, (120, 8))` devuelve arrays con hash distinto en numpy
1.24 y en 2.5.3, mientras que `rng.random`, `rng.normal`, `rng.standard_normal`
y `rng.integers` coinciden **bit a bit**. La diferencia es de un ulp y pasa
desapercibida en casi todo, pero basta para que un `argmax` cambie de corte.

**La regla para las celdas nuevas:** generar con `rng.random(forma)` y hacer la
transformación afín a mano, `a + (b - a) * rng.random(forma)`. Lo mismo con
`rng.choice(p, m, replace=False)`, cuyo algoritmo también cambió: se sustituye
por `np.argsort(rng.random(p))[:m]`. Las lecciones anteriores que usan
`rng.uniform` pasan el gate tal cual —sus dígitos impresos no dependen de ese
bit—, así que no se tocan; la regla es para lo que se escriba a partir de ahora.

**Números escritos de cabeza en los bloques de comprobación (19-09-2026).**
Van tres en dos días: Python 12 en su momento, ML 18 con $0{,}343207$ cuando la
celda daba $0{,}358358$, y ML 19 con $0{,}924528$ cuando daba $0{,}923599$. Los
tres eran la respuesta esperada de un ejercicio, calculada mentalmente al
escribir el bloque `check`.

**Los tres los cazó el procedimiento** —ejecutar todas las celdas antes de
registrar las afirmaciones—, así que ninguno llegó a publicarse. Pero la
costumbre correcta es más simple: **calcular el valor con el intérprete y pegarlo**,
nunca escribirlo de cabeza, por fácil que parezca la cuenta.

**Una cifra de la prosa se quedó huérfana de su celda (18-09-2026).** En ML 13,
la prosa y el bloque de Fuentes citaban $0{,}0887$ y $0{,}2396$ como prueba de que
el impulso sobreajusta, de una fila de la tabla que se había quitado al
reorganizarla. Lo cazó la relectura, no un gate: `salidas.py` comprueba que la
salida de la celda contenga lo declarado, **no** que las cifras de la prosa estén
en alguna celda.

**La regla que queda:** al reorganizar una tabla o una celda, releer la prosa que
la comenta. Es el tercer caso de la misma familia, después de los resúmenes
inventados del visual de Python 16 y de los dos textos del visual de ML 12 que su
propio dibujo contradecía.

**El CI se rompió por una medición de memoria (18-09-2026).** La tercera vez, en
Python 15, y la causa está desarrollada en el punto 3.16. En una línea: la celda
**medía** el pico de `tracemalloc` para contar arreglos temporales, y ese número
depende del asignador, de la versión y del sistema. Las dos parejas locales no lo
cazaron porque las dos son macOS y el runner es Linux con Python 3.12.

**La regla que queda:** cuando una afirmación necesite un número que salga de un
reloj o de un asignador, se **intercepta la operación** en vez de medir su efecto.
Contar es reproducible; medir, no.

**El CI se rompió por el número de condición (18-09-2026).** La segunda vez, en
ML 9. Y esta no la cazaba el contraste de versiones del punto anterior, por una
razón que conviene entender: **los dos venv corren en la misma máquina y sobre el
mismo LAPACK**. El numpy de aquí usa *Accelerate*, el de Ubuntu usa *OpenBLAS*, y
hay cálculos en los que eso decide el resultado.

**La causa exacta.** Las celdas centraban la matriz de diseño con
`X -= X.mean(0)`. Eso hace que las filas sumen cero, **anula un valor singular** y
deja la matriz con rango $n-1$ en vez de $n$. El número de condición salta de
$2{,}24$ a $2{,}6\times 10^{15}$. En ese régimen, decidir qué valor singular cuenta
como cero depende del umbral que use cada implementación, y `np.linalg.lstsq` y
`np.linalg.pinv` dejan de coincidir: aquí daban lo mismo a $2\times 10^{-16}$ y en
el runner no llegaban a $10^{-10}$.

Lo peor es que **otra celda de la misma lección tenía el defecto y pasó igual**:
los mismos $10^{15}$ de condición, y el runner acertó por poco. Pasar no es lo
mismo que estar bien.

**El arreglo fue quitar la causa, no aflojar la tolerancia.** Las dos celdas
trabajan ahora con la $X$ **sin centrar** —el centrado no hacía falta para lo que
demuestran— y el número de condición queda en $2{,}24$ y $3{,}63$. Además, donde
antes se citaba una norma con seis decimales ahora se comprueba la identidad
$\lVert\beta\rVert^2-\lVert\hat\beta^{+}\rVert^2=25$, que es Pitágoras y **no
depende de los datos ni de la máquina**.

**La regla, dicha para la próxima.** La regla 7 ya decía «nunca citar dígitos de
un cálculo numéricamente inestable». Lo que faltaba era el diagnóstico concreto:

- **Lo que hay que mirar es la condición de la matriz que se le pasa a un
  solucionador** —`lstsq`, `pinv`, `solve`— y de la que salen los dígitos que se
  citan. Si pasa de $10^{10}$, no se cita ningún dígito de ese cálculo.
- **No vale medir la condición de cualquier matriz de la celda.** Se auditaron las
  64 lecciones y salieron 24 «en riesgo», casi todas falsos positivos: eran
  matrices **sombrero**, **proyectores** y $X^\top X$ con $p>n$, que son singulares
  **por definición** —un proyector tiene eigenvalores $0$ y $1$— y que nunca se
  invierten para imprimir un número. El riesgo estaba solo donde una matriz mal
  condicionada entraba en un solucionador y su salida se citaba con dígitos.
- **Centrar un diseño y después descomponerlo es el olor característico**: el
  centrado introduce una dependencia lineal exacta, y a partir de ahí el rango es
  una decisión de umbral.
- Cuando dos caminos deben dar lo mismo por matemática —`lstsq` y `pinv`, primal y
  dual—, comprobar **la propiedad** (que las dos ajusten, que una tenga menor
  norma) antes que la igualdad numérica estrecha.

**El CI se rompió por una representación, no por un cálculo (17-09-2026).** Al
subir las seis lecciones, `salidas.py` falló en el runner con **5 fallos** en
Python 9 y Python 10, después de haber pasado en local. Ninguna proposición era
falsa: lo que cambió fue **cómo se imprimen las cosas** en versiones nuevas.

- **NumPy 2.0 cambió el `repr` de los escalares**: `repr(np.int64(1))` ya no es
  `1` sino `np.int64(1)`. Eso rompe cualquier `print` de una **lista** de
  escalares de NumPy, porque la lista usa el `repr` de sus elementos. El remedio
  es `.tolist()`, que devuelve enteros de Python.
- **pandas 3.0 renombró el dtype del texto**, de `object` a `str`. Eso rompe
  todo `print(str(serie.dtype))` sobre una columna de texto.

**La regla que ya existía era buena y la leí mal.** Decía «imprimen escalares y
booleanos, **nunca la representación** de un DataFrame». Entendí «representación»
como el `repr` de una tabla entera, cuando **el nombre de un dtype y el `repr` de
un escalar de NumPy son igual de frágiles**. La regla, dicha bien: *lo único que
una celda puede imprimir con seguridad son valores nativos de Python —int, float,
bool, str— y cadenas que la propia celda construya*. Todo lo demás lo decide la
librería y puede cambiar de versión.

**El arreglo fue de raíz, no de parche.** Las celdas ahora imprimen la **familia**
de cada columna —texto, entero, flotante, booleano— calculada con
`pandas.api.types`, que es la propiedad de la que hablan las proposiciones, y no
el nombre que la librería le dé. Es además mejor contenido: Python 10 explica
ahora que pandas renombró el dtype en la 3.0 y que un programa que compare contra
`"object"` deja de funcionar al actualizar.

**Y sobre todo: hay que correr el gate con las versiones del runner antes de
subir.** La máquina tiene pandas 1.2.4 y numpy 1.24; el runner instala las
últimas. Pasar en local no dice nada sobre el CI. Con esto basta:

```sh
python3.14 -m venv /tmp/ci-venv
/tmp/ci-venv/bin/python -m pip install --quiet numpy scipy scikit-learn pandas
/tmp/ci-venv/bin/python verificar/salidas.py     # el gate, con las versiones del CI
python3 verificar/salidas.py                     # y con las de la maquina
```

Las dos tienen que pasar. Si una celda solo pasa en una, lo que imprime depende
de la versión y hay que reescribirla, no declarar otra afirmación.

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

**Un alias de módulo puede hacer que un gate dé verde sobre la sección
equivocada (22-09-2026).** Al crear el módulo Fundamentos se copió la entrada de
Python en la tabla `MODULOS` de `verificar/retos.py`, alias incluido:
`"Fundamentos": ("Fundamentos", "Lección")`. Pero `F0-retos.ipynb` tiene
secciones antiguas tituladas «## Lección 1 — Tipos y estructuras», que son
`python/01`. El gate casó `Fundamentos 1` contra `Lección 1`, **dio verde, y la
sección no existía**. Se quitó el alias: `"Fundamentos": ("Fundamentos",)`.
La regla general: un alias solo vale para el módulo que ya lo usaba, y añadir un
módulo a una tabla no es copiar la fila de al lado.

`proyectos/genera_retos.py` tenía el problema complementario y silencioso: dos
alternancias con los módulos escritos a mano, ninguna con `Fundamentos`, así que
la lección **se descartaba con un `continue`** y el generador informaba «no falta
ninguna sección». Un módulo nuevo obliga a tocar las dos, más `MOD` y
`grafo/build_graph.py`.

**Leer el código de salida de la tarea equivocada (22-09-2026).** `visuales.py`
se lanzó en segundo plano dentro de una línea `gate > archivo; echo exit=$?;
grep ...`. La notificación de la tarea informó `exit code 0`, que era el del
`grep` final, no el del gate; el gate había escrito `exit=1` dentro de su propio
archivo. Con esa lectura se comitió y publicó `bd27712`, y el CI lo rechazó por
dos controles de Python 19 que no movían el dibujo (regla 19b): `rl-q` y `pu-c`
cambiaban el texto de la lectura y nada más. **Un gate en segundo plano se
comprueba abriendo su archivo de salida, no por el código de salida de la
tubería que lo envuelve.**

## 6. Decisiones pendientes

- ~~**Qué trata Estadística 25.**~~ **Resuelto el 13-09-2026.** Estaba planeada
  como *PyMC en producción* y así no se podía escribir: PyMC no corre en la
  plataforma, que solo tiene numpy en el navegador y en el runner de CI. Se
  descartó también sustituirla por una lección de A/B testing, porque **el plan
  de Causal ya la tiene**: su lección 04 es *A/B testing: diseño y potencia
  derivada* y la 05 es *Pruebas secuenciales y el problema del peeking*. Lo
  encontró Luis, y conviene recordar el método: **antes de proponer un tema,
  mirar los índices de los módulos vacíos**, que tienen su plan escrito aunque
  no tengan lecciones.

  La 25 pasa a ser **síntesis del módulo**: el mapa de las 24 en cuatro bloques,
  tres *puentes* demostrados —mínimos cuadrados igual a máxima verosimilitud,
  bootstrap igual a la fórmula del error estándar, e intervalo de confianza
  igual al de credibilidad con prior plana— y una sección de casos con once
  fuentes de datos abiertas, comprobadas una a una.
- ~~**Qué molde usan las lecciones de Python.**~~ **Decidido el 13-09-2026**: se
  mantiene el molde completo, definiciones numeradas incluidas, leyendo la
  especificación del lenguaje como el sistema de partida. El detalle está en el
  punto 3.3, y las seis lecciones ya están escritas así.
- ~~**Pasar el registro de `humanizer` por todo el texto generado por IA.**~~
  **Terminado el 15-09-2026.** Las 51 lecciones leídas párrafo a párrafo:
  6 de Python, 2 de ML, 25 de Estadística y 18 de Álgebra. Unos 120 párrafos
  reescritos en total. Los patrones que más aparecían, en orden de frecuencia:

  1. **Cierres de una línea que resumen sin añadir**: «Ese es el método
     completo», «Ahí está el problema», «Esa es la trampa», «Eso es todo lo que
     hay detrás». Se cortan o se funden con el párrafo.
  2. **Defensas contra una objeción que nadie plantea**: «no es un tecnicismo»,
     «no es casualidad», «no es decorativo», «no es un acto de fe», «no es una
     curiosidad de laboratorio». Se sustituyen por la razón directa.
  3. **Superlativos sin respaldo**: «el error más común», «la operación más
     común de toda la estadística descriptiva» (era centrar un vector), «la que
     más importa». Se cambian por la afirmación que sí se puede sostener.
  4. **Dichos que suenan profundos**: «lo que realmente importa», «quita todo el
     misterio», «la clave es», «convierte la estadística en geometría».

  Tres cosas que el barrido dejó decididas y conviene no rehacer:

  - **El vocabulario ya estaba limpio.** Un barrido de 27 palabras infladas
    (*crucial*, *fundamental*, *robusto*, *panorama*, *piedra angular*…) sobre
    las 51 lecciones da 10 aciertos y los 10 son usos técnicos legítimos
    (teorema fundamental del cálculo, sección *Robustness* de Think Stats,
    errores estándar robustos). No hay nada que corregir ahí.
  - **Las rayas largas de la bibliografía se quedan.** En las listas de
    `::: {.fuentes}`, el ` — ` separa la cita de su nota y es convención
    bibliográfica, no conector de prosa. Son unas 25, iguales en las 51
    lecciones.
  - **Quedan ~30 rayas largas dentro de las cadenas JS de los visuales.** Ese
    texto se muestra al lector aunque viva en un bloque de código, así que le
    aplica la misma regla. No se tocó en esta pasada porque cada cambio obliga
    a repasar `visuales.py`; es trabajo pendiente y acotado.

  El barrido encontró además cuatro defectos heredados que no eran de registro:
  **cuatro rayas largas huérfanas** (Est 14 dos veces, Est 16, Álgebra 04:
  quedaba el cierre del inciso sin la apertura, sobras de la conversión de
  guiones), **dos puntos dobles** (Est 13, Álgebra 05) y **una frase duplicada**
  en Est 08 («El máximo de $\ell$ está donde está», dos veces seguidas). Ya no
  queda ninguna raya impar en prosa en todo el sitio; se comprueba con un
  conteo de paridad por línea.
- **Regla 14 contra el §1 del catálogo, sin resolver.** `CLAUDE.md` permite
  «no X **sino** Y» a propósito, por precisión matemática; el catálogo de la
  skill lo prohíbe entero. En esta pasada **mandó la regla del repo**: se
  reescribió «no es X: es Y» y se dejó «no es X sino Y». Si Luis prefiere lo
  contrario, hay unas 40 construcciones con *sino* que revisar.
- **`GOLPE` de `formato.py` solo mira el verbo *ser*.** Su regex acepta
  `es|son|era|fue|fueron`, así que «no **está** fallando: **está** diciendo»
  pasa el gate. Encontrado al escribir Python 01; sin decidir si se amplía.
- **Los 357 rótulos en negrita (§19 del catálogo) se quedan.** Marcan estructura
  que `formato.py` verifica, no decoración. Recomendado mantenerlos.
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
- **El cuaderno de retos: CERRADO el 18-09-2026.** Llegó a faltar en **33** de las
  68 lecciones publicadas —Python 5, Matemática 8 a 18, Estadística 6 a 16 y 18 a
  25, y ML 1 y 2—, y llevaba días sin bajar porque cada tanda solo escribía la
  suya.

  **Se cerró sin inventar nada.** Cada lección ya llevaba sus tres retos escritos
  en su bloque `## Reto`; lo que faltaba era trasladarlos al cuaderno. De ahí
  **`proyectos/genera_retos.py`**, que lee el bloque de cada lección y escribe la
  sección con el molde de las que ya existían: encabezado, un título y una celda
  por reto, y el cierre «Qué me costó / qué aprendí». **Es idempotente**: las
  secciones que ya están no se vuelven a añadir.

  Al pasar el texto de la lección a una celda de código hubo que traducir el
  LaTeX, y ahí estuvo el trabajo real: quitar las barras a secas dejaba `dots`,
  `ge`, `bar{X}_n` y `A^top A`, que no se leen. El script mapea griegas y
  operadores a su carácter —`\sigma`→σ, `\top`→ᵀ, `\ge`→≥— y convierte los
  acentos en palabra: `\bar{X}`→«X barra», `\hat{p}`→«p gorro». Quedan cero
  residuos, comprobado con un barrido sobre los tres cuadernos.

  **Al publicar una lección nueva, correrlo:**

  ```sh
  python3 proyectos/genera_retos.py            # informe: que falta
  python3 proyectos/genera_retos.py --escribe  # lo escribe
  ```



- **Colisiones de símbolos: RESUELTAS el 18-09-2026.** La auditoría del 12-09
  quedaba pendiente de decidir; se decidió y se aplicó, y la regla está ahora en
  `CLAUDE.md` como **21b**.

  **Lo que se encontró al mirarlo de verdad era peor que lo auditado.** `T` estaba
  registrado como «variable con distribución t de Student» y se enganchaba a los
  **67** superíndices de transpuesta de `matematica/06`, porque `A^{\mathsf{T}}A`
  renderiza una `T` que KaTeX pone en su propio span. `B` decía «número de
  remuestreos bootstrap» y se enganchaba a sucesos de probabilidad en Est 03, a
  matrices en Álgebra, y a $\lVert\beta\rVert^2$ en ML 08.

  **Lo que se hizo:**

  1. **Fuera del glosario global `T`, `Q` y `B`**, que afirmaban un único
     significado falso en otras lecciones. Las tres lecciones que los introducen
     —Est 09, Est 08 y Est 11— los declaran en su tabla de notación, así que no se
     perdió nada. Comprobado en el navegador: en `matematica/06` y
     `estadistica/10` el enganche de los tres pasa a **cero**.
  2. **`p`, `α`, `β`, `δ`, `θ` y `ε` se quedan, con la definición reescrita.** No
     mentían —enumeraban sentidos— pero enumeraban **de menos** y se presentaban
     como completas: `α` mencionaba 3 de los 8 sentidos que se usan, y `β` 2 de
     13. Ahora dicen que el símbolo está sobrecargado, dan los sentidos frecuentes
     y rematan con **«la tabla de notación de la lección manda»**. A `p` se le
     añadieron los dos sentidos que le faltaban, incluido el valor p, que la
     lección 10 insiste en que **no** es una probabilidad mientras el tooltip decía
     que sí.
  3. **`verificar/simbolos.py`**, que audita la regla 21b: lista, por símbolo, qué
     lecciones lo usan en fórmula y cuáles lo declaran en su notación. Busca tanto
     el carácter como su nombre de LaTeX, porque en los `.qmd` las griegas se
     escriben `\alpha` y no `α`; sin eso el recuento salía cero y parecía que
     nadie las usaba. **No es un gate**: es la herramienta para decidir.

- **Los símbolos sin declarar: CERRADO el 18-09-2026.** La herramienta destapó
  que los símbolos se usaban mucho más de lo que se declaraban: **139 pares
  (lección, símbolo)** en 55 de las 68 lecciones. Luis decidió rellenarlos, y se
  rellenaron: **106 filas nuevas** en las tablas `::: {.notacion}` de 41
  lecciones, escritas una a una con el contexto de cada uso a la vista.

  **No había un significado por defecto, y por eso no se pudo automatizar.** `z`
  es el cuantil de la normal en Estadística 06, un vector genérico en Álgebra 15,
  la fila del diseño en ML 06, el error de estimación en ML 08 y el argumento de
  la función Gamma en Estadística 20. `λ` es una tasa, un eigenvalor o una
  penalización según el módulo. Cada fila se escribió mirando la fórmula.

  **Dos cosas que aparecieron por el camino y conviene no volver a tropezar con
  ellas:**

  1. **La constante $\pi$ no es notación de nadie.** El $2\pi$ de la densidad
     normal no hay que declararlo. La herramienta solo cuenta $\pi$ cuando actúa
     como función —$\pi(\theta)$, la densidad del prior—, que sí es notación.
  2. **`Σ` tenía la misma enfermedad que `T`, `Q` y `B`.** La entrada decía
     «símbolo de suma», y el tooltip se engancha igual sobre `\Sigma`, que en
     Estadística 12 y 23 y en cuatro lecciones de Álgebra es la **matriz de
     covarianzas**. Reescrita al molde de la regla 21b: los dos sentidos y «la
     tabla de notación de la lección manda».

  **Un fallo del propio auditor**, que costó una pasada de más: la frontera `\b`
  no separa de `_`, así que `$\sigma_i$` no contaba como declarado y salían
  falsos positivos. Se cambió por `(?![A-Za-z])`. Si alguien vuelve a escribir un
  detector de símbolos, ese es el detalle.

  Para comprobar el estado en cualquier momento:

  ```sh
  python3 verificar/simbolos.py          # todos los del glosario
  python3 verificar/simbolos.py α β θ    # los que se quieran
  ```
