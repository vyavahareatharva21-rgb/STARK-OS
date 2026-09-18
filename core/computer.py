from pathlib import Path
import subprocess


# ============================================================
# CONTROLLED APPLICATION LAUNCHER
# ============================================================

ALLOWED_APPS = {
    "vs code": "Visual Studio Code",
    "visual studio code": "Visual Studio Code",
    "vscode": "Visual Studio Code",
    "safari": "Safari",
    "terminal": "Terminal",
    "finder": "Finder",
}


APP_ALIASES = {
    "vscode": "Visual Studio Code",
    "vs code": "Visual Studio Code",
    "code": "Visual Studio Code",
    "settings": "System Settings",
    "system preferences": "System Settings",
    "browser": "Safari",
    "web browser": "Safari",
    "music": "Music",
    "photos": "Photos",
    "messages": "Messages",
    "mail": "Mail",
    "notes": "Notes",
    "calendar": "Calendar",
    "calculator": "Calculator",
    "finder": "Finder",
    "terminal": "Terminal",
}


def discover_installed_applications():
    """
    Discover macOS applications from the standard application folders.
    Returns a mapping of lowercase application names to their official names.
    """

    import subprocess

    result = subprocess.run(
        [
            "find",
            "/Applications",
            str(Path.home() / "Applications"),
            "/System/Applications",
            "-maxdepth",
            "1",
            "-type",
            "d",
            "-name",
            "*.app",
        ],
        capture_output=True,
        text=True,
    )

    applications = {}

    for line in result.stdout.splitlines():
        name = Path(line).stem.strip()

        if name:
            applications[name.lower()] = name

    return applications


def get_discovered_applications():
    """Return the installed applications discovered by STARK-OS."""
    return sorted(discover_installed_applications().values())


def find_allowed_app(app_name):
    """
    Return the official macOS application name if it is approved
    or discovered in the standard macOS application folders.
    """

    normalized = app_name.lower().strip()

    # Check natural-language application aliases.
    alias = APP_ALIASES.get(normalized)

    if alias:
        normalized = alias.lower()

    # First check explicit approved applications.
    official_name = ALLOWED_APPS.get(normalized)

    if official_name:
        return official_name

    # Then check automatically discovered applications.
    discovered_apps = discover_installed_applications()

    return discovered_apps.get(normalized)


def focus_application(app_name):
    """
    Bring a currently running approved macOS application
    to the foreground without launching it.
    """

    import subprocess

    official_name = find_allowed_app(app_name)

    if official_name is None:
        return (
            f"I don't have permission to focus '{app_name}'. "
            "This application is not on my approved list."
        )

    script = (
        'tell application "System Events"\n'
        f'    if exists process "{official_name}" then\n'
        f'        set frontmost of process "{official_name}" to true\n'
        f'        return "Focused {official_name}."\n'
        '    else\n'
        f'        return "{official_name} is not currently running."\n'
        '    end if\n'
        'end tell'
    )

    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
        )

        output = result.stdout.strip()

        if result.returncode != 0:
            return f"I couldn't focus {official_name}: {result.stderr.strip()}"

        return output

    except OSError as error:
        return f"I couldn't focus {official_name}: {error}"


def launch_application(app_name):
    """
    Launch an application through macOS 'open -a'.

    Only applications in ALLOWED_APPS can be launched.
    """

    official_name = find_allowed_app(app_name)

    if official_name is None:
        return (
            f"I don't have permission to launch '{app_name}'. "
            "This application is not on my approved list."
        )

    try:
        subprocess.Popen(
            ["open", "-a", official_name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return f"Opening {official_name}."

    except OSError as error:
        return f"I couldn't open {official_name}: {error}"


def get_allowed_applications():
    """Return each approved application once."""
    return list(dict.fromkeys(ALLOWED_APPS.values()))
