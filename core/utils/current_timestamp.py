from datetime import datetime, timezone


def current_timestamp() -> str:
    """Get current timestamp as a string"""

    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")