# Reporte de evaluación — `pln_e-commerce`

## Evaluación contra gold_e-commerce

- Símbolos en el GS: **15**
- Símbolos producidos: **38**
- VP = 12 · FP = 26 · FN = 3

| Métrica | Valor |
|---|---|
| Precisión | 0.316 |
| Cobertura (Recall) | 0.800 |
| F1 | 0.453 |
| Exactitud de tipo (sobre VP) | 0.583 |

### Detalle de emparejamientos

| Estado | Producido | ↔ Gold | Vía | Tipo prod | Tipo gold | Tipo OK |
|---|---|---|---|---|---|---|
| VP | Carrito | Carrito | exacto | Objeto | Objeto | sí |
| VP | Catálogo | Catálogo | exacto | Objeto | Objeto | sí |
| VP | Cliente | Cliente | exacto | Sujeto | Sujeto | sí |
| VP | Confirmado | Confirmado | exacto | Estado | Estado | sí |
| VP | Entrega | Entregado | similitud | Objeto | Estado | NO |
| VP | Operador | Operador de Logística | tokens | Objeto | Sujeto | NO |
| VP | Pedidos | Pedido | similitud | Estado | Objeto | NO |
| VP | Preparar | Preparar Pedido | tokens | Verbo | Verbo | sí |
| VP | Pago | Procesar Pago | tokens | Objeto | Verbo | NO |
| VP | Producto | Producto | exacto | Objeto | Objeto | sí |
| VP | Stock | Stock | exacto | Objeto | Objeto | sí |
| VP | Transportista | Transportista | exacto | Objeto | Sujeto | NO |
| FP | Aprueba | — |  | Objeto |  |  |
| FP | Armo | — |  | Objeto |  |  |
| FP | Automáticamente | — |  | Objeto |  |  |
| FP | Busca | — |  | Objeto |  |  |
| FP | Buscar | — |  | Verbo |  |  |
| FP | Camino | — |  | Objeto |  |  |
| FP | Cantidad | — |  | Objeto |  |  |
| FP | Categoría | — |  | Objeto |  |  |
| FP | Checkout | — |  | Objeto |  |  |
| FP | Complica | — |  | Objeto |  |  |
| FP | Compra | — |  | Objeto |  |  |
| FP | Correo | — |  | Objeto |  |  |
| FP | Depósito | — |  | Objeto |  |  |
| FP | Dirección | — |  | Objeto |  |  |
| FP | Disponible | — |  | Objeto |  |  |
| FP | Dueño | — |  | Sujeto |  |  |
| FP | Entrevistador | — |  | Objeto |  |  |
| FP | Envío | — |  | Objeto |  |  |
| FP | Logística | — |  | Objeto |  |  |
| FP | Manda | — |  | Objeto |  |  |
| FP | Paquete | — |  | Objeto |  |  |
| FP | Pasa | — |  | Objeto |  |  |
| FP | Pedido Queda | — |  | Objeto |  |  |
| FP | Plata | — |  | Objeto |  |  |
| FP | Productos | — |  | Objeto |  |  |
| FP | Web | — |  | Objeto |  |  |
| FN | — | Confirmar Pedido |  |  | Verbo |  |
| FN | — | Despachar Pedido |  |  | Verbo |  |
| FN | — | Gestionar Devolución |  |  | Verbo |  |
