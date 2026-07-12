import threading
from bot import bot
from web_panel import app
from database import init_db

def run_bot():
    print("🤖 ربات تلگرام در حال اجراست...")
    bot.polling(none_stop=True)

def run_web():
    print("🌐 پنل وب در حال اجراست...")
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == '__main__':
    # ساخت دیتابیس در صورت نبودن
    init_db()
    
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=run_web)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
