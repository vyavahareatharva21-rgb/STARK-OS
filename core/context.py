import string

from core.memory import get_recent_history


# Common spelling variants used in STARK memory/context requests.
NORMALIZATION_MAP = {
    "favourite": "favorite",
    "colour": "color",
    "programme": "program",
    "programmes": "programs",
}


def normalize_command(command):
    """
    Normalize common spelling variants and punctuation.

    Examples:
        favourite -> favorite
        colour -> color
        colour?  -> color
    """

    words = command.lower().strip().split()

    normalized_words = []

    for word in words:
        cleaned_word = word.strip(string.punctuation)
        normalized_word = NORMALIZATION_MAP.get(
            cleaned_word,
            cleaned_word
        )

        normalized_words.append(normalized_word)

    return " ".join(normalized_words)


def resolve_context(command):
    """
    Resolve context-related memory requests.

    Examples:
        "what about my favourite colour?"
        ->
        "what is my favorite color"
    """

    command = normalize_command(command)

    if command.startswith("what about my "):
        return command.replace(
            "what about my ",
            "what is my ",
            1
        )

    if command.startswith("how about my "):
        return command.replace(
            "how about my ",
            "what is my ",
            1
        )

    if command.startswith("and my "):
        return command.replace(
            "and my ",
            "what is my ",
            1
        )

    return command


def get_context():
    return get_recent_history(limit=5)