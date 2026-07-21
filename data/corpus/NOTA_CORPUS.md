# Nota sobre el corpus de ecoFactory

## Composición

El corpus está formado por las **cuatro transcripciones reales** disponibles del estudio original
de ecoFactory (WER 2024). Todos los tratamientos del experimento —los baselines de PLN y el
pipeline LLM— reciben exactamente este mismo corpus:

| # | Rol | Archivo |
|---|---|---|
| 1 | Dueño | `entrevista_1_dueno.txt` |
| 2 | Gerente Comercial | `entrevista_2_gerente_comercial.txt` |
| 3 | Operario ERP | `entrevista_3_operario.txt` |
| 4 | Responsable ERP (proveedor del sistema) | `entrevista_4_responsable_erp.txt` |

El estudio original contempló cinco entrevistas; de la quinta no se conserva el audio ni la
transcripción. Esa ausencia explica parte de la brecha de recuperabilidad documentada en
`../gold/RECONCILIACION.md`.

## Sobre `simuladas_deprecadas/`

Esa carpeta contiene dos entrevistas **simuladas** por el autor (Gerente Comercial y un
responsable funcional del ERP), redactadas en una etapa previa del trabajo, cuando solo se
disponía de dos de las cuatro transcripciones reales. **No forman parte del corpus ni de ninguna
medición reportada**: se conservan únicamente como evidencia del experimento aparte que se discute
en la Sección 8.7 del documento, sobre el sesgo que introduce redactar entrevistas simuladas
conociendo de antemano el Gold Standard.

## Nota sobre la naturaleza del caso

ecoFactory es una empresa real. Lo que se simuló, en el estudio de origen, fueron los usuarios
entrevistados: los distintos roles fueron interpretados en rol, grabados y transcriptos en la
asignatura Ingeniería de Software V. Cuando en el documento se habla de «entrevistas reales» se
alude a esas cuatro transcripciones efectivamente disponibles, por oposición a cualquier entrevista
redactada por el autor para fines de prueba.
