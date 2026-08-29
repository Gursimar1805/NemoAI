import os
import json
from pathlib import Path
import httpx
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "nvidia/nemotron-3.5-lightning:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


async def stream_chat_completion(messages: list[dict]):
    """Yields SSE-formatted chunks of streamed model output."""
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set in .env")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "NemoAI Chat Assistant",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": True,
        "temperature": 0.7,
        "max_tokens": 2048,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream("POST", OPENROUTER_URL, headers=headers, json=payload) as resp:
            if resp.status_code != 200:
                error_text = await resp.aread()
                raise RuntimeError(f"OpenRouter error {resp.status_code}: {error_text.decode()}")

            async for line in resp.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue
                data = line[len("data: "):]
                if data.strip() == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        yield delta
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue


async def get_chat_completion(messages: list[dict]) -> str:
    """Non-streaming version — useful for simpler Streamlit integration."""
    full_response = ""
    async for chunk in stream_chat_completion(messages):
        full_response += chunk
    return full_response