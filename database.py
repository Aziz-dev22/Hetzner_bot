import sqlite3

def init_db():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    # ساخت جدول اکانت‌های هتزنر
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hetzner_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            token TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def add_hetzner_account(name, token):
    try:
        conn = sqlite3.connect('database.sqlite')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO hetzner_accounts (name, token) VALUES (?, ?)', (name, token))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # توکن تکراری است

def get_all_accounts():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, token FROM hetzner_accounts')
    accounts = cursor.fetchall()
    conn.close()
    return accounts
