#!/data/data/com.termux/files/usr/bin/bash

clear
echo "🛠️ Installing requirements..."
pkg update -y > /dev/null
pkg install -y python ffmpeg git > /dev/null

echo "📦 Installing Python packages..."
pip install --upgrade pip > /dev/null 2>&1  # This is safe in Termux
pip install pydub requests > /dev/null

read -p "👤 Enter your name: " USERNAME
read -p "🤖 Enter your Telegram Bot Token: " TOKEN

echo "🔧 Updating bot.py with your info..."
sed -i "s|BOT_TOKEN = .*|BOT_TOKEN = \"$TOKEN\"|" bot.py
sed -i "s|Remade by .*|Remade by $USERNAME|" bot.py

echo "🚀 Starting your bot in background..."
nohup python bot.py > nohup.out 2>&1 &

sleep 1
echo ""
echo "✅ Bot is installed and running!"
echo "📂 Project Location: $(pwd)"
echo "🧠 Coded by @SuryaXCristiano | Remade by $USERNAME"
echo "📄 You can edit bot.py anytime to customize"
echo "🔍 To see logs: tail -f $(pwd)/nohup.out"
echo "🛑 To stop bot: pkill -f bot.py"
echo ""
read -p '👉 Press Enter to return to Termux shell...' _
