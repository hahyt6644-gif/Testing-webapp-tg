import os
import telebot
from telebot import types
from flask import Flask, render_template, jsonify, redirect, url_for
from threading import Thread

TOKEN = "7871347585:AAHAb40LW4fN3_cBRD2BD7znUYtGCkST6Qg"
WEBAPP_URL = "https://testing-web-545.onrender.com/"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

user_data = {}


# ===== BOT =====
@bot.message_handler(commands=['start'])
def start(message):
    kb = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        "Open WebApp",
        web_app=types.WebAppInfo(WEBAPP_URL)
    )
    kb.add(btn)

    bot.send_message(message.chat.id,
                     "👋 Open the WebApp below 👇",
                     reply_markup=kb)


@bot.message_handler(content_types=['contact'])
def on_contact(message):
    c = message.contact
    uid = message.from_user.id

    user_data[uid] = {
        "name": f"{c.first_name or ''} {c.last_name or ''}".strip(),
        "phone": c.phone_number,
        "username": message.from_user.username,
        "lang": message.from_user.language_code
    }

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


# ===== API =====
@app.route("/api/user/<int:user_id>")
def api_get(user_id):
    return jsonify(user_data.get(user_id, {}))


# ===== PAGES =====
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/full/<int:user_id>")
def full_page(user_id):
    return render_template("full.html", user_id=user_id)


# ===== RUN =====
def run_bot():
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)


def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    Thread(target=run_bot, daemon=True).start()
    run_flask()
