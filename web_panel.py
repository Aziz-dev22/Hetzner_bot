from flask import Flask, render_template_string, request, redirect, session
import sqlite3, os

app = Flask(__name__)
app.secret_key = "secure_key"

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('in'): return redirect('/login')
    if request.method == 'POST':
        # ذخیره با ۲۰٪ سود
        price = float(request.form['p']) * 1.2
        conn = sqlite3.connect('database.sqlite')
        conn.execute('INSERT INTO plans (name, cpu, ram, price) VALUES (?,?,?,?)', (request.form['n'], request.form['c'], request.form['r'], price))
        conn.commit(); conn.close()
    
    return render_template_string("""
        <h2>پنل مدیریت</h2>
        <form method=post>
            نام: <input name=n> CPU: <input name=c> RAM: <input name=r> قیمت پایه: <input name=p>
            <button>ثبت پلن با ۲۰٪ سود</button>
        </form>
    """)

# مسیر ورود (لاگین) هم مانند قبل است
app.run(host='0.0.0.0', port=5000)
