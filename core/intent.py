def detect_intent(command):
    command = command.lower().strip()

    # EXIT
    if command in [
        "exit",
        "quit",
        "shutdown",
        "shut down",
        "goodbye",
        "bye",
    ]:
        return "exit"

    # GREETING
    greeting_phrases = [
        "hello",
        "hi",
        "hey",
        "hey stark",
        "hi stark",
        "hello stark",
        "good morning",
        "good afternoon",
        "good evening",
    ]

    # Match greetings as complete phrases, not substrings.
    if command in greeting_phrases:
        return "greeting"

    # TIME
    time_phrases = [
        "time",
        "what time",
        "current time",
        "tell me the time",
        "what's the time",
        "what is the time",
    ]

    if any(phrase in command for phrase in time_phrases):
        return "time"

           # REMEMBER
    remember_phrases = [
        "remember ",
        "remember that ",
        "please remember ",
        "please remember that ",
        "don't forget ",
        "do not forget ",
    ]

    if any(command.startswith(phrase) for phrase in remember_phrases):
        return "remember"

    # CONTEXT RECALL
    context_phrases = [
        "what about my ",
        "how about my ",
        "and my ",
    ]

    if any(command.startswith(phrase) for phrase in context_phrases):
        return "context_recall"

    # RECALL
    recall_phrases = [
        "recall",
        "what is my ",
        "what's my ",
        "do you remember my ",
        "tell me my ",
        "show me my ",
    ]

    if any(phrase in command for phrase in recall_phrases):
        return "recall"

    # MEMORY OVERVIEW
    memory_phrases = [
        "what do you remember",
        "show my memories",
        "show memories",
        "what have you remembered",
        "what do you know about me",
    ]

    if any(phrase in command for phrase in memory_phrases):
        return "memory_overview"

   
    # TERMINAL EXECUTION
    terminal_phrases = [
        "run python ",
        "run python3 ",
        "execute python ",
        "execute python3 ",
    ]

    if any(command.startswith(phrase) for phrase in terminal_phrases):
        return "terminal_execute"

    # COPY
    copy_phrases = [
        "copy file ",
        "copy folder ",
        "copy ",
    ]

    if any(command.startswith(phrase) for phrase in copy_phrases):
        return "copy"

    # MOVE
    move_phrases = [
        "move file ",
        "move folder ",
        "move ",
    ]

    if any(command.startswith(phrase) for phrase in move_phrases):
        return "move"

    # RENAME
    rename_phrases = [
        "rename file ",
        "rename folder ",
        "rename ",
    ]

    if any(command.startswith(phrase) for phrase in rename_phrases):
        return "rename"

    # FILE CREATION
    file_create_phrases = [
        "create file ",
        "make a file named ",
    ]

    if any(command.startswith(phrase) for phrase in file_create_phrases):
        return "file_create"

    # PERMISSION / APPROVED APPLICATIONS
    permission_phrases = [
        "what applications are in your permission",
        "what applications do you have permission to open",
        "show approved applications",
        "which applications can you open",
        "what apps can you launch",
        "what applications can you launch",
        "show allowed applications",
    ]

    if any(phrase in command for phrase in permission_phrases):
        return "list_permissions"

    # FOLDER DELETION
    folder_delete_phrases = [
        "delete folder ",
        "remove folder ",
    ]
    if any(command.startswith(phrase) for phrase in folder_delete_phrases):
        return "folder_delete"

    # FILE DELETION
    file_delete_phrases = [
        "delete file ",
        "remove file ",
    ]
    if any(command.startswith(phrase) for phrase in file_delete_phrases):
        return "file_delete"

    # SPECIFIC FOLDER LISTING
    folder_list_phrases = [
        "list files in ",
        "show files in ",
        "list contents of ",
        "show contents of ",
    ]
    if any(command.startswith(phrase) for phrase in folder_list_phrases):
        return "folder_list"

    # WORKSPACE LISTING
    workspace_list_phrases = [
        "list files",
        "show files",
        "list workspace",
        "show workspace",
        "what files are here",
        "show me the files",
    ]
    if any(phrase in command for phrase in workspace_list_phrases):
        return "workspace_list"

    # BROWSER SEARCH
    browser_search_phrases = [
        "search google for ",
        "google search for ",
        "search for ",
        "search google ",
    ]

    if any(command.startswith(phrase) for phrase in browser_search_phrases):
        return "browser_search"

    # BROWSER / WEBSITE OPENING
    browser_phrases = [
        "open website ",
        "open url ",
        "go to ",
        "visit ",
    ]

    if any(command.startswith(phrase) for phrase in browser_phrases):
        return "browser_open"

    # Detect common direct website commands such as:
    # "open google.com"
    if command.startswith("open ") and (
        ".com" in command
        or ".in" in command
        or ".org" in command
        or ".net" in command
        or ".io" in command
    ):
        return "browser_open"

    # Common website names
    website_names = {
        "google": "google.com",
        "youtube": "youtube.com",
        "github": "github.com",
        "chatgpt": "chatgpt.com",
        "claude": "claude.ai",
    }

    if command.startswith("open "):
        site_name = command[5:].strip()

        if site_name in website_names:
            return "browser_open"

    # APPLICATION FOCUS
    focus_phrases = [
        "focus ",
        "focus on ",
        "bring ",
        "switch to ",
    ]

    if any(command.startswith(phrase) for phrase in focus_phrases):
        if " to foreground" in command or command.startswith(("focus ", "focus on ", "switch to ")):
            return "app_focus"
        

        # FILE / FOLDER OPEN
    file_folder_open_phrases = [
        "open file ",
        "open folder ",
        "open directory ",
    ]

    if any(command.startswith(phrase) for phrase in file_folder_open_phrases):
        if command.startswith("open folder ") or command.startswith("open directory "):
            return "folder_open"
        return "file_open"



  
    # APPLICATION LAUNCH
    app_launch_phrases = [
        "open ",
        "launch ",
        "start ",
    ]

    if any(command.startswith(phrase) for phrase in app_launch_phrases):
        return "app_launch"

    # FILE OPERATIONS
    file_phrases = [
        "read file ",
    ]

    if any(command.startswith(phrase) for phrase in file_phrases):
        return "file_operation"

    # FILE WRITING
    file_write_phrases = [
        "write file ",
        "write to file ",
        "write to ",
    ]

    if any(command.startswith(phrase) for phrase in file_write_phrases):
        return "file_write"

    # FOLDER CREATION
    folder_create_phrases = [
        "create folder ",
        "make a folder named ",
    ]

    if any(command.startswith(phrase) for phrase in folder_create_phrases):
        return "folder_create"

    # HELP
    if (
        command == "help"
        or "what can you do" in command
        or "what are your commands" in command
    ):
        return "help"

    # UNKNOWN → Gemini AI
    return "unknown"
