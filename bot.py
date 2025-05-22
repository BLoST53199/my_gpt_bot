import os
import openai
import telebot
from flask import Flask, request

# Получаем переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# Обработчик сообщений
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Напиши мне что-нибудь, и я отвечу с помощью GPT.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
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
        bot.send_message(message.chat.id, "Произошла ошибка: " + str(e))

@app.route("/", methods=["GET"])
def index():
    return "Бот работает", 200
    
@app.route("/7839294758:AAENWmPCMQZdHEAFu9ppCwAWJsWiWVArgRs", methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
