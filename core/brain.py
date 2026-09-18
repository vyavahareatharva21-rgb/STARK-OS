import os
from time import perf_counter

from core.commands import process_command
from core.terminal import execute_command
from core.permissions import (
    request_action,
    has_pending_action,
    get_pending_action,
    confirm_action,
    cancel_action,
)
from core.intent import detect_intent
from core.context import resolve_command
from core.ai_context import build_ai_prompt
from ai.engine import ai_engine
from ai.local_engine import local_ai_engine

DEBUG = os.getenv("STARK_DEBUG", "0") == "1"


def debug(message):
    """Print diagnostic information when developer mode is enabled."""
    if DEBUG:
        print(f"[DEBUG] {message}")


def is_yes_no_request(command):
    """
    Detect requests that clearly require a yes/no answer.
    """
    command = command.lower().strip()

    yes_no_phrases = (
        "yes or no",
        "answer in yes or no",
        "only yes or no",
        "can you do",
        "can you build",
        "can you make",
        "is it possible",
    )

    return any(phrase in command for phrase in yes_no_phrases)


def think(command):
    """
    Main STARK reasoning pipeline.

    Flow:

        User command
            ↓
        Intent detection
            ↓
        Direct-response rules
            ↓
        Context resolution
            ↓
        Local command processing OR Gemini
    """

    start_time = perf_counter()

    if not command or not command.strip():
        return "Please enter a command."

    original_command = command.strip()

    # --------------------------------------------------------
    # Intent detection
    # --------------------------------------------------------

    intent_start = perf_counter()
    intent = detect_intent(original_command)

    debug(
        f"Intent detected: {intent} "
        f"({perf_counter() - intent_start:.3f}s)"
    )

    if intent == "exit":
        return "EXIT"

    # --------------------------------------------------------
    # Direct yes/no responses
    # --------------------------------------------------------

    if is_yes_no_request(original_command):
        debug("Direct yes/no response triggered")
        return "Yes."

    # --------------------------------------------------------
    # Resolve conversational context
    # --------------------------------------------------------

    context_start = perf_counter()
    resolved_command = resolve_command(original_command)

    debug(
        f"Context resolution completed "
        f"({perf_counter() - context_start:.3f}s)"
    )

    if resolved_command != original_command.lower().strip():
        debug(
            f"Context resolved: "
            f"{original_command} -> {resolved_command}"
        )

    # --------------------------------------------------------
    # PENDING ACTION CONFIRMATION
    # --------------------------------------------------------

    if has_pending_action():
        normalized_response = original_command.lower().strip()

        if normalized_response in (
            "yes",
            "yeah",
            "yep",
            "sure",
            "ok",
            "okay",
            "do it",
            "proceed",
            "go ahead",
        ):
            response = confirm_action()

            if response is not None:
                return response

        if normalized_response in (
            "no",
            "nope",
            "cancel",
            "stop",
            "don't",
            "do not",
        ):
            cancel_action()
            return "Action cancelled."

    # --------------------------------------------------------
    # LIST APPROVED APPLICATIONS
    # --------------------------------------------------------

    if intent == "folder_delete":
        command_for_name = original_command

        prefixes = (
            "delete folder ",
            "remove folder ",
        )

        folder_name = None

        for prefix in prefixes:
            if command_for_name.lower().startswith(prefix):
                folder_name = command_for_name[len(prefix):].strip()
                break

        if not folder_name:
            return "Please provide a folder name."

        from core.commands import safe_workspace_path

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
        except OSError as error:
            return f"I could not inspect '{folder_name}': {error}"

        request_action(
            "folder_delete",
            str(folder_path),
            lambda: process_command(
                f"delete folder {folder_name}"
            ),
        )

        return (
            f"I can delete the empty folder '{folder_name}' "
            "from the STARK workspace. Shall I proceed?"
        )

    if intent == "terminal_execute":
        command_for_execution = original_command.strip()

        prefixes = (
            "run ",
            "execute ",
        )

        execution_request = None

        for prefix in prefixes:
            if command_for_execution.lower().startswith(prefix):
                execution_request = command_for_execution[len(prefix):].strip()
                break

        if not execution_request:
            return "Please provide a command to execute."

        request_action(
            "terminal_execute",
            execution_request,
            lambda: execute_command(execution_request),
        )

        return (
            f"I can execute '{execution_request}'. "
            "Shall I proceed?"
        )

    if intent == "copy":
        command_for_name = original_command

        prefixes = (
            "copy file ",
            "copy folder ",
            "copy ",
        )

        copy_request = None

        for prefix in prefixes:
            if command_for_name.lower().startswith(prefix):
                copy_request = command_for_name[len(prefix):].strip()
                break

        if not copy_request:
            return "Please provide the item to copy and the destination folder."

        separator = " to "

        if separator not in copy_request.lower():
            return (
                "Please use this format: "
                "copy <file or folder> <name> to <destination folder>"
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

        from core.commands import safe_workspace_path

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

        target_path = destination_path / source_path.name

        if target_path.exists():
            return f"The destination already contains '{source_path.name}'."

        request_action(
            "copy",
            str(target_path),
            lambda: process_command(
                f"copy {source_name} to {destination_folder}"
            ),
        )

        return (
            f"I can copy '{source_name}' to '{destination_folder}/'. "
            "Shall I proceed?"
        )

    if intent == "move":
        command_for_name = original_command

        prefixes = (
            "move file ",
            "move folder ",
            "move ",
        )

        move_request = None

        for prefix in prefixes:
            if command_for_name.lower().startswith(prefix):
                move_request = command_for_name[len(prefix):].strip()
                break

        if not move_request:
            return "Please provide the item to move and the destination folder."

        separator = " to "

        if separator not in move_request.lower():
            return (
                "Please use this format: "
                "move <file or folder> <name> to <destination folder>"
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

        from core.commands import safe_workspace_path

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

        target_path = destination_path / source_path.name

        if target_path.exists():
            return f"The destination already contains '{source_path.name}'."

        request_action(
            "move",
            str(target_path),
            lambda: process_command(
                f"move {source_name} to {destination_folder}"
            ),
        )

        return (
            f"I can move '{source_name}' to '{destination_folder}/'. "
            "Shall I proceed?"
        )

    if intent == "rename":
        command_for_name = original_command

        prefixes = (
            "rename file ",
            "rename folder ",
            "rename ",
        )

        rename_request = None

        for prefix in prefixes:
            if command_for_name.lower().startswith(prefix):
                rename_request = command_for_name[len(prefix):].strip()
                break

        if not rename_request:
            return "Please provide the item to rename and the new name."

        separator = " to "

        if separator not in rename_request.lower():
            return (
                "Please use this format: "
                "rename <file or folder> <old name> to <new name>"
            )

        separator_index = rename_request.lower().index(separator)

        old_name = rename_request[:separator_index].strip()
        new_name = rename_request[
            separator_index + len(separator):
        ].strip()

        if not old_name:
            return "Please provide the current filename or folder name."

        if not new_name:
            return "Please provide the new filename or folder name."

        from core.commands import safe_workspace_path

        old_path = safe_workspace_path(old_name)
        new_path = safe_workspace_path(new_name)

        if old_path is None or new_path is None:
            return "I cannot rename items outside the STARK workspace."

        if not old_path.exists():
            return f"The item '{old_name}' does not exist."

        if new_path.exists():
            return f"The destination '{new_name}' already exists."

        request_action(
            "rename",
            str(old_path),
            lambda: process_command(
                f"rename {old_name} to {new_name}"
            ),
        )

        return (
            f"I can rename '{old_name}' to '{new_name}'. "
            "Shall I proceed?"
        )

    if intent == "file_delete":
        command_for_name = original_command

        prefixes = (
            "delete file ",
            "remove file ",
        )

        filename = None

        for prefix in prefixes:
            if command_for_name.lower().startswith(prefix):
                filename = command_for_name[len(prefix):].strip()
                break

        if not filename:
            return "Please provide a filename."

        from core.commands import safe_workspace_path

        file_path = safe_workspace_path(filename)

        if file_path is None:
            return "I cannot delete files outside the STARK workspace."

        if not file_path.exists():
            return f"The file '{filename}' does not exist."

        if not file_path.is_file():
            return f"'{filename}' is not a file."

        request_action(
            "file_delete",
            str(file_path),
            lambda: process_command(
                f"delete file {filename}"
            ),
        )

        return (
            f"I can delete '{filename}' from the STARK workspace. "
            "This action cannot be undone. Shall I proceed?"
        )

          # --------------------------------------------------------
    # OPEN FILE
    # --------------------------------------------------------

    if intent == "file_open":
        command_for_name = original_command

        prefix = "open file "
        filename = None

        if command_for_name.lower().startswith(prefix):
            filename = command_for_name[len(prefix):].strip()

        if not filename:
            return "Please provide a filename."

        from core.commands import safe_workspace_path

        file_path = safe_workspace_path(filename)

        if file_path is None:
            return "I cannot open files outside the STARK workspace."

        if not file_path.exists():
            return f"The file '{filename}' does not exist."

        if not file_path.is_file():
            return f"'{filename}' is not a file."

        def open_file():
            os.system(f'open "{file_path}"')
            return f"Opening file '{filename}'."

        request_action(
            "file_open",
            str(file_path),
            open_file,
        )

        return (
            f"I can open the file '{filename}'. "
            "Shall I proceed?"
        )

    # --------------------------------------------------------
    # OPEN FOLDER
    # --------------------------------------------------------

    if intent == "folder_open":
        command_for_name = original_command

        prefixes = (
            "open folder ",
            "open directory ",
        )

        folder_name = None

        for prefix in prefixes:
            if command_for_name.lower().startswith(prefix):
                folder_name = command_for_name[len(prefix):].strip()
                break

        if not folder_name:
            return "Please provide a folder name."

        from core.commands import safe_workspace_path

        folder_path = safe_workspace_path(folder_name)

        if folder_path is None:
            return "I cannot open folders outside the STARK workspace."

        if not folder_path.exists():
            return f"The folder '{folder_name}' does not exist."

        if not folder_path.is_dir():
            return f"'{folder_name}' is not a folder."

        def open_folder():
            os.system(f'open "{folder_path}"')
            return f"Opening folder '{folder_name}'."

        request_action(
            "folder_open",
            str(folder_path),
            open_folder,
        )

        return (
            f"I can open the folder '{folder_name}'. "
            "Shall I proceed?"
        )

    if intent == "folder_list":
        from core.commands import list_folder

        prefixes = (
            "list files in ",
            "show files in ",
            "list contents of ",
            "show contents of ",
        )

        folder_name = None

        for prefix in prefixes:
            if original_command.lower().startswith(prefix):
                folder_name = original_command[len(prefix):].strip()
                break

        if not folder_name:
            return "Please provide a folder name."

        return list_folder(folder_name)

    if intent == "workspace_list":
        from core.commands import list_workspace
        return list_workspace()

    if intent == "list_permissions":
        from core.computer import get_allowed_applications

        applications = get_allowed_applications()

        if not applications:
            return "No applications are currently approved."

        app_list = "\n".join(
            f"• {application}" for application in applications
        )

        return (
            "My approved applications are:\n\n"
            f"{app_list}\n\n"
            "These applications require confirmation before I launch them."
        )

    # --------------------------------------------------------
    # CREATE FOLDER PERMISSION
    # --------------------------------------------------------

    if intent == "folder_create":
        normalized_command = resolved_command
        command_for_name = original_command

        prefixes = (
            "create folder ",
            "make a folder named ",
        )

        folder_name = None

        for prefix in prefixes:
            if command_for_name.lower().startswith(prefix):
                folder_name = command_for_name[len(prefix):].strip()
                break

        if not folder_name:
            return "Please provide a folder name."

        from core.commands import safe_workspace_path

        folder_path = safe_workspace_path(folder_name)

        if folder_path is None:
            return "I cannot create folders outside the STARK workspace."

        request_action(
            "folder_create",
            str(folder_path),
            lambda: process_command(command_for_name),
        )

        return (
            f"I can create the folder '{folder_name}' "
            "in the STARK workspace. Shall I proceed?"
        )

    # --------------------------------------------------------
    # CREATE FILE PERMISSION
    # --------------------------------------------------------

    if intent == "file_create":
        normalized_command = resolved_command
        command_for_name = original_command

        prefixes = (
            "create file ",
            "make a file named ",
        )

        filename = None

        for prefix in prefixes:
            if command_for_name.lower().startswith(prefix):
                filename = command_for_name[len(prefix):].strip()
                break

        if not filename:
            return "Please provide a filename."

        from core.commands import safe_workspace_path

        file_path = safe_workspace_path(filename)

        if file_path is None:
            return "I cannot create files outside the STARK workspace."

        request_action(
            "file_create",
            str(file_path),
            lambda: process_command(normalized_command),
        )

        return (
            f"I can create '{filename}' in the STARK workspace. "
            "Shall I proceed?"
        )

    # --------------------------------------------------------
    # FILE READ PERMISSION
    # --------------------------------------------------------

    if intent == "file_operation":
        command_for_name = original_command

        prefix = "read file "

        if not command_for_name.lower().startswith(prefix):
            return "Please provide a filename."

        filename = command_for_name[len(prefix):].strip()

        if not filename:
            return "Please provide a filename."

        from core.commands import safe_workspace_path

        file_path = safe_workspace_path(filename)

        if file_path is None:
            return "I cannot read files outside the STARK workspace."

        if not file_path.exists():
            return f"The file '{filename}' does not exist."

        if not file_path.is_file():
            return f"'{filename}' is not a file."

        request_action(
            "file_operation",
            str(file_path),
            lambda: process_command(command_for_name),
        )

        return (
            f"I can read '{filename}' from the STARK workspace. "
            "Shall I proceed?"
        )

    # --------------------------------------------------------
    # FILE WRITE PERMISSION
    # --------------------------------------------------------

    if intent == "file_write":
        command_for_name = original_command

        prefixes = (
            "write file ",
            "write to file ",
            "write to ",
        )

        write_request = None

        for prefix in prefixes:
            if command_for_name.lower().startswith(prefix):
                write_request = command_for_name[len(prefix):].strip()
                break

        if not write_request:
            return "Please provide a filename and content."

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

        from core.commands import safe_workspace_path

        file_path = safe_workspace_path(filename)

        if file_path is None:
            return "I cannot write files outside the STARK workspace."

        request_action(
            "file_write",
            str(file_path),
            lambda: process_command(
                f"write file {filename} with content {content}"
            ),
        )

        return (
            f"I can write to '{filename}' in the STARK workspace. "
            "Shall I proceed?"
        )

    # --------------------------------------------------------
    # BROWSER SEARCH
    # --------------------------------------------------------

    if intent == "browser_search":
        command_for_search = resolved_command

        prefixes = (
            "search google for ",
            "google search for ",
            "search for ",
            "search google ",
        )

        query = None

        for prefix in prefixes:
            if command_for_search.startswith(prefix):
                query = command_for_search[len(prefix):].strip()
                break

        if not query:
            return "Please provide something to search for."

        import urllib.parse
        import webbrowser

        encoded_query = urllib.parse.quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"

        def perform_search():
            webbrowser.open(search_url)
            return f'Searching Google for "{query}".'

        request_action(
            "browser_search",
            query,
            perform_search,
        )

        return (
            f'I can search Google for "{query}". '
            "Shall I proceed?"
        )

    # --------------------------------------------------------
    # BROWSER / WEBSITE OPENING
    # --------------------------------------------------------

    if intent == "browser_open":
        command_for_url = resolved_command

        prefixes = (
            "open website ",
            "open url ",
            "open ",
            "go to ",
            "visit ",
        )

        url = None

        for prefix in prefixes:
            if command_for_url.startswith(prefix):
                url = command_for_url[len(prefix):].strip()
                break

        if not url:
            return "Please provide a website or URL."

        website_names = {
            "google": "google.com",
            "youtube": "youtube.com",
            "github": "github.com",
            "chatgpt": "chatgpt.com",
            "claude": "claude.ai",
        }

        if url.lower() in website_names:
            url = website_names[url.lower()]

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        def open_browser():
            import webbrowser
            webbrowser.open(url)
            return f"Opened {url}."

        request_action(
            "browser_open",
            url,
            open_browser,
        )

        return (
            f"I can open {url} in your browser. "
            "Shall I proceed?"
        )

    # --------------------------------------------------------
    # APPLICATION FOCUS
    # --------------------------------------------------------

    if intent == "app_focus":
        command_for_focus = resolved_command

        prefixes = (
            "focus on ",
            "focus ",
            "bring ",
            "switch to ",
        )

        app_name = None

        for prefix in prefixes:
            if command_for_focus.startswith(prefix):
                app_name = command_for_focus[len(prefix):].strip()
                break

        if app_name and app_name.endswith(" to foreground"):
            app_name = app_name[:-14].strip()

        if not app_name:
            return "Please tell me which application to focus."

        from core.computer import find_allowed_app

        official_name = find_allowed_app(app_name)

        if official_name is None:
            return (
                f"I don't have permission to focus '{app_name}'. "
                "This application is not on my approved list."
            )

        from core.computer import focus_application

        request_action(
            "app_focus",
            official_name,
            lambda: focus_application(official_name),
        )

        return (
            f"I can bring {official_name} to the foreground. "
            "Shall I proceed?"
        )


    # --------------------------------------------------------
    # APPLICATION LAUNCH
    # --------------------------------------------------------

    if intent == "app_launch":
        normalized_command = resolved_command

        prefixes = (
            "open ",
            "launch ",
            "start ",
        )

        app_name = None

        for prefix in prefixes:
            if normalized_command.startswith(prefix):
                app_name = normalized_command[len(prefix):].strip()
                break

        if not app_name:
            return "Please tell me which application to open."

        from core.computer import find_allowed_app

        official_name = find_allowed_app(app_name)

        if official_name is None:
            return (
                f"I don't have permission to launch '{app_name}'. "
                "This application is not on my approved list."
            )

        request_action(
            "app_launch",
            official_name,
            lambda: process_command(normalized_command),
        )

        return (
            f"I can open {official_name}. "
            "Shall I proceed?"
        )

    # --------------------------------------------------------
    # FILE OPERATIONS
    # --------------------------------------------------------

    if intent == "file_operation":
        response = process_command(resolved_command)

        debug(
            f"File operation completed "
            f"({perf_counter() - start_time:.3f}s)"
        )

        return response

    # --------------------------------------------------------
    # Personal memory/context commands
    # --------------------------------------------------------

    if intent in ("context_recall", "recall"):
        response = process_command(resolved_command)

        debug(
            f"Local command completed "
            f"({perf_counter() - start_time:.3f}s)"
        )

        return response

    # --------------------------------------------------------
    # AI commands
    # --------------------------------------------------------

    if intent == "unknown":
        debug("Preparing prompt for Gemini AI")

        try:
            prompt_start = perf_counter()
            prompt = build_ai_prompt(resolved_command)

            debug(
                f"Prompt built "
                f"({perf_counter() - prompt_start:.3f}s)"
            )

            ai_start = perf_counter()
            response = ai_engine.ask(prompt)

            debug(
                f"Gemini response received "
                f"({perf_counter() - ai_start:.3f}s)"
            )

            debug(
                f"Total reasoning time "
                f"({perf_counter() - start_time:.3f}s)"
            )

            return response

        except Exception as error:
            debug(f"Gemini AI ERROR: {error}")
            debug("Switching to local Ollama AI engine")

            try:
                local_start = perf_counter()

                response = local_ai_engine.ask(resolved_command)

                debug(
                    f"Local Ollama response received "
                    f"({perf_counter() - local_start:.3f}s)"
                )

                debug(
                    f"Total reasoning time "
                    f"({perf_counter() - start_time:.3f}s)"
                )

                return response

            except Exception as local_error:
                debug(f"LOCAL AI ERROR: {local_error}")

                return "I'm having trouble connecting to my AI system right now."

    # --------------------------------------------------------
    # Normal local commands
    # --------------------------------------------------------

    response = process_command(resolved_command)

    debug(
        f"Local command completed "
        f"({perf_counter() - start_time:.3f}s)"
    )

    return response
