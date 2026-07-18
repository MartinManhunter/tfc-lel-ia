# Reporte de evaluación — `pln_consultorio`

## Evaluación contra gold_consultorio

- Símbolos en el GS: **14**
- Símbolos producidos: **32**
- VP = 10 · FP = 22 · FN = 4

| Métrica | Valor |
|---|---|
| Precisión | 0.312 |
| Cobertura (Recall) | 0.714 |
| F1 | 0.435 |
| Exactitud de tipo (sobre VP) | 0.600 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Consulta | Atender Consulta | exacto | Objeto | Verbo | NO |
| VP | Estudio | Estudio | exacto | Objeto | Objeto | sí |
| VP | Autorización | Gestionar Autorización | tokens | Verbo | Verbo | sí |
| VP | Historia Clínica | Historia Clínica | exacto | Objeto | Objeto | sí |
| VP | Médico | Médico | exacto | Objeto | Sujeto | NO |
| VP | Obra Social | Obra Social | exacto | Objeto | Objeto | sí |
| VP | Pacientes | Paciente | similitud | Objeto | Sujeto | NO |
| VP | Receta | Receta | exacto | Objeto | Objeto | sí |
| VP | Secretaria | Secretaria | exacto | Objeto | Sujeto | NO |
| VP | Turno | Turno | exacto | Objeto | Objeto | sí |
| FP | Abrir | — |  | Verbo |  |  |
| FP | Agenda | — |  | Objeto |  |  |
| FP | Antecedentes | — |  | Objeto |  |  |
| FP | Aparte | — |  | Objeto |  |  |
| FP | Autorizaciones | — |  | Objeto |  |  |
| FP | Consultas | — |  | Objeto |  |  |
| FP | Consultorio | — |  | Objeto |  |  |
| FP | Contame | — |  | Objeto |  |  |
| FP | Control | — |  | Objeto |  |  |
| FP | Doctor | — |  | Objeto |  |  |
| FP | Entrevistador | — |  | Objeto |  |  |
| FP | Estudios | — |  | Objeto |  |  |
| FP | Igual | — |  | Objeto |  |  |
| FP | Momento | — |  | Objeto |  |  |
| FP | Obras Sociales | — |  | Objeto |  |  |
| FP | Orden | — |  | Objeto |  |  |
| FP | Paciente Nuevo | — |  | Objeto |  |  |
| FP | Primero | — |  | Objeto |  |  |
| FP | Tiempo | — |  | Objeto |  |  |
| FP | Tratamiento | — |  | Verbo |  |  |
| FP | Turnos | — |  | Objeto |  |  |
| FP | Viene | — |  | Objeto |  |  |
| FN | — | Agendar Turno |  |  | Verbo |  |
| FN | — | Dar de Alta Paciente |  |  | Verbo |  |
| FN | — | Pedir Estudio |  |  | Verbo |  |
| FN | — | Sobreturno |  |  | Objeto |  |
