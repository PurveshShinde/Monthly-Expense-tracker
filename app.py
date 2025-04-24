from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

DATA_FILE = 'expenses.json'

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_expenses(expenses):
    with open(DATA_FILE, 'w') as f:
        json.dump(expenses, f, indent=4)

def calculate_summary(expenses):
    total = sum(e['amount'] for e in expenses)
    monthly = defaultdict(float)
    for e in expenses:
        month = datetime.strptime(e['date'], '%Y-%m-%d').strftime('%Y-%m')
        monthly[month] += e['amount']
    return total, dict(monthly)

@app.route('/')
def index():
    expenses = load_expenses()
    total, monthly_summary = calculate_summary(expenses)
    return render_template('index.html', expenses=expenses, total=total, monthly_summary=monthly_summary)

@app.route('/add', methods=['POST'])
def add_expense():
    new_expense = {
        'date': request.form['date'],
        'amount': float(request.form['amount']),
        'category': request.form['category'],
        'description': request.form['description']
    }
    expenses = load_expenses()
    expenses.append(new_expense)
    save_expenses(expenses)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
