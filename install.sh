#!/bin/bash

# مسیر پروژه
PROJECT_DIR="$(pwd)/hetzner_bot"

echo "⏳ در حال نصب و آماده‌سازی ربات..."

# ۱. دانلود یا به‌روزرسانی کدها
if [ ! -d "$PROJECT_DIR" ]; then
    git clone https://github.com/Aziz-dev22/Hetzner_bot.git "$PROJECT_DIR"
else
    cd "$PROJECT_DIR" && git pull origin main
fi

cd "$PROJECT_DIR"

# ۲. نصب پیش‌نیازها
sudo apt update && sudo apt install -y python3 python3-venv python3-pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ۳. دریافت اطلاعات از کاربر
echo "-----------------------------------"
read -p "🔑 توکن ربات تلگرام: " BOT_TOKEN
read -p "👤 آیدی عددی ادمین: " ADMIN_ID
read -p "🌐 آی‌پی سرور: " SERVER_IP
read -p "👤 یوزرنیم پنل وب: " WEB_USERNAME
read -p "🔐 پسورد پنل وب: " WEB_PASSWORD

# ۴. ذخیره در فایل .env
echo "BOT_TOKEN=$BOT_TOKEN" > .env
echo "ADMIN_ID=$ADMIN_ID" >> .env
echo "SERVER_IP=$SERVER_IP" >> .env
echo "WEB_USERNAME=$WEB_USERNAME" >> .env
echo "WEB_PASSWORD=$WEB_PASSWORD" >> .env

# ۵. آماده‌سازی دیتابیس
python3 -c "from database import init_db; init_db()"

echo "✅ نصب با موفقیت انجام شد!"
echo "🚀 برای اجرا دستور زیر را وارد کنید:"
echo "cd $PROJECT_DIR && source venv/bin/activate && python3 main.py"

