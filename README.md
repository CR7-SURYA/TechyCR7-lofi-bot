# 🎧 TechyCR7 Lo-Fi Bot

Turn your own Telegram bot into a powerful **Lo-Fi Music Generator** with just one install!  
This tool lets you convert any music/audio file into a slowed + pitch-modified version with cool effects like **Reverb**, **Vinyl**, or **Rain**.

> 🧠 Coded by **@SuryaXCristiano**  
> ✅ Contact Me On [Telegram](https://t.me/SuryaXCristiano)

---

## 🚀 Features

- Convert any MP3, M4A, WAV, or OGG into Lo-Fi
- Choose **speed** (50% to 200%), **pitch** (-7.0 to +7.0), and **effects**
- Works fully inside **Termux**
- Includes **Auto Mode** (defaults: speed=85, pitch=-1, no effects)
- Inline fake processing animation ⚙️
- Choose **Preview** or **Full** song after processing
- One-file setup with `bot.py` (no Pyrogram or API ID needed)
- Runs **24x7** in background using `nohup` and `termux-wake-lock`

---

## 📦 Installation

### 🔧 Requirements:
Make sure you have:
- [Termux](https://f-droid.org/en/packages/com.termux/)
- `ffmpeg` installed (`pkg install ffmpeg`)

---

## 🛠️ Setup (Do this inside Termux)

```bash
# Clone the repo
git clone https://github.com/YourUsername/TechyCR7-lofi-bot

# Go into project folder
cd TechyCR7-lofi-bot

# Run the install script
bash install.sh
# Give Permission
chmod +x *
