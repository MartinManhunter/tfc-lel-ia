"""
reporte_lel_html.py — Genera una vista HTML navegable de un LEL (símbolos, tipos,
noción e impacto), para inspeccionar visualmente el resultado de una corrida.

Uso:
  python scripts/reporte_lel_html.py resultados/lel_baseline_frecuencia.json
  python scripts/reporte_lel_html.py resultados/lel_llm_C2c_referencia.json --out mi_reporte.html

Genera un .html que se abre haciendo doble clic (o clic derecho -> "Open with Live
Server" / "Reveal in File Explorer" desde VS Code, o simplemente arrastrándolo al navegador).
"""
import os, sys, argparse, html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
from schema import LEL

COLOR_TIPO = {
    "Sujeto": "#2f6f4f",
    "Objeto": "#3b6ea5",
    "Verbo":  "#b2701a",
    "Estado": "#8a3b8f",
}
ORDEN_TIPOS = ["Sujeto", "Objeto", "Verbo", "Estado"]

PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>LEL — {titulo}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 960px; margin: 30px auto;
         padding: 0 20px; color: #222; background: #fafafa; }}
  h1 {{ font-size: 1.5em; border-bottom: 3px solid #333; padding-bottom: 8px; }}
  .resumen {{ display: flex; gap: 14px; margin: 18px 0 28px; flex-wrap: wrap; }}
  .chip {{ padding: 8px 16px; border-radius: 20px; color: white; font-weight: 600; font-size: 0.92em; }}
  .simbolo {{ background: white; border-left: 6px solid #ccc; border-radius: 6px;
              padding: 12px 16px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,.08); }}
  .simbolo .nombre {{ font-weight: 700; font-size: 1.08em; }}
  .simbolo .tipo {{ display: inline-block; font-size: 0.75em; font-weight: 700; color: white;
                     padding: 2px 9px; border-radius: 10px; margin-left: 8px; vertical-align: middle; }}
  .simbolo .sinonimos {{ color: #777; font-size: 0.85em; font-style: italic; }}
  .campo {{ margin-top: 6px; font-size: 0.94em; }}
  .campo b {{ color: #444; }}
  .vacio {{ color: #bbb; font-style: italic; }}
  h2.grupo {{ margin-top: 32px; padding: 6px 12px; border-radius: 6px; color: white; }}
  .meta {{ color: #666; font-size: 0.88em; margin-bottom: 20px; }}
</style>
</head>
<body>
<h1>LEL — {titulo}</h1>
<p class="meta">Proyecto: <b>{proyecto}</b> · Conjunto: {conjunto} · Total de símbolos: <b>{total}</b></p>
<div class="resumen">{chips}</div>
{grupos}
</body>
</html>
"""

def render_simbolo(s):
    nombre = html.escape(s.nombre)
    tipo = s.tipo or "—"
    color = COLOR_TIPO.get(tipo, "#888")
    sinonimos = f'<div class="sinonimos">Sinónimos: {html.escape(", ".join(s.sinonimos))}</div>' if s.sinonimos else ""
    nocion = " ".join(s.nocion) if s.nocion else None
    impacto = " ".join(s.impacto) if s.impacto else None
    nocion_html = f'<div class="campo"><b>Noción:</b> {html.escape(nocion)}</div>' if nocion else '<div class="campo vacio">Sin noción</div>'
    impacto_html = f'<div class="campo"><b>Impacto:</b> {html.escape(impacto)}</div>' if impacto else '<div class="campo vacio">Sin impacto</div>'
    return f"""<div class="simbolo" style="border-left-color:{color}">
  <span class="nombre">{nombre}</span><span class="tipo" style="background:{color}">{tipo}</span>
  {sinonimos}
  {nocion_html}
  {impacto_html}
</div>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("lel", help="LEL producido (.json)")
    ap.add_argument("--out", default=None, help="ruta de salida .html")
    args = ap.parse_args()

    lel = LEL.load(args.lel)
    titulo = os.path.splitext(os.path.basename(args.lel))[0]

    por_tipo = {t: [] for t in ORDEN_TIPOS}
    for s in lel.simbolos:
        por_tipo.setdefault(s.tipo or "—", []).append(s)

    chips = "".join(
        f'<span class="chip" style="background:{COLOR_TIPO.get(t,"#888")}">{t}: {len(por_tipo.get(t, []))}</span>'
        for t in ORDEN_TIPOS if por_tipo.get(t)
    )

    grupos = []
    for t in ORDEN_TIPOS:
        simbolos = por_tipo.get(t, [])
        if not simbolos:
            continue
        color = COLOR_TIPO[t]
        grupos.append(f'<h2 class="grupo" style="background:{color}">{t} ({len(simbolos)})</h2>')
        for s in sorted(simbolos, key=lambda x: x.nombre):
            grupos.append(render_simbolo(s))

    out_html = PLANTILLA.format(
        titulo=html.escape(titulo),
        proyecto=html.escape(lel.proyecto or "—"),
        conjunto=html.escape(getattr(lel, "conjunto", "") or "—"),
        total=len(lel.simbolos),
        chips=chips,
        grupos="\n".join(grupos),
    )

    out = args.out or os.path.join(RAIZ, "resultados", f"reporte_{titulo}.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(out_html)
    print(f"Reporte HTML -> {out}")

if __name__ == "__main__":
    main()
