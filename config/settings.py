from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # تنظیمات ربات
    BOT_TOKEN: str
    ADMIN_ID: int
    
    # تنظیمات هتزنر
    HETZNER_API_TOKEN: str
    
    # تنظیمات دیتابیس
    DATABASE_URL: str = "sqlite:///./zarvpn.db"
    
    # تنظیمات پنل وب
    SECRET_KEY: str
    WEB_ADMIN_USER: str
    WEB_ADMIN_PASS: str
    
    class Config:
        env_file = ".env"

settings = Settings()
