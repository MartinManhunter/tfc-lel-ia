# Reporte de evaluación — `lel_baseline_gimnasio`

## Evaluación contra gold_gimnasio

- Símbolos en el GS: **14**
- Símbolos producidos: **10**
- VP = 5 · FP = 5 · FN = 9

| Métrica | Valor |
|---|---|
| Precisión | 0.500 |
| Cobertura (Recall) | 0.357 |
| F1 | 0.417 |
| Exactitud de tipo (sobre VP) | 0.800 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Carnet | Carnet | exacto | Objeto | Objeto | sí |
| VP | Clases | Clase | similitud | Objeto | Objeto | sí |
| VP | Cuota | Cuota | exacto | Objeto | Objeto | sí |
| VP | Plan | Plan | exacto | Objeto | Objeto | sí |
| VP | Socio | Socio | exacto | Objeto | Sujeto | NO |
| FP | Deja | — |  | Objeto |  |  |
| FP | Dueño | — |  | Sujeto |  |  |
| FP | Entrevistador | — |  | Objeto |  |  |
| FP | Molinete | — |  | Objeto |  |  |
| FP | Paga | — |  | Objeto |  |  |
| FN | — | Armar Rutina |  |  | Verbo |  |
| FN | — | Cobrar Cuota |  |  | Verbo |  |
| FN | — | Cuota Vencida |  |  | Estado |  |
| FN | — | Cuota al Día |  |  | Estado |  |
| FN | — | Dar de Alta Socio |  |  | Verbo |  |
| FN | — | Profesor |  |  | Sujeto |  |
| FN | — | Recepcionista |  |  | Sujeto |  |
| FN | — | Reservar Clase |  |  | Verbo |  |
| FN | — | Rutina |  |  | Objeto |  |
