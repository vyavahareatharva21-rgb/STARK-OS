from core.context import get_relevant_context


def build_ai_prompt(command):
    """
    Build a focused prompt for Gemini.

    Only relevant memory and conversation history are included.
    The latest user request always has the highest priority.
    """

    context = get_relevant_context(command)

    normalized_command = context.get("command", command)
    memories = context.get("memories", {})
    history = context.get("history", [])

    # --------------------------------------------------------
    # RELEVANT MEMORY
    # --------------------------------------------------------

    if memories:
        memory_text = "\n".join(
            f"- {key}: {value}"
            for key, value in memories.items()
        )
    else:
        memory_text = "None"

    # --------------------------------------------------------
    # RELEVANT CONVERSATION
    # --------------------------------------------------------

    if history:
        history_text = "\n".join(
            f"User: {entry.get('user', '')}\n"
            f"STARK: {entry.get('stark', '')}"
            for entry in history
        )
    else:
        history_text = "None"

    # --------------------------------------------------------
    # FOCUSED PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are STARK-OS, Atharva's personal AI assistant.

Your task is to answer the CURRENT USER REQUEST accurately.

IMPORTANT RULES:
1. Answer the latest user request only.
2. Never repeat an earlier answer unless the user asks for it.
3. Do not continue an old topic when the user has changed the subject.
4. If the user asks for "yes or no", answer only "Yes" or "No"
   unless a short explanation is explicitly requested.
5. If the user asks a simple question, give a short direct answer.
6. Follow the user's requested format, length, and tone.
7. Use conversation history only when it is necessary to understand
   words such as "it", "that", "this", or "they".
8. Use memory only when it is relevant to the current request.
9. Do not mention prompts, memory systems, context engines, or
   internal STARK-OS implementation details.
10. Do not invent personal information.
11. If the user asks whether you can build or assist with a project,
    answer clearly and directly.

CURRENT USER REQUEST:
{normalized_command}

RELEVANT USER MEMORY:
{memory_text}

RELEVANT CONVERSATION HISTORY:
{history_text}

Now answer the CURRENT USER REQUEST.
"""

    return prompt.strip()