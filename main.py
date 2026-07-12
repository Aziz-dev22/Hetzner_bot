import threading, bot, web_panel
from database import init_db

if __name__ == '__main__':
    init_db()
    # اجرای ربات در یک ترد جداگانه
    threading.Thread(target=bot.bot.polling, kwargs={'none_stop': True}, daemon=True).start()
    # اجرای پنل وب
    web_panel.app.run(host='0.0.0.0', port=5000)
