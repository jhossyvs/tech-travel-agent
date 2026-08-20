import json
import os

from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from herramientas import obtener_clima_real

load_dotenv()

project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai = project.get_openai_client(
    agent_name="tech-travel-agent"
)

conversation = openai.conversations.create()

print("Tech Travel Agent")
print("Escribe 'salir' para terminar.\n")

while True:
    pregunta = input("Tú: ")

    if pregunta.lower() in {"salir", "exit", "quit"}:
        print("¡Hasta luego!")
        break

    response = openai.responses.create(
        conversation=conversation.id,
        input=pregunta,
    )

    # Procesar las Function Tools que solicite el agente
    for item in response.output:
        if item.type == "function_call":
            argumentos = json.loads(item.arguments)

            if item.name == "obtener_clima":
                resultado = obtener_clima_real(
                    argumentos["ciudad"]
                )

                response = openai.responses.create(
                    conversation=conversation.id,
                    input=[
                        {
                            "type": "function_call_output",
                            "call_id": item.call_id,
                            "output": resultado,
                        }
                    ],
                )

    print(f"\nAgente: {response.output_text}\n")