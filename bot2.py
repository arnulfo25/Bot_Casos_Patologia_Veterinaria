from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import requests
import logging

# Configuración del bot y OpenRouter
BOT_TOKEN = "7628252959:AAGJmD9eVM7Y06KruWWkPSiWJU_MOU5xZSI"
API_KEY = "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"
MODEL_NAME = "qwen/qwen3-235b-a22b:free"

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Función para manejar el comando /start
async def start(update: Update, context: CallbackContext) -> None:
    logger.info("Comando /start recibido")
    await update.message.reply_text(
        "🌟 ¡Bienvenido a NovelistaBot! 🌟\n\n"
        "🎭 **Crea novelas cortas personalizadas para tus redes sociales.** 🎭\n\n"
        "📜 **Instrucciones:**\n"
        "1️⃣ Escribe los personajes separados por comas.\n"
        "2️⃣ Selecciona la categoría: ficción, no ficción, terror, romance, etc.\n"
        "3️⃣ Define el tono: humorístico, dramático, misterioso, etc.\n"
        "4️⃣ Elige el tamaño de la novela (150 a 500 palabras).\n\n"
        "✍️ Ejemplo: `Juan, María, un perro | terror | misterioso | 300`\n\n"
        "✨ ¡Deja que la magia de las palabras comience! ✨"
    )

# Función para generar la novela
async def generate_story(update: Update, context: CallbackContext) -> None:
    logger.info("Generando historia...")
    user_input = update.message.text

    try:
        # Parsear la entrada del usuario
        parts = user_input.split('|')
        if len(parts) != 4:
            await update.message.reply_text(
                "⚠️ Formato incorrecto. Por favor, sigue el ejemplo: `Juan, María, un perro | terror | misterioso | 300`"
            )
            return

        characters = parts[0].strip()
        category = parts[1].strip()
        tone = parts[2].strip()
        try:
            word_count = int(parts[3].strip())
            if word_count not in [100, 150, 200, 250, 300, 350, 400, 450, 500]:
                raise ValueError
        except ValueError:
            await update.message.reply_text(
                "⚠️ El tamaño debe ser uno de los siguientes valores: 100, 150, 200, 250, 300, 350, 400, 450, 500."
            )
            return

        # Llamada a la API de OpenRouter para generar la novela
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": "Eres un novelista experto en crear historias cortas."},
                    {
                        "role": "user",
                        "content": (
                            f"Escribe una novela corta de {word_count} palabras.\n"
                            f"Personajes: {characters}.\n"
                            f"Categoría: {category}.\n"
                            f"Tono: {tone}."
                        )
                    }
                ]
            }
        )

        response.raise_for_status()
        result = response.json()

        # Validar la respuesta generada
        if 'choices' in result and isinstance(result['choices'], list) and len(result['choices']) > 0:
            story = result['choices'][0]['message']['content']
            await update.message.reply_text(f"📖 **Tu novela corta:**\n\n{story}")
        else:
            await update.message.reply_text("⚠️ No se pudo generar la novela. Intenta nuevamente más tarde.")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error de conexión con la API: {e}")
        await update.message.reply_text("⚠️ Error de conexión con la API. Por favor, intenta más tarde.")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        await update.message.reply_text("⚠️ Ocurrió un error inesperado. Por favor, intenta más tarde.")

# Función principal para iniciar el bot
def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    # Registrar comandos y manejadores
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_story))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
