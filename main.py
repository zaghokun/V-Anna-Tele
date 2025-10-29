from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters,ContextTypes
import os


load_dotenv()
TOKKEN: Final = os.getenv("BOT_API_KEY")
BOT_USR: Final = os.getenv("BOT_USERNAME")


# Commands 
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi Honey, Im Anna your personal assitant")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("What's you like to know?")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")



# Responnses

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hi Honey!'
    
    if 'how are you' in processed:
        return 'Im good always ready for you!'
    
    if 'i love you! anna' in processed:
        return 'I love you too Honey!'
    
    return 'I do not understand what you wrote!'


# Handle Messages

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text


    print(f"User ({update.message.chat.id}) in ({message_type}): {text}")

    if message_type == 'group':
        if BOT_USR in text:
            new_text: str = text.replace(BOT_USR, '').strip()
            respone: str = handle_response(new_text)
        else:
            return
    else:
        respone: str = handle_response(text)
