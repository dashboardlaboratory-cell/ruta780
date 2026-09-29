"""Caso 5. Dos cohortes de clientes que financiaron un teléfono a 24 meses.

La cohorte de 2023 trae el mes de impago. La de 2024 lo trae en la columna
oculta `_mes_impago`, que solo usa la verificación.
"""
import numpy as np
import pandas as pd


def _genera_todo(semilla=2410):
    """Dos cohortes de clientes que financiaron un telefono a 24 meses.
    La de 2023 trae el mes de impago; la de 2024 tambien, pero el caso solo
    la usa para el contraste final."""
    rng = np.random.default_rng(semilla)
    def cohorte(n, anio, desplaza):
        antig = np.minimum(rng.gamma(2.0, 9.0, n), 120).round()
        dias = np.clip(rng.normal(12, 5, n), 0, 40).round(1)
        desv = np.clip(rng.gamma(2.0, 2.2, n), 0, 25).round(1)
        digital = np.clip(rng.beta(2, 3, n) * 100, 0, 100).round(1)
        recarga = np.exp(rng.normal(np.log(9), 0.6, n)).round(2)
        canal = rng.choice(["presencial", "digital", "puerta a puerta"], n, p=[0.5, 0.3, 0.2])
        gama = rng.choice(["baja", "media", "alta"], n, p=[0.35, 0.45, 0.20])
        renov = (rng.random(n) < 0.25).astype(int)
        margen = np.exp(rng.normal(np.log(30), 0.35, n)).round(2)
        valor = np.where(gama == "alta", 900, np.where(gama == "media", 480, 250)) * np.exp(rng.normal(0, 0.12, n))
        subsidio = rng.choice([0.3, 0.5, 0.7], n)
        cuota = (valor * (1 - subsidio) / 24).round(2)
        z = (-4.4 + 0.07 * (dias - 12) + 0.10 * (desv - 4.4) - 0.012 * (digital - 40)
             - 0.015 * (np.minimum(antig, 48) - 18) - 0.6 * renov
             + np.where(canal == "puerta a puerta", 0.55, np.where(canal == "digital", -0.1, 0.0))
             + 0.35 * (gama == "alta") + desplaza)
        riesgo = 1 / (1 + np.exp(-z))                           # impago mensual
        u = rng.random(n)
        mes = np.ceil(np.log(1 - u) / np.log(1 - riesgo))        # mes del impago (geometrico)
        mes = np.where(mes <= 24, mes, np.nan)
        return pd.DataFrame({"cohorte": anio, "antiguedad_meses": antig, "dias_pago_medio": dias,
                             "desv_dias_pago": desv, "pago_digital_pct": digital,
                             "recarga_prepago_media": recarga, "canal": canal, "gama": gama,
                             "renovacion": renov, "margen_mensual": margen,
                             "valor_financiado": valor.round(2), "cuota_mensual": cuota,
                             "mes_impago": mes})
    t = pd.concat([cohorte(8000, 2023, 0.0), cohorte(8000, 2024, 0.15)], ignore_index=True)
    t.insert(0, "cliente", np.arange(100001, 100001 + len(t)))
    return t

def genera():
    t = _genera_todo()
    cartera = t[t["cohorte"] == 2023].reset_index(drop=True)
    solic = t[t["cohorte"] == 2024].reset_index(drop=True)
    solic = solic.rename(columns={"mes_impago": "_mes_impago"})
    return {"financiamiento_cartera": cartera, "financiamiento_solicitantes": solic}
