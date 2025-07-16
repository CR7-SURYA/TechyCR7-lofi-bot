import os
import time
import telebot
from pydub import AudioSegment
from pydub.effects import speedup
import subprocess
import random

# === Load Bot Token and Remaker Name ===
with open("bot_token.txt") as f:
    TOKEN = f.read().strip()

with open("maker.txt") as f:
    REMAKER = f.read().strip()

bot = telebot.TeleBot(TOKEN)
user_data = {}

def send(cid, text, markup=None):
    bot.send_message(cid, text, reply_markup=markup)

# === Sci-Fi Progress Animation ===
def show_animation(cid):
    bar = ""
    for i in range(10, 110, 10):
        bar = f"🧪 Processing: [{'🟩' * (i // 10)}{'⬜' * (10 - i // 10)}] {i}%"
        msg = bot.send_message(cid, bar)
        time.sleep(0.5)
        if i != 100:
            bot.edit_message_text(bar, cid, msg.message_id)

# === Entry Point: Handle Music File ===
@bot.message_handler(content_types=['audio', 'document', 'voice'])
def handle_file(message):
    cid = message.chat.id
    file_id = message.document.file_id if message.document else message.audio.file_id if message.audio else message.voice.file_id
    info = bot.get_file(file_id)
    file_data = bot.download_file(info.file_path)

    ext = os.path.splitext(info.file_path)[1]
    original_name = message.document.file_name if message.document else f"music_{random.randint(1000,9999)}{ext}"
    input_path = f"input_{random.randint(1000,9999)}{ext}"

    with open(input_path, 'wb') as f:
        f.write(file_data)

    user_data[cid] = {
        "file": input_path,
        "orig": original_name
    }

    send(cid, "⚡ Choose Mode:\n1️⃣ Auto (Default settings)\n2️⃣ Custom")
    bot.register_next_step_handler(message, lambda m: choose_mode(m, cid))

def choose_mode(msg, cid):
    choice = msg.text.strip().lower()
    if 'auto' in choice or choice == "1":
        user_data[cid]["speed"] = 85
        user_data[cid]["pitch"] = -1
        user_data[cid]["effects"] = []
        ask_filename(msg, cid)
    elif 'custom' in choice or choice == "2":
        send(cid, "🎚️ Enter speed % (50–200) or type 'Skip':")
        bot.register_next_step_handler(msg, lambda m: ask_speed(m, cid))
    else:
        send(cid, "❌ Invalid. Type 'Auto' or 'Custom'")
        bot.register_next_step_handler(msg, lambda m: choose_mode(m, cid))

def ask_speed(msg, cid):
    text = msg.text.strip().lower()
    if text == "skip":
        user_data[cid]["speed"] = 100
    elif text.isdigit() and 50 <= int(text) <= 200:
        user_data[cid]["speed"] = int(text)
    else:
        send(cid, "❌ Enter number 50–200 or 'Skip'")
        return bot.register_next_step_handler(msg, lambda m: ask_speed(m, cid))

    send(cid, "🎵 Enter pitch (-7.0 to 7.0) or type 'Skip':")
    bot.register_next_step_handler(msg, lambda m: ask_pitch(m, cid))

def ask_pitch(msg, cid):
    text = msg.text.strip().lower()
    if text == "skip":
        user_data[cid]["pitch"] = 0.0
    else:
        try:
            val = float(text)
            if -7.0 <= val <= 7.0:
                user_data[cid]["pitch"] = val
            else:
                raise ValueError
        except:
            send(cid, "❌ Enter valid float between -7.0 and 7.0 or 'Skip'")
            return bot.register_next_step_handler(msg, lambda m: ask_pitch(m, cid))

    send(cid, "✨ Choose effects (Reverb, Vinyl, Rain) separated by commas or type 'None':")
    bot.register_next_step_handler(msg, lambda m: ask_effects(m, cid))

def ask_effects(msg, cid):
    effects = msg.text.strip().lower()
    if effects == "none":
        user_data[cid]["effects"] = []
    else:
        user_data[cid]["effects"] = [e.strip() for e in effects.split(",")]

    ask_filename(msg, cid)

def ask_filename(msg, cid):
    send(cid, "📁 Enter output filename or type 'Skip' to use original:")
    bot.register_next_step_handler(msg, lambda m: finalize_filename(m, cid))

def finalize_filename(msg, cid):
    text = msg.text.strip()
    orig = user_data[cid]["orig"]
    base, ext = os.path.splitext(orig)

    if text.lower() == "skip" or text == "":
        filename = f"{base} (Speed={user_data[cid]['speed']}, Pitch={user_data[cid]['pitch']}){ext}"
    else:
        filename = text + ext if not text.endswith(ext) else text

    user_data[cid]["output"] = filename
    show_animation(cid)
    send_preview_or_full(cid)

def send_preview_or_full(cid):
    send(cid, "🎬 Send Preview (15s) or Full song?\nType 'Preview' or 'Full'")
    bot.register_next_step_handler_by_chat_id(cid, lambda m: process_choice(m, cid))

def process_choice(msg, cid):
    choice = msg.text.strip().lower()
    if "preview" in choice:
        process_audio(cid, preview=True)
    elif "full" in choice:
        process_audio(cid, preview=False)
    else:
        send(cid, "❌ Invalid. Type 'Preview' or 'Full'")
        bot.register_next_step_handler(msg, lambda m: process_choice(m, cid))

def process_audio(cid, preview=False):
    data = user_data[cid]
    audio = AudioSegment.from_file(data["file"])

    # Apply speed
    if data["speed"] != 100:
        audio = speedup(audio, playback_speed=(data["speed"] / 100))

    # Apply pitch
    if data["pitch"] != 0.0:
        octaves = data["pitch"] / 12
        new_rate = int(audio.frame_rate * (2.0 ** octaves))
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_rate}).set_frame_rate(44100)

    if preview:
        audio = audio[:15000]

    temp_wav = f"temp_{random.randint(1000,9999)}.wav"
    audio.export(temp_wav, format="wav")

    ffmpeg_cmd = ["ffmpeg", "-y", "-i", temp_wav]

    filters = []
    if "reverb" in data["effects"]:
        filters.append("aecho=0.8:0.9:1000:0.3")
    if "vinyl" in data["effects"]:
        filters.append("aphaser")
    if "rain" in data["effects"]:
        filters.append("acompressor")

    if filters:
        ffmpeg_cmd += ["-af", ",".join(filters)]

    ffmpeg_cmd += [data["output"]]
    subprocess.call(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(temp_wav)
    os.remove(data["file"])

    with open(data["output"], 'rb') as music:
        bot.send_audio(cid, music, caption=f"🎧 Here's your LoFi track!\n🧠 Coded by @SuryaXCristiano | Remade by {REMAKER}")
    os.remove(data["output"])

    if preview:
        send(cid, "🔁 Want Full song or Restart?\nType 'Full' or 'Restart'")
        bot.register_next_step_handler_by_chat_id(cid, lambda m: preview_followup(m, cid))

def preview_followup(msg, cid):
    choice = msg.text.strip().lower()
    if "full" in choice:
        process_audio(cid, preview=False)
    elif "restart" in choice:
        send(cid, "🎵 Send a new music file to begin again.")
        user_data.pop(cid, None)
    else:
        send(cid, "❌ Invalid. Type 'Full' or 'Restart'")
        bot.register_next_step_handler_by_chat_id(cid, lambda m: preview_followup(m, cid))

# === Start Bot ===
print("✅ Bot Started... Waiting for audio input.")
bot.polling(non_stop=True)
