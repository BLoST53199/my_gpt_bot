import os
import threading
import logging
import openai
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Настройки
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Telegram логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Flask-приложение (для Render)
app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Бот запущен и работает!"

# Обработка сообщений от Telegram
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        bot_reply = response.choices[0].message["content"]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_reply)
    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Ошибка: {e}")

# Запуск Telegram-бота
def run_bot():
    app_bot = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app_bot.run_polling()

# Запуск Flask и Telegram-бота одновременно
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def receive_update():
    update = Update.de_json(request.get_json(force=True), bot)
    application.process_update(update)
    return 'ok'

# Запуск Webhook
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    HOST = '0.0.0.0'
    WEBHOOK_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TELEGRAM_BOT_TOKEN}"
    
    bot.set_webhook(WEBHOOK_URL)
    app.run(host=HOST, port=PORT)

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
