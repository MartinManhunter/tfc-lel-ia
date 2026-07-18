"""
baseline_frecuencia.py — Baseline de PLN tradicional (réplica del antecedente UB).

Reproduce el enfoque clásico de construcción de un *bosquejo* del LEL: análisis de
frecuencia sobre el texto + extracción de candidatos a símbolo (n-gramas) + un corte
tipo Pareto, con una clasificación de tipo (S/O/V/E) por heurísticas superficiales.

Es deliberadamente "poco profundo": un método de frecuencia identifica TÉRMINOS
candidatos razonablemente bien, pero NO puede generar la noción ni el impacto, y su
clasificación de tipo es frágil. Esa limitación es justamente lo que el experimento
busca evidenciar frente al enfoque con LLM. Por eso los símbolos producidos quedan
con noción e impacto vacíos.

No requiere modelos ni red: usa solo la biblioteca estándar.
"""
from __future__ import annotations
from typing import List, Dict
from collections import Counter
import re, sys, os

sys.path.insert(0, os.path.dirname(__file__))
from schema import LEL, Simbolo, STOPWORDS, quitar_acentos, normalizar

# Léxico mínimo para la heurística de tipo (NO específico de ecoFactory salvo roles obvios).
PISTAS_SUJETO = {"cliente","clientes","operario","operarios","gerente","dueño","dueno",
                 "empresa","area","área","sistema","usuario","proveedor","responsable",
                 "consultora","afip","equipo","departamento"}
PISTAS_ESTADO_SUF = ("ado","ido","ada","ida","ados","idos","ando","iendo")
PISTAS_ESTADO = {"manual","automatico","automático","pendiente","aprobado","finalizado",
                 "listo","activo","vigente"}
VERBO_SUF = ("ar","er","ir","ación","acion","miento")

# Palabras genéricas que un analista competente filtraría aunque sean frecuentes.
# Incluye nombres de los entrevistadores (no son símbolos del dominio).
RUIDO = {"informacion","información","proceso","procesos","documento","documentos",
         "dato","datos","empresa","tema","temas","trabajo","cosa","cosas","modulo",
         "módulo","modulos","módulos","martin","martín","federico","consultora"}


def tokenizar(texto: str) -> List[str]:
    # Quitar marcadores de hablante "[Nombre]" (no son contenido hablado)
    texto = re.sub(r"(?m)^\s*\[[^\]]*\]\s*$", "", texto)
    palabras = re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]+", texto.lower())
    return palabras


def _es_stop(w: str) -> bool:
    return quitar_acentos(w) in {quitar_acentos(s) for s in STOPWORDS} or len(w) <= 2


def extraer_ngramas(palabras: List[str], n: int) -> Counter:
    cont = Counter()
    for i in range(len(palabras) - n + 1):
        gram = palabras[i:i + n]
        if _es_stop(gram[0]) or _es_stop(gram[-1]):
            continue
        if any(re.fullmatch(r"\d+", g) for g in gram):
            continue
        cont[" ".join(gram)] += 1
    return cont


def clasificar_tipo(nombre: str) -> str:
    base = quitar_acentos(nombre.lower())
    cab = base.split()[0]
    ult = base.split()[-1]
    if any(t in PISTAS_SUJETO for t in base.split()):
        return "Sujeto"
    if ult in {quitar_acentos(x) for x in PISTAS_ESTADO} or ult.endswith(PISTAS_ESTADO_SUF):
        # un adjetivo/participio suelto -> posible Estado
        if len(base.split()) == 1:
            return "Estado"
    if cab.endswith(VERBO_SUF) or ult.endswith(("acion","ación","miento")):
        return "Verbo"
    return "Objeto"


def construir(corpus_paths: List[str],
              proyecto: str = "ecoFactory",
              min_frec: int = 2,
              pareto: float = 0.80,
              tope: int = 40) -> LEL:
    """
    min_frec : frecuencia mínima para considerar un candidato.
    pareto   : corte de frecuencia acumulada (0..1) sobre los candidatos ordenados.
    tope     : número máximo de candidatos a retener.
    """
    texto = "\n".join(open(p, encoding="utf-8").read() for p in corpus_paths)
    palabras = tokenizar(texto)

    frec = Counter()
    for n in (3, 2, 1):
        frec.update(extraer_ngramas(palabras, n))

    # Filtrado: frecuencia mínima y ruido genérico
    cand = [(t, f) for t, f in frec.items()
            if f >= min_frec and normalizar(t) not in {normalizar(r) for r in RUIDO}]
    cand.sort(key=lambda x: (-x[1], x[0]))

    # Corte tipo Pareto sobre frecuencia acumulada + tope
    total = sum(f for _, f in cand) or 1
    acum, seleccion = 0, []
    for t, f in cand:
        seleccion.append((t, f))
        acum += f
        if acum / total >= pareto or len(seleccion) >= tope:
            break

    # Evitar candidatos contenidos en otro ya seleccionado más largo (p. ej. "ecologicas" ⊂ "bolsas ecologicas")
    nombres = [t for t, _ in seleccion]
    final = []
    for t, f in seleccion:
        nt = normalizar(t)
        if any(nt != normalizar(o) and nt in normalizar(o).split() and len(o.split()) > len(t.split())
               for o in nombres):
            continue
        final.append((t, f))

    simbolos = [Simbolo(nombre=t.title(), tipo=clasificar_tipo(t),
                        nocion=[], impacto=[],
                        id=f"FREQ{idx+1:02d}")
                for idx, (t, f) in enumerate(final)]

    return LEL(proyecto=proyecto, conjunto="Baseline-Frecuencia (PLN tradicional)",
               simbolos=simbolos)


if __name__ == "__main__":
    import json
    base = os.path.dirname(os.path.dirname(__file__))
    corpus = [os.path.join(base, "data/corpus/entrevista_1_dueno.txt"),
              os.path.join(base, "data/corpus/entrevista_4_operario.txt")]
    lel = construir(corpus)
    print(f"Candidatos a símbolo extraídos: {len(lel.simbolos)}")
    for s in lel.simbolos:
        print(f"  [{s.tipo:7}] {s.nombre}")
