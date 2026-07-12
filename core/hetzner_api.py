from hcloud import Client
from hcloud.servers.domain import Server as HServer
from config.settings import settings
import logging

class HetznerManager:
    def __init__(self):
        self.client = Client(token=settings.HETZNER_API_TOKEN)
        self.logger = logging.getLogger(__name__)

    def create_server(self, name: str, image: str = "ubuntu-22.04", server_type: str = "cx11"):
        """ایجاد سرور جدید در هتزنر"""
        try:
            response = self.client.servers.create(
                name=name,
                server_type=self.client.server_types.get_by_name(server_type),
                image=self.client.images.get_by_name(image)
            )
            return response.server
        except Exception as e:
            self.logger.error(f"Error creating server: {e}")
            return None

    def power_action(self, server_id: int, action: str):
        """مدیریت وضعیت سرور: power_on, power_off, reboot"""
        server = self.client.servers.get_by_id(server_id)
        if action == "power_off":
            return server.power_off()
        elif action == "power_on":
            return server.power_on()
        elif action == "reboot":
            return server.reboot()
        return None

    def get_server_metrics(self, server_id: int):
        """دریافت ترافیک مصرفی سرور"""
        # هتزنر برای متریک‌ها از بازه زمانی استفاده می‌کند
        # این متد خروجی کلی ترافیک را برای پایش (Scheduler) برمی‌گرداند
        server = self.client.servers.get_by_id(server_id)
        # در اینجا منطق دریافت ترافیک از metrics API هتزنر پیاده‌سازی می‌شود
        # برای سادگی، این بخش را پس از اتصال به کلاینت نهایی می‌کنیم
        return {"traffic_in": 0, "traffic_out": 0} 

    def delete_server(self, server_id: int):
        """حذف سرور (فقط برای ادمین)"""
        server = self.client.servers.get_by_id(server_id)
        return server.delete()

# یک نمونه برای استفاده در سایر ماژول‌ها
hetzner_manager = HetznerManager()

