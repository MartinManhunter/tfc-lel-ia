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

# Nota: requirements fija anthropic>=0.34,<1.0 a propósito. El SDK 1.x eliminó el
# parámetro 'temperature' de messages.create(), que el pipeline usa para fijar la
# reproducibilidad. No instalar la 1.x.

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

En Windows (PowerShell) la variable vale solo para esa terminal. Para dejarla
persistente en el perfil del usuario:

```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
# cerrar y reabrir la terminal (y VS Code) para que la tome
```

## 4. Configurar `config.yaml`

```yaml
proveedor: anthropic     # openai | anthropic | echo | mock
modelo: ""               # COMPLETAR con el nombre del modelo vigente del proveedor
temperatura: 0.2         # baja, para favorecer reproducibilidad
```

- `proveedor`: el LLM a usar. `mock` corre **offline** (no llama a ningún modelo): reproduce el LEL de la corrida de referencia de ecoFactory, útil para demostrar el flujo sin API.
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

El proyecto incluye entrevistas de otros dominios para probar el prototipo fuera de
ecoFactory. Todos los scripts aceptan `--corpus` para apuntar a cualquier archivo:

- `data/pruebas/entrevista_tintoreria_TEST.txt` — corpus de prueba, **sin** LEL de referencia.
- `data/muestreo/` — los seis casos de muestreo (veterinaria, consultorio, universidad,
  hotel, e-commerce, farmacia), cada uno con su `gold_<dominio>.json`.

```bash
# 1) Baseline de frecuencia sobre un dominio de muestreo
python scripts/run_baseline_frecuencia.py \
    --corpus data/muestreo/entrevista_1_veterinario.txt data/muestreo/entrevista_2_recepcionista.txt \
    --out resultados/lel_baseline_veterinaria.json

# 2) Pipeline LLM sobre el mismo dominio (modelo real)
python scripts/run_pipeline_llm.py --config C2c \
    --corpus data/muestreo/entrevista_1_veterinario.txt data/muestreo/entrevista_2_recepcionista.txt \
    --out resultados/lel_llm_veterinaria.json

# 3) Evaluar contra el LEL de referencia de ese dominio
python scripts/run_evaluacion.py resultados/lel_llm_veterinaria.json \
    --gold data/muestreo/gold_veterinaria.json
```

Podés pasar **varias** entrevistas a `--corpus` (separadas por espacio) y **varios** Gold
Standards a `--gold`.

> Nota metodológica: los LEL de referencia de los casos de muestreo fueron construidos por
> el propio autor junto con las entrevistas. Sirven para verificar que el flujo corre en un
> dominio nuevo y comparar de forma indicativa, **no** como evaluación rigurosa. Para
> métricas serias, la referencia debería construirla o validarla otra persona.

---

## 7. Modo offline (sin API): validar la plomería

```bash
# En config.yaml poné  proveedor: mock   (o editalo temporalmente)
python scripts/run_pipeline_llm.py --config C2c
```

El proveedor `mock` reproduce el LEL de la corrida de referencia de ecoFactory (símbolos reales con tipo, noción e impacto), así que el
pipeline corre de punta a punta y verifica orquestación, prompts, parseo y esquema, sin
gastar llamadas a un modelo real. Es un resultado **pre-cargado**, no una inferencia en vivo, y así debe presentarse.

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
| Modelo desconocido / 404 `not_found_error` | El modelo no existe o la cuenta no tiene acceso | Listá los disponibles y pegá el identificador exacto. Los alias tipo `-latest` no siempre funcionan. |
| `` `temperature` is deprecated for this model `` | Modelos de última generación que ya no aceptan el parámetro | Usá un modelo que sí lo acepte (para no perder la temperatura fija) o dejá que el cliente reintente sin él: avisa por consola. |
| `No module named 'anthropic'` / `'openai'` | Falta el paquete del proveedor | `pip install "anthropic<1.0"` o `pip install openai`, y **reiniciar** el proceso. |
| `Could not resolve authentication method` | La API key no está en el entorno de esa terminal | Volvé a exportarla; en Windows conviene dejarla persistente (ver §3). |
| `Expecting property name enclosed in double quotes` | Respuesta JSON truncada por el límite de tokens | Subí `max_tokens` en `config.yaml`. La etapa 4 ya verifica por lotes para evitarlo. |

---

## 11. Interfaz gráfica de ejecución paso a paso (webapp)

Una pequeña interfaz web permite correr el pipeline **etapa por etapa** con un botón por
paso, ver el resultado de cada uno en pantalla y generar al final los dos reportes (el LEL
navegable y la evaluación contra el Gold Standard). No requiere dependencias adicionales
—usa la biblioteca estándar de Python— y reutiliza el mismo motor que la línea de comandos.

```bash
python webapp/app.py            # abre http://127.0.0.1:8000 en el navegador
python webapp/app.py --port 8010 --no-browser
```

En el panel de configuración se elige el **proveedor** (`mock` corre 100 % offline, sin
API; `openai` / `anthropic` requieren la API key en el entorno) y, opcionalmente, el
**modelo**, y el **corpus** sobre el que se corre. Los corpus disponibles se declaran en la
clave `corpora` de `config.yaml` (ecoFactory y los casos de muestreo); cada uno se evalúa
contra su propio LEL de referencia, y si no tiene, se genera el reporte del LEL sin métricas
de identificación. El botón «Cargar Corpus» prepara la corrida y «Reiniciar» la descarta.
Los reportes quedan en `resultados/` y se abren desde la misma interfaz.

> Con `proveedor: mock` la interfaz reproduce la corrida de referencia de ecoFactory
> (datos pre-cargados, sin llamar a ningún modelo), así que conviene usarlo con ese corpus.
> Para correr sobre otro dominio hay que usar un proveedor real.

Ver `webapp/README.md` para más detalle.
