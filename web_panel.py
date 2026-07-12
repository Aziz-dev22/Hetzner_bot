from flask import Flask, render_template_string, request, redirect

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
    </style>
</head>
<body>
<div class="container">
    <h2>⚙️ تنظیمات قیمت‌گذاری و لوکیشن‌ها</h2>
    <form action="/save" method="POST">
        <div class="form-group">
            <label>قیمت تغییر آی‌پی (تتـر / واحد فرضی):</label>
            <input type="number" name="ip_price" value="5">
        </div>
        <div class="form-group">
            <label>لوکیشن‌های فعال برای فروش:</label>
            <select name="locations" multiple>
                <option value="fsn1" selected>فالکنشتاین (fsn1)</option>
                <option value="nbg1" selected>نورنبرگ (nbg1)</option>
                <option value="hel1">هلسینکی (hel1)</option>
            </select>
        </div>
        <button type="submit">ذخیره تنظیمات</button>
    </form>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/save', methods=['POST'])
def save():
    # منطق ذخیره تنظیمات
    return redirect('/')
