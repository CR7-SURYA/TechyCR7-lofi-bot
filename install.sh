#!/data/data/com.termux/files/usr/bin/bash

clear
echo "⚙️ Starting setup for TechyCR7 LoFi Bot..."

# Ask for user inputs
read -p "👤 Enter your name: " name
read -p "🤖 Enter your Bot Token: " token

# Inject bot token
echo "🔧 Injecting bot token..."
sed -i "s|BOT_TOKEN = \".*\"|BOT_TOKEN = \"$token\"|" bot.py

# Inject creator name
echo "🔧 Injecting your name..."
sed -i "s|CREATOR_NAME = \".*\"|CREATOR_NAME = \"$name\"|" bot.py

# Install Python dependencies
echo "📦 Installing required packages..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo "🚀 To start your bot, run: python bot.py"
