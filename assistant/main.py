from tools.git_tools import git_status, git_diff, git_commit


print("Personal AI Git Commit Test")
print("---------------------------")


print("\nCurrent Git Status:")
print("-------------------")

print(git_status())


print("\nCurrent Git Changes:")
print("--------------------")

print(git_diff())


print("\nRequesting permission to create a commit...")
print("---------------------------------------------")

result = git_commit(
    "Initial Personal AI security system"
)


print("\nCommit Result:")
print("--------------")

print(result)