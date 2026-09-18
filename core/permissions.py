# ============================================================
# STARK-OS PERMISSION SYSTEM
# ============================================================

_pending_action = None


def request_action(action_type, target, callback):
    """
    Store an action that requires user confirmation.
    """

    global _pending_action

    _pending_action = {
        "type": action_type,
        "target": target,
        "callback": callback,
    }


def has_pending_action():
    return _pending_action is not None


def get_pending_action():
    return _pending_action


def confirm_action():
    """
    Execute the currently pending action.
    """

    global _pending_action

    if _pending_action is None:
        return None

    action = _pending_action
    _pending_action = None

    return action["callback"]()


def cancel_action():
    """
    Cancel the currently pending action.
    """

    global _pending_action

    if _pending_action is None:
        return False

    _pending_action = None
    return True
