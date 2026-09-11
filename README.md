# Ruta 780

Plataforma de aprendizaje de Python, matemática y machine learning.
780 horas en 78 semanas, 2 h al día de lunes a viernes.

**Sitio:** https://dashboardlaboratory-cell.github.io/ruta780/

## Qué es

Tres capas en un solo repositorio:

- **Plataforma** — lecciones con derivación paso a paso, visuales interactivos y
  ejercicios de Python que se ejecutan en el navegador (Pyodide, sin servidor).
- **Proyectos** — `scratch/` con implementaciones desde cero en NumPy y
  `proyectos/` con los notebooks.
- **Cerebro** — `brain/`, un vault de Obsidian versionado junto con todo lo demás.

## Escalera de profundidad

Cada lección declara su nivel en el frontmatter:

| Nivel | Significa |
|---|---|
| L1 | Intuición: visual interactivo, cero fórmula |
| L2 | Derivación a mano, paso a paso |
| L3 | Implementado desde cero en NumPy, empatando con la librería |
| L4 | Producción: librería, diagnósticos, supuestos, modos de falla |

**Regla:** ningún algoritmo del núcleo se usa antes de derivarlo e implementarlo.

## Desarrollo local

El sitio se construye solo en GitHub Actions con cada push a `main`.
Para previsualizar en local hace falta [Quarto](https://quarto.org/docs/get-started/):

```bash
quarto add r-wasm/quarto-live      # solo la primera vez
python3 grafo/build_graph.py       # regenera el grafo de conocimiento
quarto preview
```

Entorno de Python para los notebooks y los tests:

```bash
uv sync
uv run pytest scratch/
```

## Publicar un cambio

```bash
git add -A
git commit -m "qué cambió"
git push
```

## Agregar una lección

1. Copia `_templates/leccion.qmd` al módulo que corresponda.
2. Llena el frontmatter: `nivel`, `modulo`, `fase`, `prereqs`, `siguientes`.
3. Agrégala a la barra lateral en `_quarto.yml`.
4. Push. El grafo se regenera solo en el build.

## Datos

Ningún dato real de CBTL entra a este repositorio: es público. Los proyectos
usan datos públicos o sintéticos que imitan la estructura real.
