# Reconciliación v1.1 — Brecha de recuperabilidad con el corpus real ampliado

**Fecha:** julio 2026. **Motivo:** incorporación de 2 transcripciones reales adicionales
(Gerente Comercial, Responsable ERP) recuperadas por la Dra. Hadad, que reemplazan a las dos
entrevistas simuladas usadas hasta la versión anterior. Este documento extiende
`Gold_Standard_v1.0_ecoFactory.md` sin reemplazarlo: los 21 símbolos de GS-Completo y los 14 de
GS-Corpus (Configuración A, 2 entrevistas) no cambian. Lo que se revisa es exclusivamente qué
subconjunto es recuperable del **corpus extendido real** (4 entrevistas), para reemplazar la
medición de la Configuración B que antes se apoyaba en 2 entrevistas simuladas.

## Método

Para cada uno de los 7 símbolos que estaban fuera de GS-Corpus (la brecha original), se buscó
evidencia textual directa en las 4 transcripciones reales (`entrevista_1_dueno.txt`,
`entrevista_2_gerente_comercial.txt`, `entrevista_3_operario.txt`,
`entrevista_4_responsable_erp.txt`), con el mismo criterio usado en la reconciliación v1.0:
la evidencia debe sostener razonablemente la noción y el impacto tal como están redactados, no
alcanza con que una palabra suelta coincida por casualidad en una oración de otro tema.

## Resultado símbolo por símbolo

| Símbolo | Tipo | ¿Recuperable del corpus real ampliado? | Evidencia / motivo |
|---|---|---|---|
| **Cliente Mayorista** | Sujeto | **Sí (parcial)** | Entrevista 2: *"trabajamos solo con clientes mayoristas"*. Sustenta la existencia del símbolo, pero no el detalle de noción/impacto ya redactado en el GS (bonificaciones, cuenta corriente), que no tiene base en esta transcripción. |
| Cliente Minorista | Sujeto | No | «Minorista» no aparece en ninguna de las 4 transcripciones reales. |
| Lista de Precios | Objeto | No | «Precio» / «lista de precios» no aparece; el Gerente Comercial es consultado sobre presupuesto, no sobre una lista de precios formal. |
| Pedido Aprobado | Estado | No | «Aprobado» / «aprobación» no aparece. El circuito de aprobación de pedidos no se describe en estas 4 entrevistas. |
| Administración de Pedidos ERP | Sujeto | No | «Administración» aparece 3 veces, pero siempre en sentido genérico (tareas administrativas, gestión), nunca nombrando un módulo específico de administración de pedidos. Falso positivo por coincidencia léxica, descartado tras revisar el contexto. |
| Ajuste de Errores de Facturación | Verbo | No | «Errores» y «facturación» aparecen, pero en la Entrevista 1 describen la *existencia* de errores de carga en general (bolsas, cantidades, direcciones), no un procedimiento de corrección de errores de facturación en particular. Mismo motivo de exclusión que en la reconciliación v1.0. |
| Verificación de Facturas | Verbo | No | La Entrevista 1 menciona *"un doble trabajo de verificación de si la factura se corresponde con el pedido"*, la misma evidencia ya considerada en la reconciliación v1.0 y marcada allí como insuficiente (no es un paso de proceso explícitamente narrado; "chequear" es genérico). No hay evidencia nueva en las dos entrevistas incorporadas, así que se mantiene la exclusión. |

**Resultado neto: +1 símbolo** respecto de GS-Corpus (14 → 15). Los otros seis siguen sin
sustento textual incluso con el corpus real completo, lo que indica que dependían de la quinta
entrevista (no recuperada) o de la sesión de facilitación gráfica del trabajo original.

## GS-Corpus-Extendido (15 símbolos)

Guardado en `data/gold/gs_corpus_extendido.json`. Es el nuevo blanco de comparación para la
Configuración B (corpus real de 4 entrevistas), reemplazando la comparación contra GS-Completo
que se usaba cuando el corpus incluía entrevistas simuladas. GS-Completo (21) se conserva como
techo teórico y sigue siendo relevante para dimensionar la brecha, pero ya no es razonable
esperar que un método —por bueno que sea— lo alcance desde este corpus de entrada.

## Por qué esto importa para el trabajo

Antes de esta revisión, la Configuración B alcanzaba una cobertura muy alta contra GS-Completo
(0,952 en la corrida de referencia). Con el nuevo análisis queda claro que una parte de esa
cobertura reflejaba **contaminación de las entrevistas simuladas** —redactadas con conocimiento
del Gold Standard— y no una propiedad genuina del corpus. La comparación correcta, de ahora en
más, es contra GS-Corpus-Extendido (15), y la brecha remanente (6 símbolos) pasa a ser, en sí
misma, un resultado cualitativo del trabajo: hay una porción no trivial del LEL experto que
ningún método —automático o manual— puede recuperar sin la quinta entrevista perdida o la
facilitación gráfica original.
