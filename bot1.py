from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from gtts import gTTS
import os
import logging

# Configurar el registro para depuración
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    logger.info("Comando /start recibido")
    keyboard = [["Español", "Inglés"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        'Hola! Soy un bot que convierte texto a audio.\n'
        'Por favor, selecciona un idioma para el texto a convertir:',
        reply_markup=reply_markup
    )
    await update.message.reply_text(
        'Instrucciones:\n'
        '1. Usa el comando /start para iniciar el bot.\n'
        '2. Selecciona un idioma escribiendo "Español" o "Inglés".\n'
        '3. Envía un texto para convertirlo a audio en el idioma seleccionado.'
    )

# Variable global para el idioma
global_language = 'es'

async def set_language(update: Update, context: CallbackContext) -> None:
    logger.info(f"Mensaje recibido para cambiar idioma: {update.message.text}")
    global global_language
    language = update.message.text.lower()
    if language == "español":
        global_language = 'es'
        await update.message.reply_text('Idioma cambiado a Español.')
    elif language == "inglés":
        global_language = 'en'
        await update.message.reply_text('Idioma cambiado a Inglés.')
    else:
        await update.message.reply_text('Por favor, selecciona un idioma válido: Español o Inglés.')

async def text_to_audio(update: Update, context: CallbackContext) -> None:
    logger.info(f"Mensaje recibido para convertir texto a audio: {update.message.text}")
    global global_language
    text = update.message.text
    try:
        tts = gTTS(text=text, lang=global_language)
        audio_file = 'output.mp3'
        tts.save(audio_file)
        with open(audio_file, 'rb') as audio:
            await update.message.reply_audio(audio)
        os.remove(audio_file)
    except Exception as e:
        logger.error(f"Error al convertir texto a audio: {e}")
        await update.message.reply_text(f'Error al convertir texto a audio: {e}')

def main() -> None:
    # Token del bot
    TOKEN = '7124432239:AAEbWKfgQZa_CAsPbBsCYnGnFJ-4T_NcnKo'

    # Reemplazar Updater por Application
    application = Application.builder().token(TOKEN).build()

    # Ajustar los manejadores para evitar conflictos
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Regex('^(Español|Inglés)$'), set_language))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_audio))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
