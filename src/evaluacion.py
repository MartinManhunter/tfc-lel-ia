"""
evaluacion.py — Protocolo de emparejamiento (matching) y métricas.

Implementa el protocolo definido en el Gold Standard v1.0 (sección 8):
clasifica cada símbolo producido como VP / FP / FN respecto de un Gold Standard,
y calcula precisión, cobertura (recall), F1, exactitud de clasificación de tipo y
matriz de confusión. Es independiente del método que generó el LEL (LLM o PLN).

El emparejamiento es determinístico para controlar el sesgo del evaluador:
  1. coincidencia exacta de nombre normalizado (o sinónimo de la tabla);
  2. un conjunto de tokens contenido en el otro;
  3. similitud de cadena (SequenceMatcher) >= UMBRAL.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from difflib import SequenceMatcher
import sys, os, json

sys.path.insert(0, os.path.dirname(__file__))
from schema import LEL, Simbolo, normalizar, tokens_significativos, TIPOS

UMBRAL_SIMILITUD = 0.85

# Tabla de sinónimos semilla (Gold Standard v1.0, sección 8.5).
# Asocia un término que puede producir un método -> nombre canónico del GS.
SINONIMOS_SEMILLA = {
    "producto": "Bolsa Ecológica / Producto",
    "bolsa ecologica": "Bolsa Ecológica / Producto",
    "bolsas ecologicas": "Bolsa Ecológica / Producto",
    "erp": "Sistema ERP",
    "sistema erp": "Sistema ERP",
    "remito": "Orden de Entrega",
    "afip": "Integración AFIP",
    "cliente": "Cliente Mayorista",   # cliente genérico -> regla de cliente (ver abajo)
    "clientes": "Cliente Mayorista",
}


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, normalizar(a), normalizar(b)).ratio()


@dataclass
class Emparejamiento:
    producido: Optional[str]
    gold: Optional[str]
    estado: str                  # "VP" | "FP" | "FN"
    score: float = 0.0
    tipo_prod: str = ""
    tipo_gold: str = ""
    tipo_ok: Optional[bool] = None
    via: str = ""                # cómo se emparejó (exacto/sinonimo/tokens/similitud)


@dataclass
class Reporte:
    gold_set: str
    n_gold: int
    n_prod: int
    vp: int
    fp: int
    fn: int
    precision: float
    cobertura: float
    f1: float
    exactitud_tipo: float
    matriz_confusion: Dict[str, Dict[str, int]]
    emparejamientos: List[Emparejamiento] = field(default_factory=list)

    def resumen(self) -> str:
        L = []
        L.append(f"Evaluación contra {self.gold_set}")
        L.append(f"  Símbolos en el GS : {self.n_gold}")
        L.append(f"  Símbolos producidos: {self.n_prod}")
        L.append(f"  VP={self.vp}  FP={self.fp}  FN={self.fn}")
        L.append(f"  Precisión = {self.precision:.3f}")
        L.append(f"  Cobertura = {self.cobertura:.3f}")
        L.append(f"  F1        = {self.f1:.3f}")
        L.append(f"  Exactitud de tipo (sobre VP) = {self.exactitud_tipo:.3f}")
        return "\n".join(L)

    def to_dict(self) -> dict:
        d = {k: getattr(self, k) for k in
             ("gold_set","n_gold","n_prod","vp","fp","fn","precision",
              "cobertura","f1","exactitud_tipo","matriz_confusion")}
        d["emparejamientos"] = [vars(e) for e in self.emparejamientos]
        return d


def _construir_indice_gold(gold: LEL):
    """Mapa nombre_normalizado -> símbolo del GS (incluye sinónimos)."""
    idx = {}
    for s in gold.simbolos:
        for n in s.nombres():
            idx[normalizar(n)] = s
    return idx


def _match_gold(nombre_prod: str, gold: LEL, idx: dict, usados: set) -> Tuple[Optional[Simbolo], float, str]:
    norm = normalizar(nombre_prod)
    # 1) exacto por nombre/sinónimo del GS
    if norm in idx and idx[norm].id not in usados:
        return idx[norm], 1.0, "exacto"
    # 2) tabla de sinónimos semilla
    if norm in SINONIMOS_SEMILLA:
        canon = normalizar(SINONIMOS_SEMILLA[norm])
        if canon in idx and idx[canon].id not in usados:
            return idx[canon], 0.99, "sinonimo"
    # 3) contención de tokens significativos
    tp = tokens_significativos(nombre_prod)
    mejor, mejor_score, via = None, 0.0, ""
    for s in gold.simbolos:
        if s.id in usados:
            continue
        for n in s.nombres():
            tg = tokens_significativos(n)
            if tp and tg and (tp <= tg or tg <= tp):
                score = len(tp & tg) / max(len(tp | tg), 1)
                if score > mejor_score:
                    mejor, mejor_score, via = s, max(score, 0.9), "tokens"
            # 4) similitud de cadena
            sim = _similar(nombre_prod, n)
            if sim >= UMBRAL_SIMILITUD and sim > mejor_score:
                mejor, mejor_score, via = s, sim, "similitud"
    return mejor, mejor_score, via


def evaluar(producido: LEL, gold: LEL, gold_set_nombre: str = "") -> Reporte:
    # Robustez: el emparejamiento rastrea los símbolos del gold ya usados por su 'id';
    # si algún símbolo no trae id (p. ej. un gold construido en memoria), se le asigna
    # uno sintético y único para evitar colisiones.
    for i, s in enumerate(gold.simbolos):
        if not s.id:
            s.id = f"_g{i:03d}"
    idx = _construir_indice_gold(gold)
    usados = set()
    emparejamientos: List[Emparejamiento] = []
    vp = 0

    # Ordenar producidos por mejor score potencial para un matching greedy estable
    candidatos = []
    for sp in producido.simbolos:
        s, score, via = _match_gold(sp.nombre, gold, idx, set())  # sin 'usados' para rankear
        candidatos.append((score, sp, s, via))
    candidatos.sort(key=lambda x: -x[0])

    matched_prod = set()
    for score, sp, _, _ in candidatos:
        s, sc, via = _match_gold(sp.nombre, gold, idx, usados)
        if s is not None and sc > 0:
            usados.add(s.id)
            matched_prod.add(id(sp))
            tipo_ok = (sp.tipo == s.tipo) if sp.tipo else None
            emparejamientos.append(Emparejamiento(
                producido=sp.nombre, gold=s.nombre, estado="VP", score=round(sc, 3),
                tipo_prod=sp.tipo, tipo_gold=s.tipo, tipo_ok=tipo_ok, via=via))
            vp += 1

    # Falsos positivos: producidos sin emparejar
    for sp in producido.simbolos:
        if id(sp) not in matched_prod:
            emparejamientos.append(Emparejamiento(
                producido=sp.nombre, gold=None, estado="FP", tipo_prod=sp.tipo))

    # Falsos negativos: símbolos del GS no cubiertos
    for s in gold.simbolos:
        if s.id not in usados:
            emparejamientos.append(Emparejamiento(
                producido=None, gold=s.nombre, estado="FN", tipo_gold=s.tipo))

    fp = sum(1 for e in emparejamientos if e.estado == "FP")
    fn = sum(1 for e in emparejamientos if e.estado == "FN")
    precision = vp / (vp + fp) if (vp + fp) else 0.0
    cobertura = vp / (vp + fn) if (vp + fn) else 0.0
    f1 = 2 * precision * cobertura / (precision + cobertura) if (precision + cobertura) else 0.0

    # Exactitud de tipo y matriz de confusión (solo sobre VP con tipo asignado)
    matriz = {g: {p: 0 for p in TIPOS + ("(sin tipo)",)} for g in TIPOS}
    ok = tot = 0
    for e in emparejamientos:
        if e.estado == "VP" and e.tipo_gold in TIPOS:
            col = e.tipo_prod if e.tipo_prod in TIPOS else "(sin tipo)"
            matriz[e.tipo_gold][col] += 1
            if e.tipo_prod:
                tot += 1
                ok += 1 if e.tipo_prod == e.tipo_gold else 0
    exactitud_tipo = ok / tot if tot else 0.0

    return Reporte(gold_set=gold_set_nombre or gold.conjunto or "GS",
                   n_gold=len(gold.simbolos), n_prod=len(producido.simbolos),
                   vp=vp, fp=fp, fn=fn, precision=precision, cobertura=cobertura,
                   f1=f1, exactitud_tipo=exactitud_tipo, matriz_confusion=matriz,
                   emparejamientos=emparejamientos)


def reporte_markdown(rep: Reporte) -> str:
    L = [f"## Evaluación contra {rep.gold_set}", "",
         f"- Símbolos en el GS: **{rep.n_gold}**",
         f"- Símbolos producidos: **{rep.n_prod}**",
         f"- VP = {rep.vp} · FP = {rep.fp} · FN = {rep.fn}",
         "",
         "| Métrica | Valor |", "|---|---|",
         f"| Precisión | {rep.precision:.3f} |",
         f"| Cobertura (Recall) | {rep.cobertura:.3f} |",
         f"| F1 | {rep.f1:.3f} |",
         f"| Exactitud de tipo (sobre VP) | {rep.exactitud_tipo:.3f} |",
         "",
         "### Detalle de emparejamientos", "",
         "| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |",
         "|---|---|---|---|---|---|---|"]
    orden = {"VP": 0, "FP": 1, "FN": 2}
    for e in sorted(rep.emparejamientos, key=lambda x: (orden[x.estado], x.gold or x.producido or "")):
        L.append(f"| {e.estado} | {e.producido or '—'} | {e.gold or '—'} | {e.via or ''} "
                 f"| {e.tipo_prod or ''} | {e.tipo_gold or ''} | "
                 f"{'' if e.tipo_ok is None else ('sí' if e.tipo_ok else 'NO')} |")
    return "\n".join(L)
