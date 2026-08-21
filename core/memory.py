import json
import os


MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "memory",
    "memory.json"
)


def load_memory():
    """
    Load STARK's persistent memory from memory.json.

    If the file does not exist or contains invalid JSON,
    return a safe empty memory structure.
    """

    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "user": {},
            "history": []
        }


def save_memory(memory):
    """
    Save STARK's complete memory structure.
    """

    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)


# ============================================================
# USER MEMORY
# ============================================================

def remember(key, value):
    """
    Store or update a long-term user memory.
    """

    memory = load_memory()

    if "user" not in memory:
        memory["user"] = {}

    memory["user"][key] = value

    save_memory(memory)


def recall(key):
    """
    Retrieve a single long-term user memory.
    """

    memory = load_memory()

    return memory.get("user", {}).get(key)


def get_user_memories():
    """
    Return all long-term user memories.
    """

    memory = load_memory()

    return memory.get("user", {})


# Backward-compatible alias.
# Existing STARK code can continue using get_all_memories().
def get_all_memories():
    return get_user_memories()


# ============================================================
# CONVERSATION HISTORY
# ============================================================

def add_history(user_input, response):
    """
    Add a user/STARK exchange to conversation history.
    """

    memory = load_memory()

    if "history" not in memory:
        memory["history"] = []

    memory["history"].append({
        "user": user_input,
        "stark": response
    })

    save_memory(memory)


def get_conversation_history():
    """
    Return the complete conversation history.
    """

    memory = load_memory()

    return memory.get("history", [])


# Backward-compatible alias.
# Existing STARK code can continue using get_history().
def get_history():
    return get_conversation_history()


def get_recent_history(limit=5):
    """
    Return the most recent conversation entries.

    Args:
        limit: Maximum number of entries to return.
    """

    history = get_conversation_history()

    return history[-limit:]