from permissions import check_permission


# Commands that are safe for normal development work
SAFE_COMMANDS = [
    "python --version",
    "python -m pytest",
    "pytest",
    "git status",
    "git diff",
]


# Commands that change the project and therefore need approval
ASK_FIRST_COMMANDS = [
    "pip install",
    "python -m pip install",
    "npm install",
    "npm uninstall",
    "git commit",
    "git checkout",
    "git switch",
]


# Commands that should always require explicit approval
ALWAYS_ASK_COMMANDS = [
    "git push",
    "git reset --hard",
    "git clean",
    "rmdir",
    "del",
    "format",
]


def classify_command(command):
    """
    Decide how much permission a terminal command requires.
    """

    command = command.strip().lower()

    # Empty commands are blocked.
    if not command:
        return "BLOCKED"

    # Check exact safe commands.
    if command in SAFE_COMMANDS:
        return "SAFE"

    # Check commands that need approval.
    for allowed_command in ASK_FIRST_COMMANDS:
        if command.startswith(allowed_command):
            return "ASK_FIRST"

    # Check commands that always need approval.
    for dangerous_command in ALWAYS_ASK_COMMANDS:
        if command.startswith(dangerous_command):
            return "ALWAYS_ASK"

    # Unknown commands are blocked.
    return "BLOCKED"