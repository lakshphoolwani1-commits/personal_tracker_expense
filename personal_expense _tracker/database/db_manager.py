import sqlite3
from config import DB_PATH
from utils.logger import log_error, log_activity


def get_connection(db_path=DB_PATH):
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_database(db_path=DB_PATH):
    """Creates tables for expenses and budgets if they do not exist."""
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS expenses
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           title
                           TEXT
                           NOT
                           NULL,
                           amount
                           REAL
                           NOT
                           NULL,
                           category
                           TEXT
                           NOT
                           NULL,
                           expense_date
                           TEXT
                           NOT
                           NULL,
                           payment_method
                           TEXT
                           DEFAULT
                           'Cash',
                           notes
                           TEXT,
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP
                       );
                       """)

        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS budgets
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           category
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           limit_amount
                           REAL
                           NOT
                           NULL,
                           alert_threshold
                           REAL
                           DEFAULT
                           0.80
                       );
                       """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_expense_date ON expenses(expense_date);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_expense_category ON expenses(category);")

        conn.commit()
        conn.close()
        log_activity("Database schema initialized.")
    except sqlite3.Error as e:
        log_error(f"Database setup error: {e}")


def run_select(query, params=(), db_path=DB_PATH):
    """Runs a SELECT query and returns rows as a list of dictionaries."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result


def run_commit(query, params=(), db_path=DB_PATH):
    """Runs INSERT, UPDATE, or DELETE and returns the last row ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id