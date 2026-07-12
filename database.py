import sqlite3
def init_db():
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, token TEXT UNIQUE)')
    c.execute('CREATE TABLE IF NOT EXISTS plans (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cpu TEXT, ram TEXT, price REAL)')
    # ذخیره سرورهای کاربران با تاریخ انقضا
    c.execute('CREATE TABLE IF NOT EXISTS user_servers (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, hetzner_id INTEGER, expire_date TIMESTAMP)')
    conn.commit(); conn.close()
