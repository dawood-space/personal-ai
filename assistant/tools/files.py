from pathlib import Path
from permissions import check_permission


# Find the main PersonalAI folder
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# The AI is only allowed to work inside this folder
WORKSPACE = BASE_DIR / "workspace"


def is_safe_path(path):
    """Make sure the AI is working inside our workspace."""

    try:
        path.resolve().relative_to(WORKSPACE.resolve())
        return True
    except ValueError:
        return False


def list_files():
    """List all files inside the workspace."""

    files = []

    for path in WORKSPACE.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(WORKSPACE)))

    return files


def read_file(filename):
    """Read a file from the workspace."""

    permission = check_permission("read_file")

    if permission != "SAFE":
        return f"BLOCKED: read_file requires {permission} permission."

    file_path = WORKSPACE / filename

    if not is_safe_path(file_path):
        return "BLOCKED: This file is outside the workspace."

    if not file_path.exists():
        return "ERROR: File does not exist."

    if not file_path.is_file():
        return "ERROR: This is not a file."

    return file_path.read_text(encoding="utf-8")


def edit_file(filename, new_content):
    """Edit a file after getting user permission."""

    from approval import request_permission

    description = f"The AI wants to edit: {filename}"

    allowed = request_permission(
        "edit_file",
        description
    )

    if not allowed:
        return "EDIT CANCELLED: User denied permission."

    file_path = WORKSPACE / filename

    if not is_safe_path(file_path):
        return "BLOCKED: This file is outside the workspace."

    if not file_path.exists():
        return "ERROR: File does not exist."

    if not file_path.is_file():
        return "ERROR: This is not a file."

    file_path.write_text(new_content, encoding="utf-8")

    return f"SUCCESS: {filename} was edited."