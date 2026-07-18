# Reporte de evaluación — `lel_baseline_configB_real`

## Evaluación contra gs_corpus_extendido

- Símbolos en el GS: **15**
- Símbolos producidos: **40**
- VP = 7 · FP = 33 · FN = 8

| Métrica | Valor |
|---|---|
| Precisión | 0.175 |
| Cobertura (Recall) | 0.467 |
| F1 | 0.255 |
| Exactitud de tipo (sobre VP) | 0.571 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Productos | Bolsa Ecológica / Producto | similitud | Objeto | Objeto | sí |
| VP | Cliente | Cliente Mayorista | sinonimo | Sujeto | Sujeto | sí |
| VP | Factura | Factura | exacto | Objeto | Objeto | sí |
| VP | Integración | Integración AFIP | tokens | Verbo | Sujeto | NO |
| VP | Entrega | Orden de Entrega | tokens | Objeto | Objeto | sí |
| VP | Pedido | Pedido | exacto | Estado | Objeto | NO |
| VP | Erp | Sistema ERP | sinonimo | Objeto | Sujeto | NO |
| FP | Algún | — |  | Objeto |  |  |
| FP | Automatizar | — |  | Verbo |  |  |
| FP | Bolsas | — |  | Objeto |  |  |
| FP | Cargar | — |  | Verbo |  |  |
| FP | Clientes | — |  | Sujeto |  |  |
| FP | Creo | — |  | Objeto |  |  |
| FP | Cuanto | — |  | Objeto |  |  |
| FP | Depósito | — |  | Objeto |  |  |
| FP | Distintos | — |  | Objeto |  |  |
| FP | Dueño | — |  | Sujeto |  |  |
| FP | Ejemplo | — |  | Objeto |  |  |
| FP | Entrevista | — |  | Objeto |  |  |
| FP | Errores | — |  | Objeto |  |  |
| FP | Facturación | — |  | Verbo |  |  |
| FP | Gestión | — |  | Objeto |  |  |
| FP | Gracias | — |  | Objeto |  |  |
| FP | Hoy | — |  | Objeto |  |  |
| FP | Informes | — |  | Objeto |  |  |
| FP | Lugar | — |  | Verbo |  |  |
| FP | Mano | — |  | Objeto |  |  |
| FP | Manual | — |  | Estado |  |  |
| FP | Mejorar | — |  | Verbo |  |  |
| FP | Parece | — |  | Objeto |  |  |
| FP | Pedidos | — |  | Estado |  |  |
| FP | Personal | — |  | Objeto |  |  |
| FP | Preguntas | — |  | Objeto |  |  |
| FP | Presupuesto | — |  | Objeto |  |  |
| FP | Problemas | — |  | Objeto |  |  |
| FP | Responsable | — |  | Sujeto |  |  |
| FP | Seguridad | — |  | Objeto |  |  |
| FP | Sistema | — |  | Sujeto |  |  |
| FP | Software | — |  | Objeto |  |  |
| FP | Trabajar | — |  | Verbo |  |  |
| FN | — | Agregar Cliente |  |  | Verbo |  |
| FN | — | Agregar Factura |  |  | Verbo |  |
| FN | — | Agregar Pedido |  |  | Verbo |  |
| FN | — | Agregar Producto |  |  | Verbo |  |
| FN | — | Creación de Reportes ERP |  |  | Verbo |  |
| FN | — | Distribución de Producto |  |  | Verbo |  |
| FN | — | Operario |  |  | Sujeto |  |
| FN | — | Pedido Finalizado |  |  | Estado |  |

## Evaluación contra gs_completo

- Símbolos en el GS: **21**
- Símbolos producidos: **40**
- VP = 9 · FP = 31 · FN = 12

| Métrica | Valor |
|---|---|
| Precisión | 0.225 |
| Cobertura (Recall) | 0.429 |
| F1 | 0.295 |
| Exactitud de tipo (sobre VP) | 0.556 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Pedidos | Administración de Pedidos ERP | tokens | Estado | Sujeto | NO |
| VP | Facturación | Ajuste de Errores de Facturación | tokens | Verbo | Verbo | sí |
| VP | Productos | Bolsa Ecológica / Producto | similitud | Objeto | Objeto | sí |
| VP | Cliente | Cliente Mayorista | sinonimo | Sujeto | Sujeto | sí |
| VP | Factura | Factura | exacto | Objeto | Objeto | sí |
| VP | Integración | Integración AFIP | tokens | Verbo | Sujeto | NO |
| VP | Entrega | Orden de Entrega | tokens | Objeto | Objeto | sí |
| VP | Pedido | Pedido | exacto | Estado | Objeto | NO |
| VP | Erp | Sistema ERP | sinonimo | Objeto | Sujeto | NO |
| FP | Algún | — |  | Objeto |  |  |
| FP | Automatizar | — |  | Verbo |  |  |
| FP | Bolsas | — |  | Objeto |  |  |
| FP | Cargar | — |  | Verbo |  |  |
| FP | Clientes | — |  | Sujeto |  |  |
| FP | Creo | — |  | Objeto |  |  |
| FP | Cuanto | — |  | Objeto |  |  |
| FP | Depósito | — |  | Objeto |  |  |
| FP | Distintos | — |  | Objeto |  |  |
| FP | Dueño | — |  | Sujeto |  |  |
| FP | Ejemplo | — |  | Objeto |  |  |
| FP | Entrevista | — |  | Objeto |  |  |
| FP | Errores | — |  | Objeto |  |  |
| FP | Gestión | — |  | Objeto |  |  |
| FP | Gracias | — |  | Objeto |  |  |
| FP | Hoy | — |  | Objeto |  |  |
| FP | Informes | — |  | Objeto |  |  |
| FP | Lugar | — |  | Verbo |  |  |
| FP | Mano | — |  | Objeto |  |  |
| FP | Manual | — |  | Estado |  |  |
| FP | Mejorar | — |  | Verbo |  |  |
| FP | Parece | — |  | Objeto |  |  |
| FP | Personal | — |  | Objeto |  |  |
| FP | Preguntas | — |  | Objeto |  |  |
| FP | Presupuesto | — |  | Objeto |  |  |
| FP | Problemas | — |  | Objeto |  |  |
| FP | Responsable | — |  | Sujeto |  |  |
| FP | Seguridad | — |  | Objeto |  |  |
| FP | Sistema | — |  | Sujeto |  |  |
| FP | Software | — |  | Objeto |  |  |
| FP | Trabajar | — |  | Verbo |  |  |
| FN | — | Agregar Cliente |  |  | Verbo |  |
| FN | — | Agregar Factura |  |  | Verbo |  |
| FN | — | Agregar Pedido |  |  | Verbo |  |
| FN | — | Agregar Producto |  |  | Verbo |  |
| FN | — | Cliente Minorista |  |  | Sujeto |  |
| FN | — | Creación de Reportes ERP |  |  | Verbo |  |
| FN | — | Distribución de Producto |  |  | Verbo |  |
| FN | — | Lista de Precios |  |  | Objeto |  |
| FN | — | Operario |  |  | Sujeto |  |
| FN | — | Pedido Aprobado |  |  | Estado |  |
| FN | — | Pedido Finalizado |  |  | Estado |  |
| FN | — | Verificación de Facturas |  |  | Verbo |  |
