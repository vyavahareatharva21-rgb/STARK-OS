from core.brain import think
from core.memory import add_history
from core.personality import shutdown_message

from ui.interface import startup_screen, prompt


def main():
    startup_screen()

    while True:
        try:
            user_input = input(prompt()).strip()

            if not user_input:
                continue

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
            print("\n")
            print(shutdown_message())
            break

        except EOFError:
            print("\n")
            print(shutdown_message())
            break


if __name__ == "__main__":
    main()