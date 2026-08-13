from core.commands import process_command
from core.intent import detect_intent
from core.memory import get_recent_history


def think(command):
    intent = detect_intent(command)

    print(f"[DEBUG] Intent detected: {intent}")

    recent_history = get_recent_history()

    print(f"[DEBUG] Recent history entries: {len(recent_history)}")

    if intent == "exit":
        return "EXIT"

    if intent == "unknown":
        return "I don't understand that command yet."

    return process_command(command)