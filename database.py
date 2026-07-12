import sqlite3

def init_db():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, token TEXT UNIQUE)')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance REAL DEFAULT 0)')
    cursor.execute('CREATE TABLE IF NOT EXISTS plans (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cpu TEXT, ram TEXT, price REAL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS user_servers (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, hetzner_id INTEGER, expire_date TIMESTAMP)')
    conn.commit()
    conn.close()
