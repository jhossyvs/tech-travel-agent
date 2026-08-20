# ✈️ Tech Travel Agent

Agente de IA conversacional construido con **Microsoft Azure AI Foundry + Python**.

Tech Travel Agent ayuda al usuario a resolver consultas relacionadas con viajes, utilizando un modelo de lenguaje y herramientas externas para obtener información que el modelo no debería inventar.

## 🎯 Objetivo

Construir un agente de viajes capaz de:

- Responder preguntas generales sobre viajes.
- Consultar información contenida en documentos mediante RAG.
- Obtener el clima actual de una ciudad mediante una API externa.
- Elegir automáticamente cuándo utilizar una herramienta.
- Reconocer cuando una fuente no contiene la información solicitada.
- Manejar errores de servicios externos de forma controlada.

---

## 🏗️ Arquitectura

```text
                    ┌─────────────────────┐
                    │       Usuario       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Tech Travel Agent  │
                    │      gpt-4.1        │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐       ┌──────────────────┐
       │   File Search    │       │ Function Calling │
       │       RAG        │       │                  │
       └────────┬─────────┘       └────────┬─────────┘
                │                          │
                ▼                          ▼
       ┌──────────────────┐       ┌──────────────────┐
       │ Documentos de    │       │ Open-Meteo API   │
       │ conocimiento     │       │                  │
       └──────────────────┘       └──────────────────┘
```

### Componentes

| Componente | Responsabilidad |
|---|---|
| Azure AI Foundry | Plataforma para administrar el proyecto y agente |
| GPT-4.1 | Modelo de lenguaje utilizado por el agente |
| Agent | Define comportamiento, instrucciones y herramientas |
| Conversation | Mantiene el contexto de una sesión |
| File Search | Recupera información desde documentos |
| Function Calling | Permite ejecutar funciones Python |
| Open-Meteo | Proporciona información meteorológica actual |
| Python | Implementación del cliente y herramientas |
| `DefaultAzureCredential` | Autenticación mediante Azure CLI |

---

## 🧰 Tecnologías

- Python 3.14
- Azure AI Foundry
- Azure AI Projects SDK `2.4.0`
- Azure Identity
- OpenAI Responses API
- Function Calling
- File Search / RAG
- Open-Meteo API
- `requests`
- `python-dotenv`

---

## 📁 Estructura del proyecto

```text
tech-travel-agent/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── agente.py
├── crear_agente.py
├── herramientas.py
│
├── data/
│   └── ...
│
└── docs/
    └── ...
```

### `crear_agente.py`

Crea una nueva versión del agente en Azure AI Foundry.

Aquí se define:

- Nombre del agente.
- Modelo utilizado.
- Instrucciones.
- Herramientas disponibles.
- Schema de las funciones.

### `agente.py`

Es el punto de entrada de la aplicación.

Se encarga de:

1. Conectarse al proyecto de Foundry.
2. Obtener el agente publicado.
3. Crear una conversación.
4. Enviar mensajes.
5. Detectar `function_call`.
6. Ejecutar la función correspondiente.
7. Enviar el resultado nuevamente al modelo.
8. Mostrar la respuesta final.

### `herramientas.py`

Contiene las funciones que puede ejecutar el agente.

Actualmente incluye:

```text
obtener_clima_real(ciudad)
```

Esta función:

1. Busca la ciudad mediante geocodificación.
2. Obtiene sus coordenadas.
3. Consulta el clima actual.
4. Devuelve una respuesta simplificada al agente.

---

# 🚀 Instalación

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd tech-travel-agent
```

## 2. Crear entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Configurar Azure

Inicia sesión mediante Azure CLI:

```bash
az login
```

Comprueba la cuenta:

```bash
az account show
```

La identidad utilizada debe tener permisos suficientes sobre el proyecto de Azure AI Foundry.

---

# 🔐 Configuración

Crea un archivo `.env` a partir de `.env.example`:

```bash
cp .env.example .env
```

El archivo debe contener:

```env
FOUNDRY_PROJECT_ENDPOINT=https://.../api/projects/tech-travel-agent
FOUNDRY_MODEL_NAME=gpt-4.1
AGENT_NAME=tech-travel-agent
```

> **Importante:** nunca subas `.env` al repositorio.

El proyecto utiliza `DefaultAzureCredential`, por lo que no es necesario guardar una clave de Azure OpenAI en el código.

---

# 🤖 Crear o actualizar el agente

Ejecuta:

```bash
python crear_agente.py
```

Una ejecución exitosa mostrará algo similar a:

```text
Agente creado correctamente.
Nombre: tech-travel-agent
Versión: 3
```

Cada vez que se modifica la definición del agente, se puede publicar una nueva versión.

La aplicación utiliza el nombre del agente publicado en lugar de crear un agente nuevo en cada conversación.

---

# 💬 Ejecutar el agente

```bash
python agente.py
```

El programa inicia una conversación interactiva:

```text
Tech Travel Agent
Escribe 'salir' para terminar.

Tú:
```

Para finalizar:

```text
salir
```

---

# 🛠️ Herramientas

## 🌤️ Obtener clima

El agente dispone de una función:

```text
obtener_clima
```

El modelo decide cuándo utilizarla basándose en las instrucciones y en la consulta del usuario.

Por ejemplo:

```text
Tú: ¿Cuál es el clima actual en Madrid?
```

El modelo puede generar un `function_call`:

```json
{
  "name": "obtener_clima",
  "arguments": {
    "ciudad": "Madrid"
  }
}
```

La aplicación recibe esa llamada y ejecuta:

```python
obtener_clima_real("Madrid")
```

Después devuelve el resultado al modelo mediante `function_call_output`.

Finalmente, el modelo genera una respuesta para el usuario:

```text
Actualmente en Madrid la temperatura es de 21.4 °C,
con un viento de 3.6 km/h.
```

---

# 📚 RAG / File Search

El agente también puede utilizar documentos como fuente de conocimiento.

El flujo es:

```text
Documento
   ↓
Vector Store
   ↓
File Search
   ↓
Agente
   ↓
Respuesta basada en evidencia
```

El objetivo es evitar que el modelo invente información que no se encuentra en los documentos proporcionados.

Por ejemplo, si el documento contiene una guía de viaje:

```text
¿Qué debo verificar antes de viajar a Europa?
```

El agente puede utilizar el contenido del documento para responder.

Si se pregunta por información que no está disponible:

```text
¿Qué requisitos necesito para obtener una visa de estudiante en Alemania?
```

El comportamiento esperado es reconocer que el documento no contiene esa información, en lugar de inventarla.

---

# 🔀 Enrutamiento de herramientas

Una de las capacidades principales del proyecto es permitir que el modelo determine qué fuente utilizar.

### Consulta general

```text
¿Qué debo verificar antes de viajar a Europa?
```

→ Conocimiento / File Search

### Consulta meteorológica

```text
¿Cuál es el clima actual en Madrid?
```

→ `obtener_clima`

### Consulta combinada

```text
¿Cuál es el clima actual en Madrid y qué debo verificar antes
de viajar a Europa?
```

→ File Search + Function Calling

El modelo puede utilizar ambas fuentes para construir una única respuesta.

---

# 🧪 Pruebas realizadas

## Caso 1 — Consulta general

### Entrada

```text
¿Qué debo verificar antes de viajar a Europa?
```

### Resultado esperado

El agente debe responder utilizando la información disponible en la guía de conocimiento.

### Resultado

El agente proporcionó recomendaciones relacionadas con:

- Documentación.
- Vigencia del pasaporte.
- Seguro de viaje.
- Reservas.
- Presupuesto.

---

## Caso 2 — Clima

### Entrada

```text
¿Cuál es el clima actual en Madrid?
```

### Resultado esperado

El agente debe utilizar `obtener_clima`.

### Resultado

El agente obtuvo información real mediante Open-Meteo:

```text
Actualmente en Madrid la temperatura es de 21.4 °C
y hay un viento de 3.6 km/h.
```

---

## Caso 3 — Ciudad inexistente

### Entrada

```text
¿Cuál es el clima actual en Xyzabc?
```

### Resultado esperado

La aplicación no debe inventar información.

### Resultado

El agente indicó que no pudo encontrar la ciudad.

---

## Caso 4 — Servicio externo no disponible

Se simuló un error modificando temporalmente el endpoint de geocodificación.

### Resultado esperado

La aplicación debe manejar el fallo sin mostrar un traceback al usuario.

### Resultado

El agente respondió indicando que no podía consultar el clima en ese momento.

---

## Caso 5 — Información fuera del conocimiento disponible

### Entrada

```text
¿Qué requisitos necesito para obtener una visa de estudiante en Alemania?
```

### Resultado esperado

El agente debe reconocer que la guía disponible no contiene esa información.

### Resultado

El agente indicó que la información específica no estaba disponible y recomendó consultar fuentes oficiales.

---

# ⚠️ Manejo de errores

La aplicación contempla diferentes tipos de errores:

### Ciudad inexistente

```text
No encontré la ciudad solicitada.
```

### Servicio meteorológico no disponible

```text
No puedo consultar el clima en este momento.
```

### Información ausente en RAG

```text
La información solicitada no está disponible
en la documentación proporcionada.
```

El objetivo es evitar:

- Datos inventados.
- Respuestas con falsa certeza.
- Tracebacks visibles al usuario.
- Dependencia silenciosa de información no verificada.

---

# 🔒 Seguridad

El proyecto sigue algunas prácticas básicas de seguridad:

- Las credenciales no están almacenadas en el código.
- `.env` está incluido en `.gitignore`.
- `.venv` no se versiona.
- Se utiliza `DefaultAzureCredential`.
- Los datos utilizados para las pruebas deben ser publicables.
- No deben incluirse datos personales o información confidencial.
- Los secretos nunca deben aparecer en commits.

Ejemplo de archivos ignorados:

```gitignore
.env
.venv/
__pycache__/
*.pyc
.DS_Store
```

---

# 💰 Costos

El proyecto utiliza recursos de Azure AI Foundry y un deployment de modelo.

Antes de ejecutar el proyecto en un entorno real se deben revisar:

- Modelo utilizado.
- Región.
- Cuota.
- Tokens utilizados.
- Frecuencia de solicitudes.
- Vector stores creados.
- Recursos temporales.

Los recursos de prueba deben eliminarse cuando ya no sean necesarios.

---

# 📊 Limitaciones actuales

El agente es un prototipo educativo.

Actualmente:

- La información meteorológica depende de Open-Meteo.
- El conocimiento documental depende de los archivos indexados.
- No realiza reservas reales.
- No compra vuelos ni hoteles.
- No ejecuta acciones sensibles.
- No sustituye fuentes oficiales para requisitos migratorios.
- La interfaz actual es de línea de comandos.

---

# 🔮 Mejoras futuras

Posibles extensiones:

1. Añadir búsqueda de vuelos.
2. Añadir búsqueda de hoteles.
3. Incorporar información de transporte.
4. Añadir fuentes oficiales para requisitos migratorios.
5. Crear una interfaz web con FastAPI.
6. Mantener conversaciones persistentes.
7. Añadir autenticación.
8. Añadir observabilidad y métricas.
9. Implementar evaluación automática.
10. Desplegar el backend en Azure Container Apps.

---

# 🧠 Arquitectura del flujo de Function Calling

```text
Usuario
   │
   ▼
Responses API
   │
   ▼
¿Necesita una herramienta?
   │
   ├── No ───────────────► Respuesta final
   │
   └── Sí
        │
        ▼
   function_call
        │
        ▼
Aplicación Python
        │
        ▼
obtener_clima_real()
        │
        ▼
Open-Meteo API
        │
        ▼
function_call_output
        │
        ▼
Responses API
        │
        ▼
Respuesta final
```

Este patrón permite que el modelo decida **qué hacer**, mientras que la aplicación mantiene el control sobre **la ejecución real de la función**.

---

# 📋 Requisitos del proyecto final

El proyecto cumple los requisitos técnicos principales:

- [x] Agente funcional.
- [x] Modelo desplegado en Azure AI Foundry.
- [x] Instrucciones específicas.
- [x] Function Calling.
- [x] API externa.
- [x] File Search / RAG.
- [x] Variables de entorno.
- [x] `.env.example`.
- [x] `.gitignore`.
- [x] Manejo de errores externos.
- [x] Pruebas normales.
- [x] Pruebas límite.
- [x] Pruebas de fallo.
- [x] Documentación.

---

# 👤 Autor

**Jhossy Vargas**

Proyecto desarrollado como parte del microprograma:

**Agentes de IA con Microsoft Foundry + Python**

Agosto 2026.