import json
from pathlib import Path


# Find the PersonalAI main folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Find our permission rules
PERMISSIONS_FILE = BASE_DIR / "config" / "permissions.json"


def load_permissions():
    """Load permission rules from permissions.json."""

    with open(PERMISSIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def check_permission(action):
    """Check what permission level an action requires."""

    permissions = load_permissions()

    if action in permissions["SAFE"]:
        return "SAFE"

    if action in permissions["ASK_FIRST"]:
        return "ASK_FIRST"

    if action in permissions["ALWAYS_ASK"]:
        return "ALWAYS_ASK"

    # Unknown actions are blocked for safety
    return "BLOCKED"


def show_permission(action):
    """Show the permission level for an action."""

    level = check_permission(action)

    print(f"Action: {action}")
    print(f"Permission: {level}")

    return level