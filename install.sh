#!/data/data/com.termux/files/usr/bin/bash

clear
echo "🎧 Installing TechyCR7 LoFi Bot..."

# Only install essential packages
pkg update -y && pkg upgrade -y
pkg install -y python ffmpeg termux-api

# Clone bot if not already cloned
if [ ! -d "TechyCR7-lofi-bot" ]; then
    git clone https://github.com/CR7-SURYA/TechyCR7-lofi-bot
fi

cd TechyCR7-lofi-bot
chmod +x *

# Install only required Python libs
pip install -r requirements.txt

# Ask for bot token
echo -e "\n🔑 Enter your Telegram Bot Token:"
read TOKEN
echo "$TOKEN" > bot_token.txt

# Ask for your credit name
echo -e "\n✍️ Enter your name or @username to show as remaker:"
read REMAKER
echo "$REMAKER" > maker.txt

# Choose server mode
echo -e "\n🚀 Choose how to run the bot:"
echo "1️⃣ Temporary Server (manual)"
echo "2️⃣ 24x7 Server (background with wakelock)"
read -p "👉 Enter 1 or 2: " MODE

if [[ "$MODE" == "1" ]]; then
    echo -e "\n🟢 Starting bot in Temporary Server mode..."
    echo -e "✅ Bot is running. (Press Ctrl + C to stop)"
    python bot.py
elif [[ "$MODE" == "2" ]]; then
    termux-wake-lock
    echo -e "\n🟢 Starting bot in 24x7 Server mode..."
    nohup python bot.py > nohup.out 2>&1 &
    sleep 1
    echo -e "\n✅ Bot is installed and running in background!"
    echo "📂 Location: $(pwd)"
    echo "📄 Logs: tail -f nohup.out"
    echo "🛑 Stop: pkill -f bot.py"
    echo -e "🧠 Coded by @SuryaXCristiano | Remade by $REMAKER"
    echo -e "👉 Press Enter to return to Termux shell..."
    read
else
    echo "❌ Invalid option. Please run install.sh again and choose 1 or 2."
fi
