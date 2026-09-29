#!/usr/bin/env python3
"""Escribe los CSV de los casos sintéticos de ML aplicado (regla 26).

Cada `caso_N.py` de esta carpeta define `genera()`, que devuelve un diccionario
{nombre: DataFrame}. Las columnas cuyo nombre empieza por «_» son el mecanismo
que el caso pide descubrir (probabilidades, efectos, etiquetas reales): se usan
en la verificación y nunca se escriben en el CSV.

Los CSV no se guardan en el repositorio: se generan aquí antes de renderizar,
en local y en el CI, y Quarto los copia al sitio por el campo `resources:` de
cada caso.

Uso:
    python3 aplicado/generadores/generar.py
"""
import importlib
import os
import pathlib
import sys

CARPETA = pathlib.Path(__file__).resolve().parent
DATOS = CARPETA.parent / "datos"


def casos():
    sys.path.insert(0, str(CARPETA))
    for p in sorted(CARPETA.glob("caso_*.py")):
        yield p.stem, importlib.import_module(p.stem)


def main():
    DATOS.mkdir(exist_ok=True)
    for nombre, modulo in casos():
        for tabla, df in modulo.genera().items():
            visibles = [c for c in df.columns if not c.startswith("_")]
            ruta = DATOS / f"{tabla}.csv"
            # se escribe aparte y se renombra: otra ejecución que lea el CSV
            # a la vez nunca lo encuentra a medio escribir
            tmp = ruta.with_suffix(f".{os.getpid()}.tmp")
            df[visibles].to_csv(tmp, index=False)
            os.replace(tmp, ruta)
            print(f"{nombre}: {ruta.relative_to(CARPETA.parent.parent)} {df[visibles].shape}")


if __name__ == "__main__":
    main()
