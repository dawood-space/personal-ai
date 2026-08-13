import subprocess

from approval import request_permission


# Find the main PersonalAI folder
BASE_DIR = __file__

# Convert the file location into the project root
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def run_git_command(command):
    """Run a Git command from the PersonalAI project root."""

    result = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        shell=True,
        capture_output=True,
        text=True
    )

    output = result.stdout

    if result.stderr:
        output += "\n" + result.stderr

    return output.strip()


def git_status():
    """Show the current Git status."""

    return run_git_command("git status")


def git_diff():
    """Show the current Git changes."""

    return run_git_command("git diff")


def git_commit(message):
    """Create a Git commit after asking for permission."""

    description = (
        "The AI wants to create a Git commit.\n\n"
        f"Commit message: {message}"
    )

    allowed = request_permission(
        "git_commit",
        description
    )

    if not allowed:
        return "COMMIT CANCELLED: User denied permission."

    add_result = run_git_command("git add .")

    if "fatal:" in add_result.lower():
        return f"ERROR while adding files:\n{add_result}"

    return run_git_command(
        f'git commit -m "{message}"'
    )