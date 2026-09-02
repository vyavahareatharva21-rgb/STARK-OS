import datetime

from core.memory import remember, recall, get_all_memories
from core.intent import detect_intent
from core.context import normalize_command


def process_command(command):
    command = command.strip()
    lower_command = command.lower()

    intent = detect_intent(command)

    # ============================================================
    # GREETING
    # ============================================================

    if intent == "greeting":
        return "Hello Atharva. STARK systems are online."

    # ============================================================
    # TIME
    # ============================================================

    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}"

    # ============================================================
    # REMEMBER
    # ============================================================

    elif intent == "remember":
        information = command[9:].strip()

        if " is " in information.lower():
            key, value = information.split(" is ", 1)

            key = normalize_command(key.strip())
            value = value.strip()

            # Remove conversational prefix.
            if key.startswith("my "):
                key = key[3:].strip()

            remember(key, value)

            return "I'll remember that, Atharva."

        return "Tell me what to remember using: remember [key] is [value]"

    # ============================================================
    # CONTEXT RECALL
    # ============================================================

    elif intent in ("context_recall", "recall"):

        normalized_command = normalize_command(command)

        # --------------------------------------------------------
        # "recall"
        # --------------------------------------------------------

        if normalized_command in (
            "recall",
            "remember",
            "my memories",
            "show my memories",
            "what do you remember",
        ):
            memories = get_all_memories()

            if not memories:
                return "I don't have any memories stored yet."

            response = "Here's what I remember:\n"

            for key, value in memories.items():
                response += f"- {key}: {value}\n"

            return response.rstrip()

        # --------------------------------------------------------
        # Specific memory queries
        # --------------------------------------------------------

        if "what is my " in normalized_command:
            key = normalized_command.split(
                "what is my ", 1
            )[1].strip(" ?!.,")

        elif "do you remember my " in normalized_command:
            key = normalized_command.split(
                "do you remember my ", 1
            )[1].strip(" ?!.,")

        elif "what's my " in normalized_command:
            key = normalized_command.split(
                "what's my ", 1
            )[1].strip(" ?!.,")

        elif "tell me my " in normalized_command:
            key = normalized_command.split(
                "tell me my ", 1
            )[1].strip(" ?!.,")

        elif "show me my " in normalized_command:
            key = normalized_command.split(
                "show me my ", 1
            )[1].strip(" ?!.,")

        else:
            return "Tell me which memory you want me to recall."

        # Normalize the requested memory key.
        key = normalize_command(key)

        if key.startswith("my "):
            key = key[3:].strip()

        value = recall(key)

        if value is not None:
            return f"Your {key} is {value}."

        return f"I don't remember your {key} yet."

    # ============================================================
    # MEMORY OVERVIEW
    # ============================================================

    elif intent == "memory_overview":

        memories = get_all_memories()

        if not memories:
            return "I don't have any memories stored yet."

        response = "Here's what I remember:\n"

        for key, value in memories.items():
            response += f"- {key}: {value}\n"

        return response.rstrip()

    # ============================================================
    # HELP
    # ============================================================

    elif intent == "help":
        return """
Available commands:

- hello / hey stark
- time / what time is it
- remember [key] is [value]
- recall
- what is my [key]
- what's my [key]
- do you remember my [key]
- tell me my [key]
- show me my [key]
- what do you remember
- show my memories
- help
- exit
"""

    # ============================================================
    # EXIT
    # ============================================================

    elif intent == "exit":
        return "EXIT"

    # ============================================================
    # UNKNOWN
    # ============================================================

    return "I am still learning this command."