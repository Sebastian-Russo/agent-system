"""
DateTime Tool
Gets current date, time, and timezone info

ANALOGY: A clock and calendar on the wall.
The agent has no sense of time on its own —
it needs to check the clock.
"""
from datetime import datetime

def get_datetime():
    """
    Get current date and time

    Output: {"date": "2026-02-24", "time": "14:30:00", "day": "Tuesday"}
    """
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
        "full": now.strftime("%A, %B %d, %Y at %I:%M %p")
    }
