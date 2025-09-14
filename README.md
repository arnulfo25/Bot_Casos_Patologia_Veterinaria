# 🐾 PatBot: Asistente de Casos Clínicos Veterinarios

Un bot de Telegram diseñado por el **Dr. Arnulfo Villanueva Castillo** para ayudar a estudiantes de medicina veterinaria a convertir artículos científicos en casos clínicos prácticos y estructurados.

## 🎯 ¿Cuál es su utilidad?

La patología es una piedra angular en la formación veterinaria, pero a menudo el material de estudio se presenta en formato de artículos de investigación densos y difíciles de digerir. PatBot cierra la brecha entre la teoría y la práctica.

Este bot utiliza Inteligencia Artificial para leer un artículo científico en formato PDF que le envíes y lo transforma en un caso clínico simulado, con una estructura clara y fácil de seguir. Es la herramienta perfecta para:

-   **Practicar el razonamiento clínico:** Conecta los hallazgos de un paper con un paciente simulado.
-   **Estudiar de forma activa:** Transforma la lectura pasiva en un ejercicio de resolución de casos.
-   **Ahorrar tiempo:** Extrae la información más relevante de un artículo y la presenta de forma ordenada.

## 🚀 ¿Cómo usarlo?

¡Es muy fácil!

1.  Abre una conversación con el bot en Telegram.
2.  Simplemente adjunta un artículo científico en formato PDF.
3.  ¡Espera unos momentos y recibirás tu caso clínico listo para estudiar!

👉 **[¡Prueba el bot aquí!](https://t.me/casos_patologia_vet_bot)** 👈

## 📋 Estructura del Caso Clínico

Cada caso generado por el bot incluye las siguientes secciones:

-   📋 **Historia clínica**
-   🗣️ **Anamnesis**
-   🔬 **Pruebas diagnósticas**
-   👁️ **Identificación de lesiones**
-   🎯 **Diagnóstico definitivo**

---

## 💻 Para Desarrolladores

Si deseas contribuir o ejecutar este bot localmente, sigue estos pasos.

### Requisitos

-   Python 3.10 o superior
-   Una clave de API de [Telegram](https://core.telegram.org/bots#6-botfather)
-   Una clave de API de [OpenRouter](https://openrouter.ai/keys)

### Instalación

1.  **Clona el repositorio** y navega al directorio.
2.  **Crea y activa un entorno virtual:** `python3 -m venv venv && source venv/bin/activate`
3.  **Instala las dependencias:** `pip install -r requirements.txt`
4.  **Configura tus claves de API:** Crea un archivo `.env` en la raíz del proyecto y añade tus claves (`TELEGRAM_TOKEN` y `OPENROUTER_API_KEY`).
5.  **Ejecuta el bot:** `python patbot.py`