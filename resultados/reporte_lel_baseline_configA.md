# Reporte de evaluación — `lel_baseline_configA`

## Evaluación contra gs_corpus

- Símbolos en el GS: **14**
- Símbolos producidos: **37**
- VP = 5 · FP = 32 · FN = 9

| Métrica | Valor |
|---|---|
| Precisión | 0.135 |
| Cobertura (Recall) | 0.357 |
| F1 | 0.196 |
| Exactitud de tipo (sobre VP) | 0.600 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Factura | Factura | exacto | Objeto | Objeto | sí |
| VP | Afip | Integración AFIP | sinonimo | Sujeto | Sujeto | sí |
| VP | Entrega | Orden de Entrega | tokens | Objeto | Objeto | sí |
| VP | Pedido | Pedido | exacto | Estado | Objeto | NO |
| VP | Erp | Sistema ERP | sinonimo | Objeto | Sujeto | NO |
| FP | Automatizar | — |  | Verbo |  |  |
| FP | Bases De Datos | — |  | Objeto |  |  |
| FP | Bolsas | — |  | Objeto |  |  |
| FP | Cliente Llama | — |  | Sujeto |  |  |
| FP | Clientes | — |  | Sujeto |  |  |
| FP | Compra | — |  | Objeto |  |  |
| FP | Creo | — |  | Objeto |  |  |
| FP | Dentro | — |  | Objeto |  |  |
| FP | Depósito | — |  | Objeto |  |  |
| FP | Dificultades | — |  | Objeto |  |  |
| FP | Distintas | — |  | Objeto |  |  |
| FP | Ecofactory | — |  | Objeto |  |  |
| FP | Ejemplo | — |  | Objeto |  |  |
| FP | Errores | — |  | Objeto |  |  |
| FP | Específicos | — |  | Objeto |  |  |
| FP | Espera | — |  | Objeto |  |  |
| FP | Excel | — |  | Objeto |  |  |
| FP | Facturación | — |  | Verbo |  |  |
| FP | Gestión | — |  | Objeto |  |  |
| FP | Hablar | — |  | Verbo |  |  |
| FP | Hoy | — |  | Objeto |  |  |
| FP | Informes | — |  | Objeto |  |  |
| FP | Listo | — |  | Estado |  |  |
| FP | Lugar | — |  | Verbo |  |  |
| FP | Mails | — |  | Objeto |  |  |
| FP | Manual | — |  | Estado |  |  |
| FP | Pedidos | — |  | Estado |  |  |
| FP | Presupuesto | — |  | Objeto |  |  |
| FP | Problemas | — |  | Objeto |  |  |
| FP | Responsable | — |  | Sujeto |  |  |
| FP | Sistema | — |  | Sujeto |  |  |
| FP | Área | — |  | Sujeto |  |  |
| FN | — | Agregar Cliente |  |  | Verbo |  |
| FN | — | Agregar Factura |  |  | Verbo |  |
| FN | — | Agregar Pedido |  |  | Verbo |  |
| FN | — | Agregar Producto |  |  | Verbo |  |
| FN | — | Bolsa Ecológica / Producto |  |  | Objeto |  |
| FN | — | Creación de Reportes ERP |  |  | Verbo |  |
| FN | — | Distribución de Producto |  |  | Verbo |  |
| FN | — | Operario |  |  | Sujeto |  |
| FN | — | Pedido Finalizado |  |  | Estado |  |

## Evaluación contra gs_completo

- Símbolos en el GS: **21**
- Símbolos producidos: **37**
- VP = 8 · FP = 29 · FN = 13

| Métrica | Valor |
|---|---|
| Precisión | 0.216 |
| Cobertura (Recall) | 0.381 |
| F1 | 0.276 |
| Exactitud de tipo (sobre VP) | 0.625 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Pedidos | Administración de Pedidos ERP | tokens | Estado | Sujeto | NO |
| VP | Facturación | Ajuste de Errores de Facturación | tokens | Verbo | Verbo | sí |
| VP | Clientes | Cliente Mayorista | sinonimo | Sujeto | Sujeto | sí |
| VP | Factura | Factura | exacto | Objeto | Objeto | sí |
| VP | Afip | Integración AFIP | sinonimo | Sujeto | Sujeto | sí |
| VP | Entrega | Orden de Entrega | tokens | Objeto | Objeto | sí |
| VP | Pedido | Pedido | exacto | Estado | Objeto | NO |
| VP | Erp | Sistema ERP | sinonimo | Objeto | Sujeto | NO |
| FP | Automatizar | — |  | Verbo |  |  |
| FP | Bases De Datos | — |  | Objeto |  |  |
| FP | Bolsas | — |  | Objeto |  |  |
| FP | Cliente Llama | — |  | Sujeto |  |  |
| FP | Compra | — |  | Objeto |  |  |
| FP | Creo | — |  | Objeto |  |  |
| FP | Dentro | — |  | Objeto |  |  |
| FP | Depósito | — |  | Objeto |  |  |
| FP | Dificultades | — |  | Objeto |  |  |
| FP | Distintas | — |  | Objeto |  |  |
| FP | Ecofactory | — |  | Objeto |  |  |
| FP | Ejemplo | — |  | Objeto |  |  |
| FP | Errores | — |  | Objeto |  |  |
| FP | Específicos | — |  | Objeto |  |  |
| FP | Espera | — |  | Objeto |  |  |
| FP | Excel | — |  | Objeto |  |  |
| FP | Gestión | — |  | Objeto |  |  |
| FP | Hablar | — |  | Verbo |  |  |
| FP | Hoy | — |  | Objeto |  |  |
| FP | Informes | — |  | Objeto |  |  |
| FP | Listo | — |  | Estado |  |  |
| FP | Lugar | — |  | Verbo |  |  |
| FP | Mails | — |  | Objeto |  |  |
| FP | Manual | — |  | Estado |  |  |
| FP | Presupuesto | — |  | Objeto |  |  |
| FP | Problemas | — |  | Objeto |  |  |
| FP | Responsable | — |  | Sujeto |  |  |
| FP | Sistema | — |  | Sujeto |  |  |
| FP | Área | — |  | Sujeto |  |  |
| FN | — | Agregar Cliente |  |  | Verbo |  |
| FN | — | Agregar Factura |  |  | Verbo |  |
| FN | — | Agregar Pedido |  |  | Verbo |  |
| FN | — | Agregar Producto |  |  | Verbo |  |
| FN | — | Bolsa Ecológica / Producto |  |  | Objeto |  |
| FN | — | Cliente Minorista |  |  | Sujeto |  |
| FN | — | Creación de Reportes ERP |  |  | Verbo |  |
| FN | — | Distribución de Producto |  |  | Verbo |  |
| FN | — | Lista de Precios |  |  | Objeto |  |
| FN | — | Operario |  |  | Sujeto |  |
| FN | — | Pedido Aprobado |  |  | Estado |  |
| FN | — | Pedido Finalizado |  |  | Estado |  |
| FN | — | Verificación de Facturas |  |  | Verbo |  |
