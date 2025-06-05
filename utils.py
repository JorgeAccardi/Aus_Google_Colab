def validate_file_path(file_path):
    """Validates the file path for loading data."""
    import os
    return os.path.isfile(file_path)

def format_data(data):
    """Formats data for display or processing."""
    return data.strip().title()

def log_message(message):
    """Logs a message to the console."""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}")