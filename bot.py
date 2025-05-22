import os
import logging
import openai
import telebot
from flask import Flask, request

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получаем переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Проверка переменных окружения
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY or not WEBHOOK_URL:
    raise ValueError("Переменные окружения не заданы!")

# Устанавливаем API-ключи
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Flask-приложение
app = Flask(__name__)

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    logging.info(f"Получено сообщение: {message.text}")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный помощник."},
                {"role": "user", "content": message.text},
            ]
        )
        reply = response['choices'][0]['message']['content']
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {str(e)}")
        bot.send_message(message.chat.id, "Произошла ошибка: " + str(e))

# Обработка входящих запросов от Telegram
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    logging.info("Webhook получил запрос")
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

# Главная страница (для проверки работоспособности)
@app.route("/", methods=["GET"])
def index():
    return "Бот работает!", 200

# Запуск приложения
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}")
    logging.info("Webhook установлен")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
