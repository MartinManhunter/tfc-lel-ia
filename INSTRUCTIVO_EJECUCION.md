# Instructivo de ejecución — Prototipo de construcción del LEL con IA Generativa

Esta guía explica cómo correr el prototipo de punta a punta: los baselines de PLN, el
pipeline basado en LLM y la evaluación, tanto sobre el caso ecoFactory como sobre
**cualquier entrevista nueva** (por ejemplo, la entrevista de testing incluida).

---

## 1. Requisitos previos

- **Python 3.10+**
- Una clave de API de **OpenAI** o **Anthropic** (solo para el pipeline LLM real).
- Acceso a internet (solo para el pipeline LLM real; los baselines y la evaluación funcionan sin red).

## 2. Instalación

```bash
cd tfc-lel-ia
python -m venv .venv && source .venv/bin/activate      # opcional pero recomendado
pip install -r requirements.txt

# Solo si vas a usar el baseline spaCy (C1b): bajar el modelo de español
python -m spacy download es_core_news_md
```

## 3. Configurar la API key

La clave **se lee de una variable de entorno**; nunca se escribe en el código.

```bash
# Según el proveedor que vayas a usar:
export OPENAI_API_KEY="sk-..."
# o bien
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 4. Configurar `config.yaml`

```yaml
proveedor: anthropic     # openai | anthropic | echo | mock
modelo: ""               # COMPLETAR con el nombre del modelo vigente del proveedor
temperatura: 0.2         # baja, para favorecer reproducibilidad
```

- `proveedor`: el LLM a usar. `mock` corre **offline** (no llama a ningún modelo; valida la plomería).
- `modelo`: el identificador del modelo según la documentación vigente del proveedor
  (los nombres cambian; consultá la doc de OpenAI/Anthropic y pegá el string exacto).

---

## 5. Ejecución sobre el caso ecoFactory

Todos los scripts se corren desde la raíz del proyecto. Las salidas quedan en `resultados/`.

```bash
# (C1a) Baseline de frecuencia — usa el corpus por defecto de config.yaml
python scripts/run_baseline_frecuencia.py

# (C1b) Baseline spaCy  (requiere es_core_news_md)
python scripts/run_baseline_spacy.py

# (C2a/C2b/C2c) Pipeline LLM — requiere proveedor real + API key
python scripts/run_pipeline_llm.py --config C2c

# Evaluar cualquier LEL producido contra los Gold Standards de ecoFactory
python scripts/run_evaluacion.py resultados/lel_llm_C2c.json
```

`run_evaluacion.py` imprime el resumen (VP/FP/FN, precisión, cobertura, F1, exactitud de
tipo) y guarda un reporte en `resultados/reporte_<nombre>.md`.

---

## 6. Probar con una entrevista nueva (entrevista de testing)

El proyecto incluye una entrevista de prueba de un dominio distinto (un gimnasio) en
`data/testing/`. Todos los scripts aceptan `--corpus` para apuntar a cualquier archivo:

```bash
# 1) Baseline de frecuencia sobre la entrevista de testing
python scripts/run_baseline_frecuencia.py \
    --corpus data/testing/entrevista_test_gimnasio.txt \
    --out resultados/lel_baseline_gimnasio.json

# 2) Pipeline LLM sobre la entrevista de testing (modelo real)
python scripts/run_pipeline_llm.py --config C2c \
    --corpus data/testing/entrevista_test_gimnasio.txt \
    --out resultados/lel_llm_gimnasio.json

# 3) Evaluar contra la referencia del gimnasio (incluida, "a validar")
python scripts/run_evaluacion.py resultados/lel_llm_gimnasio.json \
    --gold data/testing/gold_gimnasio.json
```

Podés pasar **varias** entrevistas a `--corpus` (separadas por espacio) y **varios** Gold
Standards a `--gold`.

> Nota metodológica: el LEL de referencia del gimnasio (`gold_gimnasio.json`) es una
> **referencia inicial a validar**. Como fue redactada junto con la entrevista, sirve para
> ver que el flujo corre y comparar de forma indicativa, **no** como evaluación rigurosa.
> Para métricas serias, conviene que la referencia la construya/valide otra persona.

---

## 7. Modo offline (sin API): validar la plomería

```bash
# En config.yaml poné  proveedor: mock   (o editalo temporalmente)
python scripts/run_pipeline_llm.py --config C2c \
    --corpus data/testing/entrevista_test_gimnasio.txt
```

El proveedor `mock` devuelve respuestas con el formato correcto de cada etapa, así que el
pipeline corre de punta a punta y verifica orquestación, prompts, parseo y esquema, sin
gastar llamadas a un modelo real. (No produce un LEL con contenido real.)

---

## 8. Corrida ciega definitiva (benchmark multi-modelo)

Para que los resultados del LLM sean evidencia rigurosa (y no una corrida de referencia),
conviene seguir este protocolo:

1. **No mirar el Gold Standard** mientras se preparan/corren los prompts (evita contaminación).
2. Correr cada configuración **C2a, C2b y C2c** sobre **2–3 modelos** distintos
   (p. ej. uno de OpenAI y uno de Anthropic), cambiando solo `config.yaml`.
3. Hacer **3–5 corridas por combinación** (modelo × configuración) con `temperatura: 0.2`
   para estimar la variabilidad; conservar todas las salidas crudas en `resultados/`.
4. Evaluar cada LEL producido con `run_evaluacion.py` contra `GS-Corpus` (medición primaria,
   corpus real de 2 entrevistas) y `GS-Completo` (corpus extendido de 4 entrevistas).
5. Reportar promedio y dispersión por métrica, y un análisis cualitativo de los falsos
   positivos y de la calidad de las descripciones.

```bash
# Ejemplo de barrido (editá config.yaml entre corridas para cambiar de modelo)
for cfg in C2a C2b C2c; do
  python scripts/run_pipeline_llm.py --config $cfg --out resultados/lel_${cfg}_modeloX.json
  python scripts/run_evaluacion.py resultados/lel_${cfg}_modeloX.json
done
```

---

## 9. Dónde quedan las salidas

- `resultados/lel_*.json` — los LEL producidos por cada método/corrida.
- `resultados/reporte_*.md` — los reportes de evaluación (tablas con métricas).

## 10. Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| `EchoClient activo: no hay acceso a un modelo` | `proveedor: echo` | Poné `openai`/`anthropic` (con key) o `mock`. |
| Error de autenticación / 401 | API key ausente o inválida | Revisá la variable de entorno `*_API_KEY`. |
| `OSError: [E050] ... es_core_news_md` | Falta el modelo de spaCy | `python -m spacy download es_core_news_md`. |
| La respuesta no contiene JSON | El modelo devolvió prosa | Bajá la temperatura; el parser ya tolera fences ```. |
| Modelo desconocido | `modelo` mal escrito en `config.yaml` | Pegá el identificador exacto de la doc del proveedor. |
