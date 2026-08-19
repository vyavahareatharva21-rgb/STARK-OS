from core.commands import process_command
from core.intent import detect_intent
from core.memory import get_recent_history, get_all_memories
from core.context import resolve_context
from ai.engine import ai_engine


def build_ai_prompt(command):
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


def think(command):
    intent = detect_intent(command)

    print(f"[DEBUG] Intent detected: {intent}")

    recent_history = get_recent_history()

    print(f"[DEBUG] Recent history entries: {len(recent_history)}")

    if intent == "exit":
        return "EXIT"

    if intent == "context_recall":
        command = resolve_context(command)

        print(f"[DEBUG] Context resolved to: {command}")

        return process_command(command)

    if intent == "unknown":
        print("[DEBUG] Sending command to Gemini AI")

        try:
            prompt = build_ai_prompt(command)

            return ai_engine.generate(prompt)

        except Exception as error:
            print(f"[AI ERROR] {error}")
            return "I'm having trouble connecting to my AI system right now."

    return process_command(command)
