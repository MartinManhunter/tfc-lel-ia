# Reporte de evaluación — `pln_veterinaria`

## Evaluación contra gold_veterinaria

- Símbolos en el GS: **16**
- Símbolos producidos: **15**
- VP = 10 · FP = 5 · FN = 6

| Métrica | Valor |
|---|---|
| Precisión | 0.667 |
| Cobertura (Recall) | 0.625 |
| F1 | 0.645 |
| Exactitud de tipo (sobre VP) | 0.600 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Termina La Consulta | Atender Consulta | tokens | Objeto | Verbo | NO |
| VP | Cliente | Cliente | exacto | Sujeto | Sujeto | sí |
| VP | Alta | Dar de Alta Cliente | tokens | Objeto | Verbo | NO |
| VP | Historia Clínica | Historia Clínica | exacto | Objeto | Objeto | sí |
| VP | Internada | Internado | similitud | Estado | Estado | sí |
| VP | Mascota | Mascota | exacto | Objeto | Objeto | sí |
| VP | Recepcionista | Recepcionista | exacto | Objeto | Sujeto | NO |
| VP | Turno | Turno | exacto | Objeto | Objeto | sí |
| VP | Vacuna | Vacuna | exacto | Objeto | Objeto | sí |
| VP | Veterinario | Veterinario | exacto | Objeto | Sujeto | NO |
| FP | Cobro | — |  | Objeto |  |  |
| FP | Entrevistador | — |  | Objeto |  |  |
| FP | Pasa | — |  | Objeto |  |  |
| FP | Queda | — |  | Objeto |  |  |
| FP | Sistema | — |  | Sujeto |  |  |
| FN | — | Agendar Turno |  |  | Verbo |  |
| FN | — | Cobrar Consulta |  |  | Verbo |  |
| FN | — | Receta |  |  | Objeto |  |
| FN | — | Recordatorio |  |  | Objeto |  |
| FN | — | Turno Confirmado |  |  | Estado |  |
| FN | — | Vacunar |  |  | Verbo |  |
