"""
gen_figuras_resultados.py — Regenera los graficos de resultados del Cap. 7 (fig_7_1, fig_7_2)
con los numeros reales del corpus 100% real (post revision de julio 2026).
No toca fig_7_3 / fig_7_4 (casos de muestreo, sin cambios).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "figuras_png")
ROJO = "#b23a48"
AZUL = "#3b6ea5"
TITULO_AZUL = "#1F4E79"

plt.rcParams["font.family"] = "DejaVu Sans"

def barras(categorias, series, colores, titulo, archivo, ylim=1.05):
    fig, ax = plt.subplots(figsize=(9.2, 4.6), dpi=150)
    n = len(series)
    width = 0.8 / n
    x = np.arange(len(categorias))
    for i, (label, valores) in enumerate(series):
        xpos = x - 0.4 + width/2 + i*width
        bars = ax.bar(xpos, valores, width=width*0.9, label=label, color=colores[i], edgecolor="none")
        for b, v in zip(bars, valores):
            ax.text(b.get_x() + b.get_width()/2, v + 0.015, f"{v:.2f}", ha="center", va="bottom", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(categorias, fontsize=12)
    ax.set_ylabel("Valor", fontsize=11)
    ax.set_ylim(0, ylim)
    ax.set_title(titulo, fontsize=15, fontweight="bold", color=TITULO_AZUL, pad=14)
    ax.legend(loc="upper left", frameon=False, fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    path = os.path.join(OUT, archivo)
    fig.savefig(path)
    plt.close(fig)
    print("OK", archivo, fig.get_size_inches()*fig.dpi)

# ---------- Fig 7.1: baseline de frecuencia, Config A vs Config B, frente a GS-Completo ----------
# Config A (2 entrevistas reales) vs GS-Completo: P=0.216 R=0.381 F1=0.276  (sin cambios)
# Config B (4 entrevistas, ahora reales) vs GS-Completo: P=0.225 R=0.429 F1=0.295 (nuevo, antes 0.325/0.619/0.426 con datos simulados)
barras(
    ["Precisión", "Cobertura", "F1"],
    [("Corpus-Real (2 entrevistas)", [0.216, 0.381, 0.276]),
     ("Corpus-Extendido (4 entrevistas, reales)", [0.225, 0.429, 0.295])],
    [ROJO, AZUL],
    "Baseline de frecuencia frente al GS-Completo (21 símbolos)",
    "fig_7_1_resultados_frecuencia.png",
    ylim=0.55
)

# ---------- Fig 7.2: PLN vs LLM frente al GS-Corpus-Extendido (15), incluye Tipo ----------
# PLN frecuencia (C1a) vs GS-Corpus-Ext: P=0.175 R=0.467 F1=0.255 Tipo=0.571 Descr=0
# Pipeline LLM (C2c) vs GS-Corpus-Ext:   P=0.474 R=0.600 F1=0.529 Tipo=0.889 Descr=1.00
barras(
    ["Precisión", "Cobertura", "F1", "Tipo", "Descripciones"],
    [("PLN frecuencia (C1a)", [0.175, 0.467, 0.255, 0.571, 0.00]),
     ("Pipeline LLM (C2c)", [0.474, 0.600, 0.529, 0.889, 1.00])],
    [ROJO, AZUL],
    "PLN tradicional vs. pipeline LLM frente al GS-Corpus-Extendido",
    "fig_7_2_pln_vs_llm.png",
    ylim=1.12
)

# ---------- Fig 5.3: GS-Completo (21) vs GS-Corpus (15) por tipo ----------
def barras_agrupadas_tipo():
    tipos = ["Sujeto", "Objeto", "Verbo", "Estado"]
    completo = [6, 5, 8, 2]      # GS-Completo = 21
    recuperable = [4, 4, 6, 1]   # GS-Corpus = 15
    fig, ax = plt.subplots(figsize=(7.6, 4.2), dpi=150)
    x = np.arange(len(tipos)); w = 0.38
    b1 = ax.bar(x - w/2, completo, w, label="GS-Completo (21)", color=ROJO)
    b2 = ax.bar(x + w/2, recuperable, w, label="GS-Corpus (15)", color=AZUL)
    for bars in (b1, b2):
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x()+b.get_width()/2, h+0.08, str(int(h)), ha="center", va="bottom", fontsize=11)
    ax.set_xticks(x); ax.set_xticklabels(tipos, fontsize=12)
    ax.set_ylabel("Cantidad de símbolos", fontsize=11)
    ax.set_ylim(0, 9)
    ax.set_title("Composición del Gold Standard por tipo de símbolo", fontsize=14, fontweight="bold", color=TITULO_AZUL, pad=12)
    ax.legend(loc="upper right", frameon=False, fontsize=11)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "fig_5_3_gold_standard.png"))
    plt.close(fig)
    print("OK fig_5_3_gold_standard.png")

barras_agrupadas_tipo()
