import threading
from bot.bot import dp, executor
from web.web_panel import app
from core.scheduler import start_scheduler

def run_bot():
    executor.start_polling(dp)

def run_web():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    start_scheduler() # استارت زمان‌بندی بررسی ترافیک
    
    t1 = threading.Thread(target=run_bot, daemon=True)
    t2 = threading.Thread(target=run_web, daemon=True)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()

