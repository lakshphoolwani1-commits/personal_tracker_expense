import sys
import datetime
from services.expense_service import (
    add_expense, get_all_expenses, delete_expense_by_id, save_category_budget
)
from services.analytics_service import get_monthly_report, export_expenses_csv, export_expenses_json
from models.expense import make_expense
from utils.validator import validate_amount, validate_date, validate_non_empty
from config import DEFAULT_CATEGORIES, DEFAULT_PAYMENT_METHODS


def display_menu():
    """Prints the main user menu."""
    print("\n==================================================")
    print("      PERSONAL EXPENSE TRACKER - MAIN MENU        ")
    print("==================================================")
    print(" 1. Record New Expense")
    print(" 2. View All Expense Transactions")
    print(" 3. Delete Expense Record")
    print(" 4. Configure Category Budget Limit")
    print(" 5. Generate Monthly Spending Report")
    print(" 6. Export Expenses (CSV / JSON)")
    print(" 7. Exit System")
    print("==================================================")


def handle_add_expense():
    """Menu flow for adding an expense."""
    print("\n--- Record New Expense Transaction ---")

    while True:
        raw_title = input("Enter expense title: ")
        valid, title, msg = validate_non_empty(raw_title, "Title")
        if valid:
            break
        print(f"[Error] {msg}")

    while True:
        raw_amount = input("Enter amount ($): ")
        valid, amount, msg = validate_amount(raw_amount)
        if valid:
            break
        print(f"[Error] {msg}")

    print("\nSelect Expense Category:")
    for idx, cat in enumerate(DEFAULT_CATEGORIES, 1):
        print(f" {idx}. {cat}")

    while True:
        choice = input(f"Select category (1-{len(DEFAULT_CATEGORIES)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(DEFAULT_CATEGORIES):
            category = DEFAULT_CATEGORIES[int(choice) - 1]
            break
        print("[Error] Invalid choice.")

    while True:
        raw_date = input("Enter date (YYYY-MM-DD) [Press Enter for Today]: ")
        valid, expense_date, msg = validate_date(raw_date)
        if valid:
            break
        print(f"[Error] {msg}")

    print("\nSelect Payment Method:")
    for idx, pm in enumerate(DEFAULT_PAYMENT_METHODS, 1):
        print(f" {idx}. {pm}")

    pm_choice = input(f"Select method (1-{len(DEFAULT_PAYMENT_METHODS)}) [Default 1]: ").strip()
    if pm_choice.isdigit() and 1 <= int(pm_choice) <= len(DEFAULT_PAYMENT_METHODS):
        payment_method = DEFAULT_PAYMENT_METHODS[int(pm_choice) - 1]
    else:
        payment_method = DEFAULT_PAYMENT_METHODS[0]

    notes = input("Optional notes: ").strip()

    expense = make_expense(title, amount, category, expense_date, payment_method, notes)
    result = add_expense(expense)

    print(f"\n[SUCCESS] Expense recorded with ID #{result['id']}")
    if result['warning']:
        print(f"\n[ALERT] {result['warning']}")


def handle_view_expenses():
    """Displays all expenses in a table."""
    expenses = get_all_expenses()
    print("\n----------------------------------------------------------------------------------")
    print(f"{'ID':<4} | {'Date':<10} | {'Title':<20} | {'Category':<16} | {'Amount ($)':<10} | {'Method':<10}")
    print("----------------------------------------------------------------------------------")
    if not expenses:
        print("No expense records found.")
    else:
        for exp in expenses:
            print(
                f"{exp['id']:<4} | {exp['expense_date']:<10} | {exp['title'][:20]:<20} | {exp['category'][:16]:<16} | {exp['amount']:<10.2f} | {exp['payment_method']:<10}")
    print("----------------------------------------------------------------------------------")


def handle_delete_expense():
    """Menu flow for deleting an expense."""
    handle_view_expenses()
    exp_id = input("\nEnter Expense ID to delete: ").strip()
    if exp_id.isdigit():
        success = delete_expense_by_id(int(exp_id))
        if success:
            print(f"[SUCCESS] Record ID #{exp_id} deleted successfully.")
        else:
            print(f"[ERROR] Expense ID #{exp_id} not found.")
    else:
        print("[ERROR] Please enter a valid numeric ID.")


def handle_set_budget():
    """Menu flow for setting a category budget."""
    print("\n--- Configure Category Monthly Budget ---")
    for idx, cat in enumerate(DEFAULT_CATEGORIES, 1):
        print(f" {idx}. {cat}")

    choice = input(f"Select category (1-{len(DEFAULT_CATEGORIES)}): ").strip()
    if not (choice.isdigit() and 1 <= int(choice) <= len(DEFAULT_CATEGORIES)):
        print("[ERROR] Invalid choice.")
        return

    category = DEFAULT_CATEGORIES[int(choice) - 1]

    while True:
        raw_amount = input(f"Enter monthly budget limit for '{category}': ")
        valid, amount, msg = validate_amount(raw_amount)
        if valid:
            break
        print(f"[Error] {msg}")

    save_category_budget(category, amount)
    print(f"[SUCCESS] Monthly budget of ${amount:.2f} saved for '{category}'.")


def handle_monthly_report():
    """Menu flow for generating monthly reports."""
    default_month = datetime.datetime.now().strftime("%Y-%m")
    month_str = input(f"Enter report month (YYYY-MM) [Default {default_month}]: ").strip()
    if not month_str:
        month_str = default_month

    summary = get_monthly_report(month_str)
    print(f"\n==========================================")
    print(f"      EXPENSE REPORT FOR {summary['month']}       ")
    print(f"==========================================")
    print(f"Total Expenditure: ${summary['grand_total']:.2f}\n")
    print(f"{'Category':<20} | {'Count':<12} | {'Total ($)':<10}")
    print("------------------------------------------")
    for row in summary['breakdown']:
        print(f"{row['category']:<20} | {row['transaction_count']:<12} | {row['total_spent']:<10.2f}")
    print("==========================================")


def handle_data_export():
    """Menu flow for exporting data."""
    print("\nSelect Output Export Format:")
    print(" 1. Comma-Separated Values (CSV)")
    print(" 2. JavaScript Object Notation (JSON)")
    choice = input("Select option (1-2): ").strip()

    if choice == '1':
        path = export_expenses_csv()
        print(f"[SUCCESS] Data exported to CSV: {path}")
    elif choice == '2':
        path = export_expenses_json()
        print(f"[SUCCESS] Data exported to JSON: {path}")
    else:
        print("[ERROR] Invalid export option.")


def start_app():
    """Starts the terminal user interface loop."""
    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()

        if choice == '1':
            handle_add_expense()
        elif choice == '2':
            handle_view_expenses()
        elif choice == '3':
            handle_delete_expense()
        elif choice == '4':
            handle_set_budget()
        elif choice == '5':
            handle_monthly_report()
        elif choice == '6':
            handle_data_export()
        elif choice == '7':
            print("\nExiting system. Program terminated.")
            sys.exit(0)
        else:
            print("\n[ERROR] Invalid choice. Please select 1-7.")