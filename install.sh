#!/data/data/com.termux/files/usr/bin/bash

echo "🔧 Setting up your Lofi Bot..."

# Prompt for name and token
read -p "👤 Enter your name: " USERNAME
read -p "🤖 Enter your Telegram Bot Token: " BOTTOKEN

# Replace token and name in bot.py
sed -i "s|BOT_TOKEN = .*|BOT_TOKEN = \"$BOTTOKEN\"|" bot.py
sed -i "s|REMADE_BY = .*|REMADE_BY = \"$USERNAME\"|" bot.py

# Install dependencies
pkg update -y
pkg install -y ffmpeg
pip install --upgrade pip
pip install -r requirements.txt

# Ask for run mode
echo -e "\n⚙️  How do you want to run your bot?"
select opt in "🌐 24x7 Background (using nohup)" "🧪 Temporary Session (foreground)"; do
    case $opt in
        "🌐 24x7 Background (using nohup)")
            echo "🚀 Starting your bot in background..."
            nohup python bot.py > nohup.out 2>&1 &
            break
            ;;
        "🧪 Temporary Session (foreground)")
            echo "🚀 Starting your bot in current session..."
            python bot.py
            exit
            ;;
    esac
done

# Final Info
echo -e "\n✅ Bot is installed and running!"
echo "📂 Project Location: $(pwd)"
echo "🧠 Coded by @SuryaXCristiano | Remade by $USERNAME"
echo "📄 You can edit bot.py anytime to customize"
echo "🔍 To see logs: tail -f $(pwd)/nohup.out"
echo "🛑 To stop bot: pkill -f bot.py"

# Don't use exec "$SHELL" — it fails in Termux
echo -e "\n👉 Press Enter to return to Termux shell..."
read
bash  # opens a fresh shell session
