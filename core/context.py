import re
import string

from core.memory import (
    get_recent_history,
    get_user_memories,
)


# ============================================================
# NORMALIZATION
# ============================================================

NORMALIZATION_MAP = {
    "favourite": "favorite",
    "colour": "color",
    "programme": "program",
    "programmes": "programs",
}


def normalize_command(command):
    """
    Normalize a user command.

    Examples:
        favourite -> favorite
        colour -> color
        "what is my favourite colour?"
            ->
        "what is my favorite color"
    """

    if not isinstance(command, str):
        return ""

    command = command.lower().strip()

    # Remove accidental repeated whitespace.
    command = re.sub(r"\s+", " ", command)

    words = command.split()

    normalized_words = []

    for word in words:
        cleaned_word = word.strip(string.punctuation)

        if not cleaned_word:
            continue

        normalized_word = NORMALIZATION_MAP.get(
            cleaned_word,
            cleaned_word
        )

        normalized_words.append(normalized_word)

    return " ".join(normalized_words)


# ============================================================
# CONTEXT RECALL
# ============================================================

def resolve_context(command):
    """
    Resolve context-related memory requests.

    Examples:

        what about my favourite colour?
        ->
        what is my favorite color

        how about my favourite language?
        ->
        what is my favorite language

        and my favourite movie?
        ->
        what is my favorite movie
    """

    command = normalize_command(command)

    context_patterns = [
        "what about my ",
        "how about my ",
        "and my ",
    ]

    for pattern in context_patterns:
        if command.startswith(pattern):
            return command.replace(
                pattern,
                "what is my ",
                1
            )

    return command


# ============================================================
# RECENT CONVERSATION
# ============================================================

def get_context(limit=5):
    """
    Return recent conversation history.
    """

    return get_recent_history(limit=limit)


# ============================================================
# CONTEXT ANALYSIS
# ============================================================

def needs_memory(command):
    """
    Determine whether the request is asking
    about stored user information.
    """

    command = normalize_command(command)

    memory_phrases = [
        "what is my ",
        "what's my ",
        "do you remember my ",
        "tell me my ",
        "show me my ",
        "what do you remember",
        "show my memories",
        "what have you remembered",
        "what do you know about me",
    ]

    return any(
        phrase in command
        for phrase in memory_phrases
    )


def needs_history(command):
    """
    Determine whether the request depends
    on previous conversation.
    """

    command = normalize_command(command)

    history_phrases = [
        "who created it",
        "who made it",
        "what did i say",
        "what did we discuss",
        "what were we talking about",
        "what was that",
        "what about it",
        "and what about it",
        "explain that",
        "tell me more about it",
    ]

    return any(
        phrase in command
        for phrase in history_phrases
    )


# ============================================================
# RELEVANT CONTEXT
# ============================================================

def get_relevant_context(command):
    """
    Decide what context STARK should provide to Gemini.

    Returns:

        {
            "command": normalized command,
            "memories": relevant memories,
            "history": relevant history
        }
    """

    normalized_command = normalize_command(command)

    context = {
        "command": normalized_command,
        "memories": {},
        "history": [],
    }

    if needs_memory(normalized_command):
        context["memories"] = get_user_memories()

    if needs_history(normalized_command):
        context["history"] = get_recent_history(limit=5)

    return context