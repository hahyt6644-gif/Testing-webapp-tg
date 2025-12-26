import os
import telebot
from telebot import types
from flask import Flask, render_template, jsonify
from threading import Thread

TOKEN = "7871347585:AAHAb40LW4fN3_cBRD2BD7znUYtGCkST6Qg"
WEBAPP_URL = "https://testing-web-545.onrender.com/"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# store user data in memory (simple demo)
user_data = {}


# /start
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
        "👋 Open the WebApp below 👇",
        reply_markup=kb
    )


# when phone received
@bot.message_handler(content_types=['contact'])
def on_contact(message):
    c = message.contact

    user_data[message.from_user.id] = {
        "name": f"{c.first_name or ''} {c.last_name or ''}".strip(),
        "phone": c.phone_number,
        "username": message.from_user.username,
        "lang": message.from_user.language_code
    }

    # delete the contact message
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


# ==== API for WebApp to fetch details ====
@app.route("/api/user/<int:user_id>")
def api_user(user_id):
    return jsonify(user_data.get(user_id, {}))


# ==== WebApp page ====
@app.route("/")
def home():
    return render_template("index.html")


# ==== BOT THREAD ====
def run_bot():
    bot.infinity_polling(skip_pending=True)


# ==== FLASK THREAD ====
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    Thread(target=run_bot).start()
    run_flask()
