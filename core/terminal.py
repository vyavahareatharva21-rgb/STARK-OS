import subprocess
import sys

from core.commands import safe_workspace_path


ALLOWED_COMMANDS = {
    "python",
    "python3",
}


def execute_command(command):
    """Execute a strictly controlled command inside the STARK workspace."""

    parts = command.strip().split()

    if not parts:
        return "Please provide a command to execute."

    executable = parts[0].lower()

    if executable not in ALLOWED_COMMANDS:
        return (
            f"I cannot execute '{executable}'. "
            "This command is not on my approved list."
        )

    if len(parts) != 2:
        return (
            "For now, I only support commands in this format: "
            "python <filename.py>"
        )

    filename = parts[1]

    if not filename.lower().endswith(".py"):
        return "I can only execute Python files at this stage."

    file_path = safe_workspace_path(filename)

    if file_path is None:
        return "I cannot execute files outside the STARK workspace."

    if not file_path.exists():
        return f"The file '{filename}' does not exist."

    if not file_path.is_file():
        return f"'{filename}' is not a file."

    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],
            cwd=file_path.parent,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return "The command was stopped because it exceeded the 30-second limit."
    except OSError as error:
        return f"I could not execute '{filename}': {error}"

    output = result.stdout.strip()
    errors = result.stderr.strip()

    if result.returncode == 0:
        if output:
            return f"Execution completed successfully.\n\n{output}"
        return "Execution completed successfully with no output."

    response = f"Execution failed with exit code {result.returncode}."

    if output:
        response += f"\n\nOutput:\n{output}"

    if errors:
        response += f"\n\nError:\n{errors}"

    return response
