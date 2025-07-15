#!/data/data/com.termux/files/usr/bin/bash

clear
echo "⚙️ Starting setup for TechyCR7 LoFi Bot..."

read -p "👤 Enter your name: " name
read -p "🤖 Enter your Bot Token: " token

echo "🔧 Injecting token and name..."

sed -i "s|BOT_TOKEN = .*|BOT_TOKEN = \"$token\"|" bot.py
sed -i "s|@SuryaXCristiano|@SuryaXCristiano, remade by $name|" bot.py

pip install -r requirements.txt

echo "✅ Setup complete!"
echo "🚀 To start your bot, run: python bot.py"
