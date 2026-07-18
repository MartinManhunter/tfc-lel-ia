# Guía para la dirección

**Trabajo Final de Carrera** — *Construcción del Modelo Léxico Extendido del Lenguaje (LEL)
mediante Inteligencia Artificial Generativa*
Autor: Martín Romano · Directora: Dra. Graciela D. S. Hadad · Universidad de Belgrano

Esta guía orienta la revisión del trabajo: qué es, qué contiene la entrega, en qué estado
está cada parte y qué queda pendiente.

---

## 1. Qué investiga el trabajo

En qué medida la **IA Generativa** (grandes modelos de lenguaje) puede **asistir la
construcción del LEL** a partir de entrevistas transcriptas, comparada con el **PLN
tradicional**. La contribución central es un **prototipo** que construye el LEL desde un
corpus y un **motor de evaluación determinístico** que lo mide contra un *Gold Standard*.
El aporte cualitativo clave del enfoque generativo es que **describe** los símbolos (noción e
impacto), algo que el PLN tradicional no puede hacer.

## 2. Qué contiene la entrega

- **La tesis**: `Tesis_TFC_Romano.docx` / `.pdf` (documento principal).
- **El prototipo** (código Python): `src/`, `scripts/`, `prompts/`, `config.yaml`.
- **Los datos**: `data/` — el caso ecoFactory (corpus + Gold Standard) y seis dominios de muestreo.
- **Los resultados**: `resultados/` — LEL producidos y reportes de evaluación.
- **Guías**: `README.md` (visión general), `INSTRUCTIVO_EJECUCION.md` (cómo correrlo).

## 3. Estado de cada parte

- **Prototipo**: funcional. Los baselines de PLN y el motor de evaluación **corren y están
  verificados**. El pipeline LLM **corre de punta a punta** (verificado offline con un proveedor
  simulado); para producir un LEL real requiere una clave de API de un proveedor.
- **Caso ecoFactory**: es una **empresa real**. Lo que se simuló, en el estudio de origen (WER 2024),
  fueron los usuarios entrevistados (interpretados en rol), no la empresa. Su LEL fue construido
  manualmente y publicado en WER 2024, y funciona como referencia **previa e independiente** del
  prototipo. Desde julio de 2026 el corpus de ecoFactory (Configuraciones A y B) es **enteramente
  real**: se recuperaron 2 transcripciones adicionales (Gerente Comercial, Responsable ERP) que
  reemplazan a las 2 entrevistas que antes se simulaban. Ver `data/corpus/NOTA_CORPUS.md`.
- **Resultados del LLM**: son una **corrida de referencia** empleando el asistente como modelo,
  con una **salvedad de contaminación** explícita (el operador tuvo exposición previa al Gold
  Standard). Se reportan como cota optimista, no como resultado definitivo.
- **Casos de muestreo** (6 dominios, distintos de ecoFactory): sus referencias fueron construidas
  por el autor, por lo que valen como **demostración de robustez/generalidad**, no como evaluación
  rigurosa.

## 4. Qué queda pendiente (y está señalado en el documento, Cap. 7.9)

1. La **corrida ciega definitiva**: ejecutar el pipeline con modelos reales (vía API), en
   condiciones ciegas y con varias corridas, para reemplazar la corrida de referencia. El
   procedimiento está documentado en `INSTRUCTIVO_EJECUCION.md`.
2. La evaluación cualitativa fina de las descripciones, frase por frase.
3. Extender el enfoque a la generación de escenarios (trabajo futuro).

## 5. Cómo correr el prototipo (opcional)

```bash
pip install -r requirements.txt
python scripts/run_baseline_frecuencia.py            # baseline, sin conexión
python scripts/run_evaluacion.py resultados/lel_baseline_frecuencia.json
```

Para el pipeline LLM se necesita una clave de API (`OPENAI_API_KEY` o `ANTHROPIC_API_KEY`) o,
para validar la mecánica sin conexión, el proveedor `mock`. Todo está detallado en el instructivo.

---

*El trabajo asume explícitamente sus limitaciones y las discute en el capítulo de amenazas a la
validez. Las decisiones metodológicas y los caveats se declaran de forma abierta a lo largo del
documento.*
