import re
from datetime import datetime, timedelta

def extract_url(text: str) -> str:
    match = re.search(r'https?://\S+', text)
    return match.group(0) if match else None

def extract_timeframe(text: str) -> str:
    text = text.lower()
    today = datetime.today()

    if "next week" in text:
        start = today + timedelta(days=(7 - today.weekday()))
        return start.strftime("%Y-%m-%d")
    elif "this weekend" in text:
        saturday = today + timedelta(days=(5 - today.weekday()) % 7)
        return saturday.strftime("%Y-%m-%d")
    elif "halloween" in text:
        return "2025-10-31"
    elif "christmas" in text:
        return "2025-12-25"
    return None
