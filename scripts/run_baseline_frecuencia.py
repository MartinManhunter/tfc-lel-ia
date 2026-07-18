"""Ejecuta el baseline de frecuencia (C1a) y guarda el LEL producido.
Uso:
    python scripts/run_baseline_frecuencia.py [--corpus a.txt b.txt ...] [--out ruta.json]
Sin --corpus usa el corpus por defecto de config.yaml.
"""
import os, sys, argparse, yaml
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
from baseline_frecuencia import construir

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", nargs="+", default=None, help="rutas a las entrevistas .txt")
    ap.add_argument("--out", default=None, help="ruta de salida .json")
    args = ap.parse_args()
    if args.corpus:
        corpus = args.corpus
    else:
        cfg = yaml.safe_load(open(os.path.join(RAIZ, "config.yaml"), encoding="utf-8"))
        corpus = [os.path.join(RAIZ, p) for p in cfg["corpus"]]
    lel = construir(corpus)
    out = args.out or os.path.join(RAIZ, "resultados/lel_baseline_frecuencia.json")
    lel.save(out)
    print(f"{len(lel.simbolos)} candidatos -> {out}")
