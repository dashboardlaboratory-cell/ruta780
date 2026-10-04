"""Reasigna los índices de celda de afirmaciones.json tras mover o insertar celdas.

salidas.py identifica cada celda por su posición entre las celdas {pyodide} de
la lección. Al insertar ejercicios (regla 27) las posiciones cambian y las
afirmaciones apuntan a otra celda. Este script compara la lección con su
versión en git (HEAD, o la que se indique), empareja cada celda declarada por
su código exacto y reescribe las claves. Si una celda declarada cambió de
código o aparece dos veces, lo dice y no toca esa lección.

Uso:
    python3 verificar/reindexa.py ruta.qmd [ruta.qmd ...]
    python3 verificar/reindexa.py --desde abc123 ruta.qmd
"""
import json, pathlib, re, subprocess, sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CELDA = re.compile(r"```\{pyodide\}\n(.*?)\n```", re.S)
ARCH = RAIZ / "verificar" / "afirmaciones.json"


def main():
    args = sys.argv[1:]
    desde = "HEAD"
    if args[:1] == ["--desde"]:
        desde, args = args[1], args[2:]
    afirm = json.loads(ARCH.read_text(encoding="utf-8"))
    cambios = 0
    for a in args:
        p = (RAIZ / a).resolve() if not pathlib.Path(a).is_absolute() else pathlib.Path(a)
        rel = f"{p.parent.name}/{p.name}"
        if rel not in afirm:
            print(f"  {rel}: sin afirmaciones")
            continue
        viejo = subprocess.run(["git", "show", f"{desde}:{rel}"], cwd=RAIZ,
                               capture_output=True, text=True, check=True).stdout
        antes = CELDA.findall(viejo)
        ahora = CELDA.findall(p.read_text(encoding="utf-8"))
        nuevo, malos = {}, []
        for k, v in afirm[rel].items():
            codigo = antes[int(k)]
            sitios = [i for i, c in enumerate(ahora) if c == codigo]
            if len(sitios) != 1:
                malos.append(f"celda {k}: {len(sitios)} coincidencias")
                continue
            nuevo[str(sitios[0])] = v
        if malos:
            print(f"  {rel}: sin cambios, " + "; ".join(malos))
            continue
        if list(nuevo) != list(afirm[rel]):
            print(f"  {rel}: " + ", ".join(f"{k}->{n}" for k, n in zip(afirm[rel], nuevo) if k != n))
            afirm[rel] = nuevo
            cambios += 1
        else:
            print(f"  {rel}: índices sin cambios")
    if cambios:
        ARCH.write_text(json.dumps(afirm, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
