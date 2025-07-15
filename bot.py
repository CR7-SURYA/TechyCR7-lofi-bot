import os, time, requests, threading
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

CREATOR_NAME = "unknown"  # Will be replaced by install.sh
BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE"  # Will be replaced by install.sh
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
FILE_API = f"https://api.telegram.org/file/bot{BOT_TOKEN}"
USER_STATE = {}
LAST_UPDATE = None

def send(chat_id, text):
    requests.post(f"{API}/sendMessage", data={"chat_id": chat_id, "text": text})

def send_audio(chat_id, file_path, caption):
    with open(file_path, "rb") as f:
        requests.post(f"{API}/sendAudio", data={"chat_id": chat_id, "caption": caption}, files={"audio": f})

def send_buttons(chat_id, text, buttons):
    requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {"inline_keyboard": [[{"text": t, "callback_data": d}] for t, d in buttons]}
    })

def animate(chat_id):
    msg = requests.post(f"{API}/sendMessage", data={"chat_id": chat_id, "text": progress_bar(0)}).json()
    mid = msg["result"]["message_id"]
    for i in range(10, 101, 10):
        time.sleep(0.3)
        requests.post(f"{API}/editMessageText", data={
            "chat_id": chat_id, "message_id": mid, "text": progress_bar(i)
        })

def progress_bar(p):
    filled = "🟩" * (p // 10)
    empty = "⬛" * (10 - p // 10)
    return f"🧪 Processing...\n[{filled}{empty}] {p}%"

def generate_filename(orig_name, effects, speed, pitch):
    base = os.path.splitext(orig_name)[0]
    tag = []
    if effects: tag.append(", ".join(effects))
    if speed: tag.append(f"Speed={speed}")
    if pitch != 0: tag.append(f"Pitch={pitch}")
    if tag:
        return f"{base} ({', '.join(tag)}).mp3"
    return f"{base}.mp3"

def process(chat_id, uid):
    state = USER_STATE[uid]
    animate(chat_id)

    file_id = state["file_id"]
    file_info = requests.get(f"{API}/getFile", params={"file_id": file_id}).json()
    path = file_info["result"]["file_path"]
    url = f"{FILE_API}/{path}"
    content = requests.get(url).content

    orig_name = state.get("file_name") or os.path.basename(path)
    state["original_filename"] = orig_name

    temp = NamedTemporaryFile(delete=False, suffix=".ogg")
    temp.write(content)
    temp.close()

    audio = AudioSegment.from_file(temp.name)
    os.remove(temp.name)

    if state['speed']:
        audio = audio._spawn(audio.raw_data, overrides={
            "frame_rate": int(audio.frame_rate * (state['speed'] / 100.0))
        }).set_frame_rate(44100)

    pitch_factor = 2 ** (state["pitch"] / 12.0)
    audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * pitch_factor)
    }).set_frame_rate(44100)

    if "Vinyl" in state["effects"]:
        noise = AudioSegment.silent(len(audio)).overlay(audio.low_pass_filter(300))
        audio = audio.overlay(noise - 15)
    if "Rain" in state["effects"]:
        rain = AudioSegment.silent(len(audio)).overlay(audio.high_pass_filter(200))
        audio = audio.overlay(rain - 20)

    full_temp = NamedTemporaryFile(delete=False, suffix=".mp3")
    audio.export(full_temp.name, format="mp3")
    state["full_path"] = full_temp.name

    preview_temp = NamedTemporaryFile(delete=False, suffix=".mp3")
    audio[:15000].export(preview_temp.name, format="mp3")
    state["preview_path"] = preview_temp.name

    state["step"] = "ask_name"
    send(chat_id, "📛 Enter new song name or type 'Skip' to keep original name:")

def cleanup(uid):
    s = USER_STATE.get(uid, {})
    for k in ["full_path", "preview_path"]:
        if s.get(k) and os.path.exists(s[k]):
            os.remove(s[k])
    USER_STATE[uid] = {}

def handle(update):
    global LAST_UPDATE
    msg = update.get("message")
    cb = update.get("callback_query")

    if msg:
        cid = msg["chat"]["id"]
        uid = msg["from"]["id"]
        text = msg.get("text")
        doc = msg.get("document")
        aud = msg.get("audio")
        voice = msg.get("voice")
        state = USER_STATE.setdefault(uid, {})

        if text and text.lower() == "/start" and not state.get("welcomed"):
            state["welcomed"] = True
            send(cid, f"🎧 Hi {msg['from']['first_name']}, welcome to the LoFi Bot!\n\n🚀 Coded by @SuryaXCristiano, remade by {CREATOR_NAME}")
            return

        if doc or aud or voice:
            state.clear()
            state["file_id"] = (doc or aud or voice)["file_id"]
            state["file_name"] = (doc or aud or voice).get("file_name", "audio.ogg")
            state["step"] = "await_mode"
            send_buttons(cid, "🎚️ Choose mode:", [("🎵 Auto Lofi", "auto"), ("🎛️ Custom Settings", "custom")])
            return

        step = state.get("step")

        if step == "speed":
            if text.lower() == "skip":
                state["speed"] = None
                state["step"] = "effects"
                send(cid, "🎨 Choose effects (Reverb, Vinyl, Rain) or 'None':")
            else:
                try:
                    val = int(text)
                    if 50 <= val <= 200:
                        state["speed"] = val
                        state["step"] = "effects"
                        send(cid, "🎨 Choose effects (Reverb, Vinyl, Rain) or 'None':")
                    else: send(cid, "⚠️ Speed must be 50–200")
                except: send(cid, "❌ Invalid input")

        elif step == "effects":
            if text.lower() == "none":
                state["effects"] = []
            else:
                valid = {"Reverb", "Vinyl", "Rain"}
                selected = [e.strip().title() for e in text.split(",") if e.strip().title() in valid]
                state["effects"] = selected
            state["step"] = "pitch"
            send(cid, "🎛️ Enter pitch (-7.0 to 7.0) or 'Skip':")

        elif step == "pitch":
            if text.lower() == "skip":
                state["pitch"] = 0.0
            else:
                try:
                    val = float(text)
                    if -7.0 <= val <= 7.0:
                        state["pitch"] = val
                    else: return send(cid, "⚠️ Pitch must be -7.0 to 7.0")
                except: return send(cid, "❌ Invalid pitch")
            threading.Thread(target=process, args=(cid, uid)).start()

        elif step == "ask_name":
            if text.lower() == "skip":
                name = generate_filename(state["original_filename"], state["effects"], state["speed"], state["pitch"])
            else:
                name = text.strip() + ".mp3"
            final = os.path.join("/data/data/com.termux/files/home", name)
            os.rename(state["full_path"], final)
            state["full_path"] = final
            state["filename"] = name
            state["step"] = "ask_preview"
            send(cid, "🎵 Send 'Preview' or 'Full' version:")

        elif step == "ask_preview":
            if text.lower() == "preview":
                send_audio(cid, state["preview_path"], f"🎧 {state['filename']} [Preview]")
                state["step"] = "after_preview"
                send(cid, "📥 Type 'Full' for full song or 'Restart'")
            elif text.lower() == "full":
                send_audio(cid, state["full_path"], f"🎶 {state['filename']}")
                cleanup(uid)

        elif step == "after_preview":
            if text.lower() == "full":
                send_audio(cid, state["full_path"], f"🎶 {state['filename']}")
                cleanup(uid)
            elif text.lower() == "restart":
                cleanup(uid)
                send(cid, "🔁 Send another file to restart.")
            else:
                send(cid, "❓ Type 'Full' or 'Restart'")

    elif cb:
        cid = cb["message"]["chat"]["id"]
        uid = cb["from"]["id"]
        data = cb["data"]
        state = USER_STATE.setdefault(uid, {})

        if state.get("step") == "await_mode":
            if data == "auto":
                state["mode"] = "auto"
                state["speed"] = 85
                state["pitch"] = -1
                state["effects"] = []
                threading.Thread(target=process, args=(cid, uid)).start()
            elif data == "custom":
                state["mode"] = "custom"
                state["step"] = "speed"
                send(cid, "⚙️ Enter speed (50–200) or 'Skip':")
        requests.post(f"{API}/answerCallbackQuery", data={"callback_query_id": cb["id"]})

def poll():
    global LAST_UPDATE
    while True:
        try:
            res = requests.get(f"{API}/getUpdates", params={"timeout": 100, "offset": LAST_UPDATE}).json()
            for upd in res.get("result", []):
                LAST_UPDATE = upd["update_id"] + 1
                handle(upd)
        except Exception as e:
            print("Error:", e)
            time.sleep(3)

if __name__ == "__main__":
    print("🎧 Bot Running...")
    poll()
