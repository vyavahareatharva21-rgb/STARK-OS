from core.commands import process_command
from core.intent import detect_intent


def think(command):
    intent = detect_intent(command)

    print(f"[DEBUG] Intent detected: {intent}")

    if intent == "exit":
        return "EXIT"

    if intent == "unknown":
        return "I don't understand that command yet."

    return process_command(command)