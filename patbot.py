import logging
import fitz  # PyMuPDF
import httpx  # Usar httpx para solicitudes asíncronas
import tempfile
import os
import asyncio  # Para correr funciones síncronas en un hilo separado
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import config

logging.basicConfig(level=logging.INFO)

def extract_text_from_pdf(pdf_path):
    """Extrae texto de un archivo PDF."""
    try:
        doc = fitz.open(pdf_path)
        text = "".join(page.get_text() for page in doc)
        logging.info(f"Texto extraído del PDF (primeros 500 caracteres): {text[:500]}")
        return text
    except Exception as e:
        logging.error(f"Error al extraer texto del PDF: {e}")
        return None

async def generate_case_from_text(text: str) -> str:
    """Genera un caso clínico a partir de un texto usando la API de OpenRouter de forma asíncrona."""
    prompt = config.PROMPT_TEMPLATE.format(text=text[:config.MAX_PROMPT_TEXT_LENGTH])
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": config.MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=180
            )
            response.raise_for_status()
            result = response.json()

            if 'choices' in result and result['choices'] and 'message' in result['choices'][0] and 'content' in result['choices'][0]['message']:
                return result['choices'][0]['message']['content']
            else:
                logging.warning(f"Respuesta inesperada de la API: {result}")
                return "La IA no pudo generar una respuesta válida. La estructura de la respuesta no fue la esperada."
        except httpx.TimeoutException:
            logging.error("La solicitud a la API de OpenRouter ha expirado.")
            return "La generación del caso ha tardado demasiado y ha expirado. Inténtalo de nuevo."
        except httpx.RequestError as e:
            logging.error(f"Error en la solicitud a la API de OpenRouter: {e}")
            return f"Ocurrió un error al comunicarse con el servicio de IA: {e}"
        except Exception as e:
            logging.error(f"Error inesperado al procesar la respuesta de la API: {e}")
            return "Ocurrió un error inesperado al procesar la respuesta de la IA."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /start."""
    await update.message.reply_text(config.INTRO_MESSAGE, parse_mode='HTML')

async def credits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra los créditos del bot."""
    await update.message.reply_text(config.CREDITS_MESSAGE, parse_mode='HTML')

async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja los archivos PDF enviados al bot."""
    if not update.message.document or not update.message.document.file_name.lower().endswith('.pdf'):
        await update.message.reply_text("Por favor, envía un archivo PDF válido.")
        return

    await update.message.reply_text("Descargando y procesando el PDF, esto puede tardar unos segundos...")
    pdf_file = await context.bot.get_file(update.message.document.file_id)

    pdf_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            await pdf_file.download_to_drive(tmp_file.name)
            pdf_path = tmp_file.name

        text = await asyncio.to_thread(extract_text_from_pdf, pdf_path)

        if not text or not text.strip():
            await update.message.reply_text("No se pudo extraer texto del PDF. Asegúrate de que no sea un PDF de solo imágenes (escaneado) o esté vacío.")
            return

        await update.message.reply_text("PDF procesado. Generando el caso clínico con IA... 🤖")
        case = await generate_case_from_text(text)

        full_response = f"{case}\n\n---\n\n{config.CREDITS_MESSAGE}"

        for i in range(0, len(full_response), config.TELEGRAM_MAX_MESSAGE_LENGTH):
            await update.message.reply_text(full_response[i:i + config.TELEGRAM_MAX_MESSAGE_LENGTH], parse_mode='HTML')

    except Exception as e:
        logging.error(f"Error inesperado en handle_pdf: {e}")
        await update.message.reply_text("Ocurrió un error inesperado al procesar el PDF.")
    finally:
        if pdf_path and os.path.exists(pdf_path):
            os.remove(pdf_path)

async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a mensajes que no son el comando start ni un PDF."""
    await update.message.reply_text(config.GUIDE_MESSAGE)

def main():
    """Inicia el bot de Telegram."""
    app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("creditos", credits))
    app.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"), handle_pdf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_other_messages))
    
    logging.info("Bot corriendo...")
    app.run_polling()

if __name__ == "__main__":
    main()