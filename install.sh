#!/bin/bash

# رنگ‌ها برای خوانایی بهتر در ترمینال
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# مسیرهای دقیق پروژه شما
APP_DIR="/opt/hetzner_bot"
SERVICE_NAME="hetzner_bot.service"
BACKUP_DIR="/root/hetzner_bot_backups"

function install_project() {
    echo -e "${GREEN}==> شروع فرآیند نصب...${NC}"

    # ۱. دریافت اطلاعات از کاربر
    read -p "Enter Telegram Bot Token: " BOT_TOKEN
    read -p "Enter Admin Telegram ID (Numeric): " ADMIN_ID
    read -p "Enter Hetzner API Token: " HETZNER_API_TOKEN
    read -p "Enter Web Panel Username (برای ورود به پنل وب): " WEB_USER
    read -p "Enter Web Panel Password (رمز عبور پنل وب): " WEB_PASS
    read -p "Enter Your GitHub Repository URL (مثال: https://github.com/Aziz-dev22/Hetzner_bot.git): " REPO_URL

    echo -e "${GREEN}==> در حال آپدیت سیستم و نصب پیش‌نیازها...${NC}"
    sudo apt update && sudo apt install -y python3-pip python3-venv git curl tar

    echo -e "${GREEN}==> در حال دانلود پروژه از گیت‌هاب...${NC}"
    sudo rm -rf $APP_DIR
    git clone $REPO_URL $APP_DIR
    cd $APP_DIR

    echo -e "${GREEN}==> در حال ساخت فایل تنظیمات امن...${NC}"
    # تولید یک کلید امنیتی رندوم برای سشن‌های وب
    SECRET_KEY=$(head -c 32 /dev/urandom | base64)
    
    cat <<EOF > $APP_DIR/.env
BOT_TOKEN=${BOT_TOKEN}
ADMIN_ID=${ADMIN_ID}
HETZNER_API_TOKEN=${HETZNER_API_TOKEN}
DATABASE_URL=sqlite:///./hetzner_bot.db
SECRET_KEY=${SECRET_KEY}
WEB_ADMIN_USER=${WEB_USER}
WEB_ADMIN_PASS=${WEB_PASS}
EOF

    echo -e "${GREEN}==> در حال ساخت محیط مجازی و نصب کتابخانه‌های پایتون...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    echo -e "${GREEN}==> در حال تنظیم سرویس Systemd...${NC}"
    cat <<EOF | sudo tee /etc/systemd/system/${SERVICE_NAME}
[Unit]
Description=Hetzner Manager Telegram Bot and Web Panel
After=network.target

[Service]
User=root
WorkingDirectory=${APP_DIR}
Environment="PATH=${APP_DIR}/venv/bin"
ExecStart=${APP_DIR}/venv/bin/python main.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

    echo -e "${GREEN}==> در حال اجرای سرویس‌ها...${NC}"
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_NAME}
    sudo systemctl start ${SERVICE_NAME}
    
    echo -e "${GREEN}✅ نصب با موفقیت به پایان رسید! ربات و پنل وب اکنون فعال هستند.${NC}"
}

function update_code() {
    echo -e "${GREEN}==> در حال دریافت کدهای جدید از گیت‌هاب...${NC}"
    if [ -d "$APP_DIR" ]; then
        cd $APP_DIR
        git pull
        sudo systemctl restart ${SERVICE_NAME}
        echo -e "${GREEN}✅ آپدیت با موفقیت انجام شد و سرویس ری‌استارت گردید.${NC}"
    else
        echo -e "${RED}❌ پوشه پروژه یافت نشد! آیا ربات را نصب کرده‌اید؟${NC}"
    fi
}

function backup_project() {
    echo -e "${GREEN}==> در حال تهیه فایل پشتیبان از دیتابیس و تنظیمات...${NC}"
    mkdir -p $BACKUP_DIR
    DATE=$(date +"%Y%m%d_%H%M%S")
    if [ -d "$APP_DIR" ]; then
        tar -czf $BACKUP_DIR/hetzner_bot_backup_$DATE.tar.gz -C $APP_DIR hetzner_bot.db .env
        echo -e "${GREEN}✅ فایل بکاپ در مسیر زیر ذخیره شد:${NC}"
        echo -e "${GREEN}$BACKUP_DIR/hetzner_bot_backup_$DATE.tar.gz${NC}"
    else
        echo -e "${RED}❌ پوشه پروژه یافت نشد!${NC}"
    fi
}

function uninstall_project() {
    echo -e "${RED}⚠️ هشدار: این عملیات ربات، پنل وب و تمامی دیتابیس‌ها را برای همیشه حذف می‌کند!${NC}"
    read -p "آیا از حذف کامل مطمئن هستید؟ (y/n): " confirm
    if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
        echo -e "${GREEN}==> در حال توقف سرویس...${NC}"
        sudo systemctl stop ${SERVICE_NAME}
        sudo systemctl disable ${SERVICE_NAME}
        sudo rm /etc/systemd/system/${SERVICE_NAME}
        sudo systemctl daemon-reload
        
        echo -e "${GREEN}==> در حال حذف فایل‌های پروژه...${NC}"
        sudo rm -rf $APP_DIR
        echo -e "${GREEN}✅ پروژه Hetzner Bot به طور کامل از سرور حذف شد.${NC}"
    else
        echo "عملیات حذف لغو شد."
    fi
}

echo "======================================"
echo "    Hetzner Bot Project Manager V2.0  "
echo "======================================"
echo "1. نصب کامل ربات (Install)"
echo "2. آپدیت کدها (Update)"
echo "3. بکاپ از دیتابیس (Backup)"
echo "4. حذف کامل ربات (Uninstall)"
echo "5. خروج (Exit)"
echo "======================================"
read -p "لطفاً یک گزینه را انتخاب کنید (۱-۵): " choice

case $choice in
    1) install_project ;;
    2) update_code ;;
    3) backup_project ;;
    4) uninstall_project ;;
    5) exit 0 ;;
    *) echo -e "${RED}❌ گزینه نامعتبر!${NC}" ;;
esac
