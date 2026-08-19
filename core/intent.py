def detect_intent(command):
    command = command.lower().strip()

    # EXIT
    if command in [
        "exit",
        "quit",
        "shutdown",
        "shut down",
        "goodbye",
        "bye",
    ]:
        return "exit"

    # GREETING
    greeting_phrases = [
        "hello",
        "hi",
        "hey",
        "hey stark",
        "hi stark",
        "hello stark",
        "good morning",
        "good afternoon",
        "good evening",
    ]

    if any(phrase in command for phrase in greeting_phrases):
        return "greeting"

    # TIME
    time_phrases = [
        "time",
        "what time",
        "current time",
        "tell me the time",
        "what's the time",
        "what is the time",
    ]

    if any(phrase in command for phrase in time_phrases):
        return "time"

    # REMEMBER
    if (
        command.startswith("remember ")
        or command.startswith("remember that ")
    ):
        return "remember"

    # CONTEXT RECALL
    context_phrases = [
        "what about my ",
        "how about my ",
        "and my ",
    ]

    if any(phrase in command for phrase in context_phrases):
        return "context_recall"


    

    # RECALL
    recall_phrases = [
        "recall",
        "what is my ",
        "what's my ",
        "do you remember my ",
        "tell me my ",
        "show me my ",
    ]

    if any(phrase in command for phrase in recall_phrases):
        return "recall"

    # MEMORY OVERVIEW
    memory_phrases = [
        "what do you remember",
        "show my memories",
        "show memories",
        "what have you remembered",
        "what do you know about me",
    ]

    if any(phrase in command for phrase in memory_phrases):
        return "memory_overview"

    # HELP
    if (
        command == "help"
        or "what can you do" in command
        or "what are your commands" in command
    ):
        return "help"

    return "unknown"