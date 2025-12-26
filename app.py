import os
import telebot
from telebot import types
from flask import Flask, render_template
from threading import Thread

# USE YOUR NEW TOKEN HERE
TOKEN = "7871347585:AAHAb40LW4fN3_cBRD2BD7znUYtGCkST6Qg"

WEBAPP_URL = "https://testing-web-545.onrender.com/"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# === BOT COMMANDS ===
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        "Open WebApp",
        web_app=types.WebAppInfo(WEBAPP_URL)
    )
    kb.add(btn)

    bot.send_message(
        message.chat.id,
        "👋 Welcome!\nOpen the WebApp below 👇",
        reply_markup=kb
    )


# === WHEN CONTACT IS SHARED ===
@bot.message_handler(content_types=['contact'])
def on_contact(message):
    c = message.contact

    bot.send_message(
        message.chat.id,
        f"📲 Contact Shared\n\n"
        f"👤 {c.first_name or ''} {c.last_name or ''}\n"
        f"📞 {c.phone_number}\n"
        f"🆔 {message.from_user.id}\n"
        f"🌐 {message.from_user.language_code}"
    )


# === FLASK WEBAPP ===
@app.route("/")
def home():
    return render_template("index.html")


# === START BOT POLLING ===
def run_bot():
    bot.infinity_polling(skip_pending=True)


# === START FLASK SERVER ===
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# === RUN BOTH ===
if __name__ == "__main__":
    Thread(target=run_bot).start()
    run_flask()
