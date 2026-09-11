#!/usr/bin/env python3
"""Genera grafo/grafo.json a partir de las lecciones (.qmd) y las notas del vault (.md).

Nodos:  lecciones de los modulos + notas de brain/
Aristas: prereq -> leccion, leccion -> siguiente, nota -> nota ([[wikilink]]),
         nota -> leccion (frontmatter `leccion:`)

Solo stdlib: corre en cualquier runner sin instalar nada.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODULOS = ["python", "matematica", "estadistica", "ml", "causal"]
VAULT = RAIZ / "brain"
SALIDA = Path(__file__).resolve().parent / "grafo.json"

RE_FM = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
RE_WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def leer_frontmatter(texto: str) -> dict:
    """Parser minimo de YAML frontmatter: escalares, listas inline y listas con guion."""
    m = RE_FM.match(texto)
    if not m:
        return {}
    datos: dict = {}
    clave_lista: str | None = None
    for linea in m.group(1).splitlines():
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        if clave_lista and linea.lstrip().startswith("- "):
            datos[clave_lista].append(linea.lstrip()[2:].strip().strip("\"'"))
            continue
        clave_lista = None
        if ":" not in linea or linea.startswith((" ", "\t")):
            continue
        clave, _, valor = linea.partition(":")
        clave, valor = clave.strip(), valor.strip()
        if not valor:
            datos[clave] = []
            clave_lista = clave
        elif valor.startswith("[") and valor.endswith("]"):
            cuerpo = valor[1:-1].strip()
            datos[clave] = [v.strip().strip("\"'") for v in cuerpo.split(",") if v.strip()]
        else:
            datos[clave] = valor.strip("\"'")
    return datos


def como_lista(valor) -> list[str]:
    if valor is None:
        return []
    if isinstance(valor, list):
        return [str(v) for v in valor if str(v).strip()]
    return [str(valor)] if str(valor).strip() else []


def construir() -> dict:
    nodos: dict[str, dict] = {}
    aristas: list[dict] = []
    vistos: set[tuple[str, str, str]] = set()

    def arista(origen: str, destino: str, tipo: str) -> None:
        clave = (origen, destino, tipo)
        if origen != destino and clave not in vistos:
            vistos.add(clave)
            aristas.append({"source": origen, "target": destino, "tipo": tipo})

    # --- lecciones ---
    for modulo in MODULOS:
        for ruta in sorted((RAIZ / modulo).glob("*.qmd")):
            if ruta.stem == "index":
                continue
            fm = leer_frontmatter(ruta.read_text(encoding="utf-8"))
            ident = f"{modulo}/{ruta.stem}"
            nodos[ident] = {
                "id": ident,
                "label": fm.get("title", ruta.stem),
                "tipo": "leccion",
                "modulo": modulo,
                "nivel": fm.get("nivel", "L1"),
                "url": f"{modulo}/{ruta.stem}.html",
            }
            for prereq in como_lista(fm.get("prereqs")):
                arista(prereq, ident, "prereq")
            for siguiente in como_lista(fm.get("siguientes")):
                arista(ident, siguiente, "prereq")

    # --- notas del vault ---
    if VAULT.is_dir():
        for ruta in sorted(VAULT.rglob("*.md")):
            if ruta.name.startswith("_") or ruta.name == "README.md" or "_templates" in ruta.parts:
                continue
            texto = ruta.read_text(encoding="utf-8")
            fm = leer_frontmatter(texto)
            ident = f"nota/{ruta.stem}"
            nodos[ident] = {
                "id": ident,
                "label": fm.get("name", ruta.stem),
                "tipo": "nota",
                "modulo": fm.get("modulo", "brain"),
                "nivel": fm.get("nivel", ""),
                "url": "",
            }
            cuerpo = RE_FM.sub("", texto)
            for destino in RE_WIKILINK.findall(cuerpo):
                arista(ident, f"nota/{destino.strip()}", "enlace")
            for leccion in como_lista(fm.get("leccion")):
                arista(ident, leccion, "cubre")

    # nodos referenciados que aun no existen: se dibujan como pendientes
    for a in aristas:
        for extremo in (a["source"], a["target"]):
            if extremo not in nodos:
                nodos[extremo] = {
                    "id": extremo,
                    "label": extremo.split("/")[-1],
                    "tipo": "pendiente",
                    "modulo": extremo.split("/")[0],
                    "nivel": "",
                    "url": "",
                }

    return {"nodes": list(nodos.values()), "links": aristas}


if __name__ == "__main__":
    grafo = construir()
    SALIDA.write_text(json.dumps(grafo, ensure_ascii=False, indent=2), encoding="utf-8")
    n_lec = sum(1 for n in grafo["nodes"] if n["tipo"] == "leccion")
    n_nota = sum(1 for n in grafo["nodes"] if n["tipo"] == "nota")
    print(f"grafo.json: {len(grafo['nodes'])} nodos ({n_lec} lecciones, {n_nota} notas), {len(grafo['links'])} aristas")
