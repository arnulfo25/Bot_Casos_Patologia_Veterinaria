import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = '7821284692:AAExmeBWdcfPB9es1CotZawbP-YsscWWIbQ'

welcome_msg = (
    "🌿 ¡Bienvenido al Bot de Aceites Esenciales! 🌿\n\n"
    "Antes de comenzar, recuerda:\n"
    "*Este bot no es un sustituto de consejo médico profesional. Consulta siempre a un especialista para temas de salud.*\n\n"
    "¿Cómo funciona?\n"
    "1️⃣ Cuéntame cómo te sientes o qué necesitas (ejemplo: \"estrés\", \"me duele la cabeza\", \"quiero dormir mejor\", \"ánimo bajo\").\n"
    "2️⃣ Te recomendaré aceites esenciales y formas de usarlos de manera segura y sencilla.\n\n"
    "¡Empecemos! ¿En qué puedo ayudarte hoy?"
)

recomendaciones = {
    'estrés': {
        'aceites': ['Lavanda', 'Bergamota', 'Ylang Ylang'],
        'uso': 'Difunde 3-5 gotas en tu habitación o inhala directamente del frasco. También puedes mezclar con aceite portador y aplicar en muñecas o cuello.'
    },
    'ansiedad': {
        'aceites': ['Lavanda', 'Naranja dulce', 'Manzanilla'],
        'uso': 'Inhala profundamente o coloca unas gotas en un pañuelo. Úsalo en difusor durante 20 minutos.'
    },
    'dolor de cabeza': {
        'aceites': ['Menta', 'Lavanda', 'Eucalipto'],
        'uso': 'Mezcla con aceite portador y aplica en sienes y nuca con suaves masajes.'
    },
    'ánimo bajo': {
        'aceites': ['Limón', 'Naranja', 'Pomelo'],
        'uso': 'Difunde en el ambiente o inhala directamente para levantar el ánimo.'
    },
    'dormir': {
        'aceites': ['Lavanda', 'Manzanilla', 'Sándalo'],
        'uso': 'Difunde en la habitación antes de dormir o coloca unas gotas en la almohada.'
    },
    'energía': {
        'aceites': ['Menta', 'Romero', 'Limón'],
        'uso': 'Inhala directamente o difunde en la mañana para activar tu energía.'
    }
}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(welcome_msg)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¿En qué puedo ayudarte?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    respuesta = (
        "No encontré una recomendación para tu necesidad. "
        "Prueba con palabras como: estrés, ansiedad, dolor de cabeza, ánimo bajo, dormir, energía."
    )
    for clave, valor in recomendaciones.items():
        if clave in text:
            aceites = ", ".join(valor['aceites'])
            uso = valor['uso']
            respuesta = (
                f"🌱 Para *{clave}*, te recomiendo:\n"
                f"Aceites: {aceites}\n"
                f"Modo de uso: {uso}\n\n"
                "¿Te gustaría otra recomendación? Solo dime tu necesidad."
            )
            break
    await update.message.reply_text(respuesta, parse_mode='Markdown')

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()