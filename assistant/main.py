from ai_brain import AIBrain


print("===================================")
print("      PERSONAL AI DEVELOPER")
print("===================================")
print()

print("Connecting to Gemini...")

brain = AIBrain()

print("Gemini connected successfully.")
print()
print("Type 'exit' to close Personal AI.")
print()


while True:
    message = input("You: ")

    if message.lower() == "exit":
        print()
        print("Personal AI shutting down.")
        break

    if not message.strip():
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