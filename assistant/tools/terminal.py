import subprocess
from pathlib import Path

from command_security import classify_command
from approval import request_permission


# Find the main PersonalAI folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Terminal is normally restricted to this folder
WORKSPACE = BASE_DIR / "workspace"


def run_command(command, working_folder="."):
    """Run a command after checking its security level."""

    # Decide whether the command is safe.
    permission = classify_command(command)

    # Unknown commands are blocked.
    if permission == "BLOCKED":
        return "BLOCKED: This command is not allowed."

    # Ask the user for approval when necessary.
    if permission in ["ASK_FIRST", "ALWAYS_ASK"]:

        description = (
            f'The AI wants to run this command:\n\n'
            f'    {command}\n\n'
            f'Permission level: {permission}'
        )

        allowed = request_permission(
            "run_project_command",
            description
        )

        if not allowed:
            return "COMMAND CANCELLED: User denied permission."

    # Build the working directory.
    folder = WORKSPACE / working_folder

    # Make sure the folder exists.
    if not folder.exists():
        return "ERROR: Working folder does not exist."

    if not folder.is_dir():
        return "ERROR: Working path is not a folder."

    # Make sure the folder is inside the workspace.
    try:
        folder.resolve().relative_to(WORKSPACE.resolve())
    except ValueError:
        return "BLOCKED: Terminal cannot work outside the workspace."

    # Run the command.
    try:
        result = subprocess.run(
            command,
            cwd=folder,
            shell=True,
            capture_output=True,
            text=True
        )

        output = result.stdout

        if result.stderr:
            output += "\n" + result.stderr

        return output.strip()

    except Exception as error:
        return f"ERROR: {error}"