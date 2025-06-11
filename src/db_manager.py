import sqlite3
from datetime import datetime

import os
DB_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db/database.db"))


def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT CHECK(type IN ('income', 'expense')) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category_id INTEGER,
            description TEXT,
            is_recurring INTEGER DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    conn.commit()
    conn.close()

def get_categories(category_type=None):
    conn = connect()
    cursor = conn.cursor()
    if category_type:
        cursor.execute("SELECT id, name FROM categories WHERE type = ?", (category_type,))
    else:
        cursor.execute("SELECT id, name, type FROM categories")
    results = cursor.fetchall()
    conn.close()
    return results

def add_category(name, category_type):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories (name, type) VALUES (?, ?)", (name, category_type))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()

def add_transaction(amount, date, category_id, description, is_recurring):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (amount, date, category_id, description, is_recurring)
        VALUES (?, ?, ?, ?, ?)
    """, (amount, date, category_id, description, int(is_recurring)))
    conn.commit()
    conn.close()

def get_transactions_by_month(year, month):
    conn = connect()
    cursor = conn.cursor()
    start = f"{year}-{month:02d}-01"
    end = f"{year}-{month:02d}-31"
    cursor.execute("""
        SELECT t.id, t.amount, t.date, c.name, c.type, t.description
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC
    """, (start, end))
    results = cursor.fetchall()
    conn.close()
    return results

def delete_transaction(transaction_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()
    conn.close()

def update_category_type(name, new_type):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE categories SET type = ? WHERE name = ?", (new_type, name))
    conn.commit()
    conn.close()
