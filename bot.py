import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, filters
from google_sheets import log_message

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

def handle_message(update: Update, context):
    message_text = update.message.text
    username = update.message.from_user.username or update.message.from_user.first_name
    tasks = [word for word in message_text.split() if word.startswith('#')]
    log_message(username, message_text, tasks)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok", 200

dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/", methods=["GET"])
def index():
    return "Bot is alive!", 200
