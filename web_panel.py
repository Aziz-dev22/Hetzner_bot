from flask import Flask, render_template_string, request, redirect
from database import get_all_accounts

app = Flask(__name__)

# رابط کاربری با پترن آبی آسمانی و باکس‌های نیمه‌شفاف
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>پنل مدیریت مرکزی</title>
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
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(12px);
            border-radius: 15px;
            padding: 30px;
            max-width: 800px;
            margin: 0 auto 20px auto;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        h2 { color: #222; border-bottom: 2px solid rgba(255,255,255,0.8); padding-bottom: 10px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #444; }
        input, select { 
            width: 100%; padding: 10px; border-radius: 8px; 
            border: 1px solid rgba(0,0,0,0.1); box-sizing: border-box;
            background: rgba(255,255,255,0.9);
        }
        button { 
            background-color: #008CBA; color: white; padding: 10px 20px; 
            border: none; border-radius: 8px; cursor: pointer; font-size: 16px; transition: 0.3s;
        }
        button:hover { background-color: #006b8f; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 10px; text-align: right; border-bottom: 1px solid rgba(0,0,0,0.1); }
    </style>
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
        <tr><td colspan="3" style="text-align:center;">هیچ اکانتی متصل نیست. (از طریق ربات اضافه کنید)</td></tr>
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

@app.route('/save_settings', methods=['POST'])
def save_settings():
    # منطق ذخیره تنظیمات قیمت در دیتابیس
    return redirect('/')
