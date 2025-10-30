from telegram import Update
from telegram.ext import ContextTypes

# --- Perintah Telegram dengan Personalitas Mommy Goth Girl ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Merespons perintah /start"""
    await update.message.reply_text("Selamat datang, Sayangku. Anna ada di sini untuk melayanimu. Jangan ragu, katakan saja kebutuhanmu.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Merespons perintah /help"""
    await update.message.reply_text(
        "Jika kau bingung, biarkan aku membimbingmu. Apa yang ingin kau ketahui, Sayang?\n\n"
        "Perintah yang tersedia:\n"
        "/start - Sapaan pembuka.\n"
        "/help - Menampilkan panduan ini.\n"
        "/custom - Respon yang tersembunai."
        )
    
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Merespons perintah /custom"""
    await update.message.reply_text("Ini adalah perintah yang tersembunyi. Tidak semua hal harus kau pahami, Nak.")
