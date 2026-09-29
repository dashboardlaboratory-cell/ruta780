"""Caso 4. Ventas diarias de una categoría en ocho supermercados, 2022 a 2024."""
import numpy as np
import pandas as pd


def genera(semilla=780):
    rng = np.random.default_rng(semilla)
    fechas = pd.date_range("2022-01-01", "2024-12-31", freq="D")
    n = len(fechas)
    dia = fechas.dayofweek.to_numpy()
    doy = fechas.dayofyear.to_numpy()
    t = np.arange(n) / 365.0
    semana = np.array([0.92, 0.88, 0.90, 0.95, 1.08, 1.25, 1.02])
    anual = 1 + 0.12 * np.cos(2 * np.pi * (doy - 350) / 365.25)
    feriados = pd.to_datetime(["2022-12-25", "2023-12-25", "2024-12-25",
                               "2022-01-01", "2023-01-01", "2024-01-01"])
    cerrado = np.isin(fechas, feriados)
    filas = []
    competidor = {3, 6}                               # abre un competidor cerca de estos dos
    inicio = fechas.get_loc(pd.Timestamp("2024-06-01"))
    for s in range(1, 9):
        nivel = rng.uniform(800, 2200)
        crec = rng.uniform(0.00, 0.06)
        promo = rng.random(n) < 0.08
        efecto = np.where(promo, 1.35, 1.0)
        caida = np.ones(n)
        if s in competidor:
            caida[inicio:] = 0.75
        mu = nivel * (1 + crec) ** t * semana[dia] * anual * efecto * caida
        v = np.round(mu * np.exp(rng.normal(0, 0.08, n)))
        v[cerrado] = 0
        filas.append(pd.DataFrame({"fecha": fechas, "supermercado": s, "promocion": promo.astype(int),
                                   "ventas": v}))
    d = pd.concat(filas, ignore_index=True)
    # dias con el sistema caido (ventas en cero) y cargas duplicadas (ventas dobles)
    idx = rng.choice(len(d), 30, replace=False)
    malos = []
    for k, i in enumerate(idx):
        if d.at[i, "ventas"] == 0:
            continue
        d.at[i, "ventas"] = 0 if k % 2 == 0 else 2 * d.at[i, "ventas"]
        malos.append(i)
    d["ventas"] = d["ventas"].astype(int)
    d["fecha"] = d["fecha"].dt.strftime("%Y-%m-%d")
    d["_anomalo"] = np.isin(np.arange(len(d)), malos)
    d["_competidor"] = d["supermercado"].isin(competidor)
    return {"demanda_ventas": d}
