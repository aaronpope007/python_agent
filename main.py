import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()
    verbose = False
    args = sys.argv[1:]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, user_prompt, verbose)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

def generate_content(client, messages, user_prompt, verbose):
    for i in range(20):  # max 20 iterations
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        # Add the model's response to messages
        for candidate in response.candidates:
            messages.append(candidate.content)

        # Check if there are function calls to handle
        if response.function_calls:
            # Handle function calls (your existing code)
            for function_call_part in response.function_calls:
                if verbose:
                    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                else:
                    print(f" - Calling function: {function_call_part.name}")

                function_call_result = call_function(function_call_part, verbose)
                messages.append(function_call_result)
        else:
            # No function calls means we're done!
            print("Final response:")
            print(response.text)
            break



if __name__ == "__main__":
    main()
