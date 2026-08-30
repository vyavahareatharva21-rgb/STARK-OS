"""
STARK-OS UI Theme
Professional dark workstation theme.
"""

APP_NAME = "STARK-OS"

# ANSI escape sequences
RESET = "\033[0m"

# Text styles
BOLD = "\033[1m"
DIM = "\033[2m"

# Professional monochrome palette
WHITE = "\033[97m"
GRAY = "\033[90m"

# Accent colors
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"

# Layout
LINE = "─"
CORNER_TL = "┌"
CORNER_TR = "┐"
CORNER_BL = "└"
CORNER_BR = "┘"
VERTICAL = "│"


def accent(text):
    """Return text using the primary STARK accent."""
    return f"{CYAN}{text}{RESET}"


def muted(text):
    """Return secondary/muted text."""
    return f"{DIM}{GRAY}{text}{RESET}"


def success(text):
    """Return successful system status text."""
    return f"{GREEN}{text}{RESET}"


def warning(text):
    """Return warning status text."""
    return f"{YELLOW}{text}{RESET}"


def error(text):
    """Return error status text."""
    return f"{RED}{text}{RESET}"