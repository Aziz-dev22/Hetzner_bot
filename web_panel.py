from flask import Flask, render_template_string, request, redirect
from database import add_hetzner_account, get_all_accounts

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>مدیریت ربات</title>
    <style>
        body {
            background-color: #87CEEB;
            background-image: radial-gradient(rgba(255, 255, 255, 0.4) 2px, transparent 2px);
            background-size: 30px 30px;
            font-family: Tahoma, Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            max-width: 800px;
            margin: 0 auto 20px auto;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h2 { color: #333; border-bottom: 2px solid #fff; padding-bottom: 10px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #444; }
        input, select { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #ccc; box-sizing: border-box; }
        button { background-color: #008CBA; color: white; padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; text-align: right; border-bottom: 1px solid #ddd; }
    </style>
</head>
<body>

<div class="container">
    <h2>➕ افزودن اکانت هتزنر جدید</h2>
    <form action="/add_account" method="POST">
        <div class="form-group">
            <label>نام اکانت (برای شناسایی):</label>
            <input type="text" name="acc_name" placeholder="مثلا: اکانت اصلی" required>
        </div>
        <div class="form-group">
            <label>توکن API هتزنر:</label>
            <input type="password" name="acc_token" required>
        </div>
        <button type="submit">ثبت اکانت</button>
    </form>
</div>

<div class="container">
    <h2>🔗 اکانت‌های متصل شده</h2>
    <table>
        <tr>
            <th>آیدی</th>
            <th>نام اکانت</th>
            <th>توکن (مخفی)</th>
        </tr>
        {% for acc in accounts %}
        <tr>
            <td>{{ acc[0] }}</td>
            <td>{{ acc[1] }}</td>
            <td>**************</td>
        </tr>
        {% else %}
        <tr><td colspan="3" style="text-align:center;">هیچ اکانتی متصل نیست.</td></tr>
        {% end endfor %}
    </table>
</div>

</body>
</html>
"""

@app.route('/')
def index():
    accounts = get_all_accounts()
    return render_template_string(HTML_TEMPLATE, accounts=accounts)

@app.route('/add_account', methods=['POST'])
def add_account_route():
    name = request.form.get('acc_name')
    token = request.form.get('acc_token')
    if name and token:
        add_hetzner_account(name, token)
    return redirect('/')
