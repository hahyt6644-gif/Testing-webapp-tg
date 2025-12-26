import os
import telebot
from telebot import types
from flask import Flask, render_template
from threading import Thread

# --- ENV VARIABLES (Render Dashboard) ---
# BOT_TOKEN = your bot token
TOKEN = os.getenv("7487704262:AAE34XTNrKt5D9dKtduPK0Ezwc9j3SLGoBA")

WEBAPP_URL = "https://testing-web-545.onrender.com/"   # must be https

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# /start command
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


# receives phone contact from WebApp requestContact()
@bot.message_handler(content_types=['contact'])
def on_contact(message):
    contact = message.contact

    reply = (
        "📲 Contact Shared\n\n"
        f"👤 Name: {contact.first_name or ''} {contact.last_name or ''}\n"
        f"📞 Phone: {contact.phone_number}\n"
        f"🆔 Telegram ID: {message.from_user.id}\n"
        f"🌐 Language: {message.from_user.language_code}"
    )

    bot.send_message(message.chat.id, reply)


# === Flask route ===
@app.route("/")
def home():
    return render_template("index.html")


# run bot + flask together
def run_bot():
    bot.infinity_polling(skip_pending=True)


def run_flask():
    port = int(os.environ.get("PORT", 5000))  # Render uses PORT env
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    Thread(target=run_bot).start()
    Thread(target=run_flask).start()
