"""
pipeline_llm.py — Prototipo de construcción del LEL con IA Generativa.

Implementa el pipeline multi-etapa que es el corazón de la contribución del TFC:

    1. Extracción de candidatos a símbolo        (prompts/01_extraccion.txt)
    2. Clasificación en tipos S/O/V/E             (prompts/02_clasificacion.txt)
    3. Descripción: noción e impacto por símbolo  (prompts/03_descripcion.txt)
    4. Auto-verificación contra el checklist      (prompts/04_verificacion.txt)

Las CONFIGURACIONES del experimento se controlan por banderas (Gold Standard v1.0):
    - C2a (básica)      : una sola etapa de extracción+clasificación, sin auto-verificación.
    - C2b (multi-etapa) : las cuatro etapas, sin auto-verificación.
    - C2c (completa)    : las cuatro etapas con auto-verificación final.

No accede a la red por sí mismo: usa el LLMClient configurado. Sin API key, usar el
proveedor 'echo' solo valida el armado (no produce un LEL).
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict
import os, re, json

import sys
sys.path.insert(0, os.path.dirname(__file__))
from schema import LEL, Simbolo, TIPOS
from llm_client import LLMClient, LLMConfig, get_client

PROMPTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")

# Plantillas de descripción por tipo (método de la cátedra, Hadad).
PLANTILLAS = {
    "Sujeto": ("Noción: describir quién es el sujeto, a través de su rol, posición o "
               "responsabilidad.\nImpacto: las actividades que realiza."),
    "Objeto": ("Noción: describir qué representa, sus características y su relación con "
               "otros objetos.\nImpacto: las acciones que se le aplican o que se realizan con él."),
    "Verbo": ("Noción: describir el proceso o actividad que representa mediante su "
              "propósito, e indicar quién lo ejecuta, cuándo y dónde se realiza.\n"
              "Impacto: las acciones, operaciones o procedimientos involucrados en la "
              "actividad; situaciones que impiden su realización y otras actividades o "
              "situaciones que desencadena."),
    "Estado": ("Noción: describir qué representa e identificar qué estados o actividades "
               "han conducido a este estado.\nImpacto: otros estados y actividades que "
               "pueden ocurrir a partir de este estado."),
}


@dataclass
class PipelineConfig:
    few_shot: bool = True
    auto_verificacion: bool = True
    descripcion_por_simbolo: bool = True   # si False, no genera noción/impacto (solo extrae+clasifica)


def _leer_prompt(nombre: str) -> str:
    with open(os.path.join(PROMPTS, nombre), encoding="utf-8") as f:
        return f.read()


def _parse_json(texto: str):
    """Extrae el primer bloque JSON válido de la respuesta del modelo (robusto a fences)."""
    t = texto.strip()
    t = re.sub(r"^```(?:json)?", "", t).strip()
    t = re.sub(r"```$", "", t).strip()
    # buscar el primer { o [ y su cierre balanceado
    ini = min([p for p in (t.find("{"), t.find("[")) if p != -1], default=-1)
    if ini == -1:
        raise ValueError("La respuesta no contiene JSON.")
    return json.loads(t[ini:])


def cargar_corpus(paths: List[str]) -> str:
    return "\n\n".join(open(p, encoding="utf-8").read() for p in paths)


# ---------------- etapas ----------------

SYSTEM = ("Sos un ingeniero de requisitos experto en el Léxico Extendido del Lenguaje "
          "(LEL). Respondé únicamente con JSON válido, sin texto adicional ni markdown.")


def _fill(nombre_prompt: str, **kv) -> str:
    """Rellena placeholders {CLAVE} sin romperse con las llaves literales del JSON de ejemplo."""
    t = _leer_prompt(nombre_prompt)
    for k, v in kv.items():
        t = t.replace("{" + k + "}", str(v))
    return t


def extraer_candidatos(corpus: str, cli: LLMClient) -> List[Dict]:
    user = _fill("01_extraccion.txt", TRANSCRIPCIONES=corpus)
    data = _parse_json(cli.completar(SYSTEM, user, stage="extraccion"))
    return [{"nombre": d["nombre"], "sinonimos": d.get("sinonimos", [])} for d in data]


def clasificar(candidatos: List[Dict], corpus: str, cli: LLMClient) -> Dict[str, str]:
    nombres = "\n".join(f"- {c['nombre']}" for c in candidatos)
    user = _fill("02_clasificacion.txt", CANDIDATOS=nombres, TRANSCRIPCIONES=corpus)
    data = _parse_json(cli.completar(SYSTEM, user, stage="clasificacion"))
    mapa = {}
    for d in data:
        t = d.get("tipo", "")
        mapa[d["nombre"]] = t if t in TIPOS else ""
    return mapa


def describir(simbolo: str, tipo: str, lista_simbolos: List[str],
              corpus: str, cli: LLMClient):
    user = _fill("03_descripcion.txt",
                 SIMBOLO=simbolo, TIPO=tipo,
                 PLANTILLA_TIPO=PLANTILLAS.get(tipo, ""),
                 LISTA_SIMBOLOS="\n".join(f"- {s}" for s in lista_simbolos),
                 TRANSCRIPCIONES=corpus)
    data = _parse_json(cli.completar(SYSTEM, user, stage="descripcion"))
    return data.get("nocion", []), data.get("impacto", [])


def auto_verificar(lel: LEL, corpus: str, cli: LLMClient) -> LEL:
    borrador = json.dumps(lel.to_dict(), ensure_ascii=False, indent=2)
    user = _fill("04_verificacion.txt", LEL_BORRADOR=borrador, TRANSCRIPCIONES=corpus)
    data = _parse_json(cli.completar(SYSTEM, user, stage="verificacion"))
    return LEL.from_dict(data)


# ---------------- orquestación ----------------

def construir_lel(corpus_paths: List[str],
                  llm_cfg: LLMConfig,
                  pipe_cfg: PipelineConfig | None = None,
                  proyecto: str = "ecoFactory") -> LEL:
    pipe_cfg = pipe_cfg or PipelineConfig()
    cli = get_client(llm_cfg)
    corpus = cargar_corpus(corpus_paths)

    candidatos = extraer_candidatos(corpus, cli)
    tipos = clasificar(candidatos, corpus, cli)

    nombres = [c["nombre"] for c in candidatos]
    simbolos: List[Simbolo] = []
    for i, c in enumerate(candidatos):
        nombre = c["nombre"]
        tipo = tipos.get(nombre, "")
        nocion, impacto = [], []
        if pipe_cfg.descripcion_por_simbolo and tipo:
            otros = [n for n in nombres if n != nombre]
            nocion, impacto = describir(nombre, tipo, otros, corpus, cli)
        simbolos.append(Simbolo(nombre=nombre, tipo=tipo, nocion=nocion,
                                impacto=impacto, sinonimos=c.get("sinonimos", []),
                                id=f"LLM{i+1:02d}"))

    lel = LEL(proyecto=proyecto,
              conjunto=f"LLM ({llm_cfg.proveedor}:{llm_cfg.modelo})",
              simbolos=simbolos)

    if pipe_cfg.auto_verificacion:
        lel = auto_verificar(lel, corpus, cli)
        lel.conjunto = f"LLM+verif ({llm_cfg.proveedor}:{llm_cfg.modelo})"
    return lel


# Configuraciones predefinidas del experimento
CONFIGURACIONES = {
    "C2a": PipelineConfig(few_shot=False, auto_verificacion=False, descripcion_por_simbolo=True),
    "C2b": PipelineConfig(few_shot=True,  auto_verificacion=False, descripcion_por_simbolo=True),
    "C2c": PipelineConfig(few_shot=True,  auto_verificacion=True,  descripcion_por_simbolo=True),
}
