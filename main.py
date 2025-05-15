import os
import requests
from flask import Flask, request
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # যেমন: https://your-render-app.onrender.com

CHARACTER_NAME = "Luna"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Generate reply using OpenRouter (Mythy 7B)
def generate_reply(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://t.me/YOUR_BOT_USERNAME",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gryphe/mythomax-l2-13b",
        "messages": [
            {"role": "system", "content": f"You are {CHARACTER_NAME}, a romantic and sweet virtual girlfriend."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# Handle Telegram messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        reply = generate_reply(message.text)
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        bot.send_message(message.chat.id, "Sorry, I'm having trouble replying right now.")
        print("Error:", e)

# Flask route for Telegram webhook
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Set webhook when server starts
@app.before_first_request
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{BOT_TOKEN}")
    print("Webhook set successfully.")

# Root route (optional)
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

# Start the server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
