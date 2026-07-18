# Reporte de evaluación — `pln_universidad`

## Evaluación contra gold_universidad

- Símbolos en el GS: **17**
- Símbolos producidos: **39**
- VP = 15 · FP = 24 · FN = 2

| Métrica | Valor |
|---|---|
| Precisión | 0.385 |
| Cobertura (Recall) | 0.882 |
| F1 | 0.536 |
| Exactitud de tipo (sobre VP) | 0.533 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Acta | Acta | exacto | Objeto | Objeto | sí |
| VP | Alumno | Alumno | exacto | Objeto | Sujeto | NO |
| VP | Aula | Aula | exacto | Objeto | Objeto | sí |
| VP | Bedel | Bedel | exacto | Objeto | Sujeto | NO |
| VP | Comisión | Comisión | exacto | Objeto | Objeto | sí |
| VP | Coordinador | Coordinador | exacto | Objeto | Sujeto | NO |
| VP | Correlativas | Correlativa | similitud | Objeto | Objeto | sí |
| VP | Cursar | Cursar | exacto | Verbo | Verbo | sí |
| VP | Docente | Docente | exacto | Objeto | Sujeto | NO |
| VP | Final | Final | exacto | Objeto | Objeto | sí |
| VP | Inscripción | Inscribir a Materia | exacto | Objeto | Verbo | NO |
| VP | Libreta | Libreta | exacto | Objeto | Objeto | sí |
| VP | Materia | Materia | exacto | Objeto | Objeto | sí |
| VP | Regularidad | Regularizada | similitud | Objeto | Estado | NO |
| VP | Asistencia | Tomar Asistencia | tokens | Objeto | Verbo | NO |
| FP | Alumnos | — |  | Objeto |  |  |
| FP | Aprueba | — |  | Objeto |  |  |
| FP | Aulas | — |  | Objeto |  |  |
| FP | Base De Datos | — |  | Objeto |  |  |
| FP | Cargo | — |  | Objeto |  |  |
| FP | Carrera | — |  | Objeto |  |  |
| FP | Casos | — |  | Objeto |  |  |
| FP | Comisiones | — |  | Objeto |  |  |
| FP | Cuatrimestre | — |  | Objeto |  |  |
| FP | Cursada | — |  | Estado |  |  |
| FP | Docentes | — |  | Objeto |  |  |
| FP | Ejemplo | — |  | Objeto |  |  |
| FP | Entrevistador | — |  | Objeto |  |  |
| FP | Examen | — |  | Objeto |  |  |
| FP | Genera | — |  | Objeto |  |  |
| FP | Horario | — |  | Objeto |  |  |
| FP | Inscribe | — |  | Objeto |  |  |
| FP | Materias | — |  | Objeto |  |  |
| FP | Parciales | — |  | Objeto |  |  |
| FP | Plan | — |  | Objeto |  |  |
| FP | Queda | — |  | Objeto |  |  |
| FP | Regular | — |  | Verbo |  |  |
| FP | Sistema | — |  | Sujeto |  |  |
| FP | Toma | — |  | Objeto |  |  |
| FN | — | Aprobada |  |  | Estado |  |
| FN | — | Cargar Nota |  |  | Verbo |  |
