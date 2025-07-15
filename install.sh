#!/data/data/com.termux/files/usr/bin/bash

# Welcome message
clear
echo "🎧 Welcome to TechyCR7 LoFi Bot Installer"
echo "-----------------------------------------"

# Ask for user name
read -p "👤 Enter your name (used in bot welcome message): " DEV_NAME

# Ask for bot token
read -p "🔑 Enter your Telegram bot token: " BOT_TOKEN

# Confirm setup path
BOT_DIR="$HOME/TechyCR7-lofi-bot"
mkdir -p "$BOT_DIR"
cd "$BOT_DIR" || exit

# Save user details
echo "$DEV_NAME" > devname.txt
echo "$BOT_TOKEN" > token.txt

# Write bot.py template with token and devname placeholders
cat > bot.py <<EOF
# Bot file will be inserted here (you can paste or programmatically generate using placeholders)
EOF

# Install dependencies
echo "📦 Installing dependencies..."
pkg update -y && pkg upgrade -y
pkg install -y ffmpeg python
pip install --upgrade pip
pip install pydub requests

# Wakelock to keep Termux alive
termux-wake-lock

# Kill previous bot instance if any
pkill -f bot.py > /dev/null 2>&1

# Run bot in background
echo "🚀 Starting your bot in background..."
nohup python bot.py > nohup.out 2>&1 &

# Final message
echo ""
echo "✅ Bot is installed and running!"
echo "📂 Project Location: $BOT_DIR"
echo "🧠 Coded by @SuryaXCristiano | Remade by $DEV_NAME"
echo "📄 You can edit bot.py anytime to customize"
echo "🔍 To see logs: tail -f $BOT_DIR/nohup.out"
echo "🛑 To stop bot: pkill -f bot.py"
echo ""

# Prevent Termux from exiting
read -p "👉 Press Enter to return to Termux shell..."
exec "\$SHELL"
