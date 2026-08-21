from core.memory import get_recent_history, get_all_memories


def build_ai_prompt(command):
    """
    Build the context sent to Gemini.

    Includes:
    - Current user request
    - Stored STARK memories
    - Recent conversation history
    """

    memories = get_all_memories()
    recent_history = get_recent_history(limit=5)

    memory_text = "\n".join(
        f"- {key}: {value}"
        for key, value in memories.items()
    )

    history_text = "\n".join(
        f"User: {entry['user']}\nSTARK: {entry['stark']}"
        for entry in recent_history
    )

    prompt = f"""
You are operating as STARK-OS.

The user's current request is:

{command}

STARK MEMORY:
{memory_text if memory_text else "No stored memories."}

RECENT CONVERSATION:
{history_text if history_text else "No recent conversation."}

Instructions:
- Use STARK MEMORY when it is relevant to the user's request.
- Use RECENT CONVERSATION when it helps understand the request.
- Do not reveal internal memory structure unless the user asks.
- Do not invent personal information about the user.
- Answer naturally as STARK.
- Keep the answer concise unless the user asks for detail.
"""

    return prompt