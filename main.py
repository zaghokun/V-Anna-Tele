from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters,ContextTypes
import os

# Load From .env
load_dotenv()
TOKKEN: Final = os.getenv("BOT_API_KEY")
BOT_USR: Final = os.getenv("BOT_USERNAME")

# Function from another file
from commands import start_command, help_command, custom_command
from responses import handle_message

# Debugging Tools

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

if __name__ == '__main__':

    if not TOKKEN:
        print("Error: BOT_API_KEY tidak ditemukan di file .env. Bot tidak dapat dijalankan.")
        exit()

    print('Starting bot...')
    app = Application.builder().token(TOKKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors 
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)