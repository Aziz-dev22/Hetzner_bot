from flask import Flask, render_template_string, request, redirect, session
from database import *
import os

app = Flask(__name__)
app.secret_key = "secure_key_2026"

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('in'): return redirect('/login')
    if request.method == 'POST':
        if 'add_plan' in request.form:
            # قیمت با ۲۰٪ سود
            price = float(request.form['p']) * 1.2
            # ذخیره در دیتابیس...
    return render_template_string("""
        <h2>پنل مدیریتی</h2>
        <a href='/backup'><button>بکاپ</button></a>
        <a href='/restore'><button>بازگردانی</button></a>
        <form method=post>
            <input name=p placeholder="قیمت پایه">
            <button name="add_plan">ثبت با ۲۰٪ سود</button>
        </form>
    """)

@app.route('/backup')
def backup(): backup_db(); return "Backup Saved!"

@app.route('/restore')
def restore(): restore_db(); return "Restored!"

app.run(host='0.0.0.0', port=5000)
