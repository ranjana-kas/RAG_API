from typing import List
import re
from utils.text_cleaner import clean_text


def chunk_text(text: str, chunk_size: int = 400) -> List[str]:
    cleaned_text = clean_text(text)

    sentences = re.split(r'(?<=[.!?]) +', cleaned_text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks