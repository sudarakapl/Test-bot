import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from flask import Flask, request
from google_sheets import log_message

# Load Telegram token
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Create Flask app
app = Flask(__name__)

# Global variable to store the bot application
bot_app = ApplicationBuilder().token(TOKEN).build()

# Define message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text
    username = update.message.from_user.username or update.message.from_user.first_name
    tasks = [word for word in message_text.split() if word.startswith('#')]
    log_message(username, message_text, tasks)

# Register handler
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask route for Telegram webhook
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    await bot_app.process_update(update)
    return "ok", 200

@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200
