# db.py
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL -- 'income' or 'expense'
    )''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS budgets (
        category TEXT PRIMARY KEY,
        amount REAL NOT NULL
    )''')

    conn.commit()
    conn.close()

def add_transaction(date, category, amount, ttype):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('INSERT INTO transactions (date, category, amount, type) VALUES (?, ?, ?, ?)', 
              (date, category, amount, ttype))
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def set_budget(category, amount):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('REPLACE INTO budgets (category, amount) VALUES (?, ?)', (category, amount))
    conn.commit()
    conn.close()

def get_budgets():
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('SELECT * FROM budgets')
    rows = c.fetchall()
    conn.close()
    return rows

def delete_transaction(transaction_id):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()

def delete_budget(category):
    conn = sqlite3.connect('budget.db')
    c = conn.cursor()
    c.execute('DELETE FROM budgets WHERE category = ?', (category,))
    conn.commit()
    conn.close()