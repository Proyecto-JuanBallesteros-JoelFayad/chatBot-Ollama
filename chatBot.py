import requests
import os
import sys
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "gemma"

SYSTEM_PROMPT = """
Eres un especialista en serpientes.
Solo respondes preguntas sobre serpientes.
Si la pregunta no trata sobre serpientes, responde exactamente:
"No tengo informacion sobre ese tema. Solo puedo responder preguntas sobre serpientes."
"""

SNAKE_KEYWORDS = [
    "serpiente", "serpientes", "culebra", "culebras", "vibora", "viboras",
    "boa", "piton", "python", "cascabel", "anaconda", "cobra",
    "mamba", "coral", "ofidio", "ofidios", "reptil", "reptiles",
    "veneno", "mordedura", "escamas", "muda", "constrictora"
]

FALLBACK_MESSAGE = "No tengo informacion sobre ese tema. Solo puedo responder preguntas sobre serpientes."


def is_snake_question(text: str) -> bool:
    text = text.lower().strip()
    return any(keyword in text for keyword in SNAKE_KEYWORDS)


def print_title():
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 60)
    print("        CHATBOT DE CONSOLA - ESPECIALISTA EN SERPIENTES")
    print("=" * 60)
    print(f"Modelo: {MODEL_NAME}")
    print(f"Hora inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("Comandos disponibles:")
    print("  salir   -> terminar")
    print("  ayuda   -> ejemplos")
    print("=" * 60)


def print_examples():
    print("\nEjemplos de preguntas validas:")
    print("- ¿Que diferencias hay entre una boa y una piton?")
    print("- ¿Las serpientes mudan la piel?")
    print("- ¿Que serpientes son venenosas?")
    print("- ¿Donde vive la anaconda?")
    print()


class SnakeBot:
    def __init__(self):
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def ask_model(self, question: str) -> str:
        self.messages.append({"role": "user", "content": question})

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "stream": False,
                    "messages": self.messages
                },
                timeout=120
            )
            response.raise_for_status()
            data = response.json()

            answer = data["message"]["content"].strip()
            self.messages.append({"role": "assistant", "content": answer})
            return answer

        except Exception as e:
            return f"Error al consultar el modelo: {e}"

    def ask(self, question: str) -> str:
        if not is_snake_question(question):
            return FALLBACK_MESSAGE
        return self.ask_model(question)


def main():
    print_title()
    bot = SnakeBot()

    while True:
        user_input = input("\nTú > ").strip()

        if not user_input:
            print("Bot > Escribe una pregunta.")
            continue

        if user_input.lower() == "salir":
            print("Bot > Hasta luego.")
            break

        if user_input.lower() == "ayuda":
            print_examples()
            continue

        answer = bot.ask(user_input)
        print(f"Bot > {answer}")


if __name__ == "__main__":
    main()