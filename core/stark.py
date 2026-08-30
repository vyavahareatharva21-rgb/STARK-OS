from core.brain import think
from core.memory import add_history
from core.personality import shutdown_message

from ui.interface import startup_screen, prompt, processing


def main():
    startup_screen()

    while True:
        try:
            user_input = input(prompt()).strip()

            if not user_input:
                continue

            # Exit commands should shut down immediately
            # without showing a processing message.
            exit_commands = {
                "exit",
                "quit",
                "shutdown",
            }

            if user_input.lower() in exit_commands:
                response = think(user_input)

                if response == "EXIT":
                    print()
                    print(shutdown_message())
                    break

            # Show processing state for normal commands.
            processing()

            response = think(user_input)

            if response == "EXIT":
                print()
                print(shutdown_message())
                break

            add_history(user_input, response)

            print()
            print(f"STARK › {response}")
            print()

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