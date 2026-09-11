# scratch

Tus implementaciones desde cero, en NumPy puro. Un módulo por algoritmo.

Regla: cada implementación viene con un test que la compara contra la
librería de referencia (scikit-learn, statsmodels) y falla si difiere
más de 1e-6.

```bash
uv run pytest scratch/
```

Al final de la Fase 2 esto debe tener ~18 algoritmos.
