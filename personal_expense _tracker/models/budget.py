def make_budget(category, limit_amount, alert_threshold=0.80):
    """Helper function to create a basic budget dictionary."""
    return {
        "category": category,
        "limit_amount": limit_amount,
        "alert_threshold": alert_threshold
    }

def calculate_budget_percentage(spending, limit_amount):
    """Calculates percentage of budget spent."""
    if limit_amount <= 0:
        return 0.0
    return (spending / limit_amount) * 100.0