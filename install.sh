#!/bin/bash

REPO_URL="https://github.com/Aziz-dev22/hetzner_bot.git"
REPO_NAME=$(basename "$REPO_URL" .git)
PROJECT_DIR="$(pwd)/$REPO_NAME"

echo "🟢 در حال نصب و راه‌اندازی نسخه جدید ربات..."

if [ -d "$PROJECT_DIR" ]; then
    cd "$PROJECT_DIR"
    git pull origin main
else
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

sudo apt update && sudo apt install -y python3 python3-venv python3-pip sqlite3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "-----------------------------------"
    read -p "🔑 لطفا توکن ربات تلگرام را وارد کنید: " BOT_TOKEN
    read -p "👤 لطفا آیدی عددی ادمین را وارد کنید (بدون هیچ حرف اضافه‌ای): " ADMIN_ID
    
    # حذف فاصله‌های احتمالی هنگام ذخیره
    echo "BOT_TOKEN=${BOT_TOKEN// /}" > .env
    echo "ADMIN_ID=${ADMIN_ID// /}" >> .env
    echo "✅ اطلاعات ذخیره شد."
fi

cat <<EOF > /etc/systemd/system/vpn_manager_bot.service
[Unit]
Description=Telegram Bot and Web Panel
After=network.target

[Service]
User=root
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable vpn_manager_bot
sudo systemctl restart vpn_manager_bot

echo "🚀 ربات و پنل وب با موفقیت نصب و اجرا شدند!"
