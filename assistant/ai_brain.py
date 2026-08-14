import os

from google import genai
from google.genai import types

from tools.files import read_file, edit_file
from tools.terminal import run_command


class AIBrain:
    """Gemini-powered brain for Personal AI."""

    def __init__(self):
        # --------------------------------
        # GET GEMINI API KEY
        # --------------------------------

        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY was not found."
            )

        # --------------------------------
        # CONNECT TO GEMINI
        # --------------------------------

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-2.5-flash"

        # --------------------------------
        # DEFINE PERSONAL AI TOOLS
        # --------------------------------

        self.tools = [
            types.Tool(
                function_declarations=[

                    # ==============================
                    # READ FILE
                    # ==============================

                    types.FunctionDeclaration(
                        name="read_file",
                        description=(
                            "Read a text file inside the "
                            "Personal AI workspace."
                        ),
                        parameters=types.Schema(
                            type="OBJECT",
                            properties={
                                "filename": types.Schema(
                                    type="STRING",
                                    description=(
                                        "Path of the file "
                                        "relative to the workspace."
                                    ),
                                )
                            },
                            required=[
                                "filename"
                            ],
                        ),
                    ),

                    # ==============================
                    # EDIT FILE
                    # ==============================

                    types.FunctionDeclaration(
                        name="edit_file",
                        description=(
                            "Edit an existing text file inside "
                            "the Personal AI workspace. "
                            "This action requires user permission."
                        ),
                        parameters=types.Schema(
                            type="OBJECT",
                            properties={
                                "filename": types.Schema(
                                    type="STRING",
                                    description=(
                                        "Path of the file "
                                        "relative to the workspace."
                                    ),
                                ),
                                "new_content": types.Schema(
                                    type="STRING",
                                    description=(
                                        "The complete new content "
                                        "that should be written "
                                        "to the file."
                                    ),
                                ),
                            },
                            required=[
                                "filename",
                                "new_content",
                            ],
                        ),
                    ),

                    # ==============================
                    # RUN TERMINAL COMMAND
                    # ==============================

                    types.FunctionDeclaration(
                        name="run_command",
                        description=(
                            "Run a terminal command inside "
                            "the Personal AI workspace. "
                            "The command is checked by the "
                            "Personal AI security system "
                            "before it is executed."
                        ),
                        parameters=types.Schema(
                            type="OBJECT",
                            properties={
                                "command": types.Schema(
                                    type="STRING",
                                    description=(
                                        "The terminal command "
                                        "to run."
                                    ),
                                ),
                                "working_folder": types.Schema(
                                    type="STRING",
                                    description=(
                                        "Folder inside the "
                                        "workspace where the "
                                        "command should run. "
                                        "Use '.' for the workspace root."
                                    ),
                                ),
                            },
                            required=[
                                "command"
                            ],
                        ),
                    ),
                ]
            )
        ]

        # --------------------------------
        # CREATE GEMINI CHAT
        # --------------------------------

        self.chat = self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(

                # ==============================
                # PERSONAL AI INSTRUCTIONS
                # ==============================

                system_instruction=(
                    "You are Personal AI, a personal "
                    "developer assistant. "

                    "You help the user work on software "
                    "projects safely. "

                    "You can read files, edit files, "
                    "and run terminal commands using "
                    "the available tools. "

                    "Use read_file when the user asks "
                    "you to inspect or read a file. "

                    "Use edit_file when the user asks "
                    "you to create or change the contents "
                    "of an existing file. "

                    "Use run_command when the user asks "
                    "you to run a terminal command. "

                    "The tools have their own security "
                    "and permission system. "
                    "Never bypass that system. "

                    "If a tool asks the user for permission, "
                    "wait for the result from the tool. "

                    "Never claim that an action succeeded "
                    "unless the tool actually reports "
                    "success. "

                    "If information needed to perform "
                    "an action is missing, ask the user "
                    "for clarification. "

                    "Remember previous messages in the "
                    "current conversation. "

                    "Be clear and helpful."
                ),

                # Give Gemini access to our tools.
                tools=self.tools,
            ),
        )

    # ==========================================
    # ASK GEMINI
    # ==========================================

    def ask(self, user_message):
        """Send a message to Gemini and handle tools."""

        # --------------------------------
        # SEND USER MESSAGE
        # --------------------------------

        response = self.chat.send_message(
            user_message
        )

        # --------------------------------
        # NORMAL TEXT RESPONSE
        # --------------------------------

        if not response.function_calls:
            return response.text

        # --------------------------------
        # GET FIRST TOOL CALL
        # --------------------------------

        function_call = response.function_calls[0]

        name = function_call.name
        args = function_call.args

        # --------------------------------
        # READ FILE
        # --------------------------------

        if name == "read_file":

            filename = args.get(
                "filename"
            )

            result = read_file(
                filename
            )

        # --------------------------------
        # EDIT FILE
        # --------------------------------

        elif name == "edit_file":

            filename = args.get(
                "filename"
            )

            new_content = args.get(
                "new_content"
            )

            result = edit_file(
                filename,
                new_content
            )

        # --------------------------------
        # RUN TERMINAL COMMAND
        # --------------------------------

        elif name == "run_command":

            command = args.get(
                "command"
            )

            working_folder = args.get(
                "working_folder",
                "."
            )

            result = run_command(
                command,
                working_folder
            )

        # --------------------------------
        # UNKNOWN TOOL
        # --------------------------------

        else:

            return (
                "ERROR: Unknown tool requested: "
                + str(name)
            )

        # --------------------------------
        # SEND TOOL RESULT BACK TO GEMINI
        # --------------------------------

        tool_response = (
            types.Part.from_function_response(
                name=name,
                response={
                    "result": result
                },
            )
        )

        final_response = (
            self.chat.send_message(
                tool_response
            )
        )

        return final_response.text