import re
import string

from core.memory import (
    get_recent_history,
    get_user_memories,
    get_conversation_history,
)

# ============================================================
# NORMALIZATION
# ============================================================

NORMALIZATION_MAP = {
    "favourite": "favorite",
    "colour": "color",
    "programme": "program",
    "programmes": "programs",

    # Common question typos
    "whan": "when",
    "wht": "what",
    "wat": "what",
    "wich": "which",
    "creatd": "created",
    "createdd": "created",
    "favoirite": "favorite",
    "releasd": "released",
    "relased": "released",
}


def normalize_command(command):
    """
    Normalize a user command while preserving useful command syntax.

    Examples:
        favourite -> favorite
        colour -> color
        createdd -> created
        "what is my favourite colour?"
            ->
        "what is my favorite color"
    """

    if not isinstance(command, str):
        return ""

    command = command.lower().strip()

    # Remove accidental prompt prefixes.
    command = re.sub(r"^(you\s*:\s*)+", "", command)

    # Normalize repeated whitespace.
    command = re.sub(r"\s+", " ", command)

    words = command.split()
    normalized_words = []

    for word in words:
        # Preserve command-style arguments such as:
        # --check, --staged, --oneline
        if word.startswith("--"):
            normalized_words.append(word)
            continue

        # Remove punctuation only from the edges of normal words.
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
    Resolve simple personal-memory context requests.

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
    Determine whether the request is asking about
    stored user memory.
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
        "when was it released",
        "when was it created",
        "what did i say",
        "what did we discuss",
        "what were we talking about",
        "what was that",
        "what about it",
        "and what about it",
        "explain that",
        "tell me more about it",
        "tell me more",
    ]

    if any(phrase in command for phrase in history_phrases):
        return True

    reference_words = {
        "it",
        "that",
        "this",
        "they",
        "them",
        "those",
    }

    words = set(command.split())

    if words.intersection(reference_words):
        return True

    return False


# ============================================================
# RELEVANT HISTORY
# ============================================================

def get_relevant_history(command, limit=4):
    """
    Return the most recent conversation history.

    For contextual follow-up questions, the newest
    conversation entries are most useful.
    """

    normalized_command = normalize_command(command)

    if not needs_history(normalized_command):
        return []

    history = get_conversation_history()

    if not history:
        return []

    selected = []

    for entry in reversed(history):
        user_message = normalize_command(
            entry.get("user", "")
        )

        if not user_message:
            continue

        selected.append(entry)

        if len(selected) >= limit:
            break

    selected.reverse()

    return selected


# ============================================================
# SUBJECT EXTRACTION
# ============================================================

def extract_subject(command):
    """
    Try to identify the main subject of a command.

    Examples:

        what is Python
            -> Python

        who created Python
            -> Python

        what is Java
            -> Java

        who created Iron Man
            -> Iron Man
    """

    command = normalize_command(command)

    if not command:
        return None

    patterns = [
        r"^what is (.+)$",
        r"^what are (.+)$",
        r"^who created (.+)$",
        r"^who made (.+)$",
        r"^when was (.+) released$",
        r"^when was (.+) created$",
        r"^tell me about (.+)$",
        r"^explain (.+)$",
        r"^what about (.+)$",
    ]

    for pattern in patterns:
        match = re.match(pattern, command)

        if match:
            subject = match.group(1).strip()

            subject = subject.rstrip("?!.,")

            if subject:
                return subject

    # Common direct subjects.
    known_subjects = [
        "python",
        "java",
        "javascript",
        "c++",
        "c",
        "artificial intelligence",
        "machine learning",
        "iron man",
        "stark os",
        "stark-os",
    ]

    for subject in known_subjects:
        if subject in command and "it" not in command:
            return subject

    return None


# ============================================================
# PREVIOUS SUBJECT
# ============================================================

def get_previous_subject():
    """
    Find the most recent clear subject from conversation history.

    We inspect previous USER messages rather than AI responses
    because user messages are the safest source for determining
    what the user was asking about.
    """

    history = get_conversation_history()

    if not history:
        return None

    for entry in reversed(history):
        user_message = entry.get("user", "")

        if not isinstance(user_message, str):
            continue

        subject = extract_subject(user_message)

        if subject:
            return subject

    return None


# ============================================================
# CONTEXTUAL REFERENCE RESOLUTION
# ============================================================

def resolve_references(command):
    """
    Resolve conversational references such as:

        it
        that
        this
        them

    using the most recent identifiable subject.

    Examples:

        previous subject = Python

        who created it
            ->
        who created python

        when was it released
            ->
        when was python released

        tell me more about it
            ->
        tell me more about python
    """

    normalized_command = normalize_command(command)

    if not normalized_command:
        return normalized_command

    if not needs_history(normalized_command):
        return normalized_command

    subject = get_previous_subject()

    if not subject:
        return normalized_command

    # Only replace references when the command actually
    # contains a contextual reference.
    reference_patterns = [
        (r"\bit\b", subject),
        (r"\bthat\b", subject),
        (r"\bthis\b", subject),
        (r"\bthem\b", subject),
        (r"\bthose\b", subject),
    ]

    resolved = normalized_command

    for pattern, replacement in reference_patterns:
        resolved = re.sub(
            pattern,
            replacement,
            resolved,
            count=1
        )

    return resolved


# ============================================================
# FULL COMMAND RESOLUTION
# ============================================================

def resolve_command(command):
    """
    Fully normalize and resolve a command.

    This is the main entry point for conversational
    reference resolution.
    """

    normalized = normalize_command(command)

    # First handle personal-memory context.
    normalized = resolve_context(normalized)

    # Then resolve references to previous subjects.
    normalized = resolve_references(normalized)

    return normalized


# ============================================================
# RELEVANT CONTEXT
# ============================================================

def get_relevant_context(command):
    """
    Decide what context STARK should provide to Gemini.

    Returns:

        {
            "command": normalized command,
            "resolved_command": context-resolved command,
            "subject": current subject,
            "previous_subject": previous subject,
            "memories": relevant memories,
            "history": relevant history
        }
    """

    normalized_command = normalize_command(command)

    resolved_command = resolve_command(normalized_command)

    previous_subject = get_previous_subject()

    current_subject = extract_subject(resolved_command)

    context = {
        "command": normalized_command,
        "resolved_command": resolved_command,
        "subject": current_subject,
        "previous_subject": previous_subject,
        "memories": {},
        "history": [],
    }

    if needs_memory(normalized_command):
        context["memories"] = get_user_memories()

    if needs_history(normalized_command):
        context["history"] = get_relevant_history(
            normalized_command,
            limit=4
        )

    return context
