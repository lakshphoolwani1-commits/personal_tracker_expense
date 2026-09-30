import datetime

def validate_amount(amount_text):
    """Validates that the input is a positive number."""
    try:
        val = float(amount_text)
        if val <= 0:
            return False, None, "Amount must be greater than zero."
        return True, round(val, 2), "Success"
    except ValueError:
        return False, None, "Invalid input. Please enter a valid number."

def validate_date(date_text):
    """Validates date format YYYY-MM-DD or defaults to today if empty."""
    cleaned = date_text.strip()
    if cleaned == "":
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        return True, today_str, "Defaulted to today."
    try:
        parsed = datetime.datetime.strptime(cleaned, "%Y-%m-%d")
        return True, parsed.strftime("%Y-%m-%d"), "Success"
    except ValueError:
        return False, None, "Invalid date. Please use YYYY-MM-DD format."

def validate_non_empty(text, field_name):
    """Checks that a text string is not empty."""
    cleaned = text.strip()
    if cleaned == "":
        return False, "", f"{field_name} cannot be empty."
    return True, cleaned, "Success"