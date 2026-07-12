from apscheduler.schedulers.background import BackgroundScheduler
from core.database import SessionLocal, Server
from core.hetzner_api import hetzner_manager
import datetime

def check_servers_status():
    db = SessionLocal()
    servers = db.query(Server).all()
    
    for server in servers:
        # ۱. چک کردن تاریخ انقضا و حذف خودکار
        if datetime.datetime.now() > server.expire_date:
            hetzner_manager.delete_server(int(server.hetzner_id))
            db.delete(server)
            db.commit()
            continue
        
        # ۲. چک کردن ترافیک (اگر ۹۵٪ پر بود خاموش شود)
        metrics = hetzner_manager.get_server_metrics(int(server.hetzner_id))
        if metrics.get("traffic_in", 0) > 95: # فرض بر درصد
            hetzner_manager.power_action(int(server.hetzner_id), "power_off")
            
    db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_servers_status, 'interval', minutes=5)
    scheduler.start()

