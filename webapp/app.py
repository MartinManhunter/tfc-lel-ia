"""
app.py — Interfaz gráfica de ejecución paso a paso del prototipo de construcción del LEL.

Una pequeña aplicación web (sin dependencias externas: usa solo la biblioteca estándar de
Python) que permite ejecutar el pipeline del prototipo etapa por etapa, con un botón por
etapa, mostrando en pantalla el resultado de cada una, y generar al final los dos reportes
(el LEL navegable y la evaluación contra el Gold Standard).

Reutiliza el mismo código del prototipo que la línea de comandos:
  - src/pipeline_llm.py   (extraer -> clasificar -> describir -> auto-verificar)
  - src/llm_client.py     (abstracción de proveedor: mock | openai | anthropic)
  - src/evaluacion.py     (motor de evaluación determinístico)
  - scripts/reporte_lel_html.py (render del LEL a HTML)

Uso:
    python webapp/app.py            # abre en http://127.0.0.1:8000
    python webapp/app.py --port 8010

Con proveedor 'mock' (por defecto si config.yaml no trae uno real) corre 100 % offline,
sin llamar a ningún modelo: ideal para demostrar la orquestación sin gastar API.
"""
from __future__ import annotations
import os, sys, json, argparse, webbrowser, threading, html
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

import yaml
from schema import LEL, Simbolo, TIPOS
from llm_client import LLMConfig, get_client
from pipeline_llm import (cargar_corpus, extraer_candidatos, clasificar,
                          describir, auto_verificar)
from evaluacion import evaluar, reporte_markdown
import reporte_lel_html as replel  # render_simbolo, PLANTILLA, COLOR_TIPO, ORDEN_TIPOS

RESULTADOS = os.path.join(RAIZ, "resultados")
TEMPLATES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

# ---------------------------------------------------------------- configuración
def leer_config() -> dict:
    with open(os.path.join(RAIZ, "config.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

CFG = leer_config()
CORPUS_PATHS = [os.path.join(RAIZ, p) for p in CFG.get("corpus", [])]
GOLD = {
    "GS-Corpus (15)": os.path.join(RAIZ, CFG.get("gold", {}).get("corpus", "data/gold/gs_corpus.json")),
    "GS-Completo (21)": os.path.join(RAIZ, CFG.get("gold", {}).get("completo", "data/gold/gs_completo.json")),
}


def _cargar_corpora() -> list:
    """Corpus seleccionables en la interfaz.

    Se leen de la clave 'corpora' de config.yaml. Si no está (config antigua),
    se arma una única entrada con el corpus del trabajo, de modo que la interfaz
    siga funcionando igual que antes.
    """
    items = []
    for c in CFG.get("corpora", []) or []:
        archivos = [os.path.join(RAIZ, p) for p in c.get("archivos", [])]
        archivos = [p for p in archivos if os.path.exists(p)]
        if not archivos:
            continue
        items.append({
            "nombre": c.get("nombre", "(sin nombre)"),
            "archivos": archivos,
            "gold": {k: os.path.join(RAIZ, v) for k, v in (c.get("gold") or {}).items()
                     if os.path.exists(os.path.join(RAIZ, v))},
        })
    if not items:
        items = [{"nombre": "Corpus del trabajo", "archivos": CORPUS_PATHS, "gold": GOLD}]
    return items


CORPORA = _cargar_corpora()

# --------------------------------------------------------------------- estado
# Estado en memoria de la corrida actual (aplicación local de un solo usuario).
STATE: dict = {}

def reset_state():
    STATE.clear()
    STATE.update({"paso": 0, "candidatos": None, "tipos": None,
                  "simbolos": None, "lel": None, "cli": None, "llm_cfg": None,
                  "corpus_text": None})


# ------------------------------------------------------------------ acciones
def accion_reset(body: dict) -> dict:
    proveedor = (body.get("proveedor") or CFG.get("proveedor") or "mock").strip()
    modelo = (body.get("modelo") or CFG.get("modelo") or "").strip()
    reset_state()
    llm_cfg = LLMConfig(proveedor=proveedor, modelo=modelo,
                        temperatura=float(CFG.get("temperatura", 0.2)))
    STATE["llm_cfg"] = llm_cfg
    STATE["cli"] = get_client(llm_cfg)

    try:
        idx = int(body.get("corpus", 0))
    except (TypeError, ValueError):
        idx = 0
    sel = CORPORA[idx] if 0 <= idx < len(CORPORA) else CORPORA[0]
    STATE["corpus_nombre"] = sel["nombre"]
    STATE["proyecto"] = _proyecto_de(sel["nombre"])
    STATE["gold"] = sel["gold"]

    STATE["corpus_text"] = cargar_corpus(sel["archivos"])
    STATE["paso"] = 1
    entrevistas = [{"nombre": os.path.basename(p),
                    "chars": len(open(p, encoding="utf-8").read())}
                   for p in sel["archivos"]]
    return {"ok": True, "proveedor": proveedor, "modelo": modelo or "n/a",
            "corpus": sel["nombre"], "con_gold": bool(sel["gold"]),
            "entrevistas": entrevistas,
            "total_chars": sum(e["chars"] for e in entrevistas)}


def _requiere(paso: int):
    if STATE.get("paso", 0) < paso:
        raise RuntimeError("Ejecutá primero los pasos anteriores (o cargá el corpus).")


def _proyecto_de(nombre_corpus: str) -> str:
    """Nombre del proyecto a partir del corpus elegido.

    Los corpus se nombran «Proyecto — descripción», así que alcanza con quedarse
    con la parte anterior al guion largo ("Veterinaria — caso de muestreo").
    """
    return (nombre_corpus or "").split("—")[0].strip() or (nombre_corpus or "—")


_PROVEEDORES = {"mock": "Mock", "openai": "OpenAI", "anthropic": "Anthropic", "echo": "Echo"}


def _etiqueta_modelo(cfg) -> str:
    """Texto legible del modelo usado, para el encabezado de los reportes."""
    prov = _PROVEEDORES.get(cfg.proveedor, cfg.proveedor.title())
    if cfg.proveedor == "mock":
        return f"{prov} — offline (datos de la corrida de referencia)"
    return f"{prov} — {cfg.modelo}" if cfg.modelo else prov


def _cap(nombre: str) -> str:
    """Mayúscula inicial en el nombre del símbolo, respetando el resto.

    Se aplica apenas se extraen los candidatos para que el nombre viaje ya
    normalizado a la clasificación, la descripción, el LEL y los reportes.
    No afecta el emparejamiento del evaluador, que normaliza a minúsculas.
    """
    n = (nombre or "").strip()
    return n[:1].upper() + n[1:] if n else n


def accion_extraer(body: dict) -> dict:
    _requiere(1)
    cli, corpus = STATE["cli"], STATE["corpus_text"]
    candidatos = extraer_candidatos(corpus, cli)
    for c in candidatos:
        c["nombre"] = _cap(c["nombre"])
    STATE["candidatos"] = candidatos
    STATE["paso"] = max(STATE["paso"], 2)
    return {"ok": True,
            "total": len(candidatos),
            "items": [c["nombre"] for c in candidatos]}


def accion_clasificar(body: dict) -> dict:
    _requiere(2)
    cli, corpus = STATE["cli"], STATE["corpus_text"]
    tipos = clasificar(STATE["candidatos"], corpus, cli)
    STATE["tipos"] = tipos
    STATE["paso"] = max(STATE["paso"], 3)
    conteo = {t: 0 for t in TIPOS}
    for t in tipos.values():
        if t in conteo:
            conteo[t] += 1
    items = [{"nombre": c["nombre"], "tipo": tipos.get(c["nombre"], "")}
             for c in STATE["candidatos"]]
    return {"ok": True, "conteo": conteo, "items": items}


def accion_describir(body: dict) -> dict:
    _requiere(3)
    cli, corpus = STATE["cli"], STATE["corpus_text"]
    candidatos, tipos = STATE["candidatos"], STATE["tipos"]
    nombres = [c["nombre"] for c in candidatos]
    simbolos = []
    for i, c in enumerate(candidatos):
        nombre = c["nombre"]
        tipo = tipos.get(nombre, "")
        nocion, impacto = [], []
        if tipo:
            otros = [n for n in nombres if n != nombre]
            nocion, impacto = describir(nombre, tipo, otros, corpus, cli)
        simbolos.append(Simbolo(nombre=nombre, tipo=tipo, nocion=nocion,
                                impacto=impacto, sinonimos=c.get("sinonimos", []),
                                id=f"LLM{i+1:02d}"))
    STATE["simbolos"] = simbolos
    STATE["lel"] = LEL(proyecto=STATE.get("proyecto") or CFG.get("proyecto", "ecoFactory"),
                       conjunto=_etiqueta_modelo(STATE["llm_cfg"]),
                       simbolos=simbolos)
    STATE["paso"] = max(STATE["paso"], 4)
    con_desc = sum(1 for s in simbolos if s.nocion and s.impacto)
    items = [{"nombre": s.nombre, "tipo": s.tipo,
              "nocion": " ".join(s.nocion), "impacto": " ".join(s.impacto)}
             for s in simbolos]
    return {"ok": True, "total": len(simbolos),
            "con_desc": con_desc,
            "pct_desc": round(100 * con_desc / max(len(simbolos), 1)),
            "items": items}


def accion_verificar(body: dict) -> dict:
    _requiere(4)
    cli, corpus = STATE["cli"], STATE["corpus_text"]
    lel = auto_verificar(STATE["lel"], corpus, cli)
    for s in lel.simbolos:                     # la etapa 4 puede devolver otra grafía
        s.nombre = _cap(s.nombre)
    lel.conjunto = _etiqueta_modelo(STATE["llm_cfg"])
    STATE["lel"] = lel
    STATE["paso"] = max(STATE["paso"], 5)
    conteo = lel.conteo_por_tipo()
    con_desc = sum(1 for s in lel.simbolos if s.nocion and s.impacto)
    return {"ok": True, "total": len(lel.simbolos), "conteo": conteo,
            "con_desc": con_desc,
            "pct_desc": round(100 * con_desc / max(len(lel.simbolos), 1))}


def _render_lel_html(lel: LEL, titulo: str) -> str:
    """Reutiliza el render de scripts/reporte_lel_html.py para el LEL navegable."""
    por_tipo = {t: [] for t in replel.ORDEN_TIPOS}
    for s in lel.simbolos:
        por_tipo.setdefault(s.tipo or "—", []).append(s)
    chips = "".join(
        f'<span class="chip" style="background:{replel.COLOR_TIPO.get(t,"#888")}">{t}: {len(por_tipo.get(t, []))}</span>'
        for t in replel.ORDEN_TIPOS if por_tipo.get(t))
    grupos = []
    for t in replel.ORDEN_TIPOS:
        sims = por_tipo.get(t, [])
        if not sims:
            continue
        grupos.append(f'<h2 class="grupo" style="background:{replel.COLOR_TIPO[t]}">{t} ({len(sims)})</h2>')
        for s in sorted(sims, key=lambda x: x.nombre):
            grupos.append(replel.render_simbolo(s))
    return replel.PLANTILLA.format(
        titulo=html.escape(titulo), proyecto=html.escape(lel.proyecto or "—"),
        conjunto=html.escape(lel.conjunto or "—"), total=len(lel.simbolos),
        chips=chips, grupos="\n".join(grupos))


def _render_eval_html(reportes: list, titulo: str, corpus: str = "ecoFactory") -> str:
    filas = ""
    for r in reportes:
        filas += (f"<tr><td>{html.escape(r['gold'])}</td>"
                  f"<td>{r['precision']:.3f}</td><td>{r['cobertura']:.3f}</td>"
                  f"<td>{r['f1']:.3f}</td><td>{r['tipo']:.3f}</td>"
                  f"<td>{r['pct_desc']} %</td>"
                  f"<td>{r['vp']} / {r['fp']} / {r['fn']}</td></tr>")
    return f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>Reporte de Evaluación</title>
<style>
 body{{font-family:'Segoe UI',Arial,sans-serif;max-width:960px;margin:30px auto;padding:0 20px;color:#222;background:#fafafa}}
 h1{{font-size:1.5em;border-bottom:3px solid #0E2A4C;padding-bottom:8px}}
 table{{border-collapse:collapse;width:100%;margin-top:18px;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
 th,td{{padding:10px 12px;text-align:center;border-bottom:1px solid #e3e8ee}}
 th{{background:#0E2A4C;color:#fff;font-size:.9em}} td:first-child,th:first-child{{text-align:left}}
 .meta{{color:#666;font-size:.88em}}
</style></head><body>
<h1>Reporte de Evaluación</h1>
<p class="meta">Métricas del LEL generado contra el LEL de referencia de {html.escape(corpus)}. VP/FP/FN = aciertos / de más / perdidos.</p>
<table><tr><th>Gold Standard</th><th>Precisión</th><th>Cobertura</th><th>F1</th><th>Exactitud de tipo</th><th>Descripciones</th><th>VP / FP / FN</th></tr>
{filas}</table></body></html>"""


def accion_reportes(body: dict) -> dict:
    _requiere(4)  # con describir alcanza; verificar es opcional
    lel = STATE["lel"]
    run = "lel_gui"
    os.makedirs(RESULTADOS, exist_ok=True)
    # 0) LEL en json (insumo de ambos reportes)
    lel.save(os.path.join(RESULTADOS, f"{run}.json"))
    # 1) Reporte del LEL (navegable)
    lel_html = f"reporte_{run}.html"
    with open(os.path.join(RESULTADOS, lel_html), "w", encoding="utf-8") as f:
        f.write(_render_lel_html(lel, run))
    # 2) Reporte de evaluación contra el/los Gold Standard del corpus elegido.
    #    Un corpus de prueba puede no tener referencia: en ese caso solo se
    #    informan las descripciones y no hay métricas de identificación.
    # Ojo: un corpus sin referencia trae {} y eso es distinto de "no hay selección".
    # Usar `or GOLD` lo evaluaría contra el Gold Standard de ecoFactory, que no
    # corresponde a ese corpus.
    golds = STATE["gold"] if "gold" in STATE else GOLD
    corpus_nombre = STATE.get("corpus_nombre", "corpus del trabajo")

    # El proveedor 'mock' reproduce SIEMPRE el LEL de ecoFactory (datos pre-cargados),
    # sin leer el corpus. Evaluarlo contra el gold de otro dominio daría métricas
    # sin sentido, así que en ese caso no se evalúa y se explica por qué.
    mock_fuera_de_dominio = (STATE.get("llm_cfg") and STATE["llm_cfg"].proveedor == "mock"
                             and STATE.get("proyecto") != "ecoFactory")
    if mock_fuera_de_dominio:
        golds = {}

    reportes, md = [], [f"# Reporte de evaluación — `{run}`",
                        f"Corpus: {corpus_nombre}", ""]
    con_desc = sum(1 for s in lel.simbolos if s.nocion and s.impacto)
    pct = round(100 * con_desc / max(len(lel.simbolos), 1))
    if mock_fuera_de_dominio:
        md.append("El proveedor *mock* reproduce el LEL de referencia de ecoFactory "
                  "(datos pre-cargados), por lo que no corresponde evaluarlo contra este "
                  "corpus. Para una corrida real sobre este dominio, usá un proveedor con API.")
    elif not golds:
        md.append("Este corpus no tiene un LEL de referencia asociado, "
                  "por lo que no se calculan métricas de identificación.")
        md.append(f"Símbolos producidos: {len(lel.simbolos)} · "
                  f"con noción e impacto: {pct} %.")
    for etiqueta, gs_path in golds.items():
        rep = evaluar(lel, LEL.load(gs_path), etiqueta)
        reportes.append({"gold": etiqueta, "precision": rep.precision,
                         "cobertura": rep.cobertura, "f1": rep.f1,
                         "tipo": rep.exactitud_tipo, "pct_desc": pct,
                         "vp": rep.vp, "fp": rep.fp, "fn": rep.fn})
        md.append(reporte_markdown(rep)); md.append("")
    eval_html = f"reporte_evaluacion_{run}.html"
    with open(os.path.join(RESULTADOS, eval_html), "w", encoding="utf-8") as f:
        f.write(_render_eval_html(reportes, run, STATE.get("proyecto") or corpus_nombre))
    with open(os.path.join(RESULTADOS, f"reporte_evaluacion_{run}.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    STATE["paso"] = max(STATE["paso"], 6)
    return {"ok": True, "metricas": reportes,
            "reporte_lel": f"/reports/{lel_html}",
            "reporte_eval": f"/reports/{eval_html}"}


ACCIONES = {
    "/api/reset": accion_reset,
    "/api/extraer": accion_extraer,
    "/api/clasificar": accion_clasificar,
    "/api/describir": accion_describir,
    "/api/verificar": accion_verificar,
    "/api/reportes": accion_reportes,
}


# ------------------------------------------------------------------- servidor
class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):  # silenciar el log de acceso
        pass

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(os.path.join(TEMPLATES, "index.html"), encoding="utf-8") as f:
                pagina = f.read()
            opciones = "".join(
                f'<option value="{i}"{" selected" if i == 0 else ""}>'
                f'{html.escape(c["nombre"])}</option>'
                for i, c in enumerate(CORPORA))
            pagina = pagina.replace("{{CORPORA}}", opciones)
            pagina = pagina.replace("{{MODELO}}", html.escape(str(CFG.get("modelo", "") or "")))
            return self._send(200, pagina, "text/html; charset=utf-8")
        if self.path.startswith("/reports/"):
            nombre = os.path.basename(self.path.split("?")[0])
            ruta = os.path.join(RESULTADOS, nombre)
            if os.path.isfile(ruta):
                with open(ruta, "rb") as f:
                    return self._send(200, f.read(), "text/html; charset=utf-8")
            return self._send(404, json.dumps({"error": "no encontrado"}))
        return self._send(404, json.dumps({"error": "no encontrado"}))

    def do_POST(self):
        accion = ACCIONES.get(self.path.split("?")[0])
        if not accion:
            return self._send(404, json.dumps({"error": "acción desconocida"}))
        try:
            n = int(self.headers.get("Content-Length", 0) or 0)
            body = json.loads(self.rfile.read(n) or b"{}") if n else {}
            return self._send(200, json.dumps(accion(body), ensure_ascii=False))
        except Exception as e:  # noqa: BLE001
            return self._send(200, json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-browser", action="store_true", help="no abrir el navegador solo")
    args = ap.parse_args()
    reset_state()
    url = f"http://127.0.0.1:{args.port}"
    print(f"Interfaz del prototipo LEL corriendo en {url}")
    print("Ctrl+C para cerrar.")
    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")


if __name__ == "__main__":
    main()
