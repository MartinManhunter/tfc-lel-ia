# Reporte de evaluación — `pln_farmacéutica`

## Evaluación contra gold_farmacéutica

- Símbolos en el GS: **15**
- Símbolos producidos: **24**
- VP = 9 · FP = 15 · FN = 6

| Métrica | Valor |
|---|---|
| Precisión | 0.375 |
| Cobertura (Recall) | 0.600 |
| F1 | 0.462 |
| Exactitud de tipo (sobre VP) | 0.667 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Cliente | Cliente | exacto | Sujeto | Sujeto | sí |
| VP | Dispensación | Dispensar Medicamento | exacto | Verbo | Verbo | sí |
| VP | Droguería | Droguería | exacto | Objeto | Sujeto | NO |
| VP | Farmacéutico | Farmacéutico | exacto | Objeto | Sujeto | NO |
| VP | Medicamento | Medicamento | exacto | Objeto | Objeto | sí |
| VP | Controlado | Medicamento Controlado | tokens | Estado | Objeto | NO |
| VP | Obra Social | Obra Social | exacto | Objeto | Objeto | sí |
| VP | Receta | Receta | exacto | Objeto | Objeto | sí |
| VP | Stock | Stock | exacto | Objeto | Objeto | sí |
| FP | Cantidad | — |  | Objeto |  |  |
| FP | Cobertura | — |  | Objeto |  |  |
| FP | Coberturas | — |  | Objeto |  |  |
| FP | Cualquier | — |  | Verbo |  |  |
| FP | Diferencia | — |  | Objeto |  |  |
| FP | Dispensar | — |  | Verbo |  |  |
| FP | Disponible | — |  | Objeto |  |  |
| FP | Entrevistador Contame | — |  | Objeto |  |  |
| FP | Especial | — |  | Objeto |  |  |
| FP | Especiales | — |  | Objeto |  |  |
| FP | Estantería | — |  | Objeto |  |  |
| FP | Medicamentos | — |  | Objeto |  |  |
| FP | Obras Sociales | — |  | Objeto |  |  |
| FP | Paciente | — |  | Objeto |  |  |
| FP | Vencimientos | — |  | Objeto |  |  |
| FN | — | Controlar Vencimiento |  |  | Verbo |  |
| FN | — | Ingresar Mercadería |  |  | Verbo |  |
| FN | — | Lote |  |  | Objeto |  |
| FN | — | Pedir a Droguería |  |  | Verbo |  |
| FN | — | Registrar en Libro |  |  | Verbo |  |
| FN | — | Vencido |  |  | Estado |  |
