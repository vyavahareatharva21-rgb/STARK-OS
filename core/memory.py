import json
import os

MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "memory",
    "memory.json"
)


def load_memory():
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "user": {},
            "history": []
        }


def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


def remember(key, value):
    memory = load_memory()
    memory["user"][key] = value
    save_memory(memory)


def recall(key):
    memory = load_memory()
    return memory["user"].get(key)


def add_history(user_input, response):
    memory = load_memory()

    memory["history"].append({
        "user": user_input,
        "stark": response
    })

    save_memory(memory)


def get_all_memories():
    memory = load_memory()
    return memory.get("user", {})


def get_history():
    memory = load_memory()
    return memory.get("history", [])


def get_recent_history(limit=5):
    history = get_history()
    return history[-limit:]
