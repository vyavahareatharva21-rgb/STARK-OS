from core.commands import process_command
from core.intent import detect_intent
from core.memory import get_recent_history
from core.context import resolve_context
from core.ai_context import build_ai_prompt
from ai.engine import ai_engine


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