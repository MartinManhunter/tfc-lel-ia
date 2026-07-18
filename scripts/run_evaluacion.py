"""Evalúa un LEL producido contra uno o más Gold Standards e imprime/guarda el reporte.
Uso:
    python scripts/run_evaluacion.py resultados/lel_xxx.json [--gold g1.json g2.json ...]
Sin --gold evalúa contra GS-Corpus y GS-Completo de ecoFactory.
"""
import os, sys, argparse
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
from schema import LEL
from evaluacion import evaluar, reporte_markdown

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("lel", help="LEL producido (.json)")
    ap.add_argument("--gold", nargs="+", default=None, help="uno o más Gold Standards .json")
    args = ap.parse_args()

    producido = LEL.load(args.lel)
    nombre = os.path.splitext(os.path.basename(args.lel))[0]
    if args.gold:
        golds = {os.path.splitext(os.path.basename(g))[0]: g for g in args.gold}
    else:
        golds = {"GS-Corpus (14)": os.path.join(RAIZ, "data/gold/gs_corpus.json"),
                 "GS-Completo (21)": os.path.join(RAIZ, "data/gold/gs_completo.json")}

    md = [f"# Reporte de evaluación — `{nombre}`", ""]
    for etiqueta, gs_path in golds.items():
        rep = evaluar(producido, LEL.load(gs_path), etiqueta)
        print(rep.resumen()); print()
        md.append(reporte_markdown(rep)); md.append("")
    salida = os.path.join(RAIZ, f"resultados/reporte_{nombre}.md")
    open(salida, "w", encoding="utf-8").write("\n".join(md))
    print(f"Reporte -> {salida}")
