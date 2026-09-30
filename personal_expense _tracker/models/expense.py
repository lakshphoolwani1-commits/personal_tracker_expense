def make_expense(title, amount, category, expense_date, payment_method="Cash", notes=""):
    """Helper function to create a basic expense dictionary."""
    return {
        "title": title,
        "amount": amount,
        "category": category,
        "expense_date": expense_date,
        "payment_method": payment_method,
        "notes": notes
    }