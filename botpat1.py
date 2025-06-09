# main.py
from fastapi import FastAPI, Body
from pydantic import BaseModel
import telegram
import asyncio
from telegram.ext import ApplicationBuilder, MessageHandler, filters
import os
import re
import fitz  # PyMuPDF for PDF reading
from transformers import pipeline
from bs4 import BeautifulSoup
import requests

app = FastAPI()

# Configuración del bot
TOKEN = "7100011466:AAG_4RNzAj7j3vQ5JZ5DfgpaMPeOxtGtpw0"
HUGGINGFACE_MODEL = "Kevincp560/bart-large-cnn-finetuned-pubmed"

# Inicializa el bot
bot = telegram.Bot(token=TOKEN)

# Modelo de Hugging Face para resumir artículos científicos
summary_model = pipeline("summarization", model=HUGGINGFACE_MODEL)

# Función para extraer texto de un PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Función para extraer texto de una URL pública
def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    return '\n'.join([p.get_text() for p in paragraphs])

# Función para generar caso clínico veterinario
def generate_case_clinico(summary):
    prompt = f"""
    Basado en el siguiente artículo científico de patología veterinaria:

    {summary}

    Genera un caso clínico veterinario estructurado con los siguientes puntos:

    - Historia clínica
    - Anamnesis
    - Pruebas diagnósticas
    - Identificación de lesiones
    - Diagnóstico definitivo

    Muestra todo de forma clara y profesional, como si fuera un paciente real.
    """
    return prompt

# Endpoint para recibir mensajes del bot
class UserMessage(BaseModel):
    chat_id: int
    message: str

@app.post("/message")
async def handle_message(data: UserMessage):
    chat_id = data.chat_id
    message = data.message

    if message.startswith("http"):
        article_text = extract_text_from_url(message)
    else:
        article_text = message

    summary = summary_model(article_text, max_length=500, min_length=150, do_sample=False)[0]['summary_text']
    case_prompt = generate_case_clinico(summary)

    await bot.send_message(chat_id=chat_id, text=case_prompt[:4096])  # Límite de Telegram

    return {"status": "success"}

# Función principal del bot
async def start_bot():
    app_builder = ApplicationBuilder().token(TOKEN)
    application = await app_builder.build()

    async def handle_update(update, context):
        user_id = update.effective_chat.id
        msg = update.message.text.strip()
        await handle_message(UserMessage(chat_id=user_id, message=msg))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_update))
    await application.run_polling()

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000)).start()
    asyncio.run(start_bot())
