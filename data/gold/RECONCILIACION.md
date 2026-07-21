# Reconciliación del Gold Standard — recuperabilidad desde el corpus

**Qué documenta.** Cuáles de los 21 símbolos del *GS-Completo* (el LEL de ecoFactory construido
manualmente en el estudio de origen, WER 2024) tienen sustento textual en las cuatro entrevistas
reales que conforman el corpus de este trabajo, y cuáles no.

El subconjunto recuperable —15 símbolos— es el **GS-Corpus** (`gs_corpus.json`), que funciona como
blanco alcanzable de la evaluación. La diferencia con el GS-Completo (6 símbolos) es la **brecha de
recuperabilidad**, analizada en las Secciones 5.7 y 5.8 del documento.

## Método

Para cada símbolo del GS-Completo se buscó evidencia textual directa en las cuatro transcripciones
(`entrevista_1_dueno.txt`, `entrevista_2_gerente_comercial.txt`, `entrevista_3_operario.txt`,
`entrevista_4_responsable_erp.txt`). El criterio: la evidencia debe sostener razonablemente la
noción y el impacto tal como están redactados en el Gold Standard. No alcanza con que una palabra
suelta coincida por casualidad en una oración de otro tema.

## Los 6 símbolos fuera del GS-Corpus

| Símbolo | Tipo | Motivo de exclusión |
|---|---|---|
| Cliente Minorista | Sujeto | «Minorista» no aparece en ninguna de las cuatro transcripciones. |
| Lista de Precios | Objeto | «Lista de precios» no aparece; al Gerente Comercial se lo consulta sobre presupuesto, no sobre una lista de precios formal. |
| Pedido Aprobado | Estado | «Aprobado» / «aprobación» no aparece. El circuito de aprobación de pedidos no se describe en estas entrevistas. |
| Administración de Pedidos ERP | Sujeto | «Administración» aparece 3 veces, pero siempre en sentido genérico (tareas administrativas), nunca nombrando un módulo específico. Falso positivo por coincidencia léxica, descartado tras revisar el contexto. |
| Ajuste de Errores de Facturación | Verbo | «Errores» y «facturación» aparecen, pero describen la *existencia* de errores de carga en general (bolsas, cantidades, direcciones), no un procedimiento de corrección. |
| Verificación de Facturas | Verbo | La Entrevista 1 menciona *"un doble trabajo de verificación de si la factura se corresponde con el pedido"*, evidencia insuficiente: no es un paso de proceso explícitamente narrado. |

## Un caso intermedio: Cliente Mayorista

**Cliente Mayorista** (Sujeto) se incluye en el GS-Corpus con la etiqueta **«Parcial»** en la
Tabla 5.2 del documento. La Entrevista 2 dice *"trabajamos solo con clientes mayoristas"*, lo que
sustenta la existencia del símbolo; pero los detalles de noción e impacto redactados en el
Gold Standard (bonificaciones, condiciones de pago) no tienen base en esa transcripción.

## Por qué el GS-Completo es más grande que el corpus

Los 21 símbolos del LEL manual no surgen únicamente de las entrevistas: el modelo se fue ampliando
durante el estudio original con la información anticipada, con los escenarios derivados del propio
LEL y con la sesión de facilitación gráfica. Además, de las cinco entrevistas originales solo se
conservan cuatro transcripciones. Por eso una porción del LEL experto no es recuperable de este
corpus por ningún método, automático o manual — un resultado en sí mismo, y no un defecto de la
evaluación.
