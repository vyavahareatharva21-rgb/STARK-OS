def detect_intent(command):
    command = command.lower().strip()

    if command in ["exit", "quit", "shutdown", "shut down"]:
        return "exit"

    if "hello" in command or "hi stark" in command or "hey stark" in command:
        return "greeting"

    if "time" in command or "what time" in command:
        return "time"

    if command.startswith("remember "):
        return "remember"

    if "what is my " in command or "do you remember my " in command:
        return "recall"

    if command == "help" or "what can you do" in command:
        return "help"

    return "unknown"
