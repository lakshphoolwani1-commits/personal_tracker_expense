from database.db_manager import run_select, run_commit, get_connection
from utils.logger import log_activity


def add_expense(expense_dict, db_path=None):
    """Inserts a new expense into the database and checks budget limits."""
    query = """
            INSERT INTO expenses (title, amount, category, expense_date, payment_method, notes)
            VALUES (?, ?, ?, ?, ?, ?); \
            """
    params = (
        expense_dict["title"],
        expense_dict["amount"],
        expense_dict["category"],
        expense_dict["expense_date"],
        expense_dict["payment_method"],
        expense_dict["notes"]
    )

    if db_path:
        new_id = run_commit(query, params, db_path)
        warning = check_category_budget(expense_dict["category"], expense_dict["expense_date"][:7], db_path)
    else:
        new_id = run_commit(query, params)
        warning = check_category_budget(expense_dict["category"], expense_dict["expense_date"][:7])

    log_activity(f"Expense added with ID #{new_id}")
    return {"success": True, "id": new_id, "warning": warning}


def get_all_expenses(db_path=None):
    """Retrieves all expenses sorted by date."""
    query = "SELECT * FROM expenses ORDER BY expense_date DESC, id DESC;"
    if db_path:
        return run_select(query, db_path=db_path)
    return run_select(query)


def delete_expense_by_id(expense_id, db_path=None):
    """Deletes an expense by its ID."""
    query = "DELETE FROM expenses WHERE id = ?;"
    if db_path:
        conn = get_connection(db_path)
    else:
        conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, (expense_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    if deleted:
        log_activity(f"Expense ID #{expense_id} deleted.")
    return deleted


def save_category_budget(category, limit_amount, db_path=None):
    """Saves or updates a category budget limit."""
    query = """
            INSERT INTO budgets (category, limit_amount, alert_threshold)
            VALUES (?, ?, 0.80) ON CONFLICT(category) DO \
            UPDATE SET limit_amount=excluded.limit_amount; \
            """
    if db_path:
        run_commit(query, (category, limit_amount), db_path)
    else:
        run_commit(query, (category, limit_amount))
    log_activity(f"Budget for '{category}' set to ${limit_amount:.2f}")
    return True


def check_category_budget(category, month_str, db_path=None):
    """Checks if spending in a category exceeds the set budget for the month."""
    budget_query = "SELECT * FROM budgets WHERE category = ?;"
    if db_path:
        budgets = run_select(budget_query, (category,), db_path)
    else:
        budgets = run_select(budget_query, (category,))

    if not budgets:
        return None

    limit_amount = budgets[0]["limit_amount"]
    alert_threshold = budgets[0]["alert_threshold"]

    spending_query = """
                     SELECT SUM(amount) as total \
                     FROM expenses
                     WHERE category = ? \
                       AND strftime('%Y-%m', expense_date) = ?; \
                     """
    if db_path:
        rows = run_select(spending_query, (category, month_str), db_path)
    else:
        rows = run_select(spending_query, (category, month_str))

    total_spent = rows[0]["total"] if rows[0]["total"] else 0.0

    utilization = total_spent / limit_amount
    if utilization >= 1.0:
        return f"CRITICAL ALERT: Monthly budget for '{category}' EXCEEDED! (${total_spent:.2f} / ${limit_amount:.2f})"
    elif utilization >= alert_threshold:
        return f"WARNING: Monthly budget for '{category}' is at {utilization * 100:.1f}% capacity!"

    return None