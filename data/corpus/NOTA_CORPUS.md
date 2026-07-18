# Nota sobre el corpus — revisión post-entrega (julio 2026)

## Qué cambió

La versión entregada a la directora usaba, para la Configuración B (Corpus-Extendido), dos
entrevistas **simuladas** por el autor (`Gerente Comercial` y `Funcional del ERP`), porque
en ese momento solo se contaba con 2 de las 5 transcripciones originales del caso ecoFactory
(Dueño y Operario ERP). La Dra. Hadad recuperó y envió un documento con **4 transcripciones
reales** del estudio original (2024): además de Dueño y Operario ERP (ya conocidas), incluye
una entrevista real al **Gerente Comercial** y una nueva, al **Responsable ERP** (el proveedor
del sistema, un actor no utilizado hasta ahora).

En consecuencia, la Configuración B se reconstruyó con **4 entrevistas 100 % reales**:

| # | Rol | Archivo |
|---|---|---|
| 1 | Dueño | `entrevista_1_dueno.txt` |
| 2 | Gerente Comercial | `entrevista_2_gerente_comercial.txt` |
| 3 | Operario ERP | `entrevista_3_operario.txt` |
| 4 | Responsable ERP (proveedor) | `entrevista_4_responsable_erp.txt` |

Las dos entrevistas simuladas originales quedan archivadas en `simuladas_deprecadas/`, **no
como corpus del experimento**, sino como evidencia para un hallazgo metodológico (ver abajo).

## Un hallazgo, no solo una corrección

Cotejar las entrevistas simuladas contra las reales permitió detectar algo relevante para la
discusión de amenazas a la validez: la entrevista simulada del Gerente Comercial introducía
explícitamente **ambos** términos «cliente mayorista» y «cliente minorista» —exactamente la
distinción que usa el Gold Standard—, mientras que en la entrevista **real** «mayorista»
aparece una sola vez y «minorista» no aparece nunca. Es un ejemplo concreto, dentro del propio
trabajo, del riesgo de contaminación que se discute en el Capítulo 4: al redactar una entrevista
simulada con conocimiento previo del Gold Standard, es fácil —incluso sin intención— sesgarla
hacia el vocabulario esperado. Este hallazgo se incorpora al Capítulo 8 (Discusión).

## Brecha de recuperabilidad, revisada

Con el corpus real ampliado (4 entrevistas), se volvió a evaluar cuáles de los 21 símbolos del
GS-Completo tienen sustento textual. Resultado: se recupera un símbolo adicional respecto de las
2 entrevistas originales —**Cliente Mayorista**, mencionado una vez, aunque sin base textual
para su noción/impacto completos tal como están redactados en el Gold Standard—, pero los otros
seis símbolos que "cerraban" con el corpus simulado (Cliente Minorista, Lista de Precios, Pedido
Aprobado, Administración de Pedidos ERP, Ajuste de Errores de Facturación y Verificación de
Facturas) **siguen sin aparecer** en ninguna de las 4 transcripciones reales disponibles. Es
decir: la brecha de recuperabilidad es real y persiste incluso con el corpus ampliado —no era un
artefacto de tener solo 2 entrevistas—, y lo que efectivamente cerraba esa brecha en la versión
anterior era, en buena medida, la contaminación de las entrevistas simuladas. Ver
`data/gold/RECONCILIACION_v1.1.md` para el detalle símbolo por símbolo.
