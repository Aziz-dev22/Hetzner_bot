import sqlite3

def init_db():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            token TEXT UNIQUE
        )
    ''')
    
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

# ----- توابع جدید برای کاربران -----
def get_user_balance(user_id):
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    # اگر کاربر جدید بود، او را با موجودی صفر در دیتابیس ثبت کن
    if not result:
        cursor.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
        conn.commit()
        balance = 0
    else:
        balance = result[0]
        
    conn.close()
    return balance
