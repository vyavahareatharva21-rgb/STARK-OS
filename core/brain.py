from core.commands import process_command
from core.intent import detect_intent


def think(command):
    intent = detect_intent(command)

    if intent == "exit":
        return "EXIT"

    response = process_command(command)

    return response
