from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime

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

@app.route('/')
def index():
    expenses = load_expenses()
    return render_template('index.html', expenses=expenses)

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
