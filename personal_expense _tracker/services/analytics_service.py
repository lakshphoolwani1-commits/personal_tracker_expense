import csv
import json
import os
from database.db_manager import run_select
from config import EXPORT_DIR
from utils.logger import log_activity

def get_monthly_report(month_str, db_path=None):
    """Generates monthly summary report grouped by category."""
    query = """
        SELECT category, SUM(amount) as total_spent, COUNT(id) as transaction_count
        FROM expenses
        WHERE strftime('%Y-%m', expense_date) = ?
        GROUP BY category
        ORDER BY total_spent DESC;
    """
    if db_path:
        breakdown = run_select(query, (month_str,), db_path)
        total_query = "SELECT SUM(amount) as grand_total FROM expenses WHERE strftime('%Y-%m', expense_date) = ?;"
        total_rows = run_select(total_query, (month_str,), db_path)
    else:
        breakdown = run_select(query, (month_str,))
        total_query = "SELECT SUM(amount) as grand_total FROM expenses WHERE strftime('%Y-%m', expense_date) = ?;"
        total_rows = run_select(total_query, (month_str,))

    grand_total = total_rows[0]["grand_total"] if total_rows[0]["grand_total"] else 0.0

    return {
        "month": month_str,
        "grand_total": grand_total,
        "breakdown": breakdown
    }

def export_expenses_csv(db_path=None):
    """Exports all expenses to a CSV file."""
    file_path = os.path.join(EXPORT_DIR, "expense_report.csv")
    query = "SELECT id, title, amount, category, expense_date, payment_method, notes FROM expenses ORDER BY expense_date ASC;"
    if db_path:
        records = run_select(query, db_path=db_path)
    else:
        records = run_select(query)

    if not records:
        return ""

    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    log_activity(f"Exported data to CSV at {file_path}")
    return str(file_path)

def export_expenses_json(db_path=None):
    """Exports all expenses to a JSON file."""
    file_path = os.path.join(EXPORT_DIR, "expense_report.json")
    query = "SELECT id, title, amount, category, expense_date, payment_method, notes FROM expenses ORDER BY expense_date ASC;"
    if db_path:
        records = run_select(query, db_path=db_path)
    else:
        records = run_select(query)

    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(records, f, indent=4)

    log_activity(f"Exported data to JSON at {file_path}")
    return str(file_path)