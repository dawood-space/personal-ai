from permissions import check_permission


def request_permission(action, description):
    """Check permission and ask the user when required."""

    permission = check_permission(action)

    if permission == "SAFE":
        print(f"🟢 SAFE: {description}")
        return True

    if permission == "BLOCKED":
        print(f"🚫 BLOCKED: {description}")
        return False

    print()
    print("===================================")

    if permission == "ASK_FIRST":
        print("🟡 PERMISSION REQUIRED")
    elif permission == "ALWAYS_ASK":
        print("🔴 EXPLICIT APPROVAL REQUIRED")

    print(description)
    print("===================================")

    answer = input("Allow this action? (yes/no): ").strip().lower()

    if answer == "yes":
        print("✅ Permission granted.")
        return True

    print("❌ Permission denied.")
    return False