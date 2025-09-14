import os
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env al iniciar el script
load_dotenv()

# --- Telegram Bot Configuration ---
# Obtén tu token de BotFather en Telegram y guárdalo como una variable de entorno
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8190615854:AAEUfejUULkcjCVc7_PxAjopNA3tUnJnkFA")

# --- OpenRouter API Configuration ---
# Obtén tu API Key de https://openrouter.ai/keys y guárdala como una variable de entorno
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")

# --- Model and Prompt Configuration ---
# Modelo a utilizar en OpenRouter. Puedes encontrar más en https://openrouter.ai/models
MODEL_NAME = "qwen/qwen3-235b-a22b:free"

# Límite de caracteres para el texto enviado al modelo de IA para controlar costos y tiempos
MAX_PROMPT_TEXT_LENGTH = 8000

# Límite de caracteres por mensaje de Telegram
TELEGRAM_MAX_MESSAGE_LENGTH = 4096

# Plantilla del prompt para generar el caso clínico
PROMPT_TEMPLATE = """
Basado en el siguiente artículo científico de patología veterinaria:

--- INICIO DEL ARTÍCULO ---
{text}
--- FIN DEL ARTÍCULO ---

Actúa como un patólogo veterinario experto que está creando un caso de estudio para estudiantes. Genera un caso clínico veterinario que sea atractivo, educativo y fácil de seguir. Usa un tono profesional pero cercano.

Estructura el caso con los siguientes apartados, usando negritas (con etiquetas <b>) para los títulos:

- 📋 <b>Historia clínica:</b> (Describe la reseña del animal y el motivo de la consulta).
- 🗣️ <b>Anamnesis:</b> (Describe la historia contada por el propietario).
- 🔬 <b>Pruebas diagnósticas:</b> (Enumera las pruebas realizadas y sus resultados).
- 👁️ <b>Identificación de lesiones:</b> (Describe las lesiones macroscópicas y/o microscópicas encontradas).
- 🎯 <b>Diagnóstico definitivo:</b> (Establece el diagnóstico final basado en toda la información anterior).
"""

# --- Bot Messages ---
INTRO_MESSAGE = (
    "👋 ¡Bienvenido al Bot de Patología Veterinaria! Creado por <b>Dr. Arnulfo Villanueva Castillo</b>.\n\n"
    "Envía un artículo científico en PDF y la IA generará un caso clínico para que practiques. "
    "El caso incluirá historia clínica, anamnesis, pruebas diagnósticas, identificación de lesiones y diagnóstico definitivo.\n\n"
    "Simplemente adjunta tu PDF y espera la respuesta."
)

CREDITS_MESSAGE = (
    "Este bot fue desarrollado con mucho esmero por el <b>Dr. Arnulfo Villanueva Castillo</b> 🎓.\n\n"
    "Su objetivo es ser una herramienta de apoyo para estudiantes de veterinaria. ¡Aprovéchalo!"
)

GUIDE_MESSAGE = "Por favor, para generar un caso clínico, envíame un archivo en formato PDF."
