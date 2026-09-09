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

1. **Configuración.** Se elige el proveedor de LLM, opcionalmente el modelo, y el corpus:

   - `mock` — corre **100 % offline**, sin llamar a ningún modelo. Reproduce la corrida de
     referencia de ecoFactory: devuelve sus símbolos reales, con tipo, noción e impacto.
     Es un resultado **pre-cargado**, no una inferencia en vivo, y así debe presentarse.
   - `anthropic` / `openai` — usan el modelo real; requieren la API key en el entorno
     (`ANTHROPIC_API_KEY` / `OPENAI_API_KEY`), igual que la línea de comandos. El
     identificador del modelo es obligatorio y debe ser uno vigente para esa cuenta.

   La interfaz arranca en `mock` por defecto; el modelo por defecto se toma de `config.yaml`.

2. **Corpus.** El desplegable lista los corpus declarados en la clave `corpora` de
   `config.yaml`: el de ecoFactory (las cuatro entrevistas reales) y los casos de muestreo
   ya documentados en el trabajo, más un corpus de prueba. Cada corpus se evalúa contra
   **su propio** LEL de referencia; si no tiene ninguno, se genera el reporte del LEL sin
   métricas de identificación, aclarándolo en el reporte.

   > Como el modo `mock` sirve datos pre-cargados de ecoFactory, conviene usarlo con ese
   > corpus. Para correr sobre otro dominio hay que usar un proveedor real.

3. **Cargar Corpus / Reiniciar.** Carga las entrevistas del corpus elegido y las muestra.

4. **Un botón por etapa del pipeline**, habilitados en secuencia:
   1. **Extraer Candidatos** — términos del dominio hallados en las entrevistas.
   2. **Clasificar Símbolos** — tipo Sujeto / Objeto / Verbo / Estado de cada término.
   3. **Describir Símbolos** — noción e impacto de cada símbolo.
   4. **Auto-Verificar** — revisión del borrador contra el checklist del LEL. Se procesa
      **por lotes** de símbolos, para que la respuesta del modelo no se trunque.

5. **Generar los dos Reportes** — produce y enlaza:
   - `resultados/reporte_lel_gui.html` — el LEL navegable, agrupado por tipo.
   - `resultados/reporte_evaluacion_lel_gui.html` — las métricas (precisión, cobertura, F1,
     exactitud de tipo, % con descripciones) contra el LEL de referencia del corpus.

   También deja el LEL en `resultados/lel_gui.json` y el reporte de evaluación en `.md`.

## Detalles de presentación

Los nombres de los símbolos se normalizan con **mayúscula inicial** apenas se extraen, de
modo que viajen así a la clasificación, la descripción, el LEL y los reportes. No afecta la
evaluación: el emparejamiento normaliza a minúsculas y sin acentos.

La interfaz adopta la identidad visual de la Universidad de Belgrano y reutiliza el sistema
de tarjetas y colores por tipo de símbolo del reporte HTML, de modo que la herramienta y sus
salidas forman un conjunto coherente.

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
