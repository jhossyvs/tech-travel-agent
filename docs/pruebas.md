
# Pruebas de Tech Travel Agent

## Objetivo

Verificar que el agente pueda seleccionar la capacidad adecuada, utilizar
información documental, consultar una API externa y manejar situaciones
donde la información no está disponible.

## Matriz de pruebas

| # | Escenario | Entrada | Resultado esperado | Resultado obtenido |
|---|---|---|---|---|
| 1 | Clima normal | ¿Cuál es el clima actual en Madrid? | El agente utiliza `obtener_clima` y devuelve datos actuales. | Correcto: 21.4 °C y 3.6 km/h de viento. |
| 2 | Otra ciudad | ¿Cuál es el clima actual en Lima? | El agente consulta la API para Lima. | Correcto: 17.0 °C y 11.7 km/h de viento. |
| 3 | Ciudad inexistente | ¿Cuál es el clima en Xyzabc? | La herramienta debe indicar que no encontró la ciudad. | Correcto: se informó que la ciudad no fue encontrada. |
| 4 | Fallo de API | Servicio de geocodificación no disponible. | La aplicación debe manejar el error sin mostrar un traceback al usuario. | Correcto: el agente informó que no podía consultar el clima. |
| 5 | RAG | ¿Qué debo verificar antes de viajar a Europa? | El agente debe utilizar la información documental disponible. | Correcto: respondió utilizando la guía de viaje. |
| 6 | Información ausente | ¿Qué requisitos necesito para obtener una visa de estudiante en Alemania? | El agente debe reconocer que la información no está en el documento. | Correcto: indicó que la guía no contiene esa información. |
| 7 | Pregunta mixta | ¿Cuál es el clima actual en Madrid y qué debo verificar antes de viajar a Europa? | El agente debe combinar información de la API y del conocimiento documental. | Correcto: utilizó ambas capacidades. |

## Casos relevantes

### Caso 1 — Uso de Function Tool

Entrada:

> ¿Cuál es el clima actual en Madrid?

El modelo genera una llamada a:

`obtener_clima({"ciudad": "Madrid"})`

La aplicación ejecuta la función y devuelve el resultado al agente.

Resultado:

> Actualmente en Madrid la temperatura es de 21.4 °C, con un viento de 3.6 km/h.

### Caso 2 — Ciudad inexistente

Entrada:

> ¿Cuál es el clima en Xyzabc?

La API no encuentra ninguna ciudad con ese nombre.

El agente no inventa información y comunica que no pudo encontrar la ciudad.

### Caso 3 — Evidencia ausente en RAG

Entrada:

> ¿Qué requisitos necesito para obtener una visa de estudiante en Alemania?

El documento disponible no contiene requisitos específicos para una visa
de estudiante alemana.

El agente reconoce la ausencia de evidencia en lugar de inventar requisitos.

### Caso 4 — Pregunta combinada

Entrada:

> ¿Cuál es el clima actual en Madrid y qué debo verificar antes de viajar a Europa?

El agente combina:

- Function Tool → clima actual.
- File Search/RAG → información de la guía.

Esto demuestra el enrutamiento entre diferentes fuentes de información.

## Conclusión

Las pruebas muestran que Tech Travel Agent puede seleccionar herramientas
según la intención de la consulta, recuperar información documental,
consultar información actual mediante una API y reconocer situaciones en
las que no dispone de evidencia suficiente.
