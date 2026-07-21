# Reporte de evaluación — `lel_llm_C2c_referencia`

## Evaluación contra GS-Corpus (15)

- Símbolos en el GS: **15**
- Símbolos producidos: **19**
- VP = 9 · FP = 10 · FN = 6

| Métrica | Valor |
|---|---|
| Precisión | 0.474 |
| Cobertura (Recall) | 0.600 |
| F1 | 0.529 |
| Exactitud de tipo (sobre VP) | 0.889 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Cliente | Agregar Cliente | tokens | Sujeto | Verbo | NO |
| VP | Bolsa Ecológica | Bolsa Ecológica / Producto | exacto | Objeto | Objeto | sí |
| VP | Cliente Mayorista | Cliente Mayorista | exacto | Sujeto | Sujeto | sí |
| VP | Factura | Factura | exacto | Objeto | Objeto | sí |
| VP | AFIP | Integración AFIP | sinonimo | Sujeto | Sujeto | sí |
| VP | Operario ERP | Operario | tokens | Sujeto | Sujeto | sí |
| VP | Remito | Orden de Entrega | sinonimo | Objeto | Objeto | sí |
| VP | Pedido | Pedido | exacto | Objeto | Objeto | sí |
| VP | Sistema ERP | Sistema ERP | exacto | Sujeto | Sujeto | sí |
| FP | Automatizar | — |  | Verbo |  |  |
| FP | Backup | — |  | Objeto |  |  |
| FP | Base de Datos | — |  | Objeto |  |  |
| FP | Depósito | — |  | Objeto |  |  |
| FP | Dueño | — |  | Sujeto |  |  |
| FP | Facturación | — |  | Verbo |  |  |
| FP | Gerente Comercial | — |  | Sujeto |  |  |
| FP | Integración | — |  | Verbo |  |  |
| FP | Responsable ERP | — |  | Sujeto |  |  |
| FP | Stock | — |  | Objeto |  |  |
| FN | — | Agregar Factura |  |  | Verbo |  |
| FN | — | Agregar Pedido |  |  | Verbo |  |
| FN | — | Agregar Producto |  |  | Verbo |  |
| FN | — | Creación de Reportes ERP |  |  | Verbo |  |
| FN | — | Distribución de Producto |  |  | Verbo |  |
| FN | — | Pedido Finalizado |  |  | Estado |  |

## Evaluación contra GS-Completo (21)

- Símbolos en el GS: **21**
- Símbolos producidos: **19**
- VP = 10 · FP = 9 · FN = 11

| Métrica | Valor |
|---|---|
| Precisión | 0.526 |
| Cobertura (Recall) | 0.476 |
| F1 | 0.500 |
| Exactitud de tipo (sobre VP) | 0.900 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Cliente | Agregar Cliente | tokens | Sujeto | Verbo | NO |
| VP | Facturación | Ajuste de Errores de Facturación | tokens | Verbo | Verbo | sí |
| VP | Bolsa Ecológica | Bolsa Ecológica / Producto | exacto | Objeto | Objeto | sí |
| VP | Cliente Mayorista | Cliente Mayorista | exacto | Sujeto | Sujeto | sí |
| VP | Factura | Factura | exacto | Objeto | Objeto | sí |
| VP | AFIP | Integración AFIP | sinonimo | Sujeto | Sujeto | sí |
| VP | Operario ERP | Operario | tokens | Sujeto | Sujeto | sí |
| VP | Remito | Orden de Entrega | sinonimo | Objeto | Objeto | sí |
| VP | Pedido | Pedido | exacto | Objeto | Objeto | sí |
| VP | Sistema ERP | Sistema ERP | exacto | Sujeto | Sujeto | sí |
| FP | Automatizar | — |  | Verbo |  |  |
| FP | Backup | — |  | Objeto |  |  |
| FP | Base de Datos | — |  | Objeto |  |  |
| FP | Depósito | — |  | Objeto |  |  |
| FP | Dueño | — |  | Sujeto |  |  |
| FP | Gerente Comercial | — |  | Sujeto |  |  |
| FP | Integración | — |  | Verbo |  |  |
| FP | Responsable ERP | — |  | Sujeto |  |  |
| FP | Stock | — |  | Objeto |  |  |
| FN | — | Administración de Pedidos ERP |  |  | Sujeto |  |
| FN | — | Agregar Factura |  |  | Verbo |  |
| FN | — | Agregar Pedido |  |  | Verbo |  |
| FN | — | Agregar Producto |  |  | Verbo |  |
| FN | — | Cliente Minorista |  |  | Sujeto |  |
| FN | — | Creación de Reportes ERP |  |  | Verbo |  |
| FN | — | Distribución de Producto |  |  | Verbo |  |
| FN | — | Lista de Precios |  |  | Objeto |  |
| FN | — | Pedido Aprobado |  |  | Estado |  |
| FN | — | Pedido Finalizado |  |  | Estado |  |
| FN | — | Verificación de Facturas |  |  | Verbo |  |
