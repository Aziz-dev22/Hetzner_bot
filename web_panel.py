import os
from flask import Flask, render_template_string, request, redirect, session, url_for
from dotenv import load_dotenv
from database import get_all_accounts

load_dotenv()

WEB_USERNAME = os.getenv('WEB_USERNAME', 'admin').strip()
WEB_PASSWORD = os.getenv('WEB_PASSWORD', 'admin').strip()

app = Flask(__name__)
# استفاده از کلید ثابت تا با ری‌استارت شدن سرور، سشن شما از بین نرود
app.secret_key = "hetzner_secure_session_key_2026"

COMMON_STYLE = """
<style>
    body {
        background-color: #87CEEB;
        background-image: radial-gradient(rgba(255, 255, 255, 0.4) 2px, transparent 2px);
        background-size: 30px 30px;
        font-family: Tahoma, Arial, sans-serif;
        margin: 0;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .container {
        background: rgba(255, 255, 255, 0.65);
        backdrop-filter: blur(12px);
        border-radius: 15px;
        padding: 30px;
        width: 100%;
        max-width: 800px;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        box-sizing: border-box;
    }
    .login-box {
        max-width: 400px;
        margin-top: 10vh;
    }
    h2 { color: #222; border-bottom: 2px solid rgba(255,255,255,0.8); padding-bottom: 10px; text-align: center; }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-weight: bold; color: #444; }
    input, select { 
        width: 100%; padding: 10px; border-radius: 8px; 
        border: 1px solid rgba(0,0,0,0.1); box-sizing: border-box;
        background: rgba(255,255,255,0.9);
    }
    button { 
        width: 100%; background-color: #008CBA; color: white; padding: 10px 20px; 
        border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: 0.3s;
    }
    button:hover { background-color: #006b8f; }
    table { width: 100%; border-collapse: collapse; margin-top: 15px; }
    th, td { padding: 10px; text-align: right; border-bottom: 1px solid rgba(0,0,0,0.1); }
    .error { color: red; text-align: center; font-weight: bold; margin-bottom: 15px; }
    .logout-btn { background-color: #e74c3c; margin-top: 20px; }
    .logout-btn:hover { background-color: #c0392b; }
</style>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ورود به پنل مدیریت</title>
    """ + COMMON_STYLE + """
</head>
<body>
    <div class="container login-box">
        <h2>🔒 ورود مدیر</h2>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        <form action="/login" method="POST">
            <div class="form-group">
                <label>نام کاربری:</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>رمز عبور:</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">ورود به سیستم</button>
        </form>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>پنل مدیریت مرکزی</title>
    """ + COMMON_STYLE + """
</head>
<body>

<div class="container">
    <h2>⚙️ تنظیمات قیمت‌گذاری و مالی</h2>
    <form action="/save_settings" method="POST">
        <div class="form-group">
            <label>قیمت تغییر آی‌پی توسط کاربر (تتر/تومان):</label>
            <input type="number" name="ip_change_price" value="5">
        </div>
        <div class="form-group">
            <label>درگاه‌های فعال جهت شارژ کیف پول:</label>
            <select name="gateways" multiple style="height: 80px;">
                <option value="tether_trc20" selected>تتر (TRC20)</option>
                <option value="iranian_rial" selected>درگاه ریالی ایران</option>
                <option value="crypto_other">سایر ارزهای دیجیتال</option>
            </select>
        </div>
        <button type="submit">ذخیره تغییرات</button>
    </form>
</div>

<div class="container">
    <h2>🔗 اکانت‌های متصل شده هتزنر</h2>
    <table>
        <tr>
            <th>آیدی</th>
            <th>نام اکانت</th>
            <th>وضعیت</th>
        </tr>
        {% for acc in accounts %}
        <tr>
            <td>{{ acc[0] }}</td>
            <td>{{ acc[1] }}</td>
            <td style="color: green;">متصل</td>
        </tr>
        {% else %}
        <tr><td colspan="3" style="text-align:center;">هیچ اکانتی متصل نیست. (از طریق دکمه‌های شیشه‌ای ربات اضافه کنید)</td></tr>
        {% endfor %}
    </table>
    
    <a href="/logout" style="text-decoration: none;">
        <button class="logout-btn">🚪 خروج از حساب کاربری</button>
    </a>
</div>

</body>
</html>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        
        if user == WEB_USERNAME and password == WEB_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template_string(LOGIN_TEMPLATE, error="نام کاربری یا رمز عبور اشتباه است!")
            
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    accounts = get_all_accounts()
    return render_template_string(DASHBOARD_TEMPLATE, accounts=accounts)

@app.route('/save_settings', methods=['POST'])
def save_settings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return redirect(url_for('index'))

