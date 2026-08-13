from core.commands import process_command
from core.intent import detect_intent
from core.memory import get_recent_history
from core.context import resolve_context


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
        return "I don't understand that command yet."

    return process_command(command)