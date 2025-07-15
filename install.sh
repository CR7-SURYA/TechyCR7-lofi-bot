#!/data/data/com.termux/files/usr/bin/bash

clear
echo "🔧 Installing TechyCR7 LoFi Bot..."

# Update and install dependencies
pkg update -y && pkg upgrade -y
pkg install -y python ffmpeg git wget
pip install --upgrade pip

# Optional: install termux-wake-lock to prevent sleep
pkg install -y termux-api
termux-wake-lock

# Clone bot if not already cloned
if [ ! -d "TechyCR7-lofi-bot" ]; then
    git clone https://github.com/CR7-SURYA/TechyCR7-lofi-bot
fi

cd TechyCR7-lofi-bot

# Give permission and install Python requirements
chmod +x *
pip install -r requirements.txt

# Ask user how they want to run the bot
echo -e "\n🚀 How do you want to run the bot?"
echo "1️⃣ Temporary Mode (Runs only while Termux is open)"
echo "2️⃣ 24x7 Background Mode (Runs in background even after closing Termux)"
read -p "👉 Enter 1 or 2: " mode

if [ "$mode" = "2" ]; then
    termux-wake-lock
    echo -e "\n🟢 Starting in 24x7 Background Mode..."
    nohup python bot.py > nohup.out 2>&1 &
    sleep 1
    echo -e "\n✅ Bot is installed and running!"
    echo "📂 Project Location: $(pwd)"
    echo -e "🧠 Coded by @SuryaXCristiano | Remade by Siu"
    echo -e "📄 To see logs: \033[1mtail -f $(pwd)/nohup.out\033[0m"
    echo -e "🛑 To stop bot: \033[1mpkill -f bot.py\033[0m"
    echo -e "👉 Press Enter to return to Termux shell..."
    read
else
    echo -e "\n🟢 Starting in Temporary Mode..."
    echo -e "✅ Bot is running... \033[1m(Press Ctrl + C to stop)\033[0m"
    python bot.py
fi
