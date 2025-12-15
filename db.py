import sqlite3

DB_NAME = "expenses.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(amount, category, description, date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (amount, category, description, date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, date))

    conn.commit()
    conn.close()


def get_all_expenses():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        ORDER BY date DESC
    """)

    expenses = cursor.fetchall()
    conn.close()
    return expenses


def delete_expense(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses WHERE id = ?
    """, (expense_id,))

    conn.commit()
    conn.close()

def update_expense(expense_id, amount, category, description, date):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET amount = ?,
            category = ?,
            description = ?,
            date = ?
        WHERE id = ?
    """, (amount, category, description, date, expense_id))

    conn.commit()
    conn.close()

def get_expense_by_id(expense_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM expenses
        WHERE id = ?
    """, (expense_id,))

    expense = cursor.fetchone()
    conn.close()
    return expense

def get_total_expense():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount) FROM expenses
    """)

    total = cursor.fetchone()[0]
    conn.close()

    return total if total is not None else 0


def get_category_totals():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_filtered_expenses(category=None, start=None, end=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if start:
        query += " AND date >= ?"
        params.append(start)

    if end:
        query += " AND date <= ?"
        params.append(end)

    query += " ORDER BY date DESC"

    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data
