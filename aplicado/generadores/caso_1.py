"""Caso 1. Encuesta sintética sobre una bicicleta eléctrica plegable."""
import numpy as np
import pandas as pd


def genera(semilla=780, n=1200):
    rng = np.random.default_rng(semilla)
    seg = rng.choice(4, n, p=[0.30, 0.20, 0.25, 0.25])
    def por_seg(valores):
        return np.array(valores)[seg]
    edad = np.clip(rng.normal(por_seg([32, 41, 21, 56]), por_seg([5, 6, 2.5, 7])), 18, 80).round()
    ingreso = np.exp(rng.normal(np.log(por_seg([2300, 3600, 700, 2600])), 0.3)).round(-1)
    distancia = np.clip(rng.gamma(4, por_seg([2.2, 3.0, 1.0, 6.5])), 0.3, 60).round(1)
    p_trans = {0: [0.10, 0.75, 0.10, 0.05], 1: [0.80, 0.10, 0.05, 0.05],
               2: [0.05, 0.25, 0.40, 0.30], 3: [0.85, 0.10, 0.02, 0.03]}
    modos = np.array(["coche", "bus_metro", "bicicleta", "a_pie"])
    transporte = np.array([rng.choice(modos, p=p_trans[s]) for s in seg])
    gasto_mov = np.where(transporte == "coche", 240, np.where(transporte == "bus_metro", 55, 12)) \
        * np.exp(rng.normal(0, 0.25, n))
    interes = np.clip(np.round(rng.normal(por_seg([4.1, 3.2, 4.3, 1.6]), 0.7)), 1, 5).astype(int)
    p_adop = por_seg([0.55, 0.45, 0.60, 0.10])
    adopcion = np.where(rng.random(n) < p_adop, "temprano", "tardio")
    usos = np.array(["trabajo", "ocio", "ambos", "ninguno"])
    p_uso = {0: [0.60, 0.10, 0.25, 0.05], 1: [0.10, 0.65, 0.20, 0.05],
             2: [0.35, 0.20, 0.40, 0.05], 3: [0.10, 0.15, 0.05, 0.70]}
    uso = np.array([rng.choice(usos, p=p_uso[s]) for s in seg])
    frecuencia = np.clip(rng.normal(14, 5, n), 1, 36).round()          # meses entre compras
    genero = rng.choice(["mujer", "hombre"], n)
    ciudad = rng.choice(["Norte", "Sur", "Este", "Oeste", "Centro", "Costa"], n)
    civil = np.where(rng.random(n) < 1 / (1 + np.exp(-(edad - 33) / 5)), "casado", "soltero")
    t = pd.DataFrame({
        "id": np.arange(1, n + 1), "edad": edad, "genero": genero, "estado_civil": civil,
        "ciudad": ciudad, "ingreso_mensual": ingreso, "distancia_km": distancia,
        "transporte": transporte, "gasto_movilidad_mensual": gasto_mov.round(2),
        "meses_entre_compras": frecuencia, "adopcion": adopcion, "interes": interes,
        "uso_previsto": uso})
    t["_segmento"] = seg
    return {"segmentacion_encuesta": t}

