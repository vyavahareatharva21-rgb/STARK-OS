"""
STARK-OS System Status
Lightweight health checks for the interface.
"""

from core.memory import load_memory


def check_core():
    """Check whether the core reasoning system is available."""
    try:
        from core.brain import think

        return callable(think)
    except Exception:
        return False


def check_memory():
    """Check whether the memory system is available."""
    try:
        memory = load_memory()
        return isinstance(memory, dict)
    except Exception:
        return False


def check_ai():
    """Check whether the AI engine is initialized."""
    try:
        from ai.engine import ai_engine

        return ai_engine is not None
    except Exception:
        return False


def get_system_status():
    """Return the current STARK system status."""
    return {
        "core": check_core(),
        "memory": check_memory(),
        "ai": check_ai(),
    }