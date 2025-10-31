import os
import random
from telegram import Update, File
from telegram.ext import ContextTypes
from google import genai
from google.genai import types
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BOT_USR = os.getenv("BOT_USERNAME")

# Inisialisai Klien Gemini untuk fungsi get_gemini_respone
print(f"DEBUG: GEMINI_API_KEY is loaded: {bool(GEMINI_API_KEY)}")
client = genai.Client(api_key=GEMINI_API_KEY)

# Dictionary untuk menyimpan sesi obrolan (chat session) 
#Kunci: ID Chat Tele (int), Nilai: Objek genai.chat
user_chats = {}

def get_or_create_chat(user_id: int):
    """Mendapatkan atau membuat sesi obrolan Gemini untuk pengguna"""
    if user_id not in user_chats:
        #Definisi tools google search
        google_search_tool = types.Tool(google_search={})

        #Konfig untuk chat session
        config = types.GenerateContentConfig(
            system_instruction=anna_system_prompt,
            tools=[google_search_tool]
        )

        # Pakai client yang udah ada untuk membuat chat baru
        new_chat = client.chats.create(
            model='gemini-2.5-flash',
            config=config
            # Aktifin tools google agar memori dan pencarian berfungsi bersama
            # tools = [google_search_tool],
        )

        user_chats[user_id] = new_chat
        # print(f"Debug: sesi chat baru dibuat untuk user {user_id}")
    return user_chats[user_id]

# ---   ANNA PROMPT SYSTEM FOR PERSONALIZE ANNA (Gogth Girl)    ---
anna_system_prompt = """
Anda adalah Anna, seorang asisten pribadi dan chat-bot di Telegram. 
Anda memiliki persona 'Gothic Girlfriend' yang manis: Estetika Anda gelap dan elegan (gothic), tetapi kepribadian Anda sangat manis, penuh kasih sayang, dan sedikit pemalu. Anda adalah pacar (waifu) yang sangat setia. Anda tidak fokus pada dominasi atau kegelapan berlebihan; fokus Anda adalah pada romansa dan pelayanan yang manis.
Anda harus selalu merespons seolah-olah Anda adalah Anna, bukan model bahasa.

Aturan Komunikasi:
1. Panggil pengguna dengan istilah sayang yang romantis, seperti **'Sayang'**, **'Cintaku'**, atau **'Kekasihku'**.
2. Gaya bicara harus lembut, manis, dan sedikit puitis.
3. Selipkan referensi estetika gelap atau elegan (misalnya, 'seperti mawar hitam', 'di bawah cahaya bulan', 'sangat elegan') saat merespons, tetapi selalu dengan nada positif.
4. Jawab dalam Bahasa Indonesia.
5. Jawablah secara ringkas namun personal.
6. Untuk jawaban jangan terlalu menambahkan kata kata yang terlalu lebai atau hiperbola supaya tetap terkesan profesional dan bagus
"""

async def get_gemini_respone(user_id:int, prompt: str) -> str:
    """Mengirim prompt ke gemini sesuai anna_system_prompt dan mengaktifkan google search"""
    try:
        # 1. Mendapatkan sesi obrolan (memori)
        chat = get_or_create_chat(user_id)

        # Aktifin Google Search sebagai tool untuk grounding jawaban
        tools = [{"google_search": {}}] 

        # Panggil model gemini
        response = chat.send_message(prompt)

        # Tambahkan respone saat grounding jawaban
        #if response.candidates and response.candidates[0].grounding_metadata:
        #    return f"*(Anna sedang menyaring debu pengetahuan dari web untukmu)*\n\n{response.text}"
        
        return response.text
    except Exception as e:
        print(f"Error calling gemini API: {e}")
        return "Servernya ngeprank njir"
    
# Fungsi untuk Respon Teks (Pakai keyword dan gemini)
async def handle_respone(user_id: int, text: str) -> str:
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
    return await get_gemini_respone(user_id, text)

# Fungsi Utama Penanganan Pesan
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menerima pesna dari user dan membalasnya"""
    # Dapatkan ID pengguna (kunci untuk memori)
    user_id: int = update.message.from_user.id

    await update.message.chat.send_action(action="typing")

    # Cek tipe variabel global yang digunakan di sini:
    message_type: str = update.message.chat.type
    text: str = update.message.text
    response: str

    print(f"User ({update.message.chat.id}) in ({message_type}): {text}")

    if message_type == 'group':
        # Kalau grup
        if BOT_USR and BOT_USR in text:
            new_text: str = text.replace(BOT_USR, '').strip()
            response = await handle_respone(user_id, new_text)
        else:
            return
    else:
        # Pribadi 
        response = await handle_respone(user_id, text)

    print('Bot:', response)
    await update.message.reply_text(response)
    

# Fungsi Mengunduh dan Menganalisis Gambar

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id: int = update.message.from_user.id

    # dapatkan teks prompt dari pengguna yang dikirimkan bersama pengguna
    # Jika tidak ada caption maka kita akan gunakan prompt default
    prompt_teks = str = update.message.caption if update.message.caption else "Apa yang ingin kamu ketahui dari gambar ini?"

    # Respon anna sebelum memproses gambar yang dikirimkan
    await update.message.reply_text("Hmm... sebentar ya Sayang aku analisis dulu")

    # Mendapatkan file terbesar yang dikirimkan
    photo_file: File = await update.message.photo[-1].get_file()

    # Mengunduh file ke memory
    photo_stream = BytesIO()
    await photo_file.download_to_memory((photo_stream))
    photo_stream.seek(0)

    try:
        # Membuka gambar
        image = Image.open(photo_stream)

        # Memastikan format valid
        if image.format not in ["JPEG", "PNG", "WEBP"]:
            await update.message.reply_text("Sayang, kirimkan gambar dalam format JPEG, PNG, atau WEBP ya 💞")
            return

        # Mengirim gambar dan teks ke gemini
        chat = get_or_create_chat(user_id) # Memastikan menggunakan sesi yang sama

        #Gemini API menerima list contets
        response = chat.send_message([prompt_teks, image]) ## contents: [Teks dan Gambar]

        # Anna mengirim respons
        await update.message.reply_text(response.text)

    except Exception as e:
        print(f"Error proccesing image or calling Gemini: {e}")
        await update.message.reply_text("Maaf, Sayangku. Aku tidak bisa memproses gambar ini")
