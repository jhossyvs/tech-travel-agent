import os

from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    FileSearchTool,
    FunctionTool,
    PromptAgentDefinition,
)
from azure.identity import DefaultAzureCredential

load_dotenv()

project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai = project.get_openai_client()

# ============================================================
# 1. Vector Store para conocimiento del agente
# ============================================================

vector_store = openai.vector_stores.create(
    name="vs-guia-viaje-europa"
)

with open("data/guia-viaje-europa.txt", "rb") as archivo:
    openai.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=archivo,
    )

file_search = FileSearchTool(
    vector_store_ids=[vector_store.id]
)

# ============================================================
# 2. Function Tool: clima
# ============================================================

clima_tool = FunctionTool(
    name="obtener_clima",
    description=(
        "Obtiene el clima actual de una ciudad. "
        "Debe utilizarse cuando el usuario pregunte por "
        "el clima o temperatura actual de una ciudad."
    ),
    parameters={
        "type": "object",
        "properties": {
            "ciudad": {
                "type": "string",
                "description": "Nombre de la ciudad.",
            }
        },
        "required": ["ciudad"],
        "additionalProperties": False,
    },
    strict=True,
)

# ============================================================
# 3. Crear nueva versión del agente
# ============================================================

agent = project.agents.create_version(
    agent_name="tech-travel-agent",
    definition=PromptAgentDefinition(
        model=os.environ["FOUNDRY_MODEL_NAME"],
        instructions=(
            "Eres Tech Travel Agent, un asistente de viajes. "
            "Responde siempre en español. "
            "Sé claro y útil. "
            "No inventes información. "

            "Cuando el usuario pregunte por el clima actual "
            "de una ciudad, utiliza la herramienta obtener_clima. "

            "Cuando el usuario pregunte sobre documentación, "
            "planificación o información contenida en la guía de "
            "viaje, utiliza File Search. "

            "Si File Search no contiene información suficiente "
            "para responder, indícalo claramente y no inventes "
            "información."
        ),
        tools=[
            clima_tool,
            file_search,
        ],
    ),
)

print("Agente creado correctamente.")
print(f"Nombre: {agent.name}")
print(f"Versión: {agent.version}")
print(f"Vector Store: {vector_store.id}")