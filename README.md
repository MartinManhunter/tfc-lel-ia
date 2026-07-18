# Construcción del LEL con IA Generativa — Prototipo y experimentación

Repositorio del Trabajo Final de Carrera *"Construcción del Modelo Léxico Extendido del
Lenguaje mediante Inteligencia Artificial Generativa"* (Licenciatura en Sistemas de
Información, Universidad de Belgrano).

**Autor:** Martín Romano · **Directora:** Dra. Graciela D. S. Hadad

---

## De qué se trata

El trabajo estudia **en qué medida la Inteligencia Artificial Generativa puede asistir la
construcción del Léxico Extendido del Lenguaje (LEL)** a partir de entrevistas transcriptas,
frente al Procesamiento de Lenguaje Natural (PLN) tradicional. El núcleo es:

- un **prototipo** que construye un LEL desde un corpus de entrevistas, mediante un pipeline
  LLM de cuatro etapas (extraer → clasificar → describir → auto-verificar), y
- un **motor de evaluación determinístico** que mide cualquier LEL producido contra un
  *Gold Standard* (un LEL de referencia construido manualmente), sin intervención de IA.

Se comparan tres enfoques sobre el mismo corpus y el mismo Gold Standard:

| Sigla | Enfoque | Qué hace |
|-------|---------|----------|
| **C1a** | Baseline de frecuencia | PLN tradicional: n-gramas, frecuencia, corte tipo Pareto. Réplica del antecedente de la UB. |
| **C1b** | Baseline spaCy | PLN tradicional con POS / NER / lematización. |
| **C2a/b/c** | Pipeline LLM | IA Generativa en cuatro etapas, en tres configuraciones de complejidad creciente. |

El caso principal es **ecoFactory**, una empresa real cuyo LEL fue construido manualmente y
publicado por el autor en el *Workshop em Engenharia de Requisitos* (WER 2024), a partir de
cuatro entrevistas reales del estudio original. Se complementa con **seis dominios de muestreo
adicionales** (veterinaria, consultorio médico, universidad, hotel, e-commerce, farmacéutica)
para explorar la generalidad del enfoque.

## Resultados (resumen)

Sobre el corpus de cuatro entrevistas reales de ecoFactory, comparando contra el
**GS-Recuperable** (los 15 símbolos con sustento textual en el corpus):

| Métrica | Baseline frecuencia (C1a) | Pipeline LLM (C2c) |
|---------|:---:|:---:|
| Precisión | 0,175 | 0,474 |
| Cobertura | 0,467 | 0,600 |
| F1 | 0,255 | 0,529 |
| Exactitud de tipo | 0,571 | 0,889 |
| **Descripciones** | **0 %** | **100 %** |

La diferencia decisiva es la última fila: el PLN no genera descripciones (noción e impacto),
y el enfoque generativo las genera para todos los símbolos. En los seis dominios de muestreo el
patrón se repite (LLM F1 promedio ≈ 0,90 frente a ≈ 0,50 del PLN por frecuencia).

> **Estado honesto de los resultados.** Los valores del pipeline LLM provienen de una
> **corrida de referencia** en la que las etapas fueron ejecutadas por un asistente de IA en
> lugar de un modelo llamado por API, y arrastran una **salvedad de contaminación del operador**
> (exposición previa al Gold Standard durante el desarrollo). Los casos de muestreo usan
> referencias construidas por el autor, por lo que valen como demostración de robustez y no como
> evaluación independiente. La **corrida ciega definitiva** con modelos comerciales vía API, y la
> ejecución de C1b, quedan como el paso que consolida el experimento (ver
> `INSTRUCTIVO_EJECUCION.md`). Todo lo necesario está implementado; falta únicamente el acceso a
> la API y correr los scripts.

## Estructura del repositorio

```
.
├── src/                    Código fuente del prototipo y los baselines
│   ├── pipeline_llm.py       Pipeline LLM de 4 etapas (C2a/b/c)
│   ├── baseline_frecuencia.py  Baseline de frecuencia (C1a)
│   ├── baseline_spacy.py     Baseline spaCy (C1b)
│   ├── llm_client.py         Abstracción de proveedor (OpenAI / Anthropic / echo)
│   └── schema.py             Esquema común del LEL (Símbolo, LEL)
├── scripts/                Puntos de entrada ejecutables
│   ├── run_baseline_frecuencia.py
│   ├── run_baseline_spacy.py
│   ├── run_pipeline_llm.py
│   └── run_evaluacion.py     Motor de evaluación determinístico
├── prompts/                Los 4 prompts del pipeline (una etapa cada uno)
├── data/
│   ├── corpus/               Las 4 entrevistas reales de ecoFactory (+ NOTA_CORPUS.md)
│   ├── gold/                 Gold Standards en JSON (completo y recuperable)
│   └── muestreo/             Los 6 dominios adicionales con sus entrevistas y Gold Standards
├── resultados/             Salidas de las corridas (LEL generados + reportes)
├── config.yaml             Configuración (proveedor, modelo, temperatura, corpus)
├── requirements.txt        Dependencias de Python
├── INSTRUCTIVO_EJECUCION.md  Cómo correr cada tratamiento paso a paso
├── GUIA_PARA_LA_DIRECCION.md Guía de lectura del repositorio
└── Tesis_TFC_Romano.pdf    El documento del trabajo
```

> El repositorio incluye también `build_docx.js` y `gen_figuras*.py`, que generan el documento
> y sus figuras; no son parte del prototipo evaluado.

## Cómo empezar

Requisitos: Python 3.10+.

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. (opcional) Validar el pipeline sin acceso a red, con un proveedor simulado
#    En config.yaml: proveedor: echo
python scripts/run_pipeline_llm.py

# 3. Correr el baseline de frecuencia (C1a) — determinístico, sin dependencias externas
python scripts/run_baseline_frecuencia.py
python scripts/run_evaluacion.py resultados/lel_baseline_frecuencia.json \
    --gold data/gold/gs_corpus_extendido.json data/gold/gs_completo.json

# 4. Correr el baseline spaCy (C1b) — requiere el modelo de español (sin API)
python -m spacy download es_core_news_md
python scripts/run_baseline_spacy.py

# 5. Correr el pipeline LLM con un modelo real (requiere API key)
#    En config.yaml: proveedor: anthropic|openai, y completar 'modelo'
export ANTHROPIC_API_KEY="..."      # o OPENAI_API_KEY
python scripts/run_pipeline_llm.py --config C2c
python scripts/run_evaluacion.py resultados/lel_llm_C2c.json \
    --gold data/gold/gs_corpus_extendido.json data/gold/gs_completo.json
```

El detalle completo de cada paso, incluido el protocolo de la corrida ciega (2–3 modelos,
3–5 corridas por combinación), está en **`INSTRUCTIVO_EJECUCION.md`**.

## Licencia y uso

Trabajo académico de la Universidad de Belgrano. Para consultas sobre su reutilización,
contactar al autor o a la dirección del trabajo.
