import datetime
from pathlib import Path
from core.computer import launch_application
from core.memory import remember, recall, get_all_memories
from core.intent import detect_intent
from core.context import normalize_command


# ============================================================
# SAFE WORKSPACE
# ============================================================

WORKSPACE = Path.home() / "Documents" / "STARK-OS" / "jarvis_workspace"
WORKSPACE.mkdir(parents=True, exist_ok=True)


def safe_workspace_path(filename):
    """
    Return a safe path inside the JARVIS workspace.

    Prevents paths such as:
    ../../important_file
    """

    requested_path = Path(filename)

    if requested_path.is_absolute():
        return None

    safe_path = (WORKSPACE / requested_path).resolve()

    try:
        safe_path.relative_to(WORKSPACE.resolve())
    except ValueError:
        return None

    return safe_path


def create_file(filename):
    """Create an empty file inside the safe workspace."""

    file_path = safe_workspace_path(filename)

    if file_path is None:
        return "I cannot create files outside the JARVIS workspace."

    if file_path.exists():
        return f"The file '{filename}' already exists."

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch()

    return f"File '{filename}' created successfully."



def read_file(filename):
    """Read a text file inside the safe workspace."""

    file_path = safe_workspace_path(filename)

    if file_path is None:
        return "I cannot read files outside the JARVIS workspace."

    if not file_path.exists():
        return f"The file '{filename}' does not exist."

    if not file_path.is_file():
        return f"'{filename}' is not a file."

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return f"I cannot read '{filename}' because it is not a text file."
    except OSError as error:
        return f"I could not read '{filename}': {error}"

    if not content:
        return f"The file '{filename}' is empty."

    return f"Contents of '{filename}':\n{content}"

def write_file(filename, content):
    """Write text content to a file inside the safe workspace."""

    file_path = safe_workspace_path(filename)

    if file_path is None:
        return "I cannot write files outside the JARVIS workspace."

    if file_path.exists() and not file_path.is_file():
        return f"'{filename}' is not a file."

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    except OSError as error:
        return f"I could not write to '{filename}': {error}"

    return f"File '{filename}' written successfully."


def list_workspace():
    """List files and folders inside the STARK workspace."""
    try:
        entries = sorted(
            WORKSPACE.iterdir(),
            key=lambda item: (not item.is_dir(), item.name.lower())
        )
    except OSError as error:
        return f"I could not access the STARK workspace: {error}"

    if not entries:
        return "The STARK workspace is empty."

    lines = ["Files and folders in the STARK workspace:", ""]

    for entry in entries:
        if entry.is_dir():
            lines.append(f"📁 {entry.name}")
        else:
            lines.append(f"📄 {entry.name}")

    return "\n".join(lines)


def list_folder(folder_name):
    """List files and folders inside a specific STARK workspace folder."""
    folder_path = safe_workspace_path(folder_name)

    if folder_path is None:
        return "I cannot access folders outside the STARK workspace."

    if not folder_path.exists():
        return f"The folder '{folder_name}' does not exist."

    if not folder_path.is_dir():
        return f"'{folder_name}' is not a folder."

    try:
        entries = sorted(
            folder_path.iterdir(),
            key=lambda item: (not item.is_dir(), item.name.lower())
        )
    except OSError as error:
        return f"I could not access '{folder_name}': {error}"

    if not entries:
        return f"The folder '{folder_name}' is empty."

    lines = [
        f"Contents of '{folder_name}':",
        ""
    ]

    for entry in entries:
        if entry.is_dir():
            lines.append(f"📁 {entry.name}")
        else:
            lines.append(f"📄 {entry.name}")

    return "\n".join(lines)


def delete_file(filename):
    """Delete a file inside the STARK workspace."""
    file_path = safe_workspace_path(filename)

    if file_path is None:
        return "I cannot delete files outside the STARK workspace."

    if not file_path.exists():
        return f"The file '{filename}' does not exist."

    if not file_path.is_file():
        return f"'{filename}' is not a file."

    try:
        file_path.unlink()
    except OSError as error:
        return f"I could not delete '{filename}': {error}"

    return f"File '{filename}' deleted successfully."


def copy_item(source_name, destination_folder):
    """Copy a file or folder inside the STARK workspace."""
    import shutil

    source_path = safe_workspace_path(source_name)
    destination_path = safe_workspace_path(destination_folder)

    if source_path is None or destination_path is None:
        return "I cannot copy items outside the STARK workspace."

    if not source_path.exists():
        return f"The item '{source_name}' does not exist."

    if not destination_path.exists():
        return f"The destination folder '{destination_folder}' does not exist."

    if not destination_path.is_dir():
        return f"'{destination_folder}' is not a folder."

    if source_path.is_dir():
        try:
            destination_path.relative_to(source_path)
            return (
                f"I cannot copy '{source_name}' into itself "
                "or one of its subfolders."
            )
        except ValueError:
            pass

    target_path = destination_path / source_path.name

    if target_path.exists():
        return f"The destination already contains '{source_path.name}'."

    try:
        if source_path.is_dir():
            shutil.copytree(source_path, target_path)
        else:
            shutil.copy2(source_path, target_path)
    except OSError as error:
        return f"I could not copy '{source_name}': {error}"

    return (
        f"'{source_name}' copied to '{destination_folder}/' successfully."
    )


def move_item(source_name, destination_folder):
    """Move a file or folder inside the STARK workspace."""
    source_path = safe_workspace_path(source_name)
    destination_path = safe_workspace_path(destination_folder)

    if source_path is None or destination_path is None:
        return "I cannot move items outside the STARK workspace."

    if not source_path.exists():
        return f"The item '{source_name}' does not exist."

    if not destination_path.exists():
        return f"The destination folder '{destination_folder}' does not exist."

    if not destination_path.is_dir():
        return f"'{destination_folder}' is not a folder."

    # Prevent moving a folder into itself or one of its descendants.
    if source_path.is_dir():
        try:
            destination_path.relative_to(source_path)
            return (
                f"I cannot move '{source_name}' into itself "
                "or one of its subfolders."
            )
        except ValueError:
            pass

    target_path = destination_path / source_path.name

    if target_path.exists():
        return f"The destination already contains '{source_path.name}'."

    try:
        source_path.rename(target_path)
    except OSError as error:
        return f"I could not move '{source_name}': {error}"

    return (
        f"'{source_name}' moved to '{destination_folder}/' successfully."
    )


def rename_item(old_name, new_name):
    """Rename a file or folder inside the STARK workspace."""
    old_path = safe_workspace_path(old_name)
    new_path = safe_workspace_path(new_name)

    if old_path is None or new_path is None:
        return "I cannot rename items outside the STARK workspace."

    if not old_path.exists():
        return f"The item '{old_name}' does not exist."

    if new_path.exists():
        return f"The destination '{new_name}' already exists."

    try:
        old_path.rename(new_path)
    except OSError as error:
        return f"I could not rename '{old_name}': {error}"

    return f"'{old_name}' renamed to '{new_name}' successfully."


def delete_folder(folder_name):
    """Delete an empty folder inside the STARK workspace."""
    folder_path = safe_workspace_path(folder_name)

    if folder_path is None:
        return "I cannot delete folders outside the STARK workspace."

    if not folder_path.exists():
        return f"The folder '{folder_name}' does not exist."

    if not folder_path.is_dir():
        return f"'{folder_name}' is not a folder."

    try:
        if any(folder_path.iterdir()):
            return (
                f"I cannot delete '{folder_name}' because it is not empty. "
                "Empty the folder first."
            )

        folder_path.rmdir()
    except OSError as error:
        return f"I could not delete '{folder_name}': {error}"

    return f"Folder '{folder_name}' deleted successfully."


def create_folder(folder_name):
    """Create a folder inside the safe workspace."""

    folder_path = safe_workspace_path(folder_name)

    if folder_path is None:
        return "I cannot create folders outside the JARVIS workspace."

    if folder_path.exists():
        return f"The folder '{folder_name}' already exists."

    folder_path.mkdir(parents=True, exist_ok=True)

    return f"Folder '{folder_name}' created successfully."


def process_command(command, intent=None):
    command = command.strip()
    lower_command = command.lower()

    if intent is None:
        intent = detect_intent(command)

    # ========================================================
    # GREETING
    # ========================================================

    if intent == "greeting":
        return "Hello Atharva. STARK systems are online."

    # ========================================================
    # TIME
    # ========================================================

    elif intent == "time":
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"The current time is {current_time}"

    # ========================================================
    # OPEN APPLICATION
    # ========================================================

    elif lower_command.startswith("open "):
        app_name = command[5:].strip()

        if not app_name:
            return "Please tell me which application to open."

        return launch_application(app_name)

    elif lower_command.startswith("launch "):
        app_name = command[7:].strip()

        if not app_name:
            return "Please tell me which application to launch."

        return launch_application(app_name)

    elif lower_command.startswith("start "):
        app_name = command[6:].strip()

        if not app_name:
            return "Please tell me which application to start."

        return launch_application(app_name)


    # ========================================================
    # CREATE FILE
    # ========================================================

    elif lower_command.startswith("create file "):
        filename = command[len("create file "):].strip()

        if not filename:
            return "Please provide a filename."

        return create_file(filename)

    elif lower_command.startswith("create a file "):
        filename = command[len("create a file "):].strip()

        if not filename:
            return "Please provide a filename."

        return create_file(filename)

    elif lower_command.startswith("make a file named "):
        filename = command[len("make a file named "):].strip()

        if not filename:
            return "Please provide a filename."

        return create_file(filename)

    elif lower_command.startswith("make a file called "):
        filename = command[len("make a file called "):].strip()

        if not filename:
            return "Please provide a filename."

        return create_file(filename)

    elif lower_command.startswith("make a new file called "):
        filename = command[len("make a new file called "):].strip()

        if not filename:
            return "Please provide a filename."

        return create_file(filename)

    elif lower_command.startswith("make a new file named "):
        filename = command[len("make a new file named "):].strip()

        if not filename:
            return "Please provide a filename."

        return create_file(filename)



    # ========================================================
    # WRITE FILE
    # ========================================================

    elif lower_command.startswith("write file "):
        write_request = command[len("write file "):].strip()

        separator = " with content "

        if separator not in write_request.lower():
            return (
                "Please use this format: "
                "write file <filename> with content <text>"
            )

        separator_index = write_request.lower().index(separator)

        filename = write_request[:separator_index].strip()
        content = write_request[
            separator_index + len(separator):
        ]

        if not filename:
            return "Please provide a filename."

        if not content:
            return "Please provide the content to write."

        return write_file(filename, content)

    # ========================================================
    # DELETE FILE
    # ========================================================

    elif lower_command.startswith("copy "):
        copy_request = command[len("copy "):].strip()

        separator = " to "

        if separator not in copy_request.lower():
            return (
                "Please use this format: "
                "copy <source> to <destination folder>"
            )

        separator_index = copy_request.lower().index(separator)

        source_name = copy_request[:separator_index].strip()
        destination_folder = copy_request[
            separator_index + len(separator):
        ].strip()

        if not source_name:
            return "Please provide the item to copy."

        if not destination_folder:
            return "Please provide a destination folder."

        return copy_item(source_name, destination_folder)

    elif lower_command.startswith("move "):
        move_request = command[len("move "):].strip()

        separator = " to "

        if separator not in move_request.lower():
            return (
                "Please use this format: "
                "move <source> to <destination folder>"
            )

        separator_index = move_request.lower().index(separator)

        source_name = move_request[:separator_index].strip()
        destination_folder = move_request[
            separator_index + len(separator):
        ].strip()

        if not source_name:
            return "Please provide the item to move."

        if not destination_folder:
            return "Please provide a destination folder."

        return move_item(source_name, destination_folder)

    elif lower_command.startswith("rename "):
        rename_request = command[len("rename "):].strip()

        separator = " to "

        if separator not in rename_request.lower():
            return (
                "Please use this format: "
                "rename <old name> to <new name>"
            )

        separator_index = rename_request.lower().index(separator)

        old_name = rename_request[:separator_index].strip()
        new_name = rename_request[
            separator_index + len(separator):
        ].strip()

        if not old_name:
            return "Please provide the current name."

        if not new_name:
            return "Please provide the new name."

        return rename_item(old_name, new_name)

    elif lower_command.startswith("delete folder "):
        folder_name = command[len("delete folder "):].strip()

        if not folder_name:
            return "Please provide a folder name."

        return delete_folder(folder_name)

    elif lower_command.startswith("delete file "):
        filename = command[len("delete file "):].strip()

        if not filename:
            return "Please provide a filename."

        return delete_file(filename)

    # ========================================================
    # REMOVE FILE
    # ========================================================

    elif lower_command.startswith("remove file "):
        filename = command[len("remove file "):].strip()

        if not filename:
            return "Please provide a filename."

        return delete_file(filename)

    # ========================================================
    # READ FILE
    # ========================================================

    elif lower_command.startswith("read file "):
        filename = command[len("read file "):].strip()

        if not filename:
            return "Please provide a filename."

        return read_file(filename)

    # ========================================================
    # CREATE FOLDER
    # ========================================================

    elif lower_command.startswith("create folder "):
        folder_name = command[len("create folder "):].strip()

        if not folder_name:
            return "Please provide a folder name."

        return create_folder(folder_name)

    elif lower_command.startswith("make a folder named "):
        folder_name = command[len("make a folder named "):].strip()

        if not folder_name:
            return "Please provide a folder name."

        return create_folder(folder_name)

    # ========================================================
    # REMEMBER
    # ========================================================

    elif intent == "remember":
        information = command.strip()

        prefixes = [
            "please remember that ",
            "please remember ",
            "remember that ",
            "remember ",
        ]

        lower_information = information.lower()

        for prefix in prefixes:
            if lower_information.startswith(prefix):
                information = information[len(prefix):].strip()
                break

        if " is " in information.lower():
            key, value = information.split(" is ", 1)

            key = normalize_command(key.strip())
            value = value.strip()

            if key.startswith("my "):
                key = key[3:].strip()

            remember(key, value)

            return "I'll remember that, Atharva."

        return "Tell me what to remember using: remember [key] is [value]"

    # ========================================================
    # CONTEXT RECALL
    # ========================================================

    elif intent in ("context_recall", "recall"):
        normalized_command = normalize_command(command)

        if normalized_command in (
            "recall",
            "remember",
            "my memories",
            "show my memories",
            "what do you remember",
        ):
            memories = get_all_memories()

            if not memories:
                return "I don't have any memories stored yet."

            response = "Here's what I remember:\n"

            for key, value in memories.items():
                response += f"- {key}: {value}\n"

            return response.rstrip()

        if "what is my " in normalized_command:
            key = normalized_command.split("what is my ", 1)[1].strip(" ?!.,")
        elif "do you remember my " in normalized_command:
            key = normalized_command.split(
                "do you remember my ", 1
            )[1].strip(" ?!.,")
        elif "what's my " in normalized_command:
            key = normalized_command.split("what's my ", 1)[1].strip(" ?!.,")
        elif "tell me my " in normalized_command:
            key = normalized_command.split("tell me my ", 1)[1].strip(" ?!.,")
        elif "show me my " in normalized_command:
            key = normalized_command.split("show me my ", 1)[1].strip(" ?!.,")
        else:
            return "Tell me which memory you want me to recall."

        key = normalize_command(key)

        if key.startswith("my "):
            key = key[3:].strip()

        value = recall(key)

        if value is not None:
            return f"Your {key} is {value}."

        return f"I don't remember your {key} yet."

    # ========================================================
    # MEMORY OVERVIEW
    # ========================================================

    elif intent == "memory_overview":
        memories = get_all_memories()

        if not memories:
            return "I don't have any memories stored yet."

        response = "Here's what I remember:\n"

        for key, value in memories.items():
            response += f"- {key}: {value}\n"

        return response.rstrip()

    # ========================================================
    # HELP
    # ========================================================

    elif intent == "help":
        return """
Available commands:

- hello / hey stark
- time / what time is it
- create file [filename]
- make a file named [filename]
- create folder [folder name]
- make a folder named [folder name]
- remember [key] is [value]
- recall
- what is my [key]
- what's my [key]
- do you remember my [key]
- tell me my [key]
- show me my [key]
- what do you remember
- show my memories
- help
- exit
"""

    # ========================================================
    # EXIT
    # ========================================================

    elif intent == "exit":
        return "EXIT"

    # ========================================================
    # UNKNOWN
    # ========================================================

    return "I am still learning this command."