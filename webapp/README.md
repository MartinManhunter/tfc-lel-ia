# Interfaz gráfica de ejecución paso a paso

Una pequeña aplicación web que ejecuta el prototipo de construcción del LEL **etapa por
etapa**, con un botón por paso, mostrando el resultado de cada uno en pantalla y generando
al final los dos reportes del trabajo.

No reimplementa nada: **reutiliza el mismo motor que la línea de comandos** (`src/pipeline_llm.py`,
`src/evaluacion.py`, `scripts/reporte_lel_html.py`). Lo que la interfaz muestra es fiel a lo
que produce la ejecución por consola.

## Cómo se corre

No requiere dependencias adicionales: usa la biblioteca estándar de Python (`http.server`)
y `pyyaml` (que ya está en `requirements.txt`).

```bash
# desde la raíz del repositorio
python webapp/app.py                    # abre http://127.0.0.1:8000
python webapp/app.py --port 8010        # otro puerto
python webapp/app.py --no-browser       # no abrir el navegador automáticamente
```

## Qué hace

1. **Configuración.** Se elige el proveedor de LLM y, opcionalmente, el modelo:
   - `mock` — corre **100 % offline**, sin llamar a ningún modelo (ideal para demostrar el
     flujo sin API). Es el modo recomendado para una demostración.
   - `anthropic` / `openai` — usan el modelo real; requieren la API key en el entorno
     (`ANTHROPIC_API_KEY` / `OPENAI_API_KEY`), igual que la línea de comandos.
   El valor por defecto se toma de `config.yaml`.

2. **Cargar corpus / Reiniciar.** Carga el corpus de ecoFactory definido en `config.yaml`
   y muestra las entrevistas de entrada.

3. **Un botón por etapa del pipeline**, habilitados en secuencia:
   1. **Extraer candidatos** — términos del dominio hallados en las entrevistas.
   2. **Clasificar símbolos** — tipo Sujeto / Objeto / Verbo / Estado de cada término.
   3. **Describir símbolos** — noción e impacto de cada símbolo (lo que el PLN no hace).
   4. **Auto-verificar** — revisión del borrador contra el checklist del LEL.

4. **Generar los dos reportes** — produce y enlaza:
   - `resultados/reporte_lel_gui.html` — el LEL navegable (símbolos por tipo, con noción e
     impacto).
   - `resultados/reporte_evaluacion_lel_gui.html` — las métricas (precisión, cobertura, F1,
     exactitud de tipo, % con descripciones) contra GS-Corpus y GS-Completo.
   También deja el LEL en `resultados/lel_gui.json` y el reporte de evaluación en `.md`.

## Diseño

Adopta la identidad visual de la Universidad de Belgrano (paleta navy + acento rojo) y
reutiliza el mismo sistema de tarjetas, colores por tipo de símbolo y tipografía del reporte
HTML del LEL, de modo que la herramienta y sus reportes forman un conjunto coherente.

## Archivos

```
webapp/
├── app.py                 servidor (biblioteca estándar) + orquestación de las etapas
├── templates/
│   └── index.html         interfaz (HTML + CSS + JS, sin frameworks)
└── README.md              este archivo
```

> Las salidas que genera la interfaz (`resultados/*gui*`) están en `.gitignore`: son
> artefactos de runtime y no se versionan.
