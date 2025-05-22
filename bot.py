import os
import openai
import telebot
from flask import Flask, request

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

print("TELEGRAM_BOT_TOKEN:", TELEGRAM_BOT_TOKEN)
print("OPENAI_API_KEY:", "есть" if OPENAI_API_KEY else "нет")
print("WEBHOOK_URL:", WEBHOOK_URL)

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    print("Получено сообщение:", message.text)
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
        print("Ответ отправлен:", reply)
    except Exception as e:
        bot.send_message(message.chat.id, "Ошибка: " + str(e))
        print("Ошибка OpenAI:", e)
        
@app.route("/", methods=["GET"])
def index():
    return "Бот работает", 200
    
@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    print("Webhook обновление:", update)
    bot.process_new_updates([update])
    return "!", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{TELEGRAM_BOT_TOKEN}")
    print("Webhook установлен!")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
