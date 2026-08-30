from core.commands import process_command
from core.intent import detect_intent
from core.context import (
    resolve_context,
    resolve_command,
)
from core.ai_context import build_ai_prompt
from ai.engine import ai_engine


def think(command):
    """
    Main STARK reasoning pipeline.

    Flow:

        User command
            ↓
        Intent detection
            ↓
        Context resolution
            ↓
        Local command processing OR Gemini
    """

    intent = detect_intent(command)

    print(f"[DEBUG] Intent detected: {intent}")

    print("[DEBUG] Context engine ready")

    if intent == "exit":
        return "EXIT"

    # --------------------------------------------------------
    # Resolve conversational context before deciding what
    # to send to Gemini.
    # --------------------------------------------------------

    original_command = command

    command = resolve_command(command)

    if command != original_command.lower().strip():
        print(
            f"[DEBUG] Context resolved: "
            f"{original_command} -> {command}"
        )

    # --------------------------------------------------------
    # Personal memory/context commands
    # --------------------------------------------------------

    if intent == "context_recall":
        return process_command(command)

    # --------------------------------------------------------
    # AI commands
    # --------------------------------------------------------

    if intent == "unknown":
        print("[DEBUG] Sending command to Gemini AI")

        try:
            prompt = build_ai_prompt(command)

            return ai_engine.ask(prompt)

        except Exception as error:
            print(f"[AI ERROR] {error}")

            return (
                "I'm having trouble connecting to my AI system "
                "right now."
            )

    # --------------------------------------------------------
    # Normal local commands
    # --------------------------------------------------------

    return process_command(command)
