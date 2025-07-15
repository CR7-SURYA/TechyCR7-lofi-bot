#!/data/data/com.termux/files/usr/bin/bash

clear
echo "🔧 Starting LoFi Bot Installer..."
echo

# Step 1: Ask for name
read -p "👤 Enter your name: " username

# Step 2: Ask for Bot Token
read -p "🤖 Enter your Telegram Bot Token: " bottoken

# Step 3: Save to .env
echo "USER_NAME=\"$username\"" > .env
echo "BOT_TOKEN=\"$bottoken\"" >> .env
echo "✅ Saved your details to .env"
echo

# Step 4: Install required packages
echo "📦 Installing dependencies..."
pkg update -y && pkg upgrade -y
pkg install python ffmpeg -y
pip install --upgrade pip
pip install pydub requests
echo "✅ Dependencies installed."
echo

# Step 5: Prevent Termux from sleeping
termux-wake-lock
echo "🔒 Termux wakelock activated."
echo

# Step 6: Start bot with nohup
echo "🚀 Launching your bot in background with nohup..."
nohup python bot.py > /dev/null 2>&1 &

echo
echo "✅ Done! Your bot is now running 24x7 in background!"
echo "🧪 Coded by @SuryaXCristiano |🤝 Remade by $username"
