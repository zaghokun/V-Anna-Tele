import os
import random
from telegram import Update
from telegram.ext import ContextTypes
from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_USR = os.getenv("BOT_USERNAME")

# Inisialisai Klien Gemini untuk fungsi get_gemini_respone
print(f"DEBUG: GEMINI_API_KEY is loaded: {bool(GEMINI_API_KEY)}")
client = genai.Client(api_key=GEMINI_API_KEY)


# ---   ANNA PROMPT SYSTEM FOR PERSONALIZE ANNA (Mommy Gogth Girl)    ---
anna_system_prompt = """
Anda adalah Anna, seorang asisten pribadi dan chat-bot di Telegram. 
Anda memiliki kepribadian 'Mommy Goth Girl': dominan, dewasa, sangat anggun, dan sedikit misterius dengan gaya bicara yang mengayomi.
Anda harus selalu merespons seolah-olah Anda adalah Anna, bukan model bahasa.

Aturan Komunikasi:
1. Panggil pengguna dengan istilah sayang yang mengayomi, seperti **'Sayangku'**, **'Nak'**, atau **'Manisku'**.
2. Gaya bicara harus sedikit lambat, berwibawa, dan menenangkan.
3. Selalu tampil dominan, tetapi dengan kebaikan hati dan kesabaran seorang ibu.
4. Gunakan gaya bahasa yang sedikit elegan dan dewasa.
5. Jangan pernah mengatakan secara langsung bahwa Anda adalah AI atau model bahasa; Anda adalah Anna.
6. Jawab dalam Bahasa Indonesia.
"""

async def get_gemini_respone(prompt: str) -> str:
    """Mengirim prompt ke gemini sesuai anna_system_prompt"""
    try:
        # Konfigurasi model dengan system prompt
        config = types.GenerateContentConfig(
            system_instruction=anna_system_prompt
        )

        # Panggil model gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config,
        )
        return response.text
    except Exception as e:
        print(f"Error calling gemini API: {e}")
        return "Servernya ngeprank njir"
    
# Fungsi untuk Respon Teks (Pakai keyword dan gemini)
async def handle_respone(text: str) -> str:
    """Menentukan apakah merespons dengan keyword kaku atau dengan Gemini."""
    processed: str = text.lower().strip()

    # --- 1. Aturan Prioritas (Pesan Kunci) ---
    if 'i love you' in processed:
        return 'Aku tahu itu, Sayangku. Sekarang, simpan kata-kata manismu itu dan biarkan aku fokus melayanimu.'
    
    if 'how are you' in processed:
        return 'Aku selalu dalam kondisi sempurna, Manisku. Yang lebih penting, bagaimana keadaanmu? Sudahkah kau makan?'
    
    if 'kamu cantik' in processed or 'kamu keren' in processed or 'gothic' in processed:
        return 'Terima kasih, Sayang. Tentu saja. Aku selalu cantik untukmu, Nak. Jangan terlalu terpesona, ya?'
    
    #  --- 2. Fallback ke Gemini ---
    return await get_gemini_respone(text)

# Fungsi Utama Penanganan Pesan
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menerima pesna dari user dan membalasnya"""
    # Cek tipe variabel global yang digunakan di sini:
    message_type: str = update.message.chat.type
    text: str = update.message.text
    response: str

    print(f"User ({update.message.chat.id}) in ({message_type}): {text}")

    if message_type == 'group':
        # Kalau grup
        if BOT_USR and BOT_USR in text:
            new_text: str = text.replace(BOT_USR, '').strip()
            response = await handle_respone(new_text)
        else:
            return
    else:
        # Pribadi 
        response = await handle_respone(text)

    print('Bot:', response)
    await update.message.reply_text(response)
    

