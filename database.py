import sqlite3

def init_db():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    
    # جدول اکانت‌های هتزنر
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            token TEXT UNIQUE
        )
    ''')
    
    # جدول کاربران و کیف پول
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_hetzner_account(name, token):
    try:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO accounts (name, token) VALUES (?, ?)', (name, token))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_all_accounts():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, token FROM accounts')
    accounts = cursor.fetchall()
    conn.close()
    return accounts
