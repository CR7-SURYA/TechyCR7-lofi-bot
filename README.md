# 🎧 TechyCR7 Lo-Fi Bot

🔥 Turn your own Telegram bot into a powerful **Lo-Fi Music Generator** with just one install!  
This tool lets you convert any music/audio file into a slowed + pitch-modified version with cool effects like **Reverb**, **Vinyl**, or **Rain**.

> 🔥 Coded by **Surya**  
> 🚀 Contact Me On [Telegram](https://t.me/SuryaXCristiano)

---

## 🚀 Features

- ☑️ Convert any MP3, M4A, WAV, or OGG into Lo-Fi 
- ☑️ Choose **speed** (50% to 200%), **pitch** (-7.0 to +7.0), and **effects** (Reverb, Vinyl, Rain) 
- ☑️ Works fully inside **Termux**
- ☑️ Includes **Auto Mode** ( Auto Lofi with best settings ) and **Custom Mode** ( Manually adjust settings )
- ☑️ Inline cool processing animation 
- ☑️ Choose **Preview** (15 sec) or **Full** song after processing
- ☑️ One-file setup
- ☑️ Runs **24x7** in background using `nohup` and `termux-wake-lock`, no need of any API server !!!



---

## 📦 Installation

### 🔧 Requirements:
Make sure you have:
- [Termux](https://f-droid.org/en/packages/com.termux/)


---

## 🛠️ Setup (Copy paste in Termux)

```bash
pkg update and pkg upgrade -y

pkg install git -y

pkg install ffmpeg -y

git clone https://github.com/CR7-SURYA/TechyCR7-lofi-bot

cd TechyCR7-lofi-bot

pip install -r requirements.txt

chmod +x * 

./install.sh
```
## 🛠️ After These.....

- It will ask If you want a temporary server or a 24x7 live server 🚀
- If you choose temporary server, you might need to keep the termux in split screen or floating window, otherwise it may not work 👊
- Use `CTRL+C` to exit temporary mode 🤝
- If you choose 24x7 server, you don't need to keep the termux in floating window or split screen, you can even clear it from recent apps !!! 🔥🔥🔥
- Make sure termux is running in device background 👀
- Use `pkill -f bot.py` to stop the live server 👍

## 🚀 Useful Tips...
- ✅ Make sure you have disabled battery optimisation for termux if you want your 24x7 live server
- ✅ Don't kill termux's background process
- ✅ If your bot is not working, revoke your bot token from Botfather and try again
- ✅ Lastly, if any errors are happening , report me on telegram 👍
## ✨💕 Enjoy !!!
- Share and give credits [@SuryaXCristiano](https://t.me/SuryaXCristiano) 🤝
