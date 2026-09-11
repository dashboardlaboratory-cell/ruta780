# Cerebro

Vault de Obsidian. Ábrelo con *Open folder as vault* apuntando a esta carpeta
(`ruta780/brain`), no al repo entero: así el grafo de Obsidian solo muestra tus
notas, no las lecciones.

## Estructura

| Carpeta | Qué va aquí |
|---|---|
| `00-Inbox/` | Capturas rápidas. Se vacía el viernes. |
| `10-Conceptos/` | Una nota atómica por concepto. |
| `20-Metodos/` | Algoritmos: qué, cuándo, supuestos, código, gotchas. |
| `30-Libros/` | Una nota por capítulo leído, con las 3 preguntas previas. |
| `40-Proyectos/` | Decisiones y bitácora de cada proyecto. |
| `50-Errores/` | Cada bug: síntoma, causa, fix, lección. |
| `90-MOCs/` | Mapas de contenido por fase y por tema. |

## Reglas

1. **Nada entra copiado.** Si no puedes explicarlo con tus palabras, no está aprendido.
2. **Toda nota termina con al menos 2 flashcards**, en formato `pregunta::respuesta`.
3. **Cada bug va a `50-Errores`** con su lección, no solo su fix.
4. **Viernes:** vaciar `00-Inbox` y actualizar el MOC de la fase.

## Plugins

- **Spaced Repetition** — activa FSRS en los ajustes. Lee las flashcards `pregunta::respuesta` de tus notas.
- **Dataview** — tabla de progreso por fase desde el frontmatter.
- **Templater** — las plantillas de `_templates/`.
- **Excalidraw** — diagramas de algoritmos a mano.

## Enlazar con las lecciones

En el frontmatter de una nota, el campo `leccion:` la conecta con la lección del
sitio en el grafo de conocimiento:

```yaml
---
name: descenso-de-gradiente
tipo: derivacion
modulo: matematica
leccion: [matematica/08-descenso-de-gradiente]
---
```

Los `[[wikilinks]]` entre notas también se convierten en aristas del grafo.
