"""Caso 12. Transacciones con tarjeta con etiquetas de fraude incompletas."""
import numpy as np
import pandas as pd


def transacciones(semilla=1212):
    """70 días de transacciones con tarjeta. Solo se conoce si una transacción era
    fraude cuando se revisó: la regla anterior revisaba montos altos, más una
    auditoría al azar del 0,3 %."""
    rng = np.random.default_rng(semilla)
    n_dia = 6000
    filas = []
    for dia in range(70):
        n = n_dia
        monto = np.exp(rng.normal(np.log(45), 1.0, n)).round(2)
        hora = rng.integers(0, 24, n)
        rubro = rng.choice(["supermercado", "restaurante", "electronica", "viajes", "digital"], n, p=[0.35, 0.25, 0.12, 0.08, 0.20])
        pais_distinto = (rng.random(n) < 0.05).astype(int)
        dispositivo_nuevo = (rng.random(n) < 0.08).astype(int)
        compras_hora = rng.poisson(0.6, n)
        # dos tipos de fraude: montos altos con dispositivo nuevo o país distinto,
        # y pruebas de tarjeta: montos pequeños, de noche, muchas compras seguidas
        z1 = -7.2 + 0.9 * np.log(monto / 45) + 1.8 * dispositivo_nuevo + 1.5 * pais_distinto + 0.6 * (rubro == "electronica")
        z2 = -7.0 + 1.1 * compras_hora + 1.4 * ((hora <= 5)) + 1.2 * (monto < 15) + 0.8 * (rubro == "digital")
        p = 1 / (1 + np.exp(-z1)) + 1 / (1 + np.exp(-z2))
        fraude = (rng.random(n) < np.clip(p, 0, 1)).astype(int)
        monto = np.where((fraude == 1) & (1 / (1 + np.exp(-z2)) > 1 / (1 + np.exp(-z1))),
                         np.minimum(monto, rng.uniform(1, 14, n)).round(2), monto)
        filas.append(pd.DataFrame({"dia": dia + 1, "monto": monto, "hora": hora, "rubro": rubro,
                                   "pais_distinto": pais_distinto, "dispositivo_nuevo": dispositivo_nuevo,
                                   "compras_hora": compras_hora, "_fraude": fraude}))
    t = pd.concat(filas, ignore_index=True)
    t.insert(0, "transaccion", np.arange(1, len(t) + 1))
    auditoria = rng.random(len(t)) < 0.003
    t["auditoria"] = auditoria.astype(int)
    t["revisada"] = ((t["monto"] > 500) | auditoria).astype(int)
    t["fraude"] = np.where(t["revisada"] == 1, t["_fraude"], np.nan)
    return t


def genera():
    t = transacciones()
    historia = t[t["dia"] <= 60].reset_index(drop=True)
    nuevas = t[t["dia"] > 60].drop(columns=["auditoria", "revisada", "fraude"]).reset_index(drop=True)
    return {"fraude_historia": historia, "fraude_nuevas": nuevas}
