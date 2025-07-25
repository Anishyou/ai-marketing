import re
from datetime import datetime, timedelta

def extract_url(prompt: str) -> str:
    match = re.search(r'https?://\S+', prompt)
    return match.group(0) if match else None

def extract_timeframe(prompt: str) -> str:
    prompt_lower = prompt.lower()
    today = datetime.today()

    if "next week" in prompt_lower:
        start = today + timedelta(days=(7 - today.weekday()))
        return start.strftime("%Y-%m-%d")
    elif "this weekend" in prompt_lower:
        saturday = today + timedelta(days=(5 - today.weekday()) % 7)
        return saturday.strftime("%Y-%m-%d")
    elif "halloween" in prompt_lower:
        return "2025-10-31"
    elif "christmas" in prompt_lower:
        return "2025-12-25"
    else:
        return None
