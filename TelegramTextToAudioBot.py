mkdir -p .github/workflows
nano .github/workflows/github-actions-demo.yml
name: GitHub Actions Demo
run-name: ${{ github.actor }} is testing out GitHub Actions 🚀
on: [push]
jobs:
  Explore-GitHub-Actions:
    runs-on: ubuntu-latest
    steps:
      - run: echo "🎉 The job was automatically triggered by a ${{ github.event_name }} event."
      - run: echo "🐧 This job is now running on a ${{ runner.os }} server hosted by GitHub!"
      - run: echo "🔎 The name of your branch is ${{ github.ref }} and your repository is ${{ github.repository }}."
      - name: Check out repository code
        uses: actions/checkout@v4
      - run: echo "💡 The ${{ github.repository }} repository has been cloned to the runner."
      - run: echo "🖥️ The workflow is now ready to test your code on the runner."
      - name: List files in the repository
        run: |
          ls ${{ github.workspace }}
      - run: echo "🍏 This job's status is ${{ job.status }}."
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

# Función para manejar el comando /start
async def start(update: Update, context: CallbackContext) -> None:
    logger.info("Comando /start recibido")
    keyboard = [["Español", "Inglés"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        'Hola! Soy un bot que convierte texto a audio. 🎤\n\n'
        '📜 **Descripción:**\n'
        'Este bot te permite convertir cualquier texto que escribas en un archivo de audio.\n\n'
        '📜 **Instrucciones:**\n'
        '1️⃣ Selecciona un idioma: Español o Inglés.\n'
        '2️⃣ Escribe el texto que deseas convertir a audio.\n\n'
        '🎧 ¡Recibirás un archivo de audio con tu texto convertido!',
        reply_markup=reply_markup
    )

# Variable global para el idioma
global_language = 'es'

# Función para cambiar el idioma
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

# Función para convertir texto a audio
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

# Función principal para iniciar el bot
def main() -> None:
    # Token del bot
    TOKEN = '7124432239:AAEbWKfgQZa_CAsPbBsCYnGnFJ-4T_NcnKo'

    # Crear la aplicación del bot
    application = Application.builder().token(TOKEN).build()

    # Registrar comandos y manejadores
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.Regex('^(Español|Inglés)$'), set_language))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_audio))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
    git add .github/workflows/github-actions-demo.yml
git commit -m "Add GitHub Actions demo workflow"
git push origin main
