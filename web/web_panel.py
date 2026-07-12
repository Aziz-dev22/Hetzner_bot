from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from core.database import SessionLocal, Plan
from config.settings import settings
import shutil
import os
from datetime import datetime

app = Flask(__name__)
# استفاده از سکرت کی برای امنیت سشن‌ها (ایجاد شده خودکار در نصب)
app.secret_key = settings.SECRET_KEY

# دریافت اطلاعات لاگین که کاربر در هنگام اجرای install.sh وارد کرده است
ADMIN_USER = settings.WEB_ADMIN_USER
ADMIN_PASS = settings.WEB_ADMIN_PASS

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash("نام کاربری یا رمز عبور اشتباه است!")
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        
    db = SessionLocal()
    plans = db.query(Plan).all()
    db.close()
    
    return render_template('dashboard.html', plans=plans)

@app.route('/add_plan', methods=['POST'])
def add_plan():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        
    name = request.form.get('name')
    cpu = int(request.form.get('cpu'))
    ram = int(request.form.get('ram'))
    base_price = float(request.form.get('price'))
    
    # محاسبه ۲۰٪ سود به صورت خودکار
    final_price = base_price * 1.20
    
    db = SessionLocal()
    new_plan = Plan(name=name, cpu=cpu, ram=ram, price=final_price)
    db.add(new_plan)
    db.commit()
    db.close()
    
    flash("پلن جدید با موفقیت اضافه شد!")
    return redirect(url_for('dashboard'))

@app.route('/delete_plan/<int:plan_id>')
def delete_plan(plan_id):
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        
    db = SessionLocal()
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if plan:
        db.delete(plan)
        db.commit()
        flash("پلن با موفقیت حذف شد.")
    db.close()
    
    return redirect(url_for('dashboard'))

@app.route('/backup')
def backup_db():
    """قابلیت تهیه فایل پشتیبان از دیتابیس SQLite با استفاده از shutil"""
    if 'logged_in' not in session:
        return redirect(url_for('login'))
        
    db_path = "zarvpn.db"
    if not os.path.exists(db_path):
        flash("فایل دیتابیس یافت نشد!")
        return redirect(url_for('dashboard'))
        
    # ساخت نام یکتا با تاریخ برای فایل بکاپ
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"backup_{date_str}.db"
    backup_path = os.path.join(os.getcwd(), backup_filename)
    
    # کپی کردن دیتابیس اصلی به عنوان بکاپ
    shutil.copy2(db_path, backup_path)
    
    # ارسال فایل برای دانلود در مرورگر مدیر
    return send_file(backup_path, as_attachment=True)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
