import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, token TEXT UNIQUE)')
    c.execute('CREATE TABLE IF NOT EXISTS plans (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cpu TEXT, ram TEXT, price REAL)')
    c.execute('CREATE TABLE IF NOT EXISTS user_servers (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, hetzner_id INTEGER, expire_date TIMESTAMP)')
    conn.commit()
    conn.close()

def add_hetzner_account(name, token):
    try:
        conn = sqlite3.connect('database.sqlite')
        c = conn.cursor()
        c.execute('INSERT INTO accounts (name, token) VALUES (?, ?)', (name, token))
        conn.commit()
        conn.close()
        return True
    except: return False

def get_all_accounts():
    conn = sqlite3.connect('database.sqlite')
    c = conn.cursor()
    c.execute('SELECT * FROM accounts')
    data = c.fetchall()
    conn.close()
    return data
