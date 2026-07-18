# Reporte de evaluación — `pln_hotel`

## Evaluación contra gold_hotel

- Símbolos en el GS: **15**
- Símbolos producidos: **25**
- VP = 9 · FP = 16 · FN = 6

| Métrica | Valor |
|---|---|
| Precisión | 0.360 |
| Cobertura (Recall) | 0.600 |
| F1 | 0.450 |
| Exactitud de tipo (sobre VP) | 0.444 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Check Out | Check-out | exacto | Objeto | Verbo | NO |
| VP | Cuenta | Cuenta | exacto | Objeto | Objeto | sí |
| VP | Disponible | Disponible | exacto | Objeto | Estado | NO |
| VP | Habitaciones | Habitación | similitud | Objeto | Objeto | sí |
| VP | Huésped Llega | Huésped | tokens | Objeto | Sujeto | NO |
| VP | Llave | Llave | exacto | Objeto | Objeto | sí |
| VP | Hotel Recepcionista | Recepcionista | tokens | Objeto | Sujeto | NO |
| VP | Reserva | Reserva | exacto | Objeto | Objeto | sí |
| VP | Disponibilidad | Verificar Disponibilidad | tokens | Objeto | Verbo | NO |
| FP | Agencia | — |  | Objeto |  |  |
| FP | Agencias | — |  | Objeto |  |  |
| FP | Bloqueada | — |  | Estado |  |  |
| FP | Cargado | — |  | Estado |  |  |
| FP | Consume | — |  | Objeto |  |  |
| FP | Desayuno | — |  | Objeto |  |  |
| FP | Distintas | — |  | Objeto |  |  |
| FP | Durante La Estadía | — |  | Objeto |  |  |
| FP | Entrevistador | — |  | Objeto |  |  |
| FP | Estado | — |  | Estado |  |  |
| FP | Fechas | — |  | Objeto |  |  |
| FP | Habitación Pasa | — |  | Verbo |  |  |
| FP | Noche | — |  | Objeto |  |  |
| FP | Panel | — |  | Objeto |  |  |
| FP | Sistema | — |  | Sujeto |  |  |
| FP | Temporada | — |  | Estado |  |  |
| FN | — | Check-in |  |  | Verbo |  |
| FN | — | Factura |  |  | Objeto |  |
| FN | — | Hacer Reserva |  |  | Verbo |  |
| FN | — | Limpiar Habitación |  |  | Verbo |  |
| FN | — | Mucama |  |  | Sujeto |  |
| FN | — | Ocupada |  |  | Estado |  |
