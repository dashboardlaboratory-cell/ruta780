"""Caso 9. Ventas semanales con el precio confundido por la estación y un experimento de precios."""
import numpy as np
import pandas as pd

PRECIOS = np.array([39.0, 44.0, 49.0, 54.0, 59.0, 64.0])
PESOS = {"nuevo_movil": 0.45, "nuevo_escritorio": 0.30, "recurrente": 0.25}


def conversion(precio, segmento, estacion=1.0):
    """Probabilidad de compra de un visitante; cada segmento tiene su sensibilidad."""
    a = {"nuevo_movil": 0.9, "nuevo_escritorio": 0.6, "recurrente": 0.2}[segmento]
    b = {"nuevo_movil": 0.075, "nuevo_escritorio": 0.055, "recurrente": 0.030}[segmento]
    z = a - b * (precio - 39.0) + np.log(estacion)
    return 0.12 / (1 + np.exp(-z)) * 2


def ganancia(precios, costo=18.0):
    """Ganancia esperada por cada 1000 visitantes con el comportamiento real."""
    return 1000 * sum(w * (precios[s] - costo) * conversion(precios[s], s) for s, w in PESOS.items())


def genera(semilla=909):
    rng = np.random.default_rng(semilla)
    segs = np.array(["nuevo_movil", "nuevo_escritorio", "recurrente"])
    pesos = np.array([0.45, 0.30, 0.25])
    # 1. histórico semanal: el equipo subía el precio cuando esperaba más demanda
    semanas = pd.date_range("2024-01-01", periods=104, freq="W-MON")
    est = 1 + 0.45 * np.sin(2 * np.pi * (np.arange(104) - 10) / 52) + rng.normal(0, 0.05, 104)
    precio_h = np.clip(49 + 14 * (est - 1) + rng.normal(0, 2, 104), 39, 64).round()
    visitas = rng.poisson(9000 * (0.8 + 0.4 * est))
    ventas = []
    for k in range(104):
        s = rng.choice(3, visitas[k], p=pesos)
        conv = np.array([conversion(precio_h[k], segs[j], est[k]) for j in range(3)])
        ventas.append(int((rng.random(visitas[k]) < conv[s]).sum()))
    hist = pd.DataFrame({"semana": semanas, "precio": precio_h, "visitas": visitas,
                         "ventas": ventas, "_estacion": est})
    # 2. experimento: cuatro semanas, precio al azar por visitante, estación neutra
    n = 60000
    s = rng.choice(3, n, p=pesos)
    p = rng.choice(PRECIOS, n)
    conv = np.array([conversion(p[i], segs[s[i]]) for i in range(n)])
    exp = pd.DataFrame({"visitante": np.arange(1, n + 1), "segmento": segs[s], "precio": p,
                        "compra": (rng.random(n) < conv).astype(int)})
    return {"precios_historico": hist, "precios_experimento": exp}
