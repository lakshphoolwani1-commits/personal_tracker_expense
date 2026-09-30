import os

# Base directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")

# Create required folders if they don't exist
for folder in [DATA_DIR, LOG_DIR, EXPORT_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Database file path
DB_PATH = os.path.join(DATA_DIR, "expense_tracker.db")

# Default categories and payment methods
DEFAULT_CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Utilities & Bills",
    "Entertainment",
    "Healthcare",
    "Shopping",
    "Education",
    "Miscellaneous"
]

DEFAULT_PAYMENT_METHODS = ["Cash", "Credit Card", "Debit Card", "UPI", "Bank Transfer"]