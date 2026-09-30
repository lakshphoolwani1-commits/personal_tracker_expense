from database.db_manager import init_database
from cli.interface import start_app
from utils.logger import log_activity, log_error

def main():
    """Application entry point."""
    print("Initializing Personal Expense Tracker...")
    try:
        init_database()
        log_activity("Application started.")
        start_app()
    except Exception as e:
        log_error(f"Application crash: {e}")
        print(f"\n[CRITICAL ERROR] Application closed unexpectedly: {e}")

if __name__ == "__main__":
    main()