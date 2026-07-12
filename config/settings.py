from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # تنظیمات ربات
    BOT_TOKEN: str
    ADMIN_ID: int
    
    # تنظیمات هتزنر
    HETZNER_API_TOKEN: str
    
    # تنظیمات دیتابیس
    DATABASE_URL: str = "sqlite:///./zarvpn.db"
    
    # تنظیمات پنل وب
    SECRET_KEY: str = "super-secret-key-for-session"
    
    class Config:
        env_file = ".env"

settings = Settings()

