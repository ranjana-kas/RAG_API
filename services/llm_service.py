import logging
from google import genai
from typing import List, AsyncGenerator
import json
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_client = None
query_cache = {}

def get_client():
    global _client
    if _client is None:
        logger.info("Initializing Gemini client")
        _client = genai.Client()
    return _client


def build_prompt(query: str, context_chunks: List[str], history: List[dict]) -> str:
    context_text = "\n\n".join(context_chunks)

    history_text = ""
    for msg in history[-5:]:  # limit memory
        history_text += f"{msg['role']}: {msg['content']}\n"

    return f"""
You are an AI assistant.

Conversation so far:
{history_text}

Use ONLY the provided context to answer.

Context:
{context_text}

User Question:
{query}

Answer:
"""


async def generate_answer_sync(query: str, context_chunks: List[str], history: List[dict]) -> str:
    if query in query_cache:
        return query_cache[query]

    client = get_client()
    prompt = build_prompt(query, context_chunks, history)

    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    query_cache[query] = response.text
    return response.text


async def generate_answer_stream(query: str, context_chunks: List[str]) -> AsyncGenerator[str, None]:
    if query in query_cache:
        yield f"data: {json.dumps({'text': query_cache[query]})}\n\n"
        return

    client = get_client()
    prompt = build_prompt(query, context_chunks, history)
    response_stream = await client.aio.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    full_response = ""
    async for chunk in response_stream:
        if chunk.text:
            full_response += chunk.text
            yield f"data: {json.dumps({'text': chunk.text})}\n\n"

    query_cache[query] = full_response