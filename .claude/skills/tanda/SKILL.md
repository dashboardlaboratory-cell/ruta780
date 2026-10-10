---
name: tanda
description: Aplicar un cambio a muchas lecciones de datasciencemap de una vez — una revisión externa que trae Luis, un molde nuevo, una regla nueva o una corrección que toca un módulo entero. Valora la propuesta contra el repo, fija la regla, hace un piloto a mano, reparte el resto entre agentes en paralelo e integra con gates en tres entornos y un barrido en el Pyodide real antes de publicar. Usar cuando Luis pega una lista de propuestas o pide «aplica esto a los cursos de …».
---

# Tanda: un cambio aplicado a muchas lecciones

Flujo que se usó el 04-10-2026 para llevar la regla 27 a las 42 lecciones de
Fundamentos y Python (`ESTADO.md` §3.118). Cada fase existe porque algo falló
o estuvo a punto de fallar.

## 0. Antes de nada

Leer `CLAUDE.md` y la cabecera de `ESTADO.md`. Las reglas de tono (14b), de
ejercicios (14c), de contexto (15: «ticket», «tienda» y «sucursales» están
prohibidas) y de entregables (25) aplican a todo lo que se escriba.

## 1. Valorar la propuesta (sin tocar nada)

Si Luis pega una revisión sin instrucción, la respuesta es una valoración,
no un cambio:

- Comprobar en el repo cada afirmación de la revisión (`grep`, contar
  ejercicios, leer una lección). Las revisiones externas aciertan en el
  diagnóstico y se equivocan en el detalle: la del 04-10 decía que el home
  mencionaba una racha que «la lección no muestra»; lo cierto era que nada
  la medía.
- Señalar dónde choca con reglas propias (14, 25…) o entre sí: «reto
  primero» y «examen de salida» no pueden ser el mismo bloque.
- Dar el coste de cada punto (cuántos archivos, cuántas comprobaciones
  nuevas) y un orden: lo barato y de efecto inmediato primero.

Cuando Luis dice «aplícalo», se aplica el paquete recomendado. Solo se
pregunta si una decisión cambia horas de trabajo y no se deduce de lo dicho.

## 2. Fijar la regla

- Escribir la regla nueva en `CLAUDE.md` con fecha y origen, y acotar la
  regla vieja que sustituye («En Fundamentos y Python, el molde es el de la
  regla 27»).
- Hacer que un gate la compruebe. Patrón usado: un conjunto en
  `verificar/formato.py` con las lecciones migradas, ampliable sin editar el
  archivo con una variable de entorno (`REGLA27_EXTRA=ruta.qmd`), para que
  varios agentes lo usen a la vez sin pisarse. Al terminar, el conjunto pasa
  a cubrir el módulo entero.
- Si el cambio añade algo ejecutable, añadir un gate al CI
  (`.github/workflows/publish.yml`) y a la lista de `CLAUDE.md`.
- Si se renombra un tipo de bloque (`.proposicion` → `.regla`), actualizar
  `custom.scss`, la lista de etiquetas de `verificar/tono.py` y el script de
  anclas de `encabezado.html`, que enlaza «Etiqueta N.M».

## 3. Piloto a mano

Una lección por variante del molde (el 04-10: Fundamentos 2 con examen de
salida y Python 12 con problema inicial). El piloto es el modelo que copian
los agentes, así que se cuida más que el resto.

- Gates de la lección, `verificar/reindexa.py` si se insertaron celdas,
  `quarto render` de la lección y `verificar/pyodide.py` sobre ella.
- El piloto suele cambiar la regla: Python 12 tenía demostraciones
  algebraicas de verdad y la regla 27 pasó a conservarlas. Ajustar la regla
  antes de repartir.
- Commit y push del piloto y la infraestructura.

## 4. Repartir entre agentes

Copiar `encargo.md` (junto a este archivo) al scratchpad, rellenar sus
huecos y lanzar un agente `general-purpose` por lote, todos en el mismo
mensaje y en segundo plano. Lotes de 4 a 6 lecciones, como mucho 8 agentes.
Cada prompt de lote dice qué lecciones y qué peculiaridades tienen
(paquetes, cosas que no corren en Pyodide, citas conocidas a otras
lecciones).

Lo que el encargo prohíbe y por qué:

- Editar `afirmaciones.json`, `verificar/`, `CLAUDE.md` o lecciones de otro
  lote: los agentes trabajan a la vez en el mismo árbol.
- Cambiar el código de celdas existentes: `reindexa.py` empareja por código
  exacto. Los comentarios desfasados dentro de celdas se corrigen al final.
- `quarto render` y commits: renderizar a la vez pisa `_site/`.

Cada agente deja un informe y un JSON de respuestas alternativas por
lección (`<modulo>-<NN>.json`, con «bien» y «mal» por ejercicio) para el
barrido en el navegador.

## 5. Integrar

Con todos los lotes terminados:

1. `python3 verificar/reindexa.py <las lecciones>`: reasigna los índices de
   `afirmaciones.json` contra HEAD (el piloto ya está en HEAD).
2. Ampliar el conjunto del gate al módulo entero.
3. `python3 verificar/renombra_citas.py` (informe), revisar los casos
   dudosos por contexto y `--aplicar`. Cubre lecciones, entregables y
   cuadernos de retos, también comentarios de código. Las citas a otro
   módulo sin «de Fundamentos K» hay que corregirlas a mano.
4. Gates completos, y `salidas.py` y `ejecuta.py` también con
   `/tmp/ci-venv/bin/python` (pandas 3, numpy 2). Si el venv falla al
   importar, recrearlo (memoria `ruta780-ci-venv-tmp`).
5. Renderizar cada lección, una a una. En zsh una lista en una variable no
   se parte en palabras: usar `while read f; do quarto render "$f"; done < lista`.
6. `python3 verificar/pyodide.py --alt <dir> --paralelo 3 <lecciones>`
   fuera del sandbox. Más de 3 a la vez agota los tiempos de carga de
   Pyodide con NumPy. Un «blanco» en verde puede ser un hueco cuya
   respuesta correcta es 0: mirar antes de corregir.
7. `python3 verificar/visuales.py --estricto <lecciones>` fuera del sandbox.

Lo que solo apareció en el navegador el 04-10 y conviene buscar siempre:

- `np.arange` y `np.array` de enteros dan `int32` en Pyodide (wasm32).
  Cualquier celda que imprima `strides`, `itemsize` o `nbytes` necesita
  `dtype=np.int64`.
- Un `while` cuyo cuerpo es un hueco cuelga la pestaña si la respuesta no
  avanza. El tope tiene que ser independiente del hueco:
  `for _ in range(100):` con `if <fin>: break`. Un tope sobre el contador
  que escribe el alumno no sirve.

## 6. Publicar

- Entrada nueva en `ESTADO.md` §3 con cifras contadas (no estimadas), lo
  que encontró el barrido y las comprobaciones que quedaron flojas.
- Commit con la identidad de los anteriores en variables
  (`GIT_AUTHOR_NAME="luis pitty"`, email `luispitty@mbp-de-luis-2.home.lla.com`,
  y lo mismo para `GIT_COMMITTER_*`). No tocar la configuración global.
- `./subir` fuera del sandbox (necesita el llavero).
- No decir «publicado» sin ver el CI. Si no se puede consultar, decirlo
  arriba y explícito.

## Resumen para Luis

Tabla corta por módulo (qué cambió, cifras), lo que solo vio el navegador,
y una lista de lo que conviene que él decida o revise. Nada de «gates en
verde» como sinónimo de correcto (memoria `ruta780-gates-no-verifican-verdad`).
