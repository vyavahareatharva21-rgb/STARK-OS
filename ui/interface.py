"""
STARK-OS Professional Terminal Interface
"""

import os
import shutil

from ui.theme import (
    RESET,
    BOLD,
    WHITE,
    DIM,
    accent,
    muted,
    success,
    warning,
    error,
    LINE,
)

from ui.status import get_system_status


def clear_screen():
    """Clear the terminal screen."""
    os.system("clear")


def terminal_width():
    """Return a safe terminal width."""
    return shutil.get_terminal_size((80, 20)).columns


def divider():
    """Render a subtle horizontal divider."""
    width = min(terminal_width(), 100)
    print(muted(LINE * width))


def system_indicator(name, active):
    """Render a system status indicator."""
    if active:
        return f"{success('●')} {name:<10} {success('ACTIVE')}"
    return f"{error('●')} {name:<10} {error('OFFLINE')}"


def header():
    """Render the STARK-OS header."""

    print()
    print(accent("  STARK-OS"))
    print(muted("  PERSONAL AI WORKSTATION"))
    divider()

    status = get_system_status()

    print(
        "  "
        + system_indicator("Core", status["core"])
        + "     "
        + system_indicator("Memory", status["memory"])
        + "     "
        + system_indicator("AI", status["ai"])
    )

    divider()
    print()


def welcome():
    """Render the startup message."""
    print(f"{WHITE}{BOLD}Good evening, Atharva.{RESET}")
    print(muted("How can I assist you?"))
    print()


def prompt():
    """Return the STARK command prompt."""
    return f"{accent('You')} {muted('›')} "


def status(message, level="info"):
    """Display a system status message."""

    if level == "success":
        prefix = success("✓")
    elif level == "warning":
        prefix = warning("!")
    elif level == "error":
        prefix = error("×")
    else:
        prefix = accent("•")

    print(f"{prefix} {message}")

def processing(message="Processing"):
    """Display a subtle processing indicator."""
    print(f"{accent('STARK')} {muted('•')} {message}...")

def startup_screen():
    """Render the complete STARK startup screen."""
    clear_screen()
    header()
    welcome()