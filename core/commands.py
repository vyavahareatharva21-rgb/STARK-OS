import datetime

from core.memory import remember, recall
from core.intent import detect_intent


def process_command(command):
    command = command.strip()
    lower_command = command.lower()

    intent = detect_intent(command)

    # GREETING
    if intent == "greeting":
        return "Hello Atharva. STARK systems are online."

    # TIME
    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}"

    # REMEMBER
    elif intent == "remember":
        information = command[9:].strip()

        if " is " in information.lower():
            key, value = information.split(" is ", 1)
            key = key.strip().lower()
            value = value.strip()

            remember(key, value)
            return "I'll remember that, Atharva."

        return "Tell me what to remember using: remember [key] is [value]"

    # RECALL
    elif intent == "recall":
        if "what is my " in lower_command:
            key = command.lower().split("what is my ", 1)[1].strip(" ?!.,")
        elif "do you remember my " in lower_command:
            key = command.lower().split("do you remember my ", 1)[1].strip(" ?!.,")
        else:
            return "Tell me what you want me to remember."

        value = recall(key)

        if value is not None:
            return f"Your {key} is {value}."

        return f"I don't remember your {key} yet."

    # HELP
    elif intent == "help":
        return """
Available commands:

- hello / hey stark
- time / what time is it
- remember [key] is [value]
- what is my [key]
- do you remember my [key]
- help
- exit
"""

    # EXIT
    elif intent == "exit":
        return "EXIT"

    return "I am still learning this command."
