#!/bin/bash
echo "--- منوی نصب و مدیریت ---"
echo "1) نصب کامل ربات و پنل"
echo "2) آپدیت کدها از گیت‌هاب"
echo "3) مشاهده وضعیت سرویس"
echo "4) خروج"
read -p "انتخاب کنید: " choice
case $choice in
    1) sudo apt update && sudo apt install -y python3-venv python3-pip git
       git clone https://github.com/Aziz-dev22/Hetzner_bot.git
       cd Hetzner_bot && python3 -m venv venv && source venv/bin/activate
       pip install pyTelegramBotAPI hcloud Flask python-dotenv requests
       echo "نصب تمام شد. فایل .env را تنظیم و main.py را اجرا کنید." ;;
    2) git pull ;;
    3) ps aux | grep main.py ;;
    4) exit ;;
esac
