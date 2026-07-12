import threading
import logging
import time
from bot.bot import dp
from aiogram import executor
from web.web_panel import app
from core.scheduler import start_scheduler
from core.database import init_db

# تنظیمات لاگ‌گیری برای مانیتورینگ بهتر خطاهای احتمالی
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ZarVPN_Main")

def run_bot():
    """تابع اجرای ربات تلگرام"""
    logger.info("Starting Telegram Bot...")
    # skip_updates باعث می‌شود پیام‌های زمان خاموش بودن ربات نادیده گرفته شوند
    executor.start_polling(dp, skip_updates=True)

def run_web():
    """تابع اجرای پنل وب با Flask"""
    logger.info("Starting Web Panel on port 5000...")
    # استفاده از use_reloader=False در حالت Threading الزامی است
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    try:
        logger.info("Initializing Database...")
        # ساخت جداول دیتابیس در صورت نیاز
        init_db()

        logger.info("Starting Background Scheduler...")
        # اجرای سیستم بررسی ترافیک و انقضای سرورها
        start_scheduler()

        # تعریف Thread ها برای اجرای همزمان سرویس‌ها
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        web_thread = threading.Thread(target=run_web, daemon=True)

        # استارت کردن سرویس‌ها
        bot_thread.start()
        web_thread.start()

        # نگه داشتن Thread اصلی برای جلوگیری از بسته شدن برنامه
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down ZarVPN services safely...")
    except Exception as e:
        logger.error(f"Critical Error: {e}")
