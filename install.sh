#!/bin/bash

# متغیرهای مسیر پروژه
APP_DIR="/opt/zarvpn_project"
SERVICE_NAME="zarvpn.service"

function install_project() {
    echo "Updating system and installing dependencies..."
    sudo apt update && sudo apt install -y python3-pip python3-venv git curl

    echo "Setting up project directory..."
    # فرض بر این است که کدها در این مسیر قرار می‌گیرند
    sudo mkdir -p $APP_DIR
    cd $APP_DIR

    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    
    # نصب وابستگی‌ها
    pip install -r requirements.txt

    echo "Configuring Systemd service..."
    cat <<EOF | sudo tee /etc/systemd/system/${SERVICE_NAME}
[Unit]
Description=ZarVPN Telegram Bot and Web Panel
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

    echo "Starting services..."
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_NAME}
    sudo systemctl start ${SERVICE_NAME}
    
    echo "Installation complete! The service is now running in the background."
}

function update_code() {
    echo "Pulling latest code from GitHub..."
    cd $APP_DIR
    git pull origin main
    
    echo "Restarting ZarVPN service..."
    sudo systemctl restart ${SERVICE_NAME}
    echo "Update applied and service restarted successfully."
}

function show_status() {
    sudo systemctl status ${SERVICE_NAME}
}

echo "======================================"
echo "    ZarVPN Project Manager V1.0       "
echo "======================================"
echo "1. Install completely (Deps + Systemd)"
echo "2. Update code from GitHub & Restart"
echo "3. Check Service Status"
echo "4. Exit"
echo "======================================"
read -p "Enter your choice (1-4): " choice

case $choice in
    1) install_project ;;
    2) update_code ;;
    3) show_status ;;
    4) exit 0 ;;
    *) echo "Invalid option. Please run the script again." ;;
esac
