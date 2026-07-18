"""
baseline_spacy.py — Baseline de PLN tradicional con spaCy.

Segundo baseline (más sofisticado que el de frecuencia): usa análisis lingüístico real
—POS tagging, lematización, sintagmas nominales y reconocimiento de entidades (NER)—
para extraer candidatos a símbolo y asignarles un tipo tentativo:

    - Sintagmas nominales y entidades  -> candidatos (Objeto por defecto).
    - Entidades PER/ORG                -> Sujeto.
    - Lemas de verbos principales      -> Verbo.
    - Participios usados como atributo  -> Estado.

Sigue sin poder generar la Noción y el Impacto (limitación inherente del PLN clásico):
los símbolos quedan con descripción vacía. Eso es parte del resultado a evidenciar.

Requiere: pip install spacy && python -m spacy download es_core_news_md
(no se ejecuta en un entorno sin red; correr localmente).
"""
from __future__ import annotations
from typing import List
from collections import Counter
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from schema import LEL, Simbolo, STOPWORDS, normalizar

MODELO_SPACY = "es_core_news_md"


def _cargar_nlp():
    import spacy
    try:
        return spacy.load(MODELO_SPACY)
    except OSError as e:
        raise RuntimeError(
            f"No se encontró el modelo '{MODELO_SPACY}'. Instalalo con:\n"
            f"    python -m spacy download {MODELO_SPACY}") from e


def _limpiar_marcadores(texto: str) -> str:
    import re
    return re.sub(r"(?m)^\s*\[[^\]]*\]\s*$", "", texto)


def construir(corpus_paths: List[str], min_frec: int = 2, tope: int = 40, proyecto: str = "ecoFactory") -> LEL:
    nlp = _cargar_nlp()
    texto = _limpiar_marcadores("\n".join(open(p, encoding="utf-8").read()
                                          for p in corpus_paths))
    doc = nlp(texto)

    candidatos = Counter()
    tipos = {}

    # 1) Entidades nombradas -> Sujeto (PER/ORG) u Objeto (resto)
    for ent in doc.ents:
        nombre = ent.text.strip()
        if len(nombre) < 3:
            continue
        candidatos[nombre] += 1
        tipos[normalizar(nombre)] = "Sujeto" if ent.label_ in ("PER", "ORG") else "Objeto"

    # 2) Sintagmas nominales -> Objeto (o Sujeto si el núcleo es un rol/agente)
    for chunk in doc.noun_chunks:
        toks = [t for t in chunk if not t.is_stop and t.is_alpha]
        if not toks:
            continue
        nombre = " ".join(t.text for t in toks).strip()
        if len(nombre) < 3 or normalizar(nombre) in {normalizar(s) for s in STOPWORDS}:
            continue
        candidatos[nombre] += 1
        tipos.setdefault(normalizar(nombre), "Objeto")

    # 3) Verbos principales -> Verbo (por lema)
    for tok in doc:
        if tok.pos_ == "VERB" and not tok.is_stop:
            lema = tok.lemma_.strip().lower()
            if len(lema) > 3:
                candidatos[lema] += 1
                tipos[normalizar(lema)] = "Verbo"
        # 4) participios como atributo -> Estado
        if tok.pos_ == "ADJ" and tok.tag_ and "VerbForm=Part" in str(tok.morph):
            est = tok.text.strip().lower()
            if len(est) > 3:
                candidatos[est] += 1
                tipos[normalizar(est)] = "Estado"

    seleccion = [(n, f) for n, f in candidatos.most_common() if f >= min_frec][:tope]
    simbolos = [Simbolo(nombre=n.title(),
                        tipo=tipos.get(normalizar(n), "Objeto"),
                        nocion=[], impacto=[], id=f"SPACY{i+1:02d}")
                for i, (n, f) in enumerate(seleccion)]

    return LEL(proyecto=proyecto,
               conjunto="Baseline-spaCy (PLN tradicional)", simbolos=simbolos)


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(__file__))
    corpus = [os.path.join(base, "data/corpus/entrevista_1_dueno.txt"),
              os.path.join(base, "data/corpus/entrevista_4_operario.txt")]
    lel = construir(corpus)
    print(f"Candidatos (spaCy): {len(lel.simbolos)}")
    for s in lel.simbolos:
        print(f"  [{s.tipo:7}] {s.nombre}")
