import telebot
import requests

BOT_TOKEN = '7226274181:AAEbzTRtg_GciVh_wd1042QFMiu9YR-FaJ0'
OPENROUTER_API_KEY = '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'
CHARACTER_NAME = "Luna"  # যেকোনো রোমান্টিক নাম

bot = telebot.TeleBot(BOT_TOKEN)

def generate_reply(user_input):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://t.me/YOUR_BOT_USERNAME",  # তোমার বটের ইউজারনেম
        "Content-Type": "application/json"
    }

    data = {
        "model": "gryphe/mythomax-l2-13b",  # Mythy 7B/13B (GPT-3.5 লেভেল)
        "messages": [
            {"role": "system", "content": f"You are {CHARACTER_NAME}, a romantic and sweet virtual girlfriend who always replies with affection."},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        reply = generate_reply(message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "Sorry, I couldn't reply right now.")
        print(f"Error: {e}")

bot.polling()
