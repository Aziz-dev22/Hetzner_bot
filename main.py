import threading
from bot import bot
from web_panel import app
from database import init_db

def run_bot():
    print("🤖 ربات تلگرام در حال اجراست...")
    bot.polling(none_stop=True)

def run_web():
    print("🌐 پنل وب روی پورت 5000 در حال اجراست...")
    # دسترسی از همه آی‌پی‌ها باز است
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == '__main__':
    # ساخت دیتابیس و جداول در اولین اجرا
    init_db()
    
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=run_web)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
