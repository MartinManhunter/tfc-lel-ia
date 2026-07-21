"""
graficar_resultado.py — Genera un gráfico de barras comparando resultados de evaluación.

Uso (desde la raíz del repo, con el venv activado):

  # Un solo resultado:
  python scripts/graficar_resultado.py resultados/lel_baseline_frecuencia.json

  # Comparar dos resultados (por ejemplo tu baseline vs la corrida de referencia LLM):
  python scripts/graficar_resultado.py resultados/lel_baseline_frecuencia.json resultados/lel_llm_C2c_referencia.json

  # Elegir el Gold Standard (por defecto usa GS-Recuperable, el de 15 símbolos):
  python scripts/graficar_resultado.py resultados/lel_baseline_frecuencia.json --gold data/gold/gs_completo.json

Guarda el gráfico como PNG en resultados/ y lo podés abrir haciendo clic en el archivo
dentro de VS Code (se previsualiza solo, sin instalar nada más).
"""
import os, sys, argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
from schema import LEL
from evaluacion import evaluar

def cobertura_descripciones(lel: LEL) -> float:
    if not lel.simbolos:
        return 0.0
    con_desc = sum(1 for s in lel.simbolos if s.nocion and s.impacto)
    return con_desc / len(lel.simbolos)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lel", nargs="+", help="uno o dos archivos LEL producidos (.json)")
    ap.add_argument("--gold", default=os.path.join(RAIZ, "data/gold/gs_corpus.json"),
                    help="Gold Standard contra el que evaluar (por defecto: GS-Corpus, 15 símbolos)")
    ap.add_argument("--out", default=None, help="ruta de salida .png")
    args = ap.parse_args()

    if len(args.lel) > 2:
        sys.exit("Como máximo se pueden comparar 2 resultados a la vez.")

    gold = LEL.load(args.gold)
    etiquetas = ["Precisión", "Cobertura", "F1", "Tipo", "Descripciones"]
    series = []
    for path in args.lel:
        lel = LEL.load(path)
        rep = evaluar(lel, gold, os.path.basename(args.gold))
        descr = cobertura_descripciones(lel)
        nombre = os.path.splitext(os.path.basename(path))[0]
        series.append((nombre, [rep.precision, rep.cobertura, rep.f1, rep.exactitud_tipo, descr]))
        print(f"{nombre}: P={rep.precision:.3f} R={rep.cobertura:.3f} F1={rep.f1:.3f} "
              f"Tipo={rep.exactitud_tipo:.3f} Descr={descr:.0%}")

    colores = ["#b23a48", "#3b6ea5"]
    fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=150)
    x = np.arange(len(etiquetas))
    n = len(series)
    width = 0.7 / n
    for i, (nombre, valores) in enumerate(series):
        xpos = x - 0.35 + width/2 + i*width
        barras = ax.bar(xpos, valores, width=width*0.9, label=nombre, color=colores[i % len(colores)])
        for b, v in zip(barras, valores):
            ax.text(b.get_x()+b.get_width()/2, v+0.015, f"{v:.2f}", ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels(etiquetas)
    ax.set_ylim(0, 1.1)
    ax.set_title(f"Evaluación contra {os.path.basename(args.gold)}", fontsize=13, fontweight="bold")
    ax.legend(loc="upper left", frameon=False)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()

    out = args.out or os.path.join(RAIZ, "resultados", "grafico_" + "_vs_".join(
        os.path.splitext(os.path.basename(p))[0] for p in args.lel) + ".png")
    fig.savefig(out)
    print(f"\nGráfico -> {out}")

if __name__ == "__main__":
    main()
