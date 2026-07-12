from flask import Flask, render_template, request, redirect
from core.database import SessionLocal, Plan

app = Flask(__name__)

@app.route('/admin/add-plan', methods=['GET', 'POST'])
def add_plan():
    if request.method == 'POST':
        base_price = float(request.form['price'])
        final_price = base_price * 1.20  # ۲۰٪ سود خودکار
        
        db = SessionLocal()
        new_plan = Plan(name=request.form['name'], price=final_price)
        db.add(new_plan)
        db.commit()
        db.close()
        return "پلن با موفقیت اضافه شد."
    return render_template('add_plan.html')

