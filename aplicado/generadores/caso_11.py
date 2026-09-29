"""Caso 11. Demanda diaria de un pan de masa madre en cinco puntos de venta.

Las ventas registradas son el mínimo entre la demanda y lo que se horneó."""
import numpy as np
import pandas as pd


def panaderia(semilla=1111):
    rng = np.random.default_rng(semilla)
    fechas = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    semana = np.array([0.85, 0.80, 0.85, 0.95, 1.15, 1.45, 1.20])
    filas = []
    for pv in range(1, 6):
        nivel = rng.uniform(40, 110)
        tend = rng.uniform(-0.05, 0.15)
        t = np.arange(len(fechas)) / 365
        mu = (nivel * (1 + tend) ** t * semana[fechas.dayofweek]
              * (1 + 0.08 * np.cos(2 * np.pi * (fechas.dayofyear - 20) / 365)))
        k = 8.0                                            # dispersión de la binomial negativa
        demanda = rng.negative_binomial(k, k / (k + mu))
        # la política anterior horneaba 1,15 veces la media de las ventas de las cuatro
        # semanas previas del mismo día de la semana, y al principio el nivel medio
        horneado = np.zeros(len(fechas), int)
        ventas = np.zeros(len(fechas), int)
        for i in range(len(fechas)):
            prev = [ventas[j] for j in (i - 7, i - 14, i - 21, i - 28) if j >= 0]
            horneado[i] = int(round(1.15 * np.mean(prev))) if len(prev) == 4 else int(round(mu[i]))
            ventas[i] = min(demanda[i], horneado[i])
        filas.append(pd.DataFrame({"fecha": fechas, "punto": pv, "horneado": horneado,
                                   "ventas": ventas, "_demanda": demanda, "_mu": mu}))
    return pd.concat(filas, ignore_index=True)


def genera():
    d = panaderia()
    historia = d[d["fecha"] < "2025-11-01"].reset_index(drop=True)
    futuro = d[d["fecha"] >= "2025-11-01"].reset_index(drop=True)
    # en el futuro solo se ve la fecha y el punto; lo horneado con la política
    # actual y la demanda quedan ocultos para la evaluación
    futuro = futuro.rename(columns={"horneado": "_horneado", "ventas": "_ventas"})
    return {"panaderia_historia": historia, "panaderia_futuro": futuro}
