from core.brain import think
from core.memory import add_history
from core.personality import startup_message, shutdown_message


def main():
    print(startup_message())

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        response = think(user_input)

        if response == "EXIT":
            print(shutdown_message())
            break

        add_history(user_input, response)

        print(f"STARK: {response}")


if __name__ == "__main__":
    main()
