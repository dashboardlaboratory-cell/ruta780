# Estado de Ruta 780 y qué sigue

Última actualización: **17-09-2026**, tras publicar cuatro lecciones: **ML 7**
(selección de subconjuntos, ISLP §6.1), **ML 8** (encogimiento, ridge y lasso,
ISLP §6.2), **Python 10** (carga, formatos y limpieza, McKinney §6.1 y §7.1–7.4)
y **Python 11** (wrangling, uniones y reshape, McKinney §8). **Las 62 publicadas
cumplen el molde: 62 de 62, y no queda ninguna en el molde viejo.**

Eso es una afirmación sobre el **molde**, no sobre el plan. **Estadística queda cerrada en 25 de 25.** Del
plan siguen faltando lecciones por escribir en los demás módulos: Python tiene
16 planeadas y 11 publicadas, ML 8 de 90, y Series y Causal están vacíos. El
detalle está en la tabla del punto 2.

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
| Python | 11 | 16 | **11 de 11** | 12 a 16, la Fase 1 |
| Series de tiempo | 0 | 11 | — | todas |
| Machine Learning | 8 | 90 | **8 de 8** | 09 a 19 de la Fase 2, y el resto |
| Inferencia causal | 0 | 14 | — | todas |

Los totales planeados salen de `data-total` en `index.qmd`, y las publicadas de
`data-ids`; el descuadre entre ambos es lo que mide la barra de progreso, así que
**no es un error**.

- **62 lecciones** publicadas, **62** cumplen el molde nuevo: cero pendientes de
  reescritura. Pendientes de **escribir** quedan 116 según el plan.
- **El capítulo 4 de ISLP quedó desglosado en tres lecciones** el 15-09-2026, con
  el método acordado de decidirlo justo antes de escribir: **03** regresión
  logística (§4.1–4.3, publicada), **04** modelos generativos (§4.4) y **05**
  modelos lineales generalizados (§4.6). El índice del módulo se renumeró hasta
  la 16.
- **`C=np.inf`, no `penalty=None`.** Es la única forma de apagar la penalización
  de `LogisticRegression` que aceptan a la vez el scikit-learn 0.24 de la máquina
  de trabajo y el 1.9 del CI; `penalty=None` no existe en el primero y está
  deprecado en el segundo. Anotado porque volverá a hacer falta en ML 04 y 05.
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
- **133 visuales** auditados por `visuales.py`; ningún fallo de la regla 19b.
  Siguen los mismos cuatro avisos, todos anteriores: tres de no idempotencia
  —Est 03, Est 22 y Mat 10— y uno que conviene mirar, `ml/03` visual 1,
  control `sp-i`: sus marcadores se mueven 0,3 px, que es justo el síntoma que
  la regla 19b persigue. Los seis visuales de esta tanda no añaden ninguno.
- **1228 afirmaciones numéricas** declaradas en `verificar/afirmaciones.json`,
  sobre **325 celdas** que el gate ejecuta en cada build.
- Glosario: **299 términos + 43 símbolos**. Las **34 entradas** de estas dos
  tandas —12 de ML 7, 8 de Python 10, 7 de ML 8 y 7 de Python 11— son todas de
  tipo `termino`: **cero símbolos
  globales nuevos**, por la regla aclarada en el punto 6. Los símbolos propios
  de cada lección se declaran en su tabla `::: {.notacion}` y no salen de ahí.
- Índices verificados: Think Stats 3e (75 secciones), MML (80), **Think Bayes 2e
  (20 capítulos y 193 secciones, traídas enteras el 12-09-2026; el capítulo 19
  publica las suyas sin numerar)**, McKinney 3E (capítulos + las secciones de los
  capítulos 6, 7 y 8; las subsecciones del 6 y del 8 no llevan número en el sitio
  publicado, así que no se registran ni se citan) e **ISLP (13 capítulos, 81 secciones N.M y 176 sub-subsecciones N.M.K —257 entradas— traídas el 13-09-2026 de los
  marcadores del PDF oficial)**. Desde esa fecha `citas.py` admite **tres niveles**: se puede citar
  `ISLP §10.7.1 Backpropagation`. La función `rango()` se generalizó a cualquier profundidad, porque la anterior
  desempaquetaba dos valores del `split` y reventaba con el tercer nivel; se comprobó que los casos de dos niveles
  siguen expandiéndose igual.

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

   `ml/index.qmd` enumera **33 filas**, de las que 14 se reparten los 13
   capítulos de ISLP. Pero `data-total` del plan dice **90**. Faltan 57 filas
   por escribir en el índice, y ese número no es casual: ISLP tiene exactamente
   **57 secciones sustantivas de nivel N.M**. A razón de una lección por
   sección —que es el ritmo real de las lecciones ya escritas, que citan una o
   dos secciones cada una— ISLP pide unas 57, y con las 33 listadas salen las
   90. Quien escribió el plan ya había hecho la cuenta: **las 14 filas son el
   esqueleto, un título por capítulo, pendiente de desglosar.**

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

3. **Series de tiempo e Inferencia causal** están vacías en el sidebar.
   **ML ya no tiene bloqueo de citación**: el índice de ISLP se completó el
   13-09-2026 con sus 81 secciones, así que se puede citar `§4.3 Logistic
   Regression` y no solo el capítulo. Causal sigue necesitando *Causal Inference
   for the Brave and True*, que no está verificado y por tanto no es citable.
4. **Fase 2**: traer los índices de ESL y fast.ai antes de citarlos.

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
- **Al cuaderno de retos le faltan 33 secciones, no diez.** Las lecciones
  cierran con «en `proyectos/notebooks/FN-retos.ipynb`, sección **X N**», y esa
  sección no existe en 33 de las 60 publicadas: Python 5, Matemática 8 a 18,
  Estadística 6 a 16 y 18 a 25, y ML 1 y 2. O se escriben —tres retos por
  lección, como las que ya están—, o se quita la referencia del bloque *Reto*.
  **Sin decidir**, y es la deuda más grande que queda. Cada tanda nueva sí
  escribe la suya, así que la deuda no crece: en esta se añadieron **ML 7** y
  **Python 10**. El recuento exacto se saca con el script del punto 3.4.1.

  Al añadirlas apareció además una trampa de etiqueta: los cuadernos titulan sus
  secciones **`## Python 10`** y **`## ML 7`**, mientras que algunas lecciones
  las citan como «sección **Py 10**». La abreviatura no casa con el título, así
  que **se escribe el nombre completo del módulo** en las dos partes.

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
