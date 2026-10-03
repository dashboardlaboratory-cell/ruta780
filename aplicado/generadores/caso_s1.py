"""Caso de Series de tiempo. Llamadas por hora a tres colas de un centro de
atención durante dos años, y las cuatro semanas siguientes sin llamadas."""
import numpy as np
import pandas as pd

MODULO = "series"

FERIADOS = ["01-01", "05-01", "09-15", "11-02", "12-25"]


def genera(semilla=2611):
    rng = np.random.default_rng(semilla)
    horas = pd.date_range("2024-01-01 00:00", "2026-01-28 23:00", freq="h")
    h = horas.hour.to_numpy()
    dow = horas.dayofweek.to_numpy()
    dia = (horas.normalize() - horas[0].normalize()).days.to_numpy()
    md = horas.strftime("%m-%d")
    feriado = np.isin(md, FERIADOS).astype(int)

    # perfil diario: casi nada de madrugada, picos a media mañana y a primera tarde
    perfil = (0.03 + np.exp(-0.5 * ((h - 10.5) / 2.0) ** 2)
              + 0.8 * np.exp(-0.5 * ((h - 15.5) / 2.2) ** 2))
    semana = np.where(dow < 5, 1.0, np.where(dow == 5, 0.55, 0.30))
    anual = 1 + 0.12 * np.cos(2 * np.pi * (dia - 15) / 365.25)   # mas en enero
    efecto_feriado = np.where(feriado == 1, 0.30, 1.0)

    colas = {"ventas": 22.0, "soporte": 30.0, "cobros": 12.0}
    filas = []
    for cola, base in colas.items():
        tendencia = 1 + 0.0004 * dia
        nivel = np.ones(len(horas))
        if cola == "soporte":
            # lanzamiento de un producto: desde el 2 de junio de 2025, un 40 % mas
            nivel = np.where(horas >= pd.Timestamp("2025-06-02"), 1.40, 1.0)
        mu = base * perfil * semana * anual * efecto_feriado * tendencia * nivel
        # sobredispersion: Poisson con media gamma
        llamadas = rng.poisson(mu * rng.gamma(20.0, 1 / 20.0, len(mu)))
        filas.append(pd.DataFrame({"fecha_hora": horas, "cola": cola, "feriado": feriado,
                                   "llamadas": llamadas, "_mu": mu}))
    t = pd.concat(filas, ignore_index=True)
    corte = pd.Timestamp("2026-01-01 00:00")
    historia = t[t["fecha_hora"] < corte].reset_index(drop=True)
    futuro = t[t["fecha_hora"] >= corte].reset_index(drop=True)
    futuro = futuro.rename(columns={"llamadas": "_llamadas"})
    for d in (historia, futuro):
        d["fecha_hora"] = d["fecha_hora"].dt.strftime("%Y-%m-%d %H:%M")
    return {"llamadas_historia": historia, "llamadas_futuro": futuro}
