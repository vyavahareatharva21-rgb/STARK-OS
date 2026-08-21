from core.context import get_relevant_context


def build_ai_prompt(command):
    """
    Build the context sent to Gemini.

    The Context Engine decides whether STARK needs:
    - Long-term user memory
    - Recent conversation history
    - Neither
    """

    context = get_relevant_context(command)

    normalized_command = context["command"]
    memories = context["memories"]
    history = context["history"]

    # --------------------------------------------------------
    # MEMORY
    # --------------------------------------------------------

    if memories:
        memory_text = "\n".join(
            f"- {key}: {value}"
            for key, value in memories.items()
        )
    else:
        memory_text = "No relevant memories."

    # --------------------------------------------------------
    # HISTORY
    # --------------------------------------------------------

    if history:
        history_text = "\n".join(
            f"User: {entry['user']}\nSTARK: {entry['stark']}"
            for entry in history
        )
    else:
        history_text = "No relevant conversation history."

    # --------------------------------------------------------
    # PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are operating as STARK-OS.

CURRENT USER REQUEST:
{normalized_command}

RELEVANT STARK MEMORY:
{memory_text}

RELEVANT CONVERSATION:
{history_text}

Instructions:
- Use relevant STARK memory when provided.
- Use relevant conversation history when provided.
- If no relevant context is provided, answer normally.
- Do not reveal internal memory structures unless explicitly asked.
- Do not invent personal information.
- If the user refers to something like "it", "that", or "they",
  use the provided conversation history to determine what they mean.
- Answer naturally as STARK.
- Keep responses concise unless the user asks for detail.
"""

    return prompt