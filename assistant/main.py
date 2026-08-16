from ai_brain import AIBrain
from tools.files import read_file
from tools.terminal import run_command


def local_command(message):
    text = message.strip()

    if text.lower().startswith("read "):
        filename = text[5:].strip()

        if not filename:
            return "ERROR: Please provide a filename."

        return read_file(filename)

    if text.lower().startswith("run "):
        command = text[4:].strip()

        if not command:
            return "ERROR: Please provide a command."

        return run_command(command)

    return None


print("===================================")
print("      PERSONAL AI DEVELOPER")
print("===================================")
print()

print("Connecting to Gemini...")

try:
    brain = AIBrain()
    print("Gemini connected successfully.")
except Exception as error:
    brain = None
    print("Gemini unavailable.")
    print(error)

print()
print("Type 'exit' to close Personal AI.")
print()

while True:
    try:
        message = input("You: ").strip()
    except KeyboardInterrupt:
        print()
        print("Personal AI shutting down.")
        break

    if message.lower() == "exit":
        print()
        print("Personal AI shutting down.")
        break

    if not message:
        continue

    # Handle simple commands locally.
    result = local_command(message)

    if result is not None:
        print()
        print("Personal AI:")
        print(result)
        print()
        continue

    # Send other requests to Gemini.
    if brain is None:
        print()
        print("Personal AI:")
        print("Gemini is unavailable for this request.")
        print()
        continue

    try:
        answer = brain.ask(message)

        print()
        print("Personal AI:")
        print(answer)
        print()

    except Exception as error:
        print()
        print("Personal AI encountered an error:")
        print(error)
        print()