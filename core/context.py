def resolve_context(command):
    command = command.lower().strip()

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