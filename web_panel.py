import os
from flask import Flask, render_template_string, request, redirect, session
from database import *

app = Flask(__name__)
app.secret_key = "secret_key_2026"

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get('in'): return redirect('/login')
    if request.method == 'POST':
        # محاسبه قیمت با ۲۰٪ سود
        final_price = float(request.form['p']) * 1.2
        add_plan(request.form['n'], request.form['c'], request.form['r'], final_price)
    
    plans = get_all_plans()
    return render_template_string("""
        <body style="background:#87CEEB; text-align:center;">
        <div style="background:rgba(255,255,255,0.7); padding:20px; border-radius:20px; width:80%; margin:auto;">
            <h2>مدیریت پلن‌ها (قیمت با ۲۰٪ سود خودکار لحاظ می‌شود)</h2>
            {% for p in plans %}
                <p>{{p[1]}} | قیمت نهایی: {{p[4]}} تتر</p>
            {% endfor %}
            <form method=post>
                نام: <input name=n> CPU: <input name=c> RAM: <input name=r> قیمت پایه: <input name=p>
                <button>ثبت پلن جدید</button>
            </form>
        </div>
        </body>
    """, plans=plans)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['u'] == os.getenv('WEB_USERNAME') and request.form['p'] == os.getenv('WEB_PASSWORD'):
            session['in'] = True
            return redirect('/')
    return "<form method=post>یوزر: <input name=u> پسورد: <input name=p type=password> <button>ورود</button></form>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

