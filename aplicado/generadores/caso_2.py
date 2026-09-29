"""Caso 2. Tres cohortes de alumnos (2021 a 2023) y los solicitantes de 2024."""
import numpy as np
import pandas as pd


def genera(semilla=483):
    rng = np.random.default_rng(semilla)
    filas = []
    for cohorte, n in ((2021, 300), (2022, 300), (2023, 300), (2024, 400)):
        a = rng.standard_normal(n)                    # capacidad, no observada
        e = rng.standard_normal(n)                    # esfuerzo durante el programa, no observado
        tipo = rng.choice(["comercio", "ingenieria", "ciencias", "artes"], n, p=[0.4, 0.3, 0.2, 0.1])
        exper = np.minimum(rng.poisson(1.6, n), 8)
        t = pd.DataFrame({
            "cohorte": cohorte,
            "nota_secundaria": np.clip(72 + 8 * a + rng.normal(0, 6, n), 45, 100).round(1),
            "nota_bachillerato": np.clip(70 + 7 * a + rng.normal(0, 7, n), 45, 100).round(1),
            "nota_grado": np.clip(66 + 6 * a + rng.normal(0, 7, n), 45, 100).round(1),
            "tipo_grado": tipo,
            "experiencia_anios": exper,
            "examen_percentil": np.clip(100 / (1 + np.exp(-(0.9 * a + rng.normal(0, 0.7, n)))), 1, 99).round(),
            "entrevista": np.clip(np.round(5.5 + 1.1 * a + rng.normal(0, 1.4, n)), 1, 10).astype(int),
        })
        z = (1.25 + 0.9 * a + 1.3 * e + 0.22 * np.minimum(exper, 4)
             + np.where(np.isin(tipo, ["comercio", "ingenieria"]), 0.35, 0.0)
             - 0.35 * (cohorte >= 2023))
        p = 1 / (1 + np.exp(-z))
        col = (rng.random(n) < p).astype(int)
        t["nota_final_programa"] = np.clip(68 + 4 * a + 6 * e + rng.normal(0, 3, n), 40, 100).round(1)
        t["especializacion"] = np.where(e + rng.normal(0, 0.8, n) > 0.3, "finanzas", "marketing")
        t["salario"] = np.where(col == 1, np.exp(rng.normal(np.log(2600) + 0.1 * a, 0.2, n)).round(-1), np.nan)
        t["colocado"] = col
        t["_p"] = p
        filas.append(t)
    t = pd.concat(filas, ignore_index=True)
    t.insert(0, "id", np.arange(1, len(t) + 1))
    hist = t[t["cohorte"] <= 2023].reset_index(drop=True)
    sol = t[t["cohorte"] == 2024].reset_index(drop=True)
    sol = sol.drop(columns=["nota_final_programa", "especializacion", "salario", "colocado"])
    return {"admisiones_historico": hist, "admisiones_solicitantes": sol}
