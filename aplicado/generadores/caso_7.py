"""Caso 7. Un experimento con la oferta asignada al azar y un grupo nuevo de clientes."""
import numpy as np
import pandas as pd


def genera(semilla=707):
    rng = np.random.default_rng(semilla)

    def grupo(n, experimento):
        antig = np.minimum(rng.gamma(2.0, 14.0, n), 120).round()
        cargo = np.exp(rng.normal(np.log(45), 0.35, n)).round(2)
        uso = np.clip(rng.gamma(2.0, 1.5, n), 0.05, 20).round(2)
        contrato = rng.choice(["mensual", "anual"], n, p=[0.6, 0.4])
        reclamos = rng.poisson(0.5, n)
        competencia = (rng.random(n) < 0.3).astype(int)
        base = (-1.8 + 0.9 * (contrato == "mensual") - 0.012 * (antig - 28) + 0.7 * reclamos
                + 0.015 * (cargo - 45) - 0.12 * (uso - 3) + 0.4 * competencia)
        # efecto de la oferta en escala logit: ayuda a quien es sensible al precio y
        # tiene alternativa; perjudica a los antiguos que casi no usan el servicio
        # y no cambia nada en quien ya reclamó dos veces o más
        atento = reclamos < 2
        efecto = ((-1.0 * (contrato == "mensual") * (cargo > 45) - 0.7 * competencia) * atento
                  + 0.9 * ((antig > 36) & (uso < 2.0)))
        p0 = 1 / (1 + np.exp(-base))
        p1 = 1 / (1 + np.exp(-(base + efecto)))
        t = pd.DataFrame({"antiguedad_meses": antig, "cargo_mensual": cargo, "uso_gb_dia": uso,
                          "contrato": contrato, "reclamos_90d": reclamos,
                          "oferta_competencia": competencia})
        if experimento:
            ofe = (rng.random(n) < 0.5).astype(int)
            t["oferta"] = ofe
            t["abandono"] = (rng.random(n) < np.where(ofe == 1, p1, p0)).astype(int)
        t["_p0"], t["_p1"] = p0, p1
        return t

    exp = grupo(20000, True)
    nuevos = grupo(20000, False)
    exp.insert(0, "cliente", np.arange(1, 20001))
    nuevos.insert(0, "cliente", np.arange(20001, 40001))
    return {"retencion_experimento": exp, "retencion_nuevos": nuevos}
