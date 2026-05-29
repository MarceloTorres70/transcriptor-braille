# Resultados de Pruebas

## 1. Tabla de Ejecución Completa

La siguiente matriz consolida los 9 casos de prueba entregados por el cliente, comparando el resultado esperado en el documento de referencia frente al resultado obtenido por la API.

| Texto Original | Resultado Esperado (Cliente) | Resultado Obtenido (API) | Estado |
| --- | --- | --- | --- |
| Buenas tardes! | ⠨⠃⠥⠑⠝⠁⠎ ⠞⠁⠗⠙⠑⠎⠖ | ⠨⠃⠥⠑⠝⠁⠎ ⠞⠁⠗⠙⠑⠎⠖ | Éxito |
| Niño | ⠨⠝⠊⠻⠕ | ⠨⠝⠊⠻⠕ | Éxito |
| FIS-EPN | ⠨⠨⠋⠊⠎⠤⠨⠨⠑⠏⠝ | ⠨⠨⠋⠊⠎⠤⠨⠨⠑⠏⠝ | Éxito |
| 46.37 | ⠼⠙⠋⠲⠼⠉⠛ | ⠼⠙⠋⠲⠼⠉⠛ | Éxito |
| sandía | ⠎⠁⠝⠙⠔⠁ | ⠎⠁⠝⠙⠔⠁ | Éxito |
| nov 2025 | ⠝⠕⠧ ⠼⠃⠹⠃⠑ | ⠝⠕⠧ ⠼⠃⠚⠃⠑ | Discrepancia |
| 20,15 | ⠼⠃⠹⠂⠼⠁⠑ | ⠼⠃⠚⠂⠼⠁⠑ | Discrepancia |
| 25-11-2025 | ⠼⠃⠑⠤⠼⠁⠁⠤⠼⠃⠹⠃⠑ | ⠼⠃⠑⠤⠼⠁⠁⠤⠼⠃⠚⠃⠑ | Discrepancia |
| 26-11-2025 | ⠼⠃⠋⠤⠼⠁⠁⠤⠼⠃⠹⠃⠑ | ⠼⠃⠋⠤⠼⠁⠁⠤⠼⠃⠚⠃⠑ | Discrepancia |

## 2. Análisis Técnico y Justificación

El análisis comparativo muestra que todas las discrepancias se concentran en un único criterio: la representación del dígito cero dentro de bloques numéricos.

- El cliente solicitó el símbolo `⠹` para el cero.
- El motor de traducción del sistema arroja el símbolo `⠚` para el cero.

Tras la verificación técnica contra el estándar del Braille en español, se confirma que `⠚` (puntos 2-4-5) corresponde a la representación correcta del número cero.

Por razones de integridad técnica, trazabilidad y calidad del software, el equipo decidió mantener la implementación alineada con el estándar real y no introducir una modificación artificial del código fuente para replicar lo que, desde el punto de vista normativo, constituye un probable error tipográfico en los requisitos del cliente.

Esta justificación aplica de forma uniforme a todos los casos marcados como **Discrepancia** en la tabla anterior.
