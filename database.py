import sqlite3, shutil
from datetime import datetime

def init_db():
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT, token TEXT UNIQUE)')
    c.execute('CREATE TABLE IF NOT EXISTS plans (id INTEGER PRIMARY KEY, name TEXT, cpu TEXT, ram TEXT, price REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS user_servers (id INTEGER PRIMARY KEY, user_id INTEGER, hetzner_id INTEGER, expire_date TIMESTAMP)')
    conn.commit(); conn.close()

def backup_db():
    shutil.copyfile('database.sqlite', 'backup_db.sqlite')

def restore_db():
    shutil.copyfile('backup_db.sqlite', 'database.sqlite')
