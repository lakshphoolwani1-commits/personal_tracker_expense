import os
import datetime
from config import LOG_DIR

def log_activity(message):
    """Appends an operational message to the activity log file."""
    log_file = os.path.join(LOG_DIR, "activity.log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] INFO: {message}\n")

def log_error(message):
    """Appends an error message to the error log file."""
    log_file = os.path.join(LOG_DIR, "app_errors.log")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] ERROR: {message}\n")