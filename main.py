import threading, bot, web_panel
from database import init_db

if __name__ == '__main__':
    init_db()
    # اجرای همزمان ربات و وب
    threading.Thread(target=lambda: bot.bot.polling(none_stop=True), daemon=True).start()
    web_panel.app.run(host='0.0.0.0', port=5000)
