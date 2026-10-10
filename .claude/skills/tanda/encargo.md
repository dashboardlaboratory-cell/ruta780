# Encargo: <QUÉ SE CAMBIA> en lecciones de datasciencemap

<!-- Plantilla de la skill «tanda». Copiar al scratchpad, rellenar lo que va
entre <> y borrar los bloques que no apliquen. El texto de la regla 27
(04-10-2026) queda como ejemplo de cada sección. -->

Repositorio: `/Users/luispitty/curso phyton en linea/ruta780` (Quarto, lecciones
`.qmd` con celdas `{pyodide}` de quarto-live). Es la plataforma de estudio de
Luis; está en español y se escribe con el registro de un apunte universitario
frío.

## Lee primero (obligatorio)

1. `CLAUDE.md` entero, en particular las reglas **14b** (tono), **14c**
   (ejercicios), **15** (contexto prohibido: «ticket», «tienda», «sucursales»;
   usar «compra», «línea de compra», «caja»), **25** (entregables) y
   **<REGLA NUEVA>**, que es la que vas a aplicar.
2. Los pilotos ya convertidos, que son el modelo exacto a imitar:
   - `<ruta del piloto 1>` (<variante>)
   - `<ruta del piloto 2>` (<variante>)
   Mira con `git show <commit anterior>:<ruta>` cómo eran antes.

## Qué hacer en cada lección de tu lote

<Pasos numerados y concretos. Ejemplo de la regla 27:
1. Reglas en vez de proposiciones (y cuándo se conserva una proposición).
2. Examen de salida / problema inicial: dónde va, primera frase, qué puede usar.
3. Ejercicios intercalados: cuántos, dónde, título `### Ejercicio N.k, Nombre`.
4. Pieza del proyecto: dónde va, requisitos sin nombrar herramienta, entregable.
Actualizar todas las menciones dentro de la lección (Objetivo, Para el
Cerebro, Fuentes, textos de los visuales).>

## Comprobaciones: cómo escribirlas para que funcionen en el navegador

- quarto-live ejecuta la comprobación con una **copia** del espacio de nombres
  del ejercicio como globales, más `user_code` y `result`, y con **locales
  aparte**: nada de funciones auxiliares ni comprensiones en la comprobación
  que usen nombres definidos en ella. Bucles `for` simples.
- Para que no se acierte escribiendo el número a mano, la comprobación vuelve
  a ejecutar `user_code` con otros datos: `re.sub(r"(?m)^nombre\s*=.*$",
  "nombre = …", user_code)` y `exec(otro, ns)` dentro de
  `contextlib.redirect_stdout(io.StringIO())`. Los datos van en líneas
  `nombre = …` de una sola línea.
- Una respuesta natural distinta y correcta debe pasar; una errónea debe
  fallar con un mensaje que diga qué caso falla.
- Todo debe correr en **Pyodide 0.28**: sin hilos, procesos, red ni disco real
  (`sqlite3` y el sistema de archivos en memoria sí). Paquetes usados, en
  `pyodide: packages:` del frontmatter.
- En el navegador los enteros de NumPy son de 32 bits: si se imprimen pasos o
  bytes, `dtype=np.int64`.
- Si el hueco está en el cuerpo de un bucle, el bucle es
  `for _ in range(100):` con `if <fin>: break`, para que una respuesta errónea
  no cuelgue la pestaña.
- Imprimir solo valores nativos (int, float, bool, str): el CI usa numpy 2 y
  pandas 3, la máquina local numpy 1.24 y pandas 1.2.4.

## Gates que cada lección debe pasar (desde la raíz del repo)

```sh
python3 verificar/ejecuta.py <ruta.qmd>
/tmp/ci-venv/bin/python verificar/ejecuta.py <ruta.qmd>
python3 verificar/ejercicios.py <ruta.qmd>
python3 verificar/tono.py <ruta.qmd>
python3 verificar/estructura.py
python3 verificar/citas.py && python3 verificar/referencias.py && python3 verificar/retos.py
<VARIABLE>=<ruta.qmd> python3 verificar/formato.py --estricto
```

`formato.py` también prohíbe la segunda persona en la prosa. `salidas.py` va
a fallar si insertas celdas: **no edites `verificar/afirmaciones.json`**, se
reindexa al final emparejando por el código exacto. Por eso **no cambies el
código de ninguna celda existente**; si hace falta, dilo en el informe.

## Límites

- Edita **solo** las lecciones de tu lote. Si otra lección cita algo que
  cambiaste, anótalo en el informe y no la toques.
- No toques `afirmaciones.json`, `verificar/`, `CLAUDE.md`, `ESTADO.md`,
  `encabezado.html` ni `custom.scss`; no hagas commits ni `quarto render`.
- Verifica cada afirmación nueva ejecutándola (bordes, negativos, vacíos): los
  gates no comprueban que una frase sea verdadera.
- Tono: frases declarativas e impersonales, sin rayas (—), sin «no es X sino
  Y», sin intensificadores ni valorativos, sin negrita sobre frases.

## Entregables tuyos

1. Las lecciones convertidas, con todos los gates de arriba en 0.
2. Por lección, `<scratchpad>/alt/<modulo>-<NN>.json`:
   `{"ex_id": {"bien": ["celda completa correcta alternativa"], "mal": ["celda completa errónea plausible"]}}`,
   al menos un «mal» por ejercicio.
3. Un informe en `<scratchpad>/informes/<lote>.md` y como respuesta final:
   qué cambió por lección, citas en otras lecciones que haya que actualizar,
   celdas existentes que tocaste, y lo que no pudiste verificar.
