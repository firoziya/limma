# chat.py

from collections import deque
from . import generate 

MAX_CONTEXT_CHARS = 32000
_conversation_queue = deque()
_total_length = 0


def chat(message: str, role: str = "user") -> str:
    """
    Chat with the LLM while storing recent conversation history.
    Uses a sliding window to keep the context within MAX_CONTEXT_CHARS.
    """
    global _total_length

    _add_to_queue(message, role)

    history_text = "\n".join(f"{m['role']}: {m['content']}" for m in _conversation_queue)

    ai_reply = generate(history_text)

    _add_to_queue(ai_reply, "assistant")

    return ai_reply


def _add_to_queue(content: str, role: str):
    """Add a message to the queue while respecting the max context size."""
    global _total_length

    msg_len = len(content)

    while _total_length + msg_len > MAX_CONTEXT_CHARS and _conversation_queue:
        oldest = _conversation_queue.popleft()
        _total_length -= oldest["length"]

    _conversation_queue.append({"role": role, "content": content, "length": msg_len})
    _total_length += msg_len


def reset_chat():
    """Clear the conversation history."""
    global _total_length
    _conversation_queue.clear()
    _total_length = 0


