#!/bin/bash
APP_DIR="/opt/hetzner_bot"

echo "==> شروع نصب مجدد..."
sudo apt update && sudo apt install -y python3-pip python3-venv git

sudo rm -rf $APP_DIR
git clone https://github.com/Aziz-dev22/Hetzner_bot.git $APP_DIR
cd $APP_DIR

python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

cat <<EOF | sudo tee /etc/systemd/system/hetzner_bot.service
[Unit]
Description=Hetzner Manager Bot
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable hetzner_bot
sudo systemctl start hetzner_bot
echo "==> نصب کامل شد."

