import re

def clean_text(text: str) -> str:
    # Optimizes token usage by stripping unnecessary whitespaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()