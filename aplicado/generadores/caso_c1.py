"""Caso de Inferencia causal. Una membresia con envio gratis: datos
observacionales, donde cada cliente decide si se une, y un experimento con
una prueba gratuita asignada al azar."""
import numpy as np
import pandas as pd

MODULO = "causal"


def _clientes(rng, n):
    compras = rng.poisson(rng.gamma(2.0, 3.0, n))                 # compras del semestre previo
    ticket = np.exp(rng.normal(np.log(35), 0.4, n))                # importe medio por compra
    gasto_previo = (compras * ticket).round(2)
    antig = np.minimum(rng.gamma(2.0, 12.0, n), 96).round()        # meses como cliente
    region = rng.choice(["capital", "norte", "sur"], n, p=[0.5, 0.3, 0.2])
    movil = (rng.random(n) < 0.6).astype(int)
    return compras, ticket, gasto_previo, antig, region, movil


def _resultado(rng, compras, gasto_previo, antig, region, movil, d):
    base = 0.9 * gasto_previo + 1.5 * antig + 25 * movil + np.where(region == "capital", 40, 0)
    # efecto: el envio gratis sube el gasto de quien compra a menudo y casi
    # nada en quien compra poco; en el sur el envio ya era gratis
    tau = np.where(region == "sur", 5.0, 8.0 + 9.0 * np.minimum(compras, 12))
    y0 = np.maximum(base + rng.normal(0, 80, len(base)), 0)
    return y0, tau, y0 + d * tau


def genera(semilla=1607):
    rng = np.random.default_rng(semilla)
    # observacional
    n = 20000
    compras, ticket, gp, antig, region, movil = _clientes(rng, n)
    logit = -2.2 + 0.25 * compras + 0.01 * antig + 0.4 * movil
    d = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    y0, tau, y = _resultado(rng, compras, gp, antig, region, movil, d)
    # uso del envio gratis: solo existe con membresia y crece con el gasto (mediador)
    envios = np.where(d == 1, rng.poisson(0.04 * np.maximum(y, 0) + 0.5), 0)
    # encuesta de satisfaccion: responde mas quien es miembro y quien gasta mas (colisionador)
    resp = (rng.random(n) < 1 / (1 + np.exp(-(-3.0 + 1.5 * d + 0.012 * y)))).astype(int)
    obs = pd.DataFrame({"cliente": np.arange(1, n + 1), "compras_previas": compras,
                        "gasto_previo": gp, "antiguedad_meses": antig, "region": region,
                        "usa_movil": movil, "miembro": d, "envios_gratis_usados": envios,
                        "respondio_encuesta": resp, "gasto_6m": y.round(2),
                        "_tau": tau, "_y0": y0})
    # experimento: prueba gratuita de dos meses asignada al azar
    m = 4000
    compras, ticket, gp, antig, region, movil = _clientes(rng, m)
    z = (rng.random(m) < 0.5).astype(int)
    y0, tau, y = _resultado(rng, compras, gp, antig, region, movil, z)
    exp = pd.DataFrame({"cliente": np.arange(n + 1, n + m + 1), "compras_previas": compras,
                        "gasto_previo": gp, "antiguedad_meses": antig, "region": region,
                        "usa_movil": movil, "prueba_gratis": z, "gasto_6m": y.round(2),
                        "_tau": tau})
    return {"membresia_observacional": obs, "membresia_experimento": exp}
