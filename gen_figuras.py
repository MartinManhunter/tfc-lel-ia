"""
gen_figuras.py — Genera las figuras (SVG) del marco teórico con estilo consistente.
Salida: figuras/*.svg
"""
import os, html

OUT = os.path.join(os.path.dirname(__file__), "figuras")
os.makedirs(OUT, exist_ok=True)

# Paleta
AZUL = "#3b6ea5"; AZUL_F = "#e8eef7"; ROJO = "#b23a48"; ROJO_F = "#f6e7e9"
VERDE = "#3f7d5b"; VERDE_F = "#e6f0ea"; GRIS = "#5b6470"; GRIS_F = "#eef1f4"
TXT = "#1f2937"; LINEA = "#6b7280"; FONDO = "#ffffff"

def _wrap(s, n):
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 <= n:
            line = (line + " " + w).strip()
        else:
            out.append(line); line = w
    if line: out.append(line)
    return out

def rect(x, y, w, h, label, fill=AZUL_F, stroke=AZUL, fs=15, tc=TXT, rx=8, bold=False, wrap=None):
    # Ajuste automático según el ancho de la caja (evita desbordes de texto)
    if wrap is None:
        wrap = max(6, int((w - 12) / (fs * 0.56)))
    lines = _wrap(label, wrap)
    lh = fs + 4
    ty = y + h/2 - (len(lines)-1)*lh/2 + fs/2 - 2
    t = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>']
    for i, ln in enumerate(lines):
        t.append(f'<text x="{x+w/2}" y="{ty+i*lh}" font-size="{fs}" fill="{tc}" '
                 f'text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
                 f'{"font-weight=\"700\"" if bold else ""}>{html.escape(ln)}</text>')
    return "\n".join(t)

def artifact(x, y, w, h, label, fill=GRIS_F, stroke=GRIS, fs=15, tc=TXT, bold=False, wrap=None):
    # Forma de ARTEFACTO (entrada/salida: datos, documentos) — paralelogramo,
    # deliberadamente distinta del rectángulo redondeado usado para ACTIVIDADES,
    # siguiendo la convención de diagramas de proceso (BPMN/UML).
    if wrap is None:
        wrap = max(6, int((w - 26) / (fs * 0.56)))
    lines = _wrap(label, wrap)
    lh = fs + 4
    ty = y + h/2 - (len(lines)-1)*lh/2 + fs/2 - 2
    skew = min(18, h * 0.28)
    pts = f"{x+skew},{y} {x+w},{y} {x+w-skew},{y+h} {x},{y+h}"
    t = [f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>']
    for i, ln in enumerate(lines):
        t.append(f'<text x="{x+w/2}" y="{ty+i*lh}" font-size="{fs}" fill="{tc}" '
                 f'text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" '
                 f'{"font-weight=\"700\"" if bold else ""}>{html.escape(ln)}</text>')
    return "\n".join(t)

def brace_h(x1, x2, y, point_y, color=VERDE):
    # Llave HORIZONTAL entre x1 y x2 a la altura y, con la punta central hacia point_y
    # (hacia arriba si point_y < y, hacia abajo si point_y > y).
    xm = (x1 + x2) / 2
    ym = (y + point_y) / 2
    d = (f"M {x1} {y} Q {x1} {ym} {(x1+xm)/2} {ym} "
         f"Q {xm} {ym} {xm} {point_y} "
         f"Q {xm} {ym} {(xm+x2)/2} {ym} "
         f"Q {x2} {ym} {x2} {y}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5"/>'

def arrow(x1, y1, x2, y2, label="", color=LINEA, dash=False, fs=12):
    d = 'stroke-dasharray="6 4"' if dash else ""
    s = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" {d} marker-end="url(#ah)"/>']
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        s.append(f'<rect x="{mx-len(label)*3.4-4}" y="{my-10}" width="{len(label)*6.8+8}" height="18" rx="4" fill="{FONDO}" opacity="0.9"/>')
        s.append(f'<text x="{mx}" y="{my+3}" font-size="{fs}" fill="{color}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif">{html.escape(label)}</text>')
    return "\n".join(s)

def text(x, y, s, fs=13, tc=TXT, anchor="middle", bold=False):
    return (f'<text x="{x}" y="{y}" font-size="{fs}" fill="{tc}" text-anchor="{anchor}" '
            f'font-family="Segoe UI, Arial, sans-serif" {"font-weight=\"700\"" if bold else ""}>{html.escape(s)}</text>')

def arrow_path(points, label="", color=LINEA, dash=False):
    # Flecha de varios segmentos con UNA sola punta al final (evita el efecto de
    # "varias flechas" que dejaba la versión anterior con tramos independientes).
    d = "M " + " L ".join(f"{x},{y}" for x, y in points)
    dd = 'stroke-dasharray="6 4"' if dash else ""
    s = [f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" {dd} marker-end="url(#ah)"/>']
    if label:
        mx, my = points[len(points)//2]
        s.append(f'<rect x="{mx-len(label)*3.4-4}" y="{my-10}" width="{len(label)*6.8+8}" height="18" rx="4" fill="{FONDO}" opacity="0.9"/>')
        s.append(f'<text x="{mx}" y="{my+3}" font-size="12" fill="{color}" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif">{html.escape(label)}</text>')
    return "\n".join(s)

def svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">\n'
            f'<defs><marker id="ah" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">'
            f'<path d="M0,0 L8,3 L0,6 Z" fill="{LINEA}"/></marker></defs>\n'
            f'<rect width="{w}" height="{h}" fill="{FONDO}"/>\n{body}\n</svg>\n')

def guardar(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("OK", nombre)

# ---------- Fig 2.1 Actividades de la IR ----------
b = []
b.append(text(450, 28, "Actividades de la Ingeniería de Requisitos", 18, AZUL, bold=True))
xs = [40, 250, 460, 670]
labels = ["Elicitación", "Análisis y Modelado", "Especificación", "Validación"]
for i,(x,l) in enumerate(zip(xs,labels)):
    b.append(rect(x, 120, 180, 70, l, bold=True))
    if i < 3:
        b.append(arrow(x+180, 155, xs[i+1], 155))
b.append(rect(40, 250, 810, 56, "Gestión de Requisitos (trazabilidad y gestión de cambios a lo largo de todo el proceso)", fill=ROJO_F, stroke=ROJO, fs=14))
for x in xs:
    b.append(arrow(x+90, 250, x+90, 192, color=ROJO, dash=True))
b.append(text(450, 360, "Las tres primeras producen y refinan los requisitos; la validación los contrasta con clientes y usuarios.", 12, GRIS))
guardar("fig_2_1_actividades_ir.svg", svg(900, 390, "\n".join(b)))

# ---------- Fig 2.2 Estrategia orientada al cliente ----------
b = []
b.append(text(470, 30, "Estrategia de IR orientada al cliente: artefactos y trazas", 18, AZUL, bold=True))
b.append(rect(30, 250, 150, 70, "Fuentes de Información", fill=GRIS_F, stroke=GRIS))
b.append(rect(210, 120, 140, 64, "LEL", bold=True))
b.append(rect(210, 250, 140, 64, "Escenarios Actuales", fill=GRIS_F, stroke=GRIS))
b.append(rect(400, 185, 150, 70, "Escenarios Futuros", fill=VERDE_F, stroke=VERDE, bold=True))
b.append(rect(400, 70, 150, 64, "LEL del Sistema"))
b.append(rect(600, 185, 150, 70, "Especificación de Requisitos (ERS)", fill=ROJO_F, stroke=ROJO, bold=True, fs=13))
b.append(rect(790, 70, 80, 300, "Objetivos del Sistema", fill="#fff6e0", stroke="#c08a00", fs=13))
# trazas
b.append(arrow(180, 280, 210, 282))            # fuentes -> EA (elicitación)
b.append(arrow(180, 270, 210, 150, label="Elicitación"))  # fuentes -> LEL
b.append(arrow(280, 184, 280, 250, label="Derivación", color=AZUL))
b.append(arrow(350, 282, 400, 235, label="Evolución", color=VERDE))
b.append(arrow(550, 220, 600, 220, label="Extracción", color=ROJO))
b.append(arrow(475, 185, 475, 134, color=AZUL, dash=True))
b.append(arrow(790, 220, 750, 220, color="#c08a00", dash=True))
b.append(text(470, 360, "Flujo principal: del vocabulario (LEL) a los escenarios y de allí a la especificación, guiado por los objetivos del sistema.", 12, GRIS))
guardar("fig_2_2_estrategia_cliente.svg", svg(940, 390, "\n".join(b)))

# ---------- Fig 2.3 Estructura del LEL (metamodelo) ----------
b = []
b.append(text(450, 30, "Estructura del símbolo del LEL", 18, AZUL, bold=True))
b.append(rect(330, 70, 240, 150, "", fill=AZUL_F, stroke=AZUL))
b.append(text(450, 96, "Símbolo del LEL", 16, AZUL, bold=True))
b.append(f'<line x1="330" y1="106" x2="570" y2="106" stroke="{AZUL}" stroke-width="1.5"/>')
for i, attr in enumerate(["Nombre", "Sinónimos", "Tipo", "Noción (descripción denotativa)", "Impacto (descripción connotativa)"]):
    b.append(text(345, 128+i*18, "• " + attr, 12, TXT, anchor="start"))
# tipos
tipos = [("Sujeto","entidad activa", VERDE_F, VERDE), ("Objeto","entidad pasiva", AZUL_F, AZUL),
         ("Verbo","acción/actividad", ROJO_F, ROJO), ("Estado","condición", "#fff6e0", "#c08a00")]
for i,(t,d,f,s) in enumerate(tipos):
    x = 30 + i*220
    b.append(rect(x, 300, 190, 64, f"{t}\n({d})", fill=f, stroke=s, fs=13, bold=True))
    b.append(arrow(x+95, 300, 450, 222, color=s, dash=True))
b.append(text(450, 248, "El tipo especializa en:", 12, GRIS))
b.append(rect(615, 116, 150, 76, "Otros símbolos del LEL", fill="#f3f4f6", stroke=GRIS, fs=13))
b.append(arrow(615, 150, 575, 150))
b.append(text(596, 140, "referencia", 10, GRIS))
b.append(text(690, 205, "circularidad", 11, GRIS))
guardar("fig_2_3_estructura_lel.svg", svg(900, 400, "\n".join(b)))

# ---------- Fig 2.4 Proceso de creación del LEL ----------
b = []
b.append(text(450, 30, "Proceso de creación del LEL", 18, AZUL, bold=True))
b.append(artifact(30, 150, 120, 70, "UdeD + Objetivos del Sistema", fs=12))
main = [("Recolectar\nSímbolos",190),("Clasificar\nSímbolos",360),("Describir\nSímbolos",530)]
for l,x in main:
    b.append(rect(x, 150, 130, 70, l, bold=True))
b.append(arrow(150, 185, 190, 185))
b.append(arrow(320, 185, 360, 185))
b.append(arrow(490, 185, 530, 185))
b.append(artifact(700, 108, 150, 56, "LEL", bold=True, fill=AZUL_F, stroke=AZUL))
b.append(artifact(700, 200, 150, 56, "Fichas de Información Anticipada", fill="#fff6e0", stroke="#c08a00", fs=12))
b.append(arrow(660, 175, 700, 138))
b.append(arrow(660, 195, 700, 226))
# verificar / validar: actividades que abarcan las 3 anteriores, unidas por una llave horizontal
b.append(rect(300, 40, 130, 46, "Verificar", fill=VERDE_F, stroke=VERDE, bold=True))
b.append(rect(300, 290, 130, 46, "Validar", fill=ROJO_F, stroke=ROJO, bold=True))
b.append(brace_h(190, 660, 150, 90, color=VERDE))
b.append(brace_h(190, 660, 220, 285, color=ROJO))
b.append(text(450, 372, "Flujo principal (Recolectar→Clasificar→Describir) con retroalimentación por verificación y validación.", 12, GRIS))
guardar("fig_2_4_proceso_lel.svg", svg(900, 400, "\n".join(b)))

# ---------- Fig 2.5 Modelo de escenario y derivación ----------
b = []
b.append(text(460, 30, "Modelo de Escenario y derivación desde el LEL", 18, AZUL, bold=True))
b.append(rect(40, 110, 150, 64, "LEL\n(Sujeto / Objeto / Verbo)", fill=AZUL_F, stroke=AZUL, fs=12, bold=True))
b.append(rect(330, 70, 560, 250, "", fill="#fbfcfe", stroke=AZUL))
b.append(text(610, 96, "Escenario", 16, AZUL, bold=True))
comp = ["Título", "Objetivo", "Contexto (precondición, ubicación temporal y geográfica)",
        "Recursos", "Actores", "Episodios (serie de acciones)", "Excepciones"]
for i,c in enumerate(comp):
    b.append(text(350, 126+i*30, "• " + c, 13, TXT, anchor="start"))
b.append(arrow(190, 150, 330, 150, label="Derivación", color=VERDE))
b.append(text(255, 200, "Sujeto→Actor", 11, GRIS))
b.append(text(255, 218, "Objeto→Recurso", 11, GRIS))
b.append(text(255, 236, "Verbo→Episodio/Título", 11, GRIS))
guardar("fig_2_5_escenario.svg", svg(920, 360, "\n".join(b)))

# ---------- Fig 2.6 Proceso de inspección ----------
b = []
b.append(text(460, 30, "Proceso de inspección (verificación)", 18, AZUL, bold=True))
pasos = ["Planificación","Descripción General","Preparación / Lectura","Reunión","Corrección","Seguimiento"]
x = 30
for i,p in enumerate(pasos):
    b.append(rect(x, 130, 135, 64, p, fs=13, bold=(p=="Reunión")))
    if i < len(pasos)-1:
        b.append(arrow(x+135, 162, x+145, 162))
    x += 145
b.append(rect(370, 250, 180, 50, "¿Reinspección?", fill="#fff6e0", stroke="#c08a00", bold=True))
b.append(arrow(437, 250, 437, 194, color="#c08a00"))
b.append(text(700, 250, "Defectos: Discrepancia · Error · Omisión · Ambigüedad", 12, GRIS))
b.append(text(700, 272, "Severidad: Alta · Media · Baja", 12, GRIS))
guardar("fig_2_6_inspeccion.svg", svg(920, 330, "\n".join(b)))

# ---------- Fig 2.7 Transformer simplificado ----------
b = []
b.append(text(450, 30, "Arquitectura Transformer (esquema simplificado)", 18, AZUL, bold=True))
b.append(rect(40, 150, 120, 60, "Tokens de entrada", fill=GRIS_F, stroke=GRIS, fs=12))
b.append(rect(190, 150, 130, 60, "Embeddings + Codificación posicional", fill=AZUL_F, stroke=AZUL, fs=11))
b.append(rect(360, 90, 300, 190, "", fill="#fbfcfe", stroke=AZUL))
b.append(text(510, 112, "Bloque ×N", 14, AZUL, bold=True))
b.append(rect(380, 130, 260, 56, "Autoatención (multi-cabezal)", fill=ROJO_F, stroke=ROJO, fs=13, bold=True))
b.append(rect(380, 200, 260, 56, "Red feed-forward + normalización", fill=VERDE_F, stroke=VERDE, fs=12))
b.append(arrow(510, 186, 510, 200))
b.append(rect(700, 150, 150, 60, "Distribución sobre el vocabulario → token siguiente", fill="#fff6e0", stroke="#c08a00", fs=11))
b.append(arrow(160, 180, 190, 180))
b.append(arrow(320, 180, 360, 180))
b.append(arrow(660, 180, 700, 180))
b.append(text(450, 320, "La autoatención pondera la relevancia de cada token respecto de los demás; el modelo predice el token siguiente de manera autorregresiva.", 12, GRIS, anchor="middle"))
guardar("fig_2_7_transformer.svg", svg(900, 360, "\n".join(b)))

# ---------- Fig 2.8 Pipeline PLN clásico ----------
b = []
b.append(text(450, 30, "Pipeline de PLN tradicional", 18, AZUL, bold=True))
etapas = ["Texto","Tokenización","Normalización / Lematización","Etiquetado gramatical (POS)","Reconocimiento de entidades (NER)","Análisis de frecuencia","Candidatos a término"]
fills = [GRIS_F, AZUL_F, AZUL_F, AZUL_F, AZUL_F, AZUL_F, ROJO_F]
strokes = [GRIS, AZUL, AZUL, AZUL, AZUL, AZUL, ROJO]
y = 90
for i,(e,f,s) in enumerate(zip(etapas,fills,strokes)):
    es_artefacto = (i == 0 or i == len(etapas)-1)
    if es_artefacto:
        b.append(artifact(330, y, 250, 40, e, fill=f, stroke=s, fs=12, bold=True))
    else:
        b.append(rect(330, y, 250, 40, e, fill=f, stroke=s, fs=12))
    if i < len(etapas)-1:
        b.append(arrow(455, y+40, 455, y+52))
    y += 52
b.append(text(700, 250, "Identifica términos, pero no", 12, GRIS))
b.append(text(700, 270, "genera noción ni impacto.", 12, GRIS))
guardar("fig_2_8_pln.svg", svg(900, 500, "\n".join(b)))

# ---------- Fig 4.1 Diseño experimental ----------
b = []
b.append(text(475, 30, "Diseño experimental: tratamientos y evaluación", 18, AZUL, bold=True))
b.append(artifact(20, 165, 130, 80, "Corpus de entrevistas", fs=12))
metodos = [("C1a — PLN frecuencia", ROJO_F, ROJO, 75),
           ("C1b — PLN spaCy", ROJO_F, ROJO, 165),
           ("C2 — LLM (C2a / C2b / C2c)", AZUL_F, AZUL, 255)]
for l,f,s,y in metodos:
    b.append(rect(210, y, 190, 60, l, fill=f, stroke=s, fs=12, bold=True))
    b.append(arrow(150, 205, 210, y+30))
b.append(artifact(460, 165, 150, 70, "LEL producido (por tratamiento)", fill="#fbfcfe", stroke=AZUL, fs=12, bold=True))
for _,_,_,y in metodos:
    b.append(arrow(400, y+30, 460, 200, color=LINEA, dash=True))
b.append(artifact(460, 285, 150, 60, "Gold Standard\n(GS-Corpus / GS-Completo)", fill=VERDE_F, stroke=VERDE, fs=11, bold=True))
b.append(rect(680, 210, 170, 80, "Evaluación contra GS", fill="#fff6e0", stroke="#c08a00", fs=13, bold=True))
b.append(arrow(610, 195, 680, 235))
b.append(arrow(610, 310, 680, 265))
b.append(artifact(680, 330, 170, 60, "Valores de métricas", fill="#fdf3e3", stroke="#c08a00", fs=12, bold=True))
b.append(arrow(765, 290, 765, 330))
b.append(text(475, 380, "Todos los tratamientos (C1a, C1b, C2a/C2b/C2c) reciben el mismo corpus de entrada.", 12, GRIS))
b.append(text(475, 398, "La actividad de evaluación recibe cada LEL producido y el Gold Standard, y es 100% determinística.", 12, GRIS))
guardar("fig_4_1_diseno_experimental.svg", svg(950, 420, "\n".join(b)))

# ---------- Fig 4.2 Pipeline del prototipo LLM ----------
b = []
b.append(text(480, 28, "Pipeline del prototipo basado en LLM", 18, AZUL, bold=True))
b.append(artifact(10, 148, 110, 64, "Transcripciones", fs=12, bold=True))
etapas = [("1. Extraer\ncandidatos", 150, AZUL_F, AZUL), ("2. Clasificar\n(S/O/V/E)", 315, AZUL_F, AZUL),
          ("3. Describir\n(noción/impacto)", 480, AZUL_F, AZUL), ("4. Auto-verificar\n(checklist)", 655, VERDE_F, VERDE)]
anchos = {150:140, 315:140, 480:150, 655:140}
for l,x,f,s in etapas:
    b.append(rect(x, 148, anchos[x], 64, l, fill=f, stroke=s, fs=12, bold=True))
b.append(arrow(120, 180, 150, 180))
b.append(arrow(290, 180, 315, 180))
b.append(arrow(455, 180, 480, 180))
b.append(arrow(630, 180, 655, 180))
b.append(artifact(815, 152, 120, 56, "LEL generado", fill=ROJO_F, stroke=ROJO, fs=13, bold=True))
b.append(arrow(795, 180, 815, 180))
prompts = [("Prompt\nExtraer", 150, 140), ("Prompt\nClasificar", 315, 140), ("Prompt\nDescribir", 480, 150), ("Prompt\nVerificar", 655, 140)]
for l,x,w in prompts:
    b.append(artifact(x, 258, w, 50, l, fill="#eef4fb", stroke=AZUL, fs=11))
    b.append(arrow(x+w/2, 258, x+w/2, 212, color=AZUL, dash=True))
b.append(text(480, 345, "Cada etapa recibe su propio prompt (artefacto de entrada) que codifica las reglas del método LEL.", 12, GRIS))
b.append(text(480, 365, "Configuraciones: C2a (básica) · C2b (multi-etapa con ejemplos) · C2c (multi-etapa + auto-verificación).", 12, GRIS))
guardar("fig_4_2_pipeline_llm.svg", svg(970, 390, "\n".join(b)))

# ---------- Fig 5.1 Actores de ecoFactory ----------
b = []
b.append(text(450, 28, "Actores del dominio de ecoFactory", 18, AZUL, bold=True))
b.append(rect(360, 165, 180, 84, "Sistema ERP (módulos integrados)", bold=True, fs=13))
b.append(rect(70, 70, 160, 58, "Dueño", fill=VERDE_F, stroke=VERDE, bold=True))
b.append(rect(670, 70, 160, 58, "Gerente Comercial", fill=VERDE_F, stroke=VERDE, bold=True))
b.append(rect(70, 286, 160, 58, "Funcional del ERP", fill=VERDE_F, stroke=VERDE, bold=True))
b.append(rect(670, 286, 160, 58, "Operario del ERP", fill=VERDE_F, stroke=VERDE, bold=True))
b.append(rect(75, 178, 150, 58, "Cliente (mayorista / minorista)", fill=GRIS_F, stroke=GRIS, fs=11))
b.append(rect(675, 178, 150, 58, "AFIP (organismo externo)", fill="#fff6e0", stroke="#c08a00", fs=11))
b.append(arrow(230, 99, 360, 180))
b.append(arrow(670, 99, 540, 180))
b.append(arrow(230, 315, 360, 235))
b.append(arrow(670, 315, 540, 235))
b.append(arrow(225, 207, 360, 207))
b.append(arrow(675, 207, 540, 207))
b.append(text(450, 400, "Los sujetos operan sobre el Sistema ERP; el Cliente y la AFIP son entidades externas que interactúan con la empresa.", 12, GRIS))
guardar("fig_5_1_actores.svg", svg(900, 420, "\n".join(b)))

# ---------- Fig 5.2 Circuito del pedido ----------
b = []
b.append(text(490, 28, "Circuito del pedido en ecoFactory", 18, AZUL, bold=True))
steps = [("Cliente realiza Pedido", AZUL_F, AZUL),
         ("Aprobación: crédito y stock", AZUL_F, AZUL),
         ("Pedido Aprobado", "#fff6e0", "#c08a00"),
         ("Orden de Entrega", AZUL_F, AZUL),
         ("Facturación + AFIP", AZUL_F, AZUL),
         ("Pedido Finalizado", "#fff6e0", "#c08a00")]
x = 20
for i,(l,f,s) in enumerate(steps):
    b.append(rect(x, 120, 140, 74, l, fill=f, stroke=s, fs=12, bold=True))
    if i < len(steps)-1:
        b.append(arrow(x+140, 157, x+160, 157))
    x += 160
b.append(text(490, 250, "Los recuadros ámbar son Estados del LEL (Pedido Aprobado, Pedido Finalizado); el resto, actividades y objetos del circuito.", 12, GRIS))
guardar("fig_5_2_circuito_pedido.svg", svg(980, 290, "\n".join(b)))

# ---------- Fig 6.1 Arquitectura del prototipo ----------
b = []
b.append(text(460, 28, "Arquitectura del prototipo", 18, AZUL, bold=True))
# entradas (izquierda) — artefactos
b.append(artifact(20, 80, 150, 54, "Corpus (entrevistas .txt)", fill=GRIS_F, stroke=GRIS, fs=11))
b.append(artifact(20, 165, 150, 54, "Prompts (4 etapas)", fill=GRIS_F, stroke=GRIS, fs=11))
b.append(artifact(20, 250, 150, 54, "config.yaml (modelo, flags)", fill=GRIS_F, stroke=GRIS, fs=11))
# centro — módulos de código (actividades)
b.append(rect(290, 70, 190, 48, "llm_client.py (abstracción de proveedor)", fill=AZUL_F, stroke=AZUL, fs=11, bold=True))
b.append(rect(290, 150, 200, 72, "pipeline_llm.py extraer · clasificar · describir · verificar", fill=AZUL_F, stroke=AZUL, fs=11, bold=True))
b.append(rect(290, 262, 200, 56, "baseline_frecuencia.py · baseline_spacy.py", fill=ROJO_F, stroke=ROJO, fs=11, bold=True))
# LEL — artefacto de datos (esquema común)
b.append(artifact(555, 160, 130, 72, "LEL (schema.py)", fill=VERDE_F, stroke=VERDE, fs=12, bold=True))
# derecha — artefactos, salvo el motor de evaluación (actividad)
b.append(artifact(740, 70, 160, 54, "Gold Standard (JSON)", fill="#fff6e0", stroke="#c08a00", fs=11, bold=True))
b.append(rect(740, 150, 160, 72, "evaluacion.py emparejamiento + métricas", fill=AZUL_F, stroke=AZUL, fs=11, bold=True))
b.append(artifact(740, 285, 160, 54, "resultados/ (LEL + reportes)", fill=GRIS_F, stroke=GRIS, fs=11, bold=True))
# flechas
b.append(arrow(170, 107, 290, 180))
b.append(arrow(170, 110, 290, 285))
b.append(arrow(170, 190, 290, 186))
b.append(arrow(170, 277, 290, 200, dash=True))
b.append(arrow(385, 118, 385, 150))
b.append(arrow(490, 186, 555, 192))
b.append(arrow(490, 290, 555, 215))
b.append(arrow(685, 196, 740, 186))
b.append(arrow(820, 124, 820, 150))
b.append(arrow(820, 222, 820, 285))
b.append(text(460, 375, "Las entradas (corpus, prompts, configuración) alimentan el pipeline y los baselines,", 11, GRIS))
b.append(text(460, 393, "que producen un LEL en un esquema común; el motor de evaluación lo compara contra el Gold Standard.", 11, GRIS))
guardar("fig_6_1_arquitectura.svg", svg(920, 410, "\n".join(b)))

# ---------- Fig 6.2 Protocolo de emparejamiento ----------
b = []
b.append(text(460, 28, "Protocolo de emparejamiento y métricas", 18, AZUL, bold=True))
b.append(rect(330, 56, 240, 40, "Por cada símbolo producido", fill=GRIS_F, stroke=GRIS, fs=12, bold=True))
b.append(rect(90, 122, 330, 48, "1. ¿Coincide el nombre normalizado con el GS?", fill=AZUL_F, stroke=AZUL, fs=12))
b.append(rect(90, 198, 330, 48, "2. ¿Coincide vía la tabla de sinónimos?", fill=AZUL_F, stroke=AZUL, fs=12))
b.append(rect(90, 274, 330, 56, "3. ¿Contención de tokens o similitud ≥ 0,85?", fill=AZUL_F, stroke=AZUL, fs=12))
b.append(rect(90, 360, 330, 48, "No a todo → FP (irrelevante / alucinación)", fill=ROJO_F, stroke=ROJO, fs=12, bold=True))
b.append(rect(600, 196, 160, 64, "VP (verdadero positivo)", fill=VERDE_F, stroke=VERDE, fs=12, bold=True))
b.append(rect(560, 300, 300, 52, "Símbolos del GS sin emparejar → FN (omisiones)", fill="#fdecee", stroke=ROJO, fs=12, bold=True))
b.append(arrow(450, 96, 255, 122))
b.append(arrow(420, 146, 600, 222, label="Sí", color=VERDE))
b.append(arrow(255, 170, 255, 198, label="No"))
b.append(arrow(420, 222, 600, 228, label="Sí", color=VERDE))
b.append(arrow(255, 246, 255, 274, label="No"))
b.append(arrow(420, 302, 600, 234, label="Sí", color=VERDE))
b.append(arrow(255, 330, 255, 360, label="No"))
b.append(rect(90, 432, 770, 46, "Métricas: Precisión = VP / (VP + FP) · Cobertura = VP / (VP + FN) · F1 = 2·P·R / (P + R)", fill="#fff6e0", stroke="#c08a00", fs=12, bold=True))
guardar("fig_6_2_emparejamiento.svg", svg(920, 500, "\n".join(b)))

# ---------- Fig 8.1 Revisión humana del LEL generado ----------
b = []
b.append(text(460, 28, "El LEL generado y la revisión humana", 18, AZUL, bold=True))
b.append(artifact(20, 120, 130, 64, "Corpus (entrevistas)", fill=GRIS_F, stroke=GRIS, fs=12))
b.append(rect(195, 120, 150, 64, "Pipeline LLM", fill=AZUL_F, stroke=AZUL, fs=12, bold=True))
b.append(artifact(390, 120, 130, 64, "LEL borrador", fill=AZUL_F, stroke=AZUL, fs=12, bold=True))
b.append(rect(560, 108, 180, 88, "Revisión del ingeniero aceptar · corregir · descartar", fill=VERDE_F, stroke=VERDE, fs=12, bold=True))
b.append(artifact(785, 120, 115, 64, "LEL validado", fill=ROJO_F, stroke=ROJO, fs=12, bold=True))
b.append(arrow(150, 152, 195, 152))
b.append(arrow(345, 152, 390, 152))
b.append(arrow(520, 152, 560, 152))
b.append(arrow(740, 152, 785, 152))
b.append(arrow_path([(650, 196), (650, 250), (270, 250), (270, 184)], label="retroalimentación: ajustar prompts", color=GRIS))
b.append(text(460, 300, "El enfoque generativo desplaza el esfuerzo humano de redactar el LEL a revisar y corregir un borrador.", 12, GRIS))
guardar("fig_8_1_revision_humana.svg", svg(920, 320, "\n".join(b)))

# ---------- Fig 9.1 Líneas de trabajo futuro ----------
b = []
b.append(text(460, 24, "Líneas de trabajo futuro", 18, AZUL, bold=True))
b.append(rect(335, 205, 250, 76, "Prototipo de construcción del LEL con IA Generativa (este trabajo)", fill=AZUL_F, stroke=AZUL, fs=12, bold=True))
ramas = [("Generación automática de Escenarios", 40, 50),
         ("Validación con organizaciones reales", 630, 50),
         ("Refinamiento post-revisión humana", 40, 205),
         ("Ajuste fino (fine-tuning) especializado", 630, 205),
         ("Más dominios y modelos", 40, 360),
         ("Integración en una herramienta de IR", 630, 360)]
for l, x, y in ramas:
    b.append(rect(x, y, 250, 64, l, fill=VERDE_F, stroke=VERDE, fs=12))
b.append(arrow(365, 205, 210, 114))
b.append(arrow(555, 205, 710, 114))
b.append(arrow(335, 243, 290, 237))
b.append(arrow(585, 243, 630, 237))
b.append(arrow(365, 281, 210, 360))
b.append(arrow(555, 281, 710, 360))
guardar("fig_9_1_trabajo_futuro.svg", svg(920, 460, "\n".join(b)))

print("Figuras generadas en", OUT)
