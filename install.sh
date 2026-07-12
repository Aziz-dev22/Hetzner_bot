#!/bin/bash

REPO_URL="https://github.com/Aziz-dev22/hetzner_bot.git"
REPO_NAME=$(basename "$REPO_URL" .git)
PROJECT_DIR="$(pwd)/$REPO_NAME"

echo -e "\n=================================================="
echo -e "      🤖 پنل مدیریت و نصب ربات هتزنر (Hetzner)      "
echo -e "=================================================="
echo -e "1) 🟢 نصب و راه‌اندازی اولیه"
echo -e "2) 🔄 بروزرسانی ربات (آپدیت به آخرین نسخه)"
echo -e "3) 📥 بکاپ کامل (دریافت فایل فشرده از دیتابیس)"
echo -e "4) 🗑 حذف کامل ربات"
echo -e "0) ❌ خروج"
echo -e "=================================================="

read -p "لطفاً یک گزینه را انتخاب کنید [0-4]: " choice < /dev/tty

case $choice in
    1)
        echo "⏳ در حال نصب و راه‌اندازی..."
        if [ -d "$PROJECT_DIR" ]; then
            echo "⚠️ ربات از قبل نصب شده است! لطفاً گزینه 2 را انتخاب کنید."
            exit 1
        fi

        git clone "$REPO_URL" "$PROJECT_DIR"
        cd "$PROJECT_DIR"
        
        sudo apt update && sudo apt install -y python3 python3-venv python3-pip sqlite3 tar
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt

        echo "-----------------------------------"
        read -p "🔑 لطفا توکن ربات تلگرام را وارد کنید: " BOT_TOKEN < /dev/tty
        read -p "👤 لطفا آیدی عددی ادمین (تلگرام) را وارد کنید: " ADMIN_ID < /dev/tty
        read -p "🌐 لطفا آی‌پی سرور لینوکس خود را وارد کنید (مثلا 1.2.3.4): " SERVER_IP < /dev/tty
        echo "--- امنیت پنل وب ---"
        read -p "👤 نام کاربری برای ورود به پنل وب: " WEB_USERNAME < /dev/tty
        read -p "🔐 رمز عبور برای ورود به پنل وب: " WEB_PASSWORD < /dev/tty
        
        echo "BOT_TOKEN=${BOT_TOKEN// /}" > .env
        echo "ADMIN_ID=${ADMIN_ID// /}" >> .env
        echo "SERVER_IP=${SERVER_IP// /}" >> .env
        echo "WEB_USERNAME=${WEB_USERNAME// /}" >> .env
        echo "WEB_PASSWORD=${WEB_PASSWORD// /}" >> .env
        echo "✅ اطلاعات ذخیره شد."

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
        ;;
    
    2)
        echo "⏳ در حال بروزرسانی ربات..."
        if [ ! -d "$PROJECT_DIR" ]; then
            echo "❌ ربات نصب نیست! لطفاً ابتدا گزینه 1 را انتخاب کنید."
            exit 1
        fi
        
        cd "$PROJECT_DIR"
        git pull origin main
        source venv/bin/activate
        pip install -r requirements.txt
        sudo systemctl restart vpn_manager_bot
        echo "✅ ربات با موفقیت به آخرین نسخه بروزرسانی شد."
        ;;
    
    3)
        echo "⏳ در حال ایجاد بکاپ..."
        if [ ! -d "$PROJECT_DIR" ]; then
            echo "❌ پوشه ربات پیدا نشد!"
            exit 1
        fi
        
        BACKUP_NAME="hetzner_bot_backup_$(date +%Y%m%d_%H%M%S).tar.gz"
        tar --exclude="$PROJECT_DIR/venv" -czvf "$BACKUP_NAME" "$PROJECT_DIR"
        echo "✅ بکاپ شما با موفقیت ایجاد شد."
        echo "📂 مسیر فایل بکاپ: $(pwd)/$BACKUP_NAME"
        ;;
    
    4)
        read -p "⚠️ آیا از حذف کامل ربات و دیتابیس مطمئن هستید؟ (y/n): " confirm < /dev/tty
        if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
            sudo systemctl stop vpn_manager_bot 2>/dev/null
            sudo systemctl disable vpn_manager_bot 2>/dev/null
            sudo rm /etc/systemd/system/vpn_manager_bot.service 2>/dev/null
            sudo systemctl daemon-reload
            rm -rf "$PROJECT_DIR"
            echo "🗑 ربات حذف شد."
        else
            echo "❌ عملیات حذف لغو شد."
        fi
        ;;
    
    0)
        exit 0
        ;;
    
    *)
        echo "❌ گزینه نامعتبر!"
        exit 1
        ;;
esac
