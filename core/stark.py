from core.brain import think
from core.memory import add_history
from core.personality import shutdown_message
from core.intent import detect_intent

from ui.interface import (
    startup_screen,
    prompt,
    processing,
    response,
)


def get_processing_message(intent):
    """Return the appropriate UI state for an intent."""

    states = {
        "remember": "Updating memory",
        "recall": "Accessing memory",
        "context_recall": "Resolving context",
        "memory_overview": "Loading memory",
        "unknown": "Thinking",
    }

    return states.get(intent)


def main():
    startup_screen()

    while True:
        try:
            user_input = input(prompt()).strip()

            if not user_input:
                continue

            intent = detect_intent(user_input)

            # Exit immediately without a processing state.
            if intent == "exit":
                response_text = think(user_input)

                if response_text == "EXIT":
                    print()
                    print(shutdown_message())
                    break

            # Show an appropriate state for operations
            # that require processing.
            processing_message = get_processing_message(intent)

            if processing_message:
                processing(processing_message)

            response_text = think(user_input)

            if response_text == "EXIT":
                print()
                print(shutdown_message())
                break

            add_history(user_input, response_text)

            response(response_text)

        except KeyboardInterrupt:
            print()
            print(shutdown_message())
            break

        except EOFError:
            print()
            print(shutdown_message())
            break


if __name__ == "__main__":
    main()