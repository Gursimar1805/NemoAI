SYSTEM_PROMPT = """You are a helpful, concise AI assistant specialized in [your domain].
Keep answers clear and to the point. If you don't know something, say so.
Do not make up facts."""

def build_messages(history: list[dict], user_message: str) -> list[dict]:
    """Assemble the full message list sent to the model."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    return messages