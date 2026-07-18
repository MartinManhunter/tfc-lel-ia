"""Ejecuta el pipeline LLM en una configuración dada y guarda el LEL producido.
Uso:
    python scripts/run_pipeline_llm.py --config C2c [--corpus a.txt b.txt ...] [--out ruta.json]
Lee proveedor/modelo/temperatura de config.yaml. Requiere la API key en el entorno
(OPENAI_API_KEY o ANTHROPIC_API_KEY). Con proveedor 'mock' corre offline (valida la plomería).
"""
import os, sys, argparse, yaml
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
from llm_client import LLMConfig
from pipeline_llm import construir_lel, CONFIGURACIONES

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="C2c", choices=list(CONFIGURACIONES))
    ap.add_argument("--corpus", nargs="+", default=None, help="rutas a las entrevistas .txt")
    ap.add_argument("--out", default=None, help="ruta de salida .json")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(os.path.join(RAIZ, "config.yaml"), encoding="utf-8"))
    corpus = args.corpus or [os.path.join(RAIZ, p) for p in cfg["corpus"]]
    llm_cfg = LLMConfig(proveedor=cfg["proveedor"], modelo=cfg.get("modelo", ""),
                        temperatura=cfg.get("temperatura", 0.2))
    lel = construir_lel(corpus, llm_cfg, CONFIGURACIONES[args.config])
    out = args.out or os.path.join(RAIZ, f"resultados/lel_llm_{args.config}.json")
    lel.save(out)
    print(f"{len(lel.simbolos)} símbolos -> {out}  (proveedor={llm_cfg.proveedor}, modelo={llm_cfg.modelo or 'n/a'})")
