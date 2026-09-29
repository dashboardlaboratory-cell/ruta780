"""Caso 3. Préstamos personales concedidos y su resultado a doce meses."""
import numpy as np
import pandas as pd


def genera(semilla=932, n=6000):
    rng = np.random.default_rng(semilla)
    edad = np.clip(rng.normal(38, 11, n), 19, 75).round()
    ingreso = np.exp(rng.normal(np.log(1500), 0.5, n)).round(-1)
    antig = np.clip(rng.gamma(2.0, 2.5, n) * (edad - 18) / 20, 0, 40).round(1)
    monto = (np.exp(rng.normal(np.log(4000), 0.6, n)) / 100).round() * 100
    plazo = rng.choice([12, 24, 36, 48], n, p=[0.2, 0.35, 0.3, 0.15])
    cuota = monto * (0.015 + 1 / plazo)
    deuda = np.exp(rng.normal(np.log(2500), 0.9, n)).round(-1)
    consultas = rng.poisson(1.2, n)
    atrasos = rng.poisson(0.35, n)
    vivienda = rng.choice(["propia", "alquilada", "familiar"], n, p=[0.35, 0.45, 0.2])
    z = (-3.3 + 1.6 * np.log(cuota / ingreso + 0.05) / 1.0 + 0.5 * np.log1p(deuda / ingreso)
         + 0.25 * consultas + 0.55 * atrasos - 0.03 * (antig - 5)
         + np.where(vivienda == "propia", -0.4, 0.0) - 0.012 * (edad - 38) + 2.0)
    p = 1 / (1 + np.exp(-z))
    impago = (rng.random(n) < p).astype(int)
    t = pd.DataFrame({"id": np.arange(1, n + 1), "edad": edad, "ingreso_mensual": ingreso,
                      "antiguedad_empleo": antig, "monto": monto, "plazo_meses": plazo,
                      "deuda_total": deuda, "consultas_6m": consultas, "atrasos_previos": atrasos,
                      "vivienda": vivienda, "impago": impago})
    # 1. el ingreso no declarado falta mas entre quienes luego no pagan
    falta = rng.random(n) < np.where(impago == 1, 0.30, 0.08)
    t.loc[falta, "ingreso_mensual"] = np.nan
    # 2. un lote de deudas se cargo en milesimas de la moneda
    malas = rng.choice(n, 45, replace=False)
    t.loc[malas, "deuda_total"] = t.loc[malas, "deuda_total"] * 1000
    t["_p"] = p
    t["_deuda_erronea"] = np.isin(np.arange(n), malas)
    return {"credito_prestamos": t}
